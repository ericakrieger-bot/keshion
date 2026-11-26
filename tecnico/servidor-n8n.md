# Servidor do n8n (Keshion) · resumo da instalação

Instalado em 12/11/2026. Este arquivo não tem senhas nem chaves. Elas estão só em `/opt/keshion/.env` dentro do servidor.

## Acesso

| Item | Valor |
|---|---|
| Provedor | Contabo |
| IP | 169.58.41.107 |
| Sistema | Ubuntu 24.04.5 LTS (4 núcleos, 7,8 GB de memória, 96 GB de disco) |
| Entrar | `ssh -i ~/.ssh/keshion_vps root@169.58.41.107` (só por chave desde 12/11/2026, tarde: `/etc/ssh/sshd_config.d/00-keshion.conf` desliga senha e teclado interativo e deixa o root só com chave; vem antes do `50-cloud-init.conf` da Contabo, que ligava a senha. Conferido com `sshd -T` e com tentativa de senha recusada. Se perder a chave, entrar pelo console VNC do painel da Contabo) |
| Endereço do n8n (provisório) | https://n8n.169-58-41-107.sslip.io |
| Certificado | Let's Encrypt, renovação automática pelo Caddy (primeiro vence em 10/02/2027) |
| Fuso | America/Sao_Paulo (servidor e n8n) |

Observação: o Norton do computador da Erica intercepta o HTTPS e mostra o certificado dele. O certificado real do servidor foi conferido de dentro do próprio servidor e está correto.

## O que foi preparado no sistema

- Pacotes atualizados e servidor reiniciado.
- Atualizações automáticas de segurança ligadas (`unattended-upgrades`).
- Firewall (`ufw`): entrada só nas portas 22, 80 e 443; o resto bloqueado.
- `fail2ban` ligado para o SSH (5 erros em 10 minutos bloqueiam o IP por 1 hora).
- Docker 29.9.3 e Docker Compose v5.7.1, pelo repositório oficial.

## O que roda em `/opt/keshion` (Docker Compose)

| Serviço | Imagem | Observação |
|---|---|---|
| `postgres` | `postgres:16` | Banco do n8n (`n8n`) e da Clara (`clara`, usuário `clara`, senha `CLARA_DB_PASSWORD` no `.env`). Sem porta aberta para fora. O n8n 2.47 avisa que prefere Postgres 17: funciona, mas planejar a atualização. |
| `n8n` | `docker.n8n.io/n8nio/n8n:stable` | Versão 2.47.5 na instalação. Sem porta aberta para fora. |
| `caddy` | `caddy:2` | Única porta pública (80 e 443). HTTPS automático e repasse para o n8n. |

Versões fixas desde 12/11/2026 (tarde), para nenhuma atualização chegar de surpresa: `docker.n8n.io/n8nio/n8n:2.47.5`, `postgres:16.15`, `caddy:2.11.9`. Variáveis novas: `N8N_WEBHOOK_URL` (no lugar da obsoleta `WEBHOOK_URL`), `EXECUTIONS_DATA_PRUNE=true` e `EXECUTIONS_DATA_MAX_AGE=336` (execuções guardadas por 14 dias). Cópia do Compose anterior: `docker-compose.yml.bak-20261112`. Para atualizar uma versão: trocar a etiqueta no Compose, fazer backup antes e testar.

Todos com `restart: always` (voltam sozinhos depois de reinício). Dados em volumes Docker: `postgres_data`, `n8n_data`, `caddy_data`, `caddy_config`.

Arquivos importantes no servidor:

- `/opt/keshion/docker-compose.yml`: a definição dos três serviços.
- `/opt/keshion/caddy/Caddyfile`: o endereço e o repasse para o n8n.
- `/opt/keshion/.env` (permissão 600): endereço, usuário e senha do Postgres, `N8N_ENCRYPTION_KEY`. Desde 25/11/2026 também `TYPESAFE_API_KEY` (Jev em modo sombra; a mesma chave está na credencial "TypeSafe (Jev)" do n8n, id `typesafejev00001`: se trocar a chave, trocar nos dois).
- `/opt/keshion/backup-postgres.sh`: backup.

