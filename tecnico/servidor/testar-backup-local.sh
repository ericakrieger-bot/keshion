#!/bin/bash
# Teste local (no PC, sem custo, sem servidor) do backup-postgres.sh.
# Troca docker, age, rclone, flock, curl e mktemp por substitutos e confere o status em cada cenário.
# Uso (Git Bash, na pasta do projeto): bash tecnico/servidor/testar-backup-local.sh
# Não toca no servidor, no Drive nem em nenhum dado real.
set -u
AQUI=$(cd "$(dirname "$0")" && pwd)
RAIZ=$(mktemp -d)
trap 'rm -rf "$RAIZ"' EXIT
OK=0; RUIM=0

mkdir -p "$RAIZ/bin"
cat > "$RAIZ/bin/docker" <<'E'
#!/bin/bash
case "${STUB_DOCKER:-ok}" in
  fail) exit 1 ;;
  lento) sleep 20; exit 0 ;;
  incompleto) echo "-- dump sem o marcador final"; exit 0 ;;
  *) echo "-- dump de teste"; echo "-- PostgreSQL database cluster dump complete" ;;
esac
E
cat > "$RAIZ/bin/age" <<'E'
#!/bin/bash
[ "${STUB_AGE:-ok}" = fail ] && exit 1
while [ $# -gt 0 ]; do case "$1" in -o) O="$2"; shift 2 ;; -R) shift 2 ;; *) I="$1"; shift ;; esac; done
if [ -n "${I:-}" ]; then cp "$I" "$O"; else cat > "$O"; fi
E
cat > "$RAIZ/bin/rclone" <<'E'
#!/bin/bash
[ "${STUB_RCLONE:-ok}" = fail ] && exit 1
shift 2   # --config X
cmd="$1"; shift
case "$cmd" in
  copy) src="$1"; dst="${2#gdrive:keshion-backups/}"; mkdir -p "$STUB_REMOTE/$dst"; cp "$src" "$STUB_REMOTE/$dst" ;;
  size) p="$STUB_REMOTE/${1#gdrive:keshion-backups/}"; n=$(stat -c %s "$p")
        [ "${STUB_RCLONE:-ok}" = tamanho ] && n=$((n+1)); echo "{\"count\":1,\"bytes\":$n,\"sizeless\":0}" ;;
  delete) : ;;
esac
E
cat > "$RAIZ/bin/flock" <<'E'
#!/bin/bash
[ "${STUB_FLOCK:-ok}" = ocupado ] && exit 1 || exit 0
E
cat > "$RAIZ/bin/curl" <<'E'
#!/bin/bash
echo "ARGS: $*" >> "$STUB_CURL_LOG"
cat >> "$STUB_CURL_LOG"
[ "${STUB_CURL:-ok}" = fail ] && exit 22 || exit 0
E
cat > "$RAIZ/bin/mktemp" <<'E'
#!/bin/bash
[ "${STUB_MKTEMP:-ok}" = fail ] && exit 1
exec /usr/bin/mktemp "$@"
E
cat > "$RAIZ/bin/mkdir" <<'E'
#!/bin/bash
[ "${STUB_MKDIR:-ok}" = fail ] && exit 1
exec /usr/bin/mkdir "$@"
E
cat > "$RAIZ/bin/mv" <<'E'
#!/bin/bash
# STUB_MV=ok_status: só falha ao gravar um status que começa com OK; status_sempre: falha em qualquer gravação de status.
destino="${@: -1}"; origem="${@: -2:1}"
case "$destino" in
  */STATUS-BACKUP.txt)
    [ "${STUB_MV:-ok}" = status_sempre ] && exit 1
    if [ "${STUB_MV:-ok}" = ok_status ] && head -c 3 "$origem" | grep -q '^OK '; then exit 1; fi ;;
