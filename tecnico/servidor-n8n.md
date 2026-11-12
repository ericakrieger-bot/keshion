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

- Todo dia às 03h (`/etc/cron.d/keshion-backup`), um `pg_dumpall` compactado em `/opt/keshion/backups/`, guardando os 7 mais recentes. Registro em `/var/log/keshion-backup.log`.
- Testado em 12/11/2026: arquivo gerado normalmente.
- Limite: o backup fica no mesmo servidor. Se o servidor se perder, o backup vai junto. Falta uma cópia fora dele (ver pendências).

## Comandos úteis (dentro do servidor, em `/opt/keshion`)

- Ver estado: `docker compose ps`
- Ver registros do n8n: `docker compose logs --tail 100 n8n`
- Reiniciar: `docker compose restart`
- Atualizar o n8n: trocar a versão fixa no `docker-compose.yml`, depois `docker compose pull && docker compose up -d` (fazer um backup antes: `./backup-postgres.sh`)

## Pendências deste servidor

1. **A Erica cria o usuário dono do n8n** na primeira tela do endereço acima.
2. **Guardar uma cópia do `/opt/keshion/.env` fora do servidor** (gerenciador de senhas). Sem a `N8N_ENCRYPTION_KEY`, as credenciais salvas no n8n não podem ser lidas de novo se o servidor for refeito.
3. Copiar os backups para fora do servidor (por exemplo, para o Google Drive da Keshion).
4. Hoje o acesso é como root, só por chave. O LEIA-PRIMEIRO previa um usuário não root com sudo; não foi pedido nesta etapa e fica para decidir.
5. Trocar o endereço para `n8n.keshion.com.br` quando o domínio for registrado (mudar `DOMINIO` no `.env` e o DNS, e reiniciar).
