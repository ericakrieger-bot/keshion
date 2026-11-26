# Prompt para o Codex revisar a Clara no n8n

Atualizado em 24/11/2026 (a versão de 12/11 era da migração do Make e foi substituída). Copie tudo abaixo da linha e cole no Codex, aberto na pasta `Documents\Claude Code\keshion` (repositório privado `ericakrieger-bot/keshion`).

**Onde o Codex salva:** sempre em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion\tecnico\codex\` (seção "Entrega" abaixo).

**Para quem mantém este arquivo:** a única parte que muda a cada revisão é a seção "Escopo desta revisão". Atualize-a antes de entregar o prompt à Erica. O resto é contexto e regras de segurança.

---

Você vai fazer uma revisão independente de um sistema que outra IA (Claude) montou e testou. Quero uma segunda opinião honesta: o que está certo, o que está errado, o que é arriscado e o que não foi testado. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: no relatório final, explique cada problema em linguagem simples, além do detalhe técnico.

## Escopo desta revisão (24/11/2026)

A migração do Make para o n8n foi feita em 12/11 e está **fechada: não revise a migração** nem compare com os cenários do Make. Revise estas mudanças recentes, que já estão publicadas na demo (ou, onde dito, só no Git):

1. **Pacote C** (20/11): cancelar só quando a pergunta da IA é de cancelamento, horário negado, urgência com pergunta e negativa, pausa humana.
2. **Correção do "cancelar" de 23/11** (publicada). Problema que ela deixou: quando a pergunta da IA ("é a avaliação de ..., certo?") não tem a palavra "cancelar", o fluxo pergunta de novo e, em alguns perfis, fica em loop (no teste de 24/11: Bia e Sandra nunca cancelaram; Thiago, Júlia e Emily repetiram). **Há uma nova correção pendente, ainda não escrita**: confirme a causa no código e proponha como resolver sem criar outro risco (cancelar sem confirmação do paciente seria o pior erro).
3. **Correções de 24/11 do teste da Erica** (publicadas às 07h20, cópia anterior em `/opt/keshion/versoes/clinica-demo/`): `#reiniciar` agora apaga todos os campos da ficha e aceita `reiniciar` sem `#`; espera de 20 s (era 7 s) depois da última mensagem; "digitando" mais longo; espera do envio anterior de 180 s.
4. **Clara só em português** (`be5ff46`, instruções, pedido à IA e frases fixas): está **só no Git, não publicada**.
5. **Testes locais** (`node tecnico/n8n/teste_pacote_a.js`, `teste_pacote_c.js`, `teste_validacao_data_hora.js`): confira se testam o que dizem e se há caso importante sem teste.

Também no radar (diga se concorda): dúvida geral de clareamento e gengiva indo para a equipe (caso 8), Diego (não oferece horário ao remarcar) e Dona Lourdes (não diz que a clínica não faz implante nem dentadura; promete retorno depois das 17h). Média dos 22 perfis em 24/11: **6,64** (rodadas anteriores 7,05 a 7,32). O número real de uma clínica só conecta com média 7 ou mais.

## O que é o sistema

A Keshion vende uma atendente de IA no WhatsApp para clínicas odontológicas. A **Clara** é a atendente da clínica de demonstração (Dra. Suzana, fictícia) e roda no **n8n próprio** desde 12/11/2026. Cada clínica tem banco, fluxos e credenciais próprios, gerados de um arquivo por clínica. O 1º piloto com clínica conhecida começa até 30/11 e roda em dezembro, como clínica parceira, com a Clara respondendo só fora do horário na semana 1.

Leia primeiro, nesta ordem:
1. `CLAUDE.md` (contexto do negócio e regras do projeto)
2. `tecnico/RETOMAR-AQUI.md` (estado atual e pendências; é o mais atual de todos)
3. `tecnico/n8n/LEIA-ME.md` (como a Clara está montada no n8n)
4. `tecnico/servidor-n8n.md` (o servidor)
5. `tecnico/n8n/gerar_fluxos.py` (gera os dois fluxos; é a fonte da verdade, os `.json` saem dele para `tecnico/n8n/gerados/<slug>/`, fora do Git)
6. `tecnico/n8n/schema-clara.sql` e `tecnico/n8n/preparar_banco.py` (banco)
7. `clientes/clinica-demo/` (`clinica.json`, instruções e `base-clinica.md`) e `clientes/_modelo/`
8. `tecnico/testes-checklist.md` (o que foi testado, rodada a rodada) e `tecnico/teste-ab/2026-11-24-erros-teste-demo-erica.md` (erros do teste da Erica de 24/11 e as correções)
9. `tecnico/n8n/codex-19-11/` (a revisão anterior do Codex e o plano de correções)
10. `tecnico/n8n/CLINICA-NOVA.md` (como publicar sem reiniciar e como voltar atrás)

