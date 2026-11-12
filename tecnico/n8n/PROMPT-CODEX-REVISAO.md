# Prompt para o Codex revisar a Clara no n8n

Copie tudo abaixo da linha e cole no Codex, aberto na pasta `negocio-ia-clinicas` (repositório privado `ericakrieger-bot/keshion`).

---

Você vai fazer uma revisão independente de um sistema que outra IA (Claude) montou e testou. Quero uma segunda opinião honesta: o que está certo, o que está errado, o que é arriscado e o que não foi testado. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: no relatório final, explique cada problema em linguagem simples, além do detalhe técnico.

## O que é o sistema

A Keshion vende uma atendente de IA no WhatsApp para clínicas. A **Clara** é a atendente da clínica de demonstração (Dra. Suzana, fictícia). Ela acabou de ser migrada do Make para um **n8n próprio** e **já está no ar**: o WhatsApp de demonstração (Whapi, canal GRNLTR-4K8ZF) manda as mensagens para o n8n desde 12/11/2026.

Leia primeiro, nesta ordem:
1. `CLAUDE.md` (contexto do negócio e regras do projeto)
2. `tecnico/MIGRACAO-N8N-LEIA-PRIMEIRO.md` (o passo a passo da migração e o que já foi feito)
3. `tecnico/n8n/LEIA-ME.md` (como a Clara está montada no n8n, o que foi testado e o que não foi)
4. `tecnico/servidor-n8n.md` (o servidor)
5. `tecnico/n8n/gerar_fluxos.py` (gera os dois fluxos; é a fonte da verdade, os `.json` saem dele)
6. `tecnico/n8n/schema-clara.sql` (banco de dados)
7. `clientes/clinica-demo/instrucoes-sarah.md` e `clientes/clinica-demo/base-clinica.md` (as instruções e a base que a IA recebe; "Sarah" é o nome antigo da Clara)
8. `tecnico/make-cenarios/` (os cenários originais do Make, 1A, 1B, 1C e 1D, para comparar com a versão n8n)
9. `tecnico/teste-ab/teste_n8n.py`, `tecnico/teste-ab/comparar_n8n.py` e `tecnico/teste-ab/relatorio-n8n.md` (o teste das 56 mensagens e o resultado)

## Onde as coisas estão

- n8n: https://n8n.169-58-41-107.sslip.io (fluxos `Clara · Atendimento (WhatsApp)`, id `ClaraAtendimento`, e `Clara · Envio (até 3 mensagens)`, id `ClaraEnvio000001`)
- Webhook que o Whapi chama: `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`. Desde 12/11/2026 (tarde) o caminho fica só em `tecnico/n8n/segredos.local.json` (fora do Git); peça à Erica ou leia esse arquivo local. O corpo precisa ter `"channel_id": "GRNLTR-4K8ZF"`, e mídia só é baixada de links do Whapi (Wasabi).
- Servidor: `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`, tudo em `/opt/keshion` (Docker Compose com n8n, Postgres 16 e Caddy)
- Banco da Clara: Postgres, banco `clara`, usuário `clara`. Senha só em `/opt/keshion/.env` (`CLARA_DB_PASSWORD`). Exemplo de leitura, sem mostrar a senha:
  `cd /opt/keshion && set -a && . ./.env && set +a && docker compose exec -T postgres sh -c "PGPASSWORD=\"$CLARA_DB_PASSWORD\" psql -h localhost -U clara -d clara -c 'select chave, left(valor, 40) from config'"`
- Execuções do n8n (para ver erros): banco `n8n`, tabelas `execution_entity` e `execution_data`, usuário `keshion`.

## Regras de segurança (obrigatórias, a Clara está no ar)

1. **Teste só com números que começam com `554199900`** (exemplo: 554199900201). Esse prefixo está em `config.prefixo_teste`: qualquer conversa com esses números vai para a tabela `saidas_teste` e nada sai pelo WhatsApp, nem os avisos para a equipe. **Nunca** use outro número inventado: cada número novo que recebe mensagem pelo Whapi conta no plano pago e pode bloquear o canal.
2. **Não mude nada em produção sem me perguntar antes:** fluxos do n8n, tabela `config`, `.env`, credenciais, painel do Whapi, Docker. Leitura pode à vontade. Escrita permitida sem perguntar: só apagar as linhas de teste que você mesmo criou (`DELETE FROM pacientes WHERE telefone LIKE '554199900%'` e `DELETE FROM saidas_teste WHERE telefone LIKE '554199900%'`).
3. **Nunca mostre senha, token ou chave** no chat nem em arquivo. Se precisar de uma, leia do `.env` dentro do comando.
4. **Google Agenda é real** (agenda da conta da clínica demo). Se um teste marcar uma avaliação, cancele pela própria conversa no fim do teste e confira que nenhum evento de teste sobrou. Liste no relatório os eventos que sobraram, se algum sobrar.
5. Não toque no número da Erica (972584285541) nem no do Sérgio (972552994413): são números reais.
6. Não rode as 56 mensagens em paralelo mais de uma vez: cada rodada custa chamadas de IA.

## Como os testes foram feitos (para você repetir e ir além)

