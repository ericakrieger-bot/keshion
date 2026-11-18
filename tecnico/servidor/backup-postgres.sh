#!/bin/bash
# Backup diário da Keshion (servidor /opt/keshion). Roda às 03h pelo /etc/cron.d/keshion-backup.
# 1. pg_dumpall compactado em /opt/keshion/backups/ (guarda 7 dias no servidor, por idade).
# 2. Criptografa com age (só a chave PÚBLICA fica no servidor; a privada fica com a Erica).
# 3. Envia para o Google Drive da Keshion (rclone, remoto "gdrive", pasta keshion-backups/).
#    Junto vai uma cópia criptografada da configuração (.env, docker-compose.yml, Caddyfile).
# 4. Confere o tamanho dos dois arquivos no Drive e apaga lá o que tiver mais de 30 dias.
# 5. Grava o resultado em /opt/keshion/backups/STATUS-BACKUP.txt:
#      EM ANDAMENTO (no início), OK (só no fim, com tudo conferido) ou FALHA (com a etapa).
# 6. Se HC_BACKUP_URL estiver no .env (monitor externo, ex.: Healthchecks.io), avisa início,
#    sucesso e falha. Sem a variável, nada é enviado. O aviso leva só a etapa e o código do
#    erro, nunca dados de paciente. A URL é secreta: fica só no .env, nunca em argumento.
# Uma segunda execução ao mesmo tempo é ignorada (flock). Falha em qualquer ponto, inclusive
# antes de ler o .env, vira FALHA no status: o OK antigo nunca fica no lugar.
# Cópia oficial deste arquivo: tecnico/servidor/backup-postgres.sh no Git.
# Teste local sem custo: tecnico/servidor/testar-backup-local.sh
set -Eeuo pipefail
umask 077

BASE=${KESHION_BASE:-/opt/keshion}
DEST="$BASE/backups"
STATUS="$DEST/STATUS-BACKUP.txt"
CHAVE_PUBLICA="$BASE/backup-chave-publica.txt"
RCLONE="rclone --config $BASE/rclone.conf"
REMOTO="gdrive:keshion-backups"
DIAS_LOCAL=7
DIAS_DRIVE=30

ETAPA="preparação"
LINHA="?"
CONCLUIDO=0
TMP=""
HC_URL=""

agora() { date '+%Y-%m-%d %H:%M'; }

# Grava o status por arquivo temporário + mv, para nunca ficar meio escrito.
gravar_status() {
  { printf '%s\n' "$1" > "$STATUS.novo" && mv -f "$STATUS.novo" "$STATUS"; } 2>/dev/null \
    || echo "AVISO: não consegui gravar o status ($1)"
}

# Aviso ao monitor externo. A URL vai por stdin (curl -K -), nunca na linha de comando.
# $1 = sufixo (vazio = sucesso, /start, /fail); $2 = texto curto. Erro aqui nunca derruba o backup.
ping_monitor() {
  [ -n "$HC_URL" ] || return 0
  local texto="${2:-}"; texto="${texto//\"/}"
  printf 'url = "%s%s"\ndata = "%s"\n' "$HC_URL" "$1" "$texto" \
    | curl -fsS -m 10 --retry 3 -o /dev/null -K - 2>/dev/null || true
}

falha() { ETAPA="$1"; exit 1; }

ao_sair() {
  local codigo=$?
  trap - EXIT ERR INT TERM
  [ -z "$TMP" ] || rm -rf "$TMP"
  if [ "$CONCLUIDO" != 1 ]; then
    local msg
    msg="FALHA $(agora) etapa: $ETAPA (linha $LINHA, código $codigo)"
    echo "$msg"
    gravar_status "$msg"
    ping_monitor /fail "etapa: $ETAPA; código $codigo"
    [ "$codigo" -ne 0 ] || codigo=1
    exit "$codigo"
  fi
}

mkdir -p "$DEST"

# Trava contra duas execuções ao mesmo tempo. Quem chega depois sai sem mexer no status.
exec 9>"$DEST/.backup.lock"
if ! flock -n 9; then
  echo "== $(agora) já existe um backup em andamento; esta execução foi ignorada"
  exit 0