esac
exec /usr/bin/mv "$@"
E
chmod +x "$RAIZ"/bin/*

# $1 = nome; cria uma pasta nova com status antigo "OK ANTIGO"
novo() {
  B="$RAIZ/$1"; mkdir -p "$B/backups" "$B/caddy" "$RAIZ/remoto-$1" "$RAIZ/curl-$1.log"; rmdir "$RAIZ/curl-$1.log"
  printf 'POSTGRES_USER=teste\nHC_BACKUP_URL=https://exemplo.invalido/segredo123\n' > "$B/.env"
  echo x > "$B/docker-compose.yml"; echo x > "$B/caddy/Caddyfile"; echo x > "$B/backup-postgres.sh"
  echo x > "$B/backup-chave-publica.txt"; echo x > "$B/rclone.conf"
  echo "OK ANTIGO" > "$B/backups/STATUS-BACKUP.txt"
  export KESHION_BASE="$B" STUB_REMOTE="$RAIZ/remoto-$1" STUB_CURL_LOG="$RAIZ/curl-$1.log"
  : > "$STUB_CURL_LOG"
  unset STUB_DOCKER STUB_AGE STUB_RCLONE STUB_FLOCK STUB_CURL STUB_MKTEMP STUB_MKDIR STUB_MV
}
rodar() { PATH="$RAIZ/bin:$PATH" bash "$AQUI/backup-postgres.sh" > "$RAIZ/saida.txt" 2>&1; CODIGO=$?; STAT=$(cat "$B/backups/STATUS-BACKUP.txt"); }
confere() { # descrição, condição (0 = passou)
  if [ "$2" = 0 ]; then OK=$((OK+1)); echo "  ok    $1"; else RUIM=$((RUIM+1)); echo "  ERRO  $1  (status: $STAT)"; fi
}
tem() { case "$STAT" in $1) return 0 ;; *) return 1 ;; esac; }

echo "1. tudo certo"
novo c1
touch -d '10 days ago' "$B/backups/postgres-velho.sql.gz" "$B/backups/postgres-velho.sql.gz.parcial"
touch -d '3 days ago' "$B/backups/postgres-recente.sql.gz"
rodar
confere "código 0" $([ $CODIGO = 0 ]; echo $?)
confere "status OK novo" $(tem 'OK 20*'; echo $?)
confere "dois arquivos no remoto" $([ -n "$(ls "$STUB_REMOTE/postgres")" ] && [ -n "$(ls "$STUB_REMOTE/config")" ]; echo $?)
confere "retenção local apagou velho e .parcial velho" $([ ! -e "$B/backups/postgres-velho.sql.gz" ] && [ ! -e "$B/backups/postgres-velho.sql.gz.parcial" ]; echo $?)
confere "retenção local manteve o de 3 dias" $([ -e "$B/backups/postgres-recente.sql.gz" ]; echo $?)
confere "monitor recebeu início e sucesso" $(grep -q '/start' "$STUB_CURL_LOG" && grep -q 'ok postgres' "$STUB_CURL_LOG"; echo $?)
confere "URL do monitor não aparece em argumento nem na saída" $(! grep -q 'ARGS:.*segredo123' "$STUB_CURL_LOG" && ! grep -q segredo123 "$RAIZ/saida.txt"; echo $?)
confere "sem arquivo temporário sobrando" $([ ! -e "$B/backups/STATUS-BACKUP.txt.novo" ]; echo $?)

falha_esperada() { # nome, descrição
  confere "$1: código 1" $([ $CODIGO = 1 ]; echo $?)
  confere "$1: status FALHA (não ficou o OK antigo)" $(tem 'FALHA*'; echo $?)
  confere "$1: monitor recebeu /fail" $(grep -q '/fail' "$STUB_CURL_LOG"; echo $?)
}
echo "2. docker falha";           novo c2; STUB_DOCKER=fail rodar;       falha_esperada docker
echo "3. dump incompleto";        novo c3; STUB_DOCKER=incompleto rodar; falha_esperada incompleto
confere "incompleto: citou o dump" $(tem '*dump incompleto*'; echo $?)
echo "4. age falha";              novo c4; STUB_AGE=fail rodar;          falha_esperada age
echo "5. rclone falha";           novo c5; STUB_RCLONE=fail rodar;       falha_esperada rclone
echo "6. tamanho diverge";        novo c6; STUB_RCLONE=tamanho rodar;    falha_esperada tamanho
echo "7. .env ausente";           novo c7; rm "$B/.env"; rodar;          confere "código 1" $([ $CODIGO = 1 ]; echo $?); confere "FALHA, não OK antigo" $(tem 'FALHA*'; echo $?)
echo "8. mktemp falha";           novo c8; STUB_MKTEMP=fail rodar;       falha_esperada mktemp
echo "9. monitor fora do ar não derruba o backup"
novo c9; STUB_CURL=fail rodar
confere "código 0 e OK" $([ $CODIGO = 0 ] && tem 'OK 20*'; echo $?)
echo "10. outra execução em andamento"
novo c10; STUB_FLOCK=ocupado rodar
confere "saiu sem mexer no status" $([ "$STAT" = "OK ANTIGO" ] && [ $CODIGO = 0 ]; echo $?)
echo "11. interrompido (kill) no meio do dump"
novo c11; export STUB_DOCKER=lento
PATH="$RAIZ/bin:$PATH" bash "$AQUI/backup-postgres.sh" > "$RAIZ/saida.txt" 2>&1 &
PID=$!; sleep 2; kill -TERM $PID; wait $PID; CODIGO=$?; STAT=$(cat "$B/backups/STATUS-BACKUP.txt")
confere "status FALHA por interrupção" $(tem 'FALHA*interrompido*'; echo $?)
echo "12. sem HC_BACKUP_URL não chama o monitor"
novo c12; printf 'POSTGRES_USER=teste\n' > "$B/.env"; rodar
confere "OK e curl nunca chamado" $(tem 'OK 20*' && [ ! -s "$STUB_CURL_LOG" ]; echo $?)

echo "13. falhas antes dos traps antigos (D1, 20/11/2026)"
echo " 13a. mkdir da pasta de backups falha"
novo c13a; STUB_MKDIR=fail rodar; falha_esperada mkdir
confere "mkdir: etapa citada no status" $(tem '*pasta de backups*'; echo $?)
echo " 13b. arquivo de trava indisponível (flock não chega a rodar)"
novo c13b; mkdir "$B/backups/.backup.lock"; rodar; falha_esperada trava
confere "trava: etapa citada no status" $(tem '*arquivo de trava*'; echo $?)
echo " 13c. falha ao gravar o status OK final"
novo c13c; STUB_MV=ok_status rodar; falha_esperada status_ok
confere "status OK final: não ficou OK nem OK ANTIGO" $(! tem 'OK*'; echo $?)
confere "status OK final: etapa citada" $(tem '*gravação do resultado*'; echo $?)
confere "status OK final: monitor NÃO recebeu aviso de sucesso" $(! grep -q 'ok postgres' "$STUB_CURL_LOG"; echo $?)
confere "status OK final: arquivos já estavam no Drive (falha só do status)" $([ -n "$(ls "$STUB_REMOTE/postgres")" ]; echo $?)
echo " 13d. nenhum status consegue ser gravado (disco só leitura simulado)"
novo c13d; STUB_MV=status_sempre rodar
confere "sem status: código diferente de zero" $([ $CODIGO != 0 ]; echo $?)
confere "sem status: o OK antigo não vira OK novo" $([ "$STAT" = "OK ANTIGO" ]; echo $?)
confere "sem status: monitor recebeu /fail" $(grep -q '/fail' "$STUB_CURL_LOG"; echo $?)
confere "sem status: nenhum OK enviado ao monitor" $(! grep -q 'ok postgres' "$STUB_CURL_LOG"; echo $?)

echo; echo "Resultado: $OK conferências certas, $RUIM erradas."
[ "$RUIM" = 0 ]