## Onde as coisas estão

- n8n: https://n8n.169-58-41-107.sslip.io. Demo: `ClaraAtendimento` e `ClaraEnvio000001`. Clínica fictícia de teste: `TesteAtendimento` e `TesteEnvio000001`.
- Webhook que o Whapi chama: `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`. O caminho fica só em `tecnico/n8n/segredos.local.json` (fora do Git). O corpo precisa ter `"channel_id": "GRNLTR-4K8ZF"`, e mídia só é baixada de links do Whapi (Wasabi).
- Servidor: `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`, tudo em `/opt/keshion` (Docker Compose com n8n, Postgres 16 e Caddy). A impressão digital ED25519 do servidor é `SHA256:B5bjFLwt0jSQJFH7xIubvFLSqi5oTVL3zYf4wpSQ8Yo` (conferida pela Keshion em 24/11); se pedir confirmação com essa, pode confiar.
- Banco da demo: Postgres, banco `clara`, usuário `clara`. Senha só em `/opt/keshion/.env` (`CLARA_DB_PASSWORD`). Exemplo de leitura, sem mostrar a senha:
  `cd /opt/keshion && set -a && . ./.env && set +a && docker compose exec -T postgres sh -c "PGPASSWORD=\"$CLARA_DB_PASSWORD\" psql -h localhost -U clara -d clara -c 'select chave, left(valor, 40) from config'"`
- Execuções do n8n (para ver erros): banco `n8n`, tabelas `execution_entity` e `execution_data`, usuário `keshion`.

## Regras de segurança (obrigatórias, a Clara está no ar)

1. **Teste só com números que começam com `554199900`** (exemplo: 554199900201). Esse prefixo está em `config.prefixo_teste`: qualquer conversa com esses números vai para a tabela `saidas_teste` e nada sai pelo WhatsApp, nem os avisos para a equipe. **Nunca** use outro número inventado: cada número novo que recebe mensagem pelo Whapi conta no plano pago e pode bloquear o canal.
2. **Não mude nada em produção sem me perguntar antes:** fluxos do n8n, tabela `config`, `.env`, credenciais, painel do Whapi, Docker. **Nunca reinicie o n8n** (derruba conversas em andamento). Leitura pode à vontade. Escrita permitida sem perguntar: só apagar as linhas de teste que você mesmo criou (`DELETE FROM pacientes WHERE telefone LIKE '554199900%'` e `DELETE FROM saidas_teste WHERE telefone LIKE '554199900%'`).
3. **Nunca mostre senha, token ou chave** no chat nem em arquivo. Se precisar de uma, leia do `.env` dentro do comando.
4. **Google Agenda é real** (agenda da conta da clínica demo). Se um teste marcar uma avaliação, cancele pela própria conversa no fim do teste e confira que nenhum evento de teste sobrou. Liste no relatório os eventos que sobraram, se algum sobrar. A autorização do Google dada em 19/11 vence por volta de 26/11: se a agenda falhar, registre e não tente reconectar.
5. Não toque no número da Erica (972584285541) nem no do Sérgio (972552994413): são números reais.
6. Cada rodada de testes custa chamadas de IA: não repita rodadas completas (as 56 mensagens ou os 22 perfis) mais de uma vez.
7. Os testes pedidos nesta revisão são para confirmar o que aponta o código. Prefira ler o código e o histórico a rodar teste caro.

## Como os testes simulam o WhatsApp

