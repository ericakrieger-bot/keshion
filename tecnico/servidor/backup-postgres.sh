#!/bin/bash
# Backup diário da Keshion (servidor /opt/keshion). Roda às 03h pelo /etc/cron.d/keshion-backup.
# 1. pg_dumpall compactado em /opt/keshion/backups/ (guarda os 7 mais recentes no servidor).
# 2. Criptografa com age (só a chave PÚBLICA fica no servidor; a privada fica com a Erica).
# 3. Envia para o Google Drive da Keshion (rclone, remoto "gdrive", pasta keshion-backups/).
#    Junto vai uma cópia criptografada da configuração (.env, docker-compose.yml, Caddyfile).
# 4. Apaga no Drive o que tiver mais de 30 dias.
# 5. Grava o resultado em /opt/keshion/backups/STATUS-BACKUP.txt (OK ou FALHA).
# Cópia oficial deste arquivo: tecnico/servidor/backup-postgres.sh no Git.
set -euo pipefail
umask 077

cd /opt/keshion
. ./.env

DEST=/opt/keshion/backups
CHAVE_PUBLICA=/opt/keshion/backup-chave-publica.txt
RCLONE="rclone --config /opt/keshion/rclone.conf"
REMOTO="gdrive:keshion-backups"
STATUS="$DEST/STATUS-BACKUP.txt"
DATA=$(date +%Y-%m-%d_%H%M)
ARQ="$DEST/postgres-$DATA.sql.gz"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

falha() {
  echo "FALHA $(date '+%Y-%m-%d %H:%M') etapa: $1" | tee "$STATUS"
  exit 1
}
trap 'falha "linha $LINENO"' ERR

echo "== $(date '+%Y-%m-%d %H:%M:%S') início"

# 1. Dump local
docker compose exec -T postgres pg_dumpall -U "$POSTGRES_USER" | gzip > "$ARQ.parcial"
gzip -t "$ARQ.parcial"
zcat "$ARQ.parcial" | tail -n 5 | grep -q "PostgreSQL database cluster dump complete" || falha "dump incompleto"
mv "$ARQ.parcial" "$ARQ"
chmod 600 "$ARQ"
ls -1t "$DEST"/postgres-*.sql.gz | tail -n +8 | xargs -r rm -f
echo "dump local: $(du -h "$ARQ" | cut -f1)"

# 2. Criptografar
age -R "$CHAVE_PUBLICA" -o "$TMP/postgres-$DATA.sql.gz.age" "$ARQ"
tar -czf - .env docker-compose.yml caddy/Caddyfile backup-postgres.sh \
  | age -R "$CHAVE_PUBLICA" -o "$TMP/config-$DATA.tar.gz.age"

# 3. Enviar e conferir o tamanho no Drive
$RCLONE copy "$TMP/postgres-$DATA.sql.gz.age" "$REMOTO/postgres/" -q
$RCLONE copy "$TMP/config-$DATA.tar.gz.age" "$REMOTO/config/" -q
LOCAL=$(stat -c %s "$TMP/postgres-$DATA.sql.gz.age")
REMOTO_TAM=$($RCLONE size "$REMOTO/postgres/postgres-$DATA.sql.gz.age" --json | grep -o '"bytes":[0-9]*' | cut -d: -f2)
[ "$LOCAL" = "$REMOTO_TAM" ] || falha "tamanho no Drive diferente ($LOCAL x $REMOTO_TAM)"

# 4. Guardar 30 dias no Drive
$RCLONE delete "$REMOTO/postgres/" --min-age 30d -q
$RCLONE delete "$REMOTO/config/" --min-age 30d -q

# 5. Resultado
echo "OK $(date '+%Y-%m-%d %H:%M') postgres-$DATA.sql.gz.age ($LOCAL bytes) no Drive" | tee "$STATUS"
