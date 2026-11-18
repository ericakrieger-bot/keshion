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
- `/opt/keshion/.env` (permissão 600): endereço, usuário e senha do Postgres, `N8N_ENCRYPTION_KEY`.
- `/opt/keshion/backup-postgres.sh`: backup.

Configuração do n8n: banco Postgres, `N8N_HOST` e `WEBHOOK_URL` com o endereço acima, `N8N_PROXY_HOPS=1` (atrás do Caddy), estatísticas de uso desligadas.

## Backup

Desde 18/11/2026 o backup tem cópia fora do servidor, criptografada. Script: `/opt/keshion/backup-postgres.sh` (cópia oficial no Git: `tecnico/servidor/backup-postgres.sh`; versão antiga em `backup-postgres.sh.bak-20261118`).

- **Quando:** todo dia às 03h, horário do servidor (`/etc/cron.d/keshion-backup`). Registro em `/var/log/keshion-backup.log`.
- **O que faz:** `pg_dumpall` compactado em `/opt/keshion/backups/` (7 mais recentes no servidor), confere que o dump terminou inteiro, criptografa com `age` e envia ao Google Drive da conta keshion.ai.2026@gmail.com, pasta `keshion-backups/` (`postgres/` com os bancos, `config/` com `.env`, `docker-compose.yml`, `Caddyfile` e o próprio script). Confere o tamanho no Drive e apaga lá o que tiver mais de 30 dias.
- **Resultado:** `/opt/keshion/backups/STATUS-BACKUP.txt` diz `OK` ou `FALHA` com data e etapa. Conferir: `ssh -i ~/.ssh/keshion_vps root@169.58.41.107 cat /opt/keshion/backups/STATUS-BACKUP.txt`. Ainda não avisa ninguém sozinho: isso entra com o canal de alerta fora do WhatsApp.
- **Chaves:** o servidor só tem a chave **pública** (`/opt/keshion/backup-chave-publica.txt`, só tranca). A chave **privada** (abre) fica no PC da Erica em `C:\Users\Erica Krieger-Akerma\.keshion-backup\chave-backup-keshion.txt` e no Bitwarden da Erica (junto com o `.env`). Na mesma pasta do PC: `rclone.conf` (acesso ao Drive, escopo só dos arquivos que o rclone criou), `chave-publica.txt` e `env-servidor-20261118.txt` (cópia do `.env` do servidor). Nada disso entra no Git. **Sem a chave privada, os backups do Drive não abrem.**
- **Ferramentas:** servidor com `age` 1.1.1 e `rclone` 1.60 (apt); PC com age 1.3.2 e rclone 1.76 (winget), em `%LOCALAPPDATA%\Microsoft\WinGet\Packages\`.
- **Atenção:** o rclone usa o client_id compartilhado dele para o Google Drive, que o rclone avisa que será desativado em 2026. Se o backup começar a dar `FALHA` na etapa de envio, criar um client_id próprio no Google Cloud, num app só para o backup (escopo `drive.file`, não sensível: deve dar para publicar sem análise do Google, sem logo; app em modo Teste expira a autorização em 7 dias), refazer `rclone config` no PC com esse client_id e copiar o `rclone.conf` novo para `/opt/keshion/`. Decidido em 18/11: só migrar quando o compartilhado parar.
- **Tamanho:** o dump cresce com as execuções do n8n (52 MB em 18/11 de manhã, 66 MB à tarde). 30 dias cabem folgados nos 15 GB do Drive.

### Restaurar (testado em 18/11/2026)

Teste de ponta a ponta feito em 18/11: arquivo baixado do Drive, aberto com a chave do PC, restaurado num Postgres temporário sem rede; `clara`, `clinica_teste` e `n8n` voltaram com todas as tabelas (diferenças só de movimento depois da hora do backup), e um n8n 2.47.5 temporário ligado na cópia abriu as 6 credenciais e os 6 fluxos. Produção não foi tocada.

Passos (no Git Bash do PC; `RC` e `AGE` são os caminhos do rclone e do age instalados pelo winget):

```bash
D="$HOME/.keshion-backup"; K="$HOME/.ssh/keshion_vps"; S=root@169.58.41.107
"$RC" --config "$D/rclone.conf" lsl gdrive:keshion-backups/postgres     # escolher o arquivo
ARQ=postgres-AAAA-MM-DD_HHMM.sql.gz.age
```

1. **Cópia isolada para conferir (não mexe na produção):**
   ```bash
   ssh -i "$K" $S 'docker run -d --name restore-teste --network none -e POSTGRES_PASSWORD=descartavel postgres:16.15'
   "$RC" --config "$D/rclone.conf" cat gdrive:keshion-backups/postgres/$ARQ | "$AGE" -d -i "$D/chave-backup-keshion.txt" \
     | ssh -i "$K" $S 'gunzip | docker exec -i restore-teste psql -U postgres -q -o /dev/null'
   ```
   Para ver o n8n abrindo as credenciais: rodar a imagem `docker.n8n.io/n8nio/n8n:2.47.5` com `--network container:restore-teste`, `DB_POSTGRESDB_HOST=localhost`, as variáveis do `.env` e `n8n export:credentials --all --decrypted` (não imprimir o resultado). No fim: `docker rm -f -v restore-teste`.
2. **Servidor novo (perda total):** instalar Docker; criar `/opt/keshion`; abrir a configuração do Drive (`"$RC" ... cat gdrive:keshion-backups/config/<arquivo> | "$AGE" -d -i "$D/chave-backup-keshion.txt" | ssh ... 'tar -xzf - -C /opt/keshion'`); `docker compose up -d postgres`; esperar ficar saudável; restaurar o dump como no passo 1, mas em `docker compose exec -T postgres psql -U <POSTGRES_USER> -d postgres`; depois `docker compose up -d`. O `.env` restaurado traz a mesma `N8N_ENCRYPTION_KEY`, então as credenciais abrem. Apontar o DNS (ou o sslip) para o IP novo, recolocar `backup-chave-publica.txt`, `rclone.conf`, o cron e instalar `age` e `rclone`.
3. **Voltar a produção a um dia anterior (servidor vivo):** só com OK da Erica e com o n8n parado (`docker compose stop n8n`); fazer antes um backup do estado atual. Restaurar sobre bancos existentes exige apagá-los antes (`DROP DATABASE`), por isso a recomendação é conferir primeiro na cópia isolada.

## Comandos úteis (dentro do servidor, em `/opt/keshion`)

- Ver estado: `docker compose ps`
- Ver registros do n8n: `docker compose logs --tail 100 n8n`
- Reiniciar: `docker compose restart`
- Atualizar o n8n: trocar a versão fixa no `docker-compose.yml`, depois `docker compose pull && docker compose up -d` (fazer um backup antes: `./backup-postgres.sh`)

## Pendências deste servidor

1. **A Erica cria o usuário dono do n8n** na primeira tela do endereço acima.
2. ✅ Cópia do `/opt/keshion/.env` fora do servidor (18/11/2026): no PC (`.keshion-backup\env-servidor-20261118.txt`) e criptografada no Drive todo dia. Guardado também no Bitwarden da Erica, junto com a chave privada do backup.
3. ✅ Backups copiados para fora do servidor (18/11/2026, Google Drive, ver Backup).
4. Hoje o acesso é como root, só por chave. O LEIA-PRIMEIRO previa um usuário não root com sudo; não foi pedido nesta etapa e fica para decidir.
5. Trocar o endereço para `n8n.keshion.com.br` quando o domínio for registrado (mudar `DOMINIO` no `.env` e o DNS, e reiniciar).