Os testes simulam o Whapi: um POST no webhook com o mesmo formato que o Whapi manda. Exemplo de corpo de mensagem de texto:
```json
{"messages":[{"id":"t-1","from_me":false,"type":"text","chat_id":"554199900201@s.whatsapp.net","from":"554199900201","from_name":"Teste","source":"mobile","text":{"body":"Oi, vocês fazem clareamento?"}}],"event":{"type":"messages","event":"post"}}
```
- Foto: `"type":"image","image":{"link":"<url pública de imagem>","caption":"..."}`. A OpenAI não consegue baixar imagens da Wikimedia; use outro site (Pexels funcionou).
- Áudio: `"type":"voice","voice":{"link":"<url pública de um .ogg, .wav ou .mp3>"}`.
- Doutora respondendo pelo celular: `"from_me":true,"source":"mobile"` e `chat_id` com o número do paciente.
- Mensagens da própria Clara voltando: `"from_me":true,"source":"api"` (devem ser ignoradas).
- Envie sempre o corpo em UTF-8 (no Windows, use Python, não `curl` com acentos na linha de comando).

Depois de cada mensagem, a Clara espera 20 s (fila) e responde em alguns segundos. Confira:
- `saidas_teste`: o que teria sido enviado (para o paciente e para o aprovador 972584285541).
- `pacientes`: a ficha (conversa, pendente, nome_paciente, tratamento, avaliacao_inicio/texto/evento, pausado_ate).
- `execution_entity`: se a execução terminou com `success`.

Os scripts de teste da Clara ficam em `tecnico/teste-ab/` (`teste_n8n.py` das 56 mensagens, `paciente_simulado.py` dos perfis, `teste_isolamento.py`) e rodam dentro do servidor ou da conversa de testes da Erica. Leia-os para entender; só rode algo se a seção "Escopo" pedir.

## O que ainda NÃO foi testado (prioridade para você)

1. **Áudio no formato WAV e Ogg** (caso 11 do Pacote C): falta o arquivo de áudio hospedado no Whapi. Dá para revisar só o código da transcrição.
2. **Horário ocupado** entre a oferta e a escolha (a Clara deve dizer que o horário acabou de ser preenchido e oferecer outros).
3. **Falha da IA** (resposta ilegível ou erro da Anthropic): o paciente deve receber "Só um instante..." e o aprovador um aviso. Sugira como testar sem mexer em produção.
4. **Falha do Google Agenda** (a Clara não deve oferecer horários e deve chamar uma pessoa).
5. **Documento, figurinha, vídeo, localização** (tipo "outro").
6. **Mensagem repetida** (o Whapi às vezes reenvia o mesmo id): não pode gerar resposta duplicada.
7. **Duas conversas ao mesmo tempo** com o mesmo número, e a nova espera de 20 s: o que acontece se chegar mensagem durante o envio.
8. **Conversa longa** (mais de 11.000 caracteres): o histórico é cortado; ver se nada quebra.
9. **Mensagem de grupo** e eventos sem mensagem (status): devem ser ignorados.
10. **Envio real pelo WhatsApp**: esse a Erica testa do número dela. Não teste você.

## Revisão de código (sem rodar nada)

Leia `gerar_fluxos.py`, os testes locais e as instruções e aponte:
- Problemas de lógica nas consultas SQL (fila, pendentes, corte do histórico, avaliação futura, reinício).
- Riscos de segurança: o webhook não tem autenticação (só um caminho difícil de adivinhar); dados de pacientes ficam nas execuções do n8n; o que mais você vê.
- Pontos frágeis para a 1ª clínica real (piloto até 30/11) e para clínicas com agenda diferente (papel, sistema odontológico).
- Configurações do servidor que merecem atenção (Postgres 16 com aviso do n8n, backup, acesso root por chave, usuário `_app` do banco ainda não ligado na demo).

## Entrega

Salve o relatório (não deixe só no chat) em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion\tecnico\codex\revisao-codex-AAAA-MM-DD.md` (com a data do dia). Esse é o endereço completo e obrigatório: não grave em outra pasta. O arquivo deve conter:
1. Resumo em 5 linhas: a Clara está pronta para o piloto? O que impede?
2. Tabela de testes: teste, como fez, resultado (ok, falhou, não deu para testar), evidência (id da execução ou trecho da `saidas_teste`).
3. Problemas encontrados, do mais grave ao mais leve: o que é, por que importa (em linguagem simples), como corrigir (técnico).
4. Pontos em que você discorda de decisões tomadas, com argumento.
5. Confirmação de limpeza: linhas de teste apagadas e nenhum evento de teste sobrando na agenda.

Não corrija nada no código nem em produção: só aponte. Eu decido depois o que aplicar.