Os testes simulam o Whapi: um POST no webhook com o mesmo formato que o Whapi manda. Exemplo de corpo de mensagem de texto:
```json
{"messages":[{"id":"t-1","from_me":false,"type":"text","chat_id":"554199900201@s.whatsapp.net","from":"554199900201","from_name":"Teste","source":"mobile","text":{"body":"Oi, vocês fazem clareamento?"}}],"event":{"type":"messages","event":"post"}}
```
- Foto: `"type":"image","image":{"link":"<url pública de imagem>","caption":"..."}`. Atenção: a OpenAI não consegue baixar imagens da Wikimedia; use outro site (Pexels funcionou).
- Áudio: `"type":"voice","voice":{"link":"<url pública de um .ogg ou .mp3>"}`.
- Doutora respondendo pelo celular: `"from_me":true,"source":"mobile"` e `chat_id` com o número do paciente.
- Mensagens da própria Clara voltando: `"from_me":true,"source":"api"` (devem ser ignoradas).
- Envie sempre o corpo em UTF-8 (no Windows, use Python, não `curl` com acentos na linha de comando).

Depois de cada mensagem, a Clara espera 7 s (fila) e responde em uns 15 s. Confira:
- `saidas_teste`: o que teria sido enviado (para o paciente e para o aprovador 972584285541).
- `pacientes`: a ficha (conversa, pendente, nome_paciente, tratamento, avaliacao_inicio/texto/evento, pausado_ate).
- `execution_entity`: se a execução terminou com `success`.

O teste das 56 mensagens (`tecnico/teste-ab/teste_n8n.py`) roda **dentro do servidor** (`python3 teste_n8n.py`), usa os números 554199900101 a 554199900107 e grava o resultado em `/root/teste-n8n-resultado.json`. `comparar_n8n.py` compara com o Haiku da rodada 2 do teste A/B (`resultado-20261111-2044.json`).

## O que já foi testado pelo Claude (repita os principais para confirmar)

Em 12/11/2026, todos com resultado ok:
1. Primeira mensagem (apresentação e resposta curta).
2. Fila de 7 s: duas ou três mensagens seguidas geram uma resposta só.
3. Pedido de nome e ficha guardando nome e tratamento.
4. Marcação: escolher horário, dar o nome, evento criado no Google Agenda, aviso para o aprovador.
5. Despedida 1 minuto depois de marcar, se o paciente não responde.
6. Remarcar (evento mudado na agenda) e cancelar (confirma antes, apaga o evento, avisa).
7. "Já tem avaliação marcada" quando pede outra.
8. Pausa de 12 h quando a doutora responde pelo celular (a Clara só guarda a conversa).
9. `#reiniciar` (só funciona para os números da Keshion).
10. Leitura de foto.
11. As 56 mensagens do teste A/B: 56 de 56 respondidas, ações corretas, tom parecido com o do Make.
12. Prefixo de teste: lógica testada com dados simulados e uma mensagem real de teste.

## O que ainda NÃO foi testado (prioridade para você)

1. **Áudio** (download do link do Whapi e transcrição pela OpenAI).
2. **Horário que ficou ocupado** entre a oferta e a escolha (a Clara deve dizer que o horário acabou de ser preenchido e oferecer outros).
3. **Falha da IA** (resposta ilegível ou erro da Anthropic): o paciente deve receber "Só um instante..." e o aprovador um aviso. Sugira como testar sem mexer em produção.
4. **Falha do Google Agenda** (a Clara não deve oferecer horários e deve chamar uma pessoa).
5. **Documento, figurinha, vídeo, localização** (tipo "outro").
6. **Mensagem repetida** (o Whapi às vezes reenvia o mesmo id): não pode gerar resposta duplicada.
7. **Duas conversas ao mesmo tempo** com o mesmo número em momentos muito próximos (corrida na fila).
8. **Conversa longa** (mais de 11.000 caracteres): o histórico é cortado; ver se nada quebra.
9. **Mensagem de grupo** e eventos sem mensagem (status): devem ser ignorados.
10. **Envio real pelo WhatsApp**: esse eu (Erica) testo do meu número. Não teste você.

## Revisão de código (sem rodar nada)

Leia `gerar_fluxos.py` e os cenários do Make e aponte:
- Diferenças de comportamento entre o Make e o n8n que possam ser erro (o LEIA-ME lista as diferenças intencionais).
- Problemas de lógica nas consultas SQL (fila, pendentes, corte do histórico, avaliação futura).
- Riscos de segurança: o webhook não tem autenticação (só um caminho difícil de adivinhar); dados de pacientes ficam nas execuções do n8n; o que mais você vê.
- Pontos frágeis: o que pode quebrar quando trocarmos de clínica (Dra. Vivian, piloto em 01/12/2026) ou de domínio (`n8n.keshion.com.br`).
- Configurações do servidor que merecem atenção (Postgres 16 com aviso do n8n, backups só no próprio servidor, acesso root por chave).

## Entrega

Crie o arquivo `tecnico/n8n/revisao-codex-AAAA-MM-DD.md` (com a data do dia) contendo:
1. Resumo em 5 linhas: a Clara está pronta para o piloto? O que impede?
2. Tabela de testes: teste, como fez, resultado (ok, falhou, não deu para testar), evidência (id da execução ou trecho da `saidas_teste`).
3. Problemas encontrados, do mais grave ao mais leve: o que é, por que importa (em linguagem simples), como corrigir (técnico).
4. Pontos em que você discorda de decisões tomadas, com argumento.
5. Confirmação de limpeza: linhas de teste apagadas e nenhum evento de teste sobrando na agenda.

Não corrija nada no código nem em produção: só aponte. Eu decido depois o que aplicar.