Configuração do n8n: banco Postgres, `N8N_HOST` e `WEBHOOK_URL` com o endereço acima, `N8N_PROXY_HOPS=1` (atrás do Caddy), estatísticas de uso desligadas.

## Backup

Desde 18/11/2026 o backup tem cópia fora do servidor, criptografada. Script: `/opt/keshion/backup-postgres.sh` (cópia oficial no Git: `tecnico/servidor/backup-postgres.sh`; versões antigas em `backup-postgres.sh.bak-AAAAMMDD`). Teste local sem custo: `bash tecnico/servidor/testar-backup-local.sh` (52 conferências, com substitutos de docker, age, rclone, flock, curl, mkdir e mv).

- **Quando:** todo dia às 03h, horário do servidor (`/etc/cron.d/keshion-backup`). Registro em `/var/log/keshion-backup.log`.
- **O que faz:** `pg_dumpall` compactado em `/opt/keshion/backups/`, confere que o dump terminou inteiro, criptografa com `age` e envia ao Google Drive da conta keshion.ai.2026@gmail.com, pasta `keshion-backups/` (`postgres/` com os bancos, `config/` com `.env`, `docker-compose.yml`, `Caddyfile` e o próprio script). Confere o tamanho **dos dois arquivos** no Drive e apaga lá o que tiver mais de 30 dias. Os nomes levam data e hora com segundos: `postgres-AAAA-MM-DD_HHMMSS.sql.gz.age`.
- **Retenção no servidor:** por idade, 7 dias (`find -mtime +7`), incluindo dumps `.parcial` que sobraram de uma falha.
- **Resultado:** `/opt/keshion/backups/STATUS-BACKUP.txt` tem sempre uma de três formas: `EM ANDAMENTO` (logo no início), `OK` (só depois de tudo conferido) ou `FALHA` com data, etapa, linha e código. Qualquer erro, inclusive pasta de backups (`mkdir`), arquivo de trava, `.env` ausente, pasta temporária, interrupção ou **falha ao gravar o próprio status**, vira `FALHA` e código de saída diferente de zero (os `trap` são os primeiros comandos do script; o `OK` só é anunciado depois de gravado e relido; desde 20/11/2026): o `OK` antigo não fica no lugar. Duas execuções ao mesmo tempo não acontecem (`flock`): a segunda sai sem mexer no status. Limite: com o disco realmente cheio nenhum status local pode ser gravado; por isso o monitor externo precisa alertar também pela **ausência** de um sucesso novo. Conferir: `ssh -i ~/.ssh/keshion_vps root@169.58.41.107 cat /opt/keshion/backups/STATUS-BACKUP.txt`.
- **Alerta fora do WhatsApp (preparado, ainda desligado):** se existir `HC_BACKUP_URL` no `.env`, o script avisa o monitor externo (Healthchecks.io) no início, no sucesso e na falha, só com a etapa e o código do erro (nunca dados de paciente; a URL vai por stdin, não aparece em comando nem em log). O monitor também manda e-mail se não chegar sucesso até as 04h de Curitiba, o que cobre servidor fora do ar, cron parado ou `.env` perdido. Sem a variável, o script funciona igual e nada é enviado. Falta a Erica criar a conta (Pacote B2 no `RETOMAR-AQUI.md`).
- **Chaves:** o servidor só tem a chave **pública** (`/opt/keshion/backup-chave-publica.txt`, só tranca). A chave **privada** (abre) fica no PC da Erica em `C:\Users\Erica Krieger-Akerma\.keshion-backup\chave-backup-keshion.txt` e no Bitwarden da Erica (junto com o `.env`). Na mesma pasta do PC: `rclone.conf` (acesso ao Drive, escopo só dos arquivos que o rclone criou), `chave-publica.txt` e `env-servidor-20261118.txt` (cópia do `.env` do servidor). Nada disso entra no Git. **Sem a chave privada, os backups do Drive não abrem.**
- **Ferramentas:** servidor com `age` 1.1.1 e `rclone` 1.60 (apt); PC com age 1.3.2 e rclone 1.76 (winget), em `%LOCALAPPDATA%\Microsoft\WinGet\Packages\`.
- **Atenção (client_id do rclone):** o rclone usa o client_id compartilhado dele para o Google Drive, que será desativado em 2026 (sem data confirmada). Plano antes de 01/12/2026: criar um client_id próprio no Google Cloud (app só para o backup, **publicado**, escopo `drive.file`; em modo Teste a autorização expira em 7 dias), refazer `rclone config` no PC e copiar o `rclone.conf` novo para `/opt/keshion/`. Como `drive.file` só enxerga arquivos que o próprio aplicativo criou, **conferir se as cópias antigas continuam visíveis para o app novo**; se não, baixar uma cópia delas para o PC antes de trocar. Passo a passo para a Erica no `RETOMAR-AQUI.md` (Pacote B5).
- **O que o backup não cobre:** `rclone.conf`, chave pública e cron (refazer a partir do PC e deste documento), volumes `n8n_data` e Caddy (certificados são reemitidos sozinhos), Google Agenda e Whapi (depois de restaurar, conferir eventos e mensagens posteriores ao horário do backup), SSH, firewall, fail2ban e DNS (recriar).
- **Tamanho:** o dump cresce com as execuções do n8n (52 MB em 18/11 de manhã, 66 MB à tarde). 30 dias cabem folgados nos 15 GB do Drive.

### Restaurar (roteiro completo, versão de 20/11/2026)

Teste de ponta a ponta feito em 18/11 (com o roteiro anterior): arquivo baixado do Drive, aberto com a chave do PC, restaurado num Postgres temporário sem rede; `clara`, `clinica_teste` e `n8n` voltaram com todas as tabelas, e um n8n 2.47.5 temporário ligado na cópia abriu as 6 credenciais e os 6 fluxos. A versão de 18/11 com parada em erro parava num erro que ela mesma criava; esta de 20/11/2026 corrige isso (usuário inicial do destino diferente do usuário da produção, `--entrypoint sh` na imagem do n8n, arquivo de segredos apagado por `trap` mesmo em erro) e foi executada de ponta a ponta em 20/11/2026 num Postgres e num n8n descartáveis, sem rede, com dados e chaves **fictícios** (a chave privada real e os arquivos reais do Drive não foram usados). **Falta ainda um ensaio com o arquivo real do Drive e a chave privada real, com a Erica presente; anotar aqui qualquer parada.** Produção nunca é destino dos passos 1 e 2.

Regras: nada de segredo na tela (as conferências só mostram números e "sim/não"); se qualquer comando parar com erro, **parar e não seguir**; o Postgres e o n8n temporários são sempre apagados no fim (passo 4), mesmo com falha.

#### Passo 0: preparar o PC (Git Bash, uma vez por sessão)

```bash
set -euo pipefail
D="$HOME/.keshion-backup"; K="$HOME/.ssh/keshion_vps"; S=root@169.58.41.107
W="$LOCALAPPDATA/Microsoft/WinGet/Packages"
RC=$(command -v rclone || ls "$W"/Rclone.Rclone_*/rclone-*/rclone.exe | head -n 1)
AGE=$(command -v age || ls "$W"/FiloSottile.age_*/age/age.exe | head -n 1)
for f in "$RC" "$AGE" "$D/rclone.conf" "$D/chave-backup-keshion.txt" "$K"; do [ -e "$f" ] || { echo "FALTA: $f"; false; }; done
echo "ferramentas e chaves encontradas"
"$RC" --config "$D/rclone.conf" lsl gdrive:keshion-backups/postgres
```

Escolher o arquivo mais recente da lista e anotar o nome (`postgres-AAAA-MM-DD_HHMMSS.sql.gz.age`). Arquivos de antes de 19/11 têm hora sem segundos (`HHMM`); vale o nome que aparecer na lista.

```bash
ARQ=postgres-AAAA-MM-DD_HHMMSS.sql.gz.age
"$RC" --config "$D/rclone.conf" lsl "gdrive:keshion-backups/postgres/$ARQ"
```

#### Passo 1: Postgres temporário isolado (sem rede) e restauração

Rodar os blocos dos passos 1 e 2 na mesma janela do passo 0 (as variáveis `K`, `S`, `D`, `RC`, `AGE`, `ARQ` e `R` só existem nela). O `pg_dumpall` recria o usuário da produção (`CREATE ROLE`). Por isso o banco temporário **não pode** nascer com esse mesmo usuário: ele nasce com um usuário só do teste, `restaurador` (o usuário da produção entra pelo próprio dump). O nome do usuário da produção não é segredo:

```bash
set -euo pipefail
R=restaurador
U=$(ssh -i "$K" $S "sed -n 's/^POSTGRES_USER=//p' /opt/keshion/.env")
{ [ -n "$U" ] && [ "$U" != "$R" ]; } || { echo "usuário da produção vazio ou igual a $R"; false; }
echo "usuário da produção lido"
ssh -i "$K" $S "docker rm -f -v restore-teste >/dev/null 2>&1 || true
docker run -d --name restore-teste --network none -e POSTGRES_USER=$R -e POSTGRES_PASSWORD=descartavel postgres:16.15 >/dev/null
for i in \$(seq 1 60); do docker exec restore-teste pg_isready -U $R -d postgres -q && exit 0; sleep 2; done
echo 'Postgres temporário não ficou pronto'; exit 1"
echo "Postgres temporário pronto"
```

Restaurar, parando no primeiro erro de SQL (`ON_ERROR_STOP=1`) e em qualquer elo da cadeia (`pipefail` no PC e no servidor):

```bash
set -euo pipefail
"$RC" --config "$D/rclone.conf" cat "gdrive:keshion-backups/postgres/$ARQ" \
  | "$AGE" -d -i "$D/chave-backup-keshion.txt" \
  | ssh -i "$K" $S "set -o pipefail; gunzip | docker exec -i restore-teste psql -v ON_ERROR_STOP=1 -U $R -d postgres -q -o /dev/null"
