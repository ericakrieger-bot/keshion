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

**Regras de segurança deste roteiro:** (1) **nunca reiniciar o n8n**: ele atende todas as clínicas e reiniciar derruba conversas em andamento; para publicar, `import:workflow` e `publish:workflow` bastam. (2) Senha nunca vai na linha de comando (quem tem acesso ao servidor consegue ver os argumentos de um processo): entra por entrada padrão (`<<SQL`), por variável de ambiente (`-e PGPASSWORD`) ou por arquivo temporário com permissão 600 que é apagado em seguida. (3) Nada de senha, token ou caminho do webhook no chat nem no Git.

---

## 0. Antes de começar (E e Cl)

- Questionário da clínica respondido: tratamentos, valores, endereço, horários, voz, nome da assistente.
- Quem recebe os avisos da equipe (aprovador), com o OK da clínica. O alerta de falha do WhatsApp é da Keshion (`alerta-keshion.json`) e não muda por clínica.
- Número de WhatsApp da clínica conectado num canal do Whapi (anotar o id do canal) e plano do Whapi pago.
- Conta Google com a agenda das avaliações (pode ser a da clínica ou uma conta criada para ela).
- Contrato e termo de dados assinados.

## 1. Pasta e ficha (C)

1. Copiar `clientes/_modelo/` para `clientes/<slug>/`.
2. Preencher `clinica.json`. Todo `PREENCHER` precisa sumir. Ids dos fluxos: exatamente 16 letras ou números, diferentes de todas as outras clínicas (ex.: `VivianAtendiment`, `VivianEnvio00001`).
3. Deixar `numeros_keshion` vazio: `#reiniciar` só existe na demo, e o `preparar_banco.py` recusa se tiver número.
4. Escrever `instrucoes.md` e `base-clinica.md` na pasta. A voz da clínica fica na parte "Registro" da base.
5. Conferir: `python tecnico/n8n/preparar_banco.py <slug>`. Ele recusa e diz o que falta. Os ids das credenciais só existem depois da seção 4: se a recusa for só por isso, seguir e rodar de novo depois de preenchê-los.

## 2. Senhas no servidor (C)

Duas senhas novas, só no `/opt/keshion/.env`, nunca no chat nem no Git:

```bash
cd /opt/keshion && umask 077 && cp .env .env.bak-$(date +%Y%m%d-%H%M)
echo "<BANCO>_DB_PASSWORD=$(openssl rand -hex 24)" >> .env
echo "<BANCO>_APP_DB_PASSWORD=$(openssl rand -hex 24)" >> .env
chmod 600 .env
```

## 3. Banco no servidor (C)

```bash
cd /opt/keshion; set -a; . ./.env; set +a
# senhas entram pela entrada padrão (<<SQL), nunca na linha de comando
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U $POSTGRES_USER -d $POSTGRES_DB -q <<SQL
CREATE ROLE <banco> LOGIN PASSWORD '$<BANCO>_DB_PASSWORD';
CREATE ROLE <banco>_app LOGIN PASSWORD '$<BANCO>_APP_DB_PASSWORD';
CREATE DATABASE <banco> OWNER <banco>;
REVOKE CONNECT ON DATABASE <banco> FROM PUBLIC;
SQL
```

Gerar o SQL no PC (`python tecnico/n8n/preparar_banco.py <slug>`), copiar `tecnico/n8n/gerados/<slug>/banco.sql` para `/tmp/banco.sql` no servidor (permissão 600) e rodar **como dono**. Ele cria as tabelas, grava a config e dá as permissões ao `<banco>_app`. A senha do dono vai pelo ambiente (`-e PGPASSWORD`, sem valor na linha de comando):

```bash
export PGPASSWORD="$<BANCO>_DB_PASSWORD"
docker compose exec -T -e PGPASSWORD postgres psql -v ON_ERROR_STOP=1 -h localhost -U <banco> -d <banco> -q < /tmp/banco.sql
unset PGPASSWORD; rm -f /tmp/banco.sql
```

O SQL para sozinho se for rodado no banco de outra clínica. Toda vez que mudar instruções, base ou config, rodar de novo o `preparar_banco.py` e aplicar o SQL do mesmo jeito.

Conferir que o banco de outra clínica recusa o usuário novo (precisa dar "does not have CONNECT privilege"):

```bash
export PGPASSWORD="$<BANCO>_APP_DB_PASSWORD"
docker compose exec -T -e PGPASSWORD postgres psql -h localhost -U <banco>_app -d clara -c 'select 1' || echo "recusado, como esperado"
unset PGPASSWORD
```

## 4. Credenciais no n8n (E e C)

- **Postgres (C):** pelo servidor, com o usuário **`<banco>_app`**, nunca o dono. O id é escolhido por nós (16 caracteres; mesmo formato da `clinicateste0001`). A senha sai do `.env` direto para um arquivo com permissão 600, entra no contêiner por entrada padrão (sem aparecer em comando) e os dois arquivos são apagados no fim:

  ```bash
  cd /opt/keshion; set -a; . ./.env; set +a; umask 077
  J=$(mktemp)
  cat > "$J" <<JSON
  [{"id":"<id16caracteres>","name":"Postgres <slug>","type":"postgres",
    "data":{"host":"postgres","port":5432,"database":"<banco>","user":"<banco>_app",
            "password":"$<BANCO>_APP_DB_PASSWORD","ssl":"disable"}}]
  JSON
  docker compose exec -T n8n sh -c 'umask 077; cat > /tmp/cred.json' < "$J"
  docker compose exec -T n8n n8n import:credentials --input=/tmp/cred.json
  docker compose exec -T -u root n8n rm -f /tmp/cred.json; rm -f "$J"
  ```

  Conferir na tela do n8n que a credencial apareceu com o banco e o usuário certos (a senha não aparece). Se o formato do JSON for recusado, exportar a credencial da demo **sem** `--decrypted` só para ver os nomes dos campos.