fi

# A partir daqui qualquer erro vira FALHA no status, mesmo antes de cd, .env ou mktemp.
trap 'LINHA=$LINENO' ERR
trap ao_sair EXIT
trap 'ETAPA="interrompido por sinal"; exit 143' INT TERM

gravar_status "EM ANDAMENTO $(agora) início"
echo "== $(date '+%Y-%m-%d %H:%M:%S') início"

ETAPA="leitura do .env"
cd "$BASE"
. ./.env
HC_URL="${HC_BACKUP_URL:-}"
ping_monitor /start "início"

ETAPA="pasta temporária"
TMP=$(mktemp -d)

DATA=$(date +%Y-%m-%d_%H%M%S)
ARQ="$DEST/postgres-$DATA.sql.gz"
PG_ARQ="postgres-$DATA.sql.gz.age"
CFG_ARQ="config-$DATA.tar.gz.age"

# 1. Dump local
ETAPA="dump do banco"
docker compose exec -T postgres pg_dumpall -U "$POSTGRES_USER" | gzip > "$ARQ.parcial"
ETAPA="conferência do dump"
gzip -t "$ARQ.parcial"
zcat "$ARQ.parcial" | tail -n 5 | grep -q "PostgreSQL database cluster dump complete" || falha "dump incompleto"
mv "$ARQ.parcial" "$ARQ"
chmod 600 "$ARQ"
echo "dump local: $(du -h "$ARQ" | cut -f1)"

# Retenção local por idade (7 dias), incluindo dumps que ficaram pela metade (.parcial).
ETAPA="limpeza local"
find "$DEST" -maxdepth 1 -type f \( -name 'postgres-*.sql.gz' -o -name 'postgres-*.sql.gz.parcial' \) \
  -mtime +"$DIAS_LOCAL" -delete

# 2. Criptografar
ETAPA="criptografia"
age -R "$CHAVE_PUBLICA" -o "$TMP/$PG_ARQ" "$ARQ"
tar -czf - .env docker-compose.yml caddy/Caddyfile backup-postgres.sh \
  | age -R "$CHAVE_PUBLICA" -o "$TMP/$CFG_ARQ"

# 3. Enviar e conferir o tamanho dos dois arquivos no Drive
ETAPA="envio ao Drive"
$RCLONE copy "$TMP/$PG_ARQ" "$REMOTO/postgres/" -q
$RCLONE copy "$TMP/$CFG_ARQ" "$REMOTO/config/" -q
ETAPA="conferência no Drive"
tamanho_remoto() { $RCLONE size "$1" --json | grep -o '"bytes":[0-9]*' | cut -d: -f2; }
LOCAL_PG=$(stat -c %s "$TMP/$PG_ARQ")
LOCAL_CFG=$(stat -c %s "$TMP/$CFG_ARQ")
REMOTO_PG=$(tamanho_remoto "$REMOTO/postgres/$PG_ARQ")
REMOTO_CFG=$(tamanho_remoto "$REMOTO/config/$CFG_ARQ")
[ "$LOCAL_PG" = "$REMOTO_PG" ] || falha "tamanho do banco no Drive diferente ($LOCAL_PG x $REMOTO_PG)"
[ "$LOCAL_CFG" = "$REMOTO_CFG" ] || falha "tamanho da configuração no Drive diferente ($LOCAL_CFG x $REMOTO_CFG)"

# 4. Guardar 30 dias no Drive (as duas pastas são só deste backup)
ETAPA="limpeza no Drive"
$RCLONE delete "$REMOTO/postgres/" --min-age "${DIAS_DRIVE}d" -q
$RCLONE delete "$REMOTO/config/" --min-age "${DIAS_DRIVE}d" -q

# 5. Resultado: OK só aqui, com tudo conferido
ETAPA="gravação do resultado"
CONCLUIDO=1
MSG="OK $(agora) $PG_ARQ ($LOCAL_PG bytes) e $CFG_ARQ ($LOCAL_CFG bytes) no Drive"
gravar_status "$MSG"
echo "$MSG"
ping_monitor "" "ok $PG_ARQ"