echo "RESTAURAÇÃO TERMINOU SEM ERRO"
```

Só a frase final conta como sucesso. Se parar antes, o dump e o banco temporário não batem: anotar a mensagem, apagar tudo (passo 4) e pedir ajuda técnica; não improvisar em produção. (O erro `role "..." already exists` era justamente o do usuário inicial igual ao da produção: com `restaurador` ele não deve mais aparecer; se aparecer, merece investigação.)

#### Passo 2: critérios de conferência (todos precisam dar "sim")

2.1 Mesmas tabelas que a produção (a produção só é **lida**; diferença de linhas por movimento depois da hora do backup é normal, tabela faltando não):

```bash
ssh -i "$K" $S "set -euo pipefail; cd /opt/keshion; . ./.env
for B in clara clinica_teste n8n; do
  Q=\"select count(*) from information_schema.tables where table_schema='public'\"
  P=\$(docker compose exec -T postgres psql -U \$POSTGRES_USER -d \$B -Atc \"\$Q\")
  T=\$(docker exec restore-teste psql -U restaurador -d \$B -Atc \"\$Q\")
  [ \"\$P\" = \"\$T\" ] && echo \"\$B: tabelas iguais (\$T) = sim\" || { echo \"\$B: produção \$P x cópia \$T = NÃO\"; exit 1; }
done"
```

2.2 Papéis e fluxos presentes (só números e nomes de papéis, nada de pacientes):

```bash
ssh -i "$K" $S "set -euo pipefail; cd /opt/keshion; . ./.env
docker exec restore-teste psql -U restaurador -d postgres -Atc \"select 'papéis: '||string_agg(rolname, ', ' order by rolname) from pg_roles where rolname !~ '^pg_'\"
docker exec restore-teste psql -U restaurador -d n8n -Atc \"select 'fluxos: '||count(*) from workflow_entity\"
docker exec restore-teste psql -U restaurador -d n8n -Atc \"select 'credenciais: '||count(*) from credentials_entity\""
```

Esperado: papéis `clara`, `clinica_teste`, o usuário do banco da produção e `restaurador` (este só existe no teste); fluxos e credenciais com as mesmas contagens da produção (6 e 6 em 18/11; se a demo ganhou fluxos, comparar com a produção).

2.3 O n8n consegue **abrir** as credenciais (prova de que a chave de criptografia e o banco combinam). Só mostra uma contagem. O arquivo com os segredos nasce com permissão restrita e é **apagado por `trap` em qualquer saída, inclusive erro**; as credenciais abertas ficam só dentro do contêiner descartável (`--rm`). A imagem do n8n tem entrypoint próprio, então o shell precisa de `--entrypoint sh` (sem isso o Docker tenta rodar `n8n sh`):

```bash
ssh -i "$K" $S 'bash -s' <<'REMOTO'
set -euo pipefail; umask 077; cd /opt/keshion
E=$(mktemp)
trap 'rm -f "$E"' EXIT
{ sed -n 's/^N8N_ENCRYPTION_KEY=/N8N_ENCRYPTION_KEY=/p' .env
  echo DB_TYPE=postgresdb; echo DB_POSTGRESDB_HOST=localhost; echo DB_POSTGRESDB_DATABASE=n8n
  echo DB_POSTGRESDB_USER=restaurador
  echo DB_POSTGRESDB_PASSWORD=descartavel; } > "$E"
docker run --rm --network container:restore-teste --env-file "$E" --entrypoint sh docker.n8n.io/n8nio/n8n:2.47.5 \
  -c 'R=$(n8n export:credentials --all --decrypted --output=/tmp/c.json 2>&1) || { echo "n8n NÃO abriu as credenciais (a chave não bate com o banco?)"; exit 1; }; echo "$R" | grep -Eo "Successfully exported [0-9]+ credentials?"'
REMOTO
```

Esperado: "Successfully exported N credentials" com o mesmo N do 2.2. Se vier vazio ou o comando falhar, a `N8N_ENCRYPTION_KEY` não bate com o banco: **não considerar o backup válido**. (Se o `.env` usar outros nomes de variável, `grep -o '^[A-Z_]*=' /opt/keshion/.env` mostra só os nomes.)

#### Passo 3: servidor novo (perda total)

Só depois de passar o passo 2 com o arquivo escolhido.

1. Servidor Ubuntu 24.04 novo: instalar Docker e Compose (repositório oficial), `age` e `rclone`; criar `/opt/keshion` com permissão 700.
2. Trazer a configuração (`.env`, `docker-compose.yml`, `caddy/Caddyfile`) da pasta `config/` do Drive, pelo PC, parando em erro:
   ```bash
   set -euo pipefail
   "$RC" --config "$D/rclone.conf" lsl gdrive:keshion-backups/config
   CFG=config-AAAA-MM-DD_HHMMSS.tar.gz.age
   "$RC" --config "$D/rclone.conf" cat "gdrive:keshion-backups/config/$CFG" \
     | "$AGE" -d -i "$D/chave-backup-keshion.txt" \
     | ssh -i "$K" root@IP-NOVO 'set -o pipefail; tar -xzf - -C /opt/keshion'
   ```
3. No servidor novo, subir **só o Postgres, com um usuário inicial diferente do da produção** (a variável digitada no comando vence a do `.env`; `POSTGRES_DB=postgres` evita criar um banco `n8n` vazio, que colidiria com o do dump): `cd /opt/keshion && POSTGRES_USER=restaurador POSTGRES_DB=postgres docker compose up -d postgres`; esperar `docker compose exec -T postgres pg_isready -U restaurador` responder "accepting connections".
4. Restaurar o dump como no passo 1, trocando o destino por `docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U restaurador -d postgres -q -o /dev/null` (o usuário da produção, com a mesma senha do `.env`, volta pelo próprio dump). Só seguir se aparecer a frase de sucesso. Depois, **entrando como o usuário da produção** (`U` = `POSTGRES_USER` do `.env`), travar o usuário inicial: `docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U U -d postgres -c "ALTER ROLE restaurador NOLOGIN PASSWORD NULL"`. (O Postgres não deixa apagar nem repassar o usuário que criou o cluster; travado, ele não entra mais. Testado em 20/11/2026.) Conferir com `-U restaurador`: tem de dar "not permitted to log in".
5. `docker compose up -d`. O `.env` restaurado traz a mesma `N8N_ENCRYPTION_KEY`, então as credenciais abrem.
6. Apontar o DNS (ou o sslip) para o IP novo; recolocar `backup-chave-publica.txt` (de `~/.keshion-backup/chave-publica.txt` no PC), `rclone.conf` (do PC), o cron `/etc/cron.d/keshion-backup` e o `HC_BACKUP_URL` no `.env`; refazer firewall (`ufw`: 22, 80 e 443), `fail2ban` e SSH só por chave (seções acima).
7. Reconciliar o que fica fora do banco: eventos do Google Agenda e mensagens do Whapi posteriores ao horário do backup; reconectar autorizações revogadas (Google, Whapi).
8. Rodar `./backup-postgres.sh` uma vez (com OK da Erica) e conferir `OK` no status.

#### Passo 4: limpar (sempre, também se algo falhou)

```bash
ssh -i "$K" $S 'docker rm -f -v restore-teste >/dev/null 2>&1 || true; docker ps -a --format "{{.Names}}" | grep -c restore-teste || echo "nenhum contêiner temporário sobrando"'
```

#### Voltar a produção a um dia anterior (servidor vivo)

Só com OK da Erica e depois de conferir o arquivo na cópia isolada (passos 1 e 2). Fazer antes um backup do estado atual e decidir a janela. Restaurar sobre bancos existentes exige apagá-los antes (`DROP DATABASE`) com o n8n parado: é uma decisão à parte, com OK explícito, e não faz parte da rotina de conferência.

## Comandos úteis (dentro do servidor, em `/opt/keshion`)

- Ver estado: `docker compose ps`
- Ver registros do n8n: `docker compose logs --tail 100 n8n`
- **Não reiniciar o n8n** com conversas em andamento (`docker compose restart n8n` derruba o atendimento). Para publicar fluxo, `import:workflow` e `publish:workflow` bastam. Reinício só com OK da Erica e fora do horário de atendimento.
- Atualizar o n8n: trocar a versão fixa no `docker-compose.yml`, depois `docker compose pull && docker compose up -d` (fazer um backup antes: `./backup-postgres.sh`)

## Pendências deste servidor

1. **A Erica cria o usuário dono do n8n** na primeira tela do endereço acima.
2. ✅ Cópia do `/opt/keshion/.env` fora do servidor (18/11/2026): no PC (`.keshion-backup\env-servidor-20261118.txt`) e criptografada no Drive todo dia. Guardado também no Bitwarden da Erica, junto com a chave privada do backup.
3. ✅ Backups copiados para fora do servidor (18/11/2026, Google Drive, ver Backup).
4. Hoje o acesso é como root, só por chave. O LEIA-PRIMEIRO previa um usuário não root com sudo; não foi pedido nesta etapa e fica para decidir.
5. Trocar o endereço para `n8n.keshion.com` quando o domínio for registrado (mudar `DOMINIO` no `.env` e o DNS; o Caddy e o n8n precisam recarregar a configuração, então combinar a janela e pedir OK da Erica antes).