- **Whapi (E):** na tela do n8n, tipo "Header Auth", com o token do canal da clínica.
- **Google Agenda (E):** na tela do n8n, entrando com a conta Google da agenda dela.
- Anotar os três ids em `credenciais_n8n` no `clinica.json`. Anthropic e OpenAI podem ser as da Keshion.

## 5. Fluxos (C)

1. Criar um caminho secreto para o webhook (`openssl rand -hex 16`) e colocar em `tecnico/n8n/segredos.local.json`: `"<slug>": {"webhook_path": "..."}`.
2. Gerar: `python tecnico/n8n/gerar_fluxos.py <slug>`. Ele recusa a ficha se algo coincidir com outra clínica.
3. Se já existir versão no ar (fluxo atualizado, não clínica nova), guardar a atual antes. A pasta fica no servidor, com permissão 700, porque o fluxo contém o caminho secreto do webhook:

```bash
cd /opt/keshion; umask 077; mkdir -p versoes/<slug>; chmod 700 versoes versoes/<slug>
A=versoes/<slug>/<id>-$(date +%Y%m%d-%H%M).json
docker compose exec -T n8n n8n export:workflow --id=<id> --output=/tmp/anterior.json
docker compose exec -T n8n cat /tmp/anterior.json > "$A"; chmod 600 "$A"
docker compose exec -T -u root n8n rm -f /tmp/anterior.json
ls -l "$A"
```

4. Copiar `gerados/<slug>/envio.json` e `atendimento.json` para o servidor e, para cada id (**primeiro o de envio**, depois o de atendimento). **Sem reiniciar o n8n**:

```bash
docker compose cp /tmp/<id>.json n8n:/tmp/<id>.json
docker compose exec -T n8n sh -c "n8n import:workflow --input=/tmp/<id>.json && n8n publish:workflow --id=<id>"
docker compose exec -T -u root n8n rm -f /tmp/<id>.json; rm -f /tmp/<id>.json
```

5. Conferir na tela do n8n: os dois fluxos com os ids certos, publicados, com as credenciais desta clínica (nenhuma da demo) e o nome da assistente certo. Conferir também que o publicado é igual ao gerado (exportar e comparar com o arquivo de `gerados/`).

**Voltar à versão anterior** (se o teste da seção 7 falhar, ou a Erica pedir): com OK da Erica, importar de novo o arquivo guardado no passo 3 e publicar, sem reiniciar:

```bash
cd /opt/keshion
docker compose cp versoes/<slug>/<id>-AAAAMMDD-HHMM.json n8n:/tmp/<id>.json
docker compose exec -T n8n sh -c "n8n import:workflow --input=/tmp/<id>.json && n8n publish:workflow --id=<id>"
docker compose exec -T -u root n8n rm -f /tmp/<id>.json
```

Em clínica nova (sem versão anterior), voltar atrás é despublicar os dois fluxos (`n8n unpublish:workflow --id=<id>`) e, se preciso, tirar o webhook do painel do Whapi. O banco da clínica não é apagado.

## 6. Ligar o WhatsApp (E, com OK da clínica)

No painel do Whapi, no canal da clínica: webhook apontando para `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`, evento de mensagens. A clínica continua no `modo_teste = 1`: o fluxo recebe, mas nada sai para pacientes reais.

## 7. Testar (C, um teste por vez)

- Mandar conversas de números `554199900...` para o webhook da clínica e conferir as respostas na tabela `saidas_teste` do banco dela, nunca no banco de outra.
- Conferir: nome da assistente, endereço, valores, agenda livre e marcação no calendário certo. Depois, apagar os eventos de teste da agenda.
- Rodar o paciente simulado adaptado para a clínica e mandar o resultado para a Erica.
- Limpar as fichas de teste no banco dela.
- **Backup antes de valer:** depois da próxima rodada das 03h (ou de um backup manual com OK da Erica), conferir `STATUS-BACKUP.txt` em `OK` e que o banco novo aparece na restauração de teste (`tecnico/servidor-n8n.md`, passo 2.1).

## 8. Valer (E, com a clínica)

- Combinar o dia com a clínica. Na 1ª semana, acompanhar as conversas de perto. **Modo copiloto (aprovar antes de enviar) ainda não existe no fluxo**: não oferecer à clínica até ser construído.
- Trocar `modo_teste` para `0` no `clinica.json`, gerar e aplicar o SQL de novo.
- Acompanhar as primeiras conversas reais.

## 9. Depois (C)

- Atualizar a tabela de clínicas no `LEIA-ME.md` e o `tecnico/RETOMAR-AQUI.md`.
- Pedir revisão do Codex com `tecnico/n8n/PROMPT-CODEX-REVISAO.md`.
