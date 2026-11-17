# Clínica nova: passo a passo

Roteiro geral para colocar uma clínica no ar. Serve para a Dra. Vivian e para as próximas. Troque nos comandos:

| Marcador | O que é | Exemplo |
|---|---|---|
| `<slug>` | nome da pasta da clínica | `dra-vivian` |
| `<banco>` | banco dela no Postgres (só letras minúsculas, números e `_`) | `clinica_vivian` |
| `<BANCO>` | o mesmo nome em maiúsculas, para as senhas no `.env` | `CLINICA_VIVIAN` |

Cada clínica tem dois usuários no banco:
- **dono `<banco>`:** cria as tabelas e só é usado na instalação;
- **dia a dia `<banco>_app`:** é o usuário do n8n. Lê e grava fichas e mensagens, só lê a `config` e não pode apagar nem mudar tabelas. Testado em 17/11 num Postgres descartável.

Quem faz o quê: **E** = Erica, **C** = Claude (pelo servidor), **Cl** = clínica. Passos que mexem no servidor de produção: o Claude pede OK antes.

---

## 0. Antes de começar (E e Cl)

- Questionário da clínica respondido: tratamentos, valores, endereço, horários, voz, nome da assistente.
- Quem recebe os avisos (aprovador) e quem recebe o alerta de falha, com o OK da clínica.
- Número de WhatsApp da clínica conectado num canal do Whapi (anotar o id do canal) e plano do Whapi pago.
- Conta Google com a agenda das avaliações (pode ser a da clínica ou uma conta criada para ela).
- Contrato e termo de dados assinados.

## 1. Pasta e ficha (C)

1. Copiar `clientes/_modelo/` para `clientes/<slug>/`.
2. Preencher `clinica.json`. Todo `PREENCHER` precisa sumir. Ids dos fluxos: exatamente 16 letras ou números, diferentes de todas as outras clínicas (ex.: `VivianAtendiment`, `VivianEnvio00001`).
3. Deixar `numeros_keshion` vazio: `#reiniciar` só existe na demo, e o `preparar_banco.py` recusa se tiver número.
4. Escrever `instrucoes.md` e `base-clinica.md` na pasta. A voz da clínica fica na parte "Registro" da base.
5. Conferir: `python tecnico/n8n/preparar_banco.py <slug>`. Ele recusa e diz o que falta.

## 2. Senhas no servidor (C)

Duas senhas novas, só no `/opt/keshion/.env`, nunca no chat nem no Git:

```bash
cd /opt/keshion && cp .env .env.bak-$(date +%Y%m%d)
echo "<BANCO>_DB_PASSWORD=$(openssl rand -hex 24)" >> .env
echo "<BANCO>_APP_DB_PASSWORD=$(openssl rand -hex 24)" >> .env
chmod 600 .env
```

## 3. Banco no servidor (C)

```bash
cd /opt/keshion; set -a; . ./.env; set +a
P="docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $POSTGRES_USER -d $POSTGRES_DB -q"
$P -c "CREATE ROLE <banco> LOGIN PASSWORD '$<BANCO>_DB_PASSWORD'"
$P -c "CREATE ROLE <banco>_app LOGIN PASSWORD '$<BANCO>_APP_DB_PASSWORD'"
$P -c "CREATE DATABASE <banco> OWNER <banco>"        # sozinho: não roda dentro de transação
$P -c "REVOKE CONNECT ON DATABASE <banco> FROM PUBLIC"
```

Gerar o SQL no PC (`python tecnico/n8n/preparar_banco.py <slug>`), copiar `tecnico/n8n/gerados/<slug>/banco.sql` para o servidor e rodar **como dono**. Ele cria as tabelas, grava a config e dá as permissões ao `<banco>_app`:

```bash
docker compose exec -T postgres sh -c "PGPASSWORD=\"$<BANCO>_DB_PASSWORD\" psql -v ON_ERROR_STOP=1 -h localhost -U <banco> -d <banco> -q" < /tmp/banco.sql
rm /tmp/banco.sql
```

O SQL para sozinho se for rodado no banco de outra clínica. Toda vez que mudar instruções, base ou config, rodar de novo o `preparar_banco.py` e aplicar o SQL do mesmo jeito.

Conferir que o banco de outra clínica recusa o usuário novo (precisa dar "does not have CONNECT privilege"):

```bash
docker compose exec -T postgres sh -c "PGPASSWORD=\"$<BANCO>_APP_DB_PASSWORD\" psql -h localhost -U <banco>_app -d clara -c 'select 1'"
```

## 4. Credenciais no n8n (E e C)

- **Postgres (C):** pelo servidor, com o usuário **`<banco>_app`**, nunca o dono. Montar um arquivo temporário dentro do contêiner com a senha do `.env`, rodar `n8n import:credentials --input=/tmp/cred.json` e apagar o arquivo. Foi assim com `clinicateste0001`. O id é escolhido por nós (16 caracteres).
- **Whapi (E):** na tela do n8n, tipo "Header Auth", com o token do canal da clínica.
- **Google Agenda (E):** na tela do n8n, entrando com a conta Google da agenda dela.
- Anotar os três ids em `credenciais_n8n` no `clinica.json`. Anthropic e OpenAI podem ser as da Keshion.

## 5. Fluxos (C)

1. Criar um caminho secreto para o webhook (`openssl rand -hex 16`) e colocar em `tecnico/n8n/segredos.local.json`: `"<slug>": {"webhook_path": "..."}`.
2. Gerar: `python tecnico/n8n/gerar_fluxos.py <slug>`. Ele recusa a ficha se algo coincidir com outra clínica.
3. Copiar `gerados/<slug>/envio.json` e `atendimento.json` para o servidor e, para cada id (primeiro o de envio):

```bash
docker compose cp /tmp/<id>.json n8n:/tmp/<id>.json
docker compose exec -T n8n sh -c "n8n import:workflow --input=/tmp/<id>.json && n8n publish:workflow --id=<id>"
docker compose exec -T -u root n8n rm -f /tmp/<id>.json; rm /tmp/<id>.json
docker compose restart n8n
```

4. Conferir na tela do n8n: os dois fluxos com os ids certos, publicados, com as credenciais desta clínica (nenhuma da demo) e o nome da assistente certo.

## 6. Ligar o WhatsApp (E, com OK da clínica)

No painel do Whapi, no canal da clínica: webhook apontando para `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`, evento de mensagens. A clínica continua no `modo_teste = 1`: o fluxo recebe, mas nada sai para pacientes reais.

## 7. Testar (C, um teste por vez)

- Mandar conversas de números `554199900...` para o webhook da clínica e conferir as respostas na tabela `saidas_teste` do banco dela, nunca no banco de outra.
- Conferir: nome da assistente, endereço, valores, agenda livre e marcação no calendário certo. Depois, apagar os eventos de teste da agenda.
- Rodar o paciente simulado adaptado para a clínica e mandar o resultado para a Erica.
- Limpar as fichas de teste no banco dela.

## 8. Valer (E, com a clínica)

- Combinar o dia com a clínica. Na 1ª semana, decidir se roda em copiloto (aprovar antes de enviar).
- Trocar `modo_teste` para `0` no `clinica.json`, gerar e aplicar o SQL de novo.
- Acompanhar as primeiras conversas reais.

## 9. Depois (C)

- Atualizar a tabela de clínicas no `LEIA-ME.md` e o `tecnico/RETOMAR-AQUI.md`.
- Conferir que o backup inclui o banco novo.
- Pedir revisão do Codex com `tecnico/n8n/PROMPT-CODEX-REVISAO.md`.
