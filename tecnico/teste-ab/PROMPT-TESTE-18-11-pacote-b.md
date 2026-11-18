# Prompt de verificação: Pacote B do backup e dos roteiros (18/11/2026)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. **Só use depois que a Erica confirmar que o script novo foi instalado no servidor** (a conversa que fez o Pacote B avisa). Isto é só leitura: nenhum teste da Clara roda aqui.

---

Projeto Keshion. Quero conferir no servidor a correção do backup (Pacote B, itens B1 e B3, e B2 se o monitor já estiver ligado). Leia `CLAUDE.md` e `tecnico/servidor-n8n.md` (seção Backup). **Só leitura**: não rode backup manual, não reinicie o n8n, não restaure nada, não apague nada e não mostre senha, token, chave privada nem o endereço do monitor. Se achar problema, descreva; quem corrige é outra conversa.

## O que mudou

`tecnico/servidor/backup-postgres.sh` agora: grava `EM ANDAMENTO` no início e `OK` só no fim; qualquer erro (até `.env` ausente ou falha do `mktemp`) vira `FALHA`; usa `flock` para não rodar duas vezes ao mesmo tempo; apaga dumps locais com mais de 7 dias, inclusive `.parcial`; confere o tamanho dos **dois** arquivos no Drive; os nomes têm segundos (`postgres-AAAA-MM-DD_HHMMSS.sql.gz.age`); e, se `HC_BACKUP_URL` estiver no `.env`, avisa o Healthchecks.io (início, sucesso, falha).

## Conferir (SSH: `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`)

1. **Script instalado = Git:** comparar o SHA-256 de `/opt/keshion/backup-postgres.sh` com o de `tecnico/servidor/backup-postgres.sh` (ignorando fim de linha CRLF); `bash -n` no servidor; permissão 700; existe cópia `backup-postgres.sh.bak-*` da versão antiga; `command -v flock curl` presentes.
2. **Status e primeira rodada automática** (se já passou das 03h de 19/11, hora de Curitiba): `cat /opt/keshion/backups/STATUS-BACKUP.txt` deve dizer `OK 2026-11-19 03:..`; `tail` do `/var/log/keshion-backup.log` mostra início e fim sem erro; `ls -l /opt/keshion/backups/` mostra um `postgres-2026-11-19_03....sql.gz` novo (com segundos no nome), nenhum `.parcial` e nada com mais de 7 dias.
3. **Drive (só nomes e tamanhos, sem baixar):** `rclone --config /opt/keshion/rclone.conf lsl gdrive:keshion-backups/postgres` e `.../config`: os dois arquivos da rodada de 19/11 existem, com o mesmo carimbo de hora, e o tamanho do banco bate com o `.age` da rodada (o script já conferiu; aqui só confirmar).
4. **Cron intacto:** `/etc/cron.d/keshion-backup` continua `0 3 * * *` chamando o script; anotar a permissão de `/var/log/keshion-backup.log` (recomendado 600; só avisar, não mudar).
5. **Monitor (só se a Erica já criou a conta):** `grep -c '^HC_BACKUP_URL=' /opt/keshion/.env` deve dar 1 (nunca mostrar o valor); na tela do Healthchecks (a Erica confere ou mostra print) o check "Backup Keshion" aparece verde depois da rodada.
6. **Teste local sem custo no PC (pode rodar):** `bash tecnico/servidor/testar-backup-local.sh` deve terminar com "33 conferências certas, 0 erradas".
7. **n8n intocado:** `docker compose ps` mostra o n8n no ar há muito tempo (sem reinício recente) e o uptime não zerou por causa do backup.

## Trazer de volta

Uma tabela curta: item, resultado (OK, atenção, problema), evidência em uma linha. Anotar também o horário de Curitiba da conferência e qualquer coisa que a Erica precise decidir. Se a rodada de 03h de 19/11 ainda não aconteceu, dizer isso e marcar os itens 2 e 3 como pendentes.
