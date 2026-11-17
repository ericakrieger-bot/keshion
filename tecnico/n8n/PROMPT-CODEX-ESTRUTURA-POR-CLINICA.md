# Prompt para o Codex revisar a feature "estrutura por clínica" (17/11/2026)

Abra o Codex na pasta `Documents\Claude Code\keshion` (repositório privado `ericakrieger-bot/keshion`). Antes de colar, confira que nenhuma outra conversa está rodando teste da Clara: duas rodadas ao mesmo tempo apagam as fichas uma da outra. Copie tudo abaixo da linha e cole no Codex.

---

Você vai fazer uma revisão independente de uma feature que outra IA (Claude) montou, publicou e testou: a **estrutura por clínica** da assistente de WhatsApp da Keshion. Quero uma segunda opinião honesta: o que está certo, o que está errado, o que é arriscado e o que não foi testado. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: explique cada problema em linguagem simples, além do detalhe técnico.

## Regras de segurança (obrigatórias, a demo está no ar)

Leia e siga a seção "Regras de segurança" de `tecnico/n8n/PROMPT-CODEX-REVISAO.md`. Em resumo: só números com prefixo `554199900`; nada em produção sem me perguntar (fluxos, config, .env, credenciais, Docker, Whapi); nunca mostrar senha, token ou caminho do webhook; Google Agenda é real, então cancele o que marcar e confira que nada sobrou; não use os números 972584285541 e 972552994413. Para a clínica de teste, valem as mesmas regras, no banco `clinica_teste` (senha `CLINICA_TESTE_DB_PASSWORD` no `/opt/keshion/.env`).

## O que mudou

Antes, o gerador montava os fluxos de uma clínica só, com nome, fuso, cidade, canal e credenciais escritos no código. Agora:
- Cada clínica tem `clientes/<slug>/clinica.json` (sem chaves, só ids de credenciais do n8n), instruções e base.
- `tecnico/n8n/gerar_fluxos.py <slug>` gera o par de fluxos da clínica em `tecnico/n8n/gerados/<slug>/` (fora do Git). O caminho secreto do webhook de cada clínica fica em `tecnico/n8n/segredos.local.json`, no formato `{"<slug>": {"webhook_path": "..."}}`.
- `tecnico/n8n/preparar_banco.py <slug>` gera o SQL do banco da clínica: tabelas de `schema-clara.sql` mais a tabela `config` (instruções, base, aprovador, endereço, prefixo de teste). Os valores fixos da demo saíram do `schema-clara.sql`.
- Um banco por clínica, com usuário próprio. Bancos `clara` (demo) e `clinica_teste` com `REVOKE CONNECT ... FROM PUBLIC`; o banco `n8n` também.
- Clínicas: demo (`clinica-demo`, banco `clara`, fluxos `ClaraAtendimento` e `ClaraEnvio000001`), clínica fictícia de teste (`clinica-teste`, banco `clinica_teste`, fluxos `TesteAtendimento` e `TesteEnvio000001`, canal falso `TESTE-ISOLAMENTO`, usa o Whapi e o Google da demo) e ficha da Dra. Vivian ainda sem dados (`clientes/dra-vivian/clinica.json`, piloto em 01/12/2026). Modelo em `clientes/_modelo/clinica.json`.
- A demo foi reimportada pelo gerador novo. Cópia dos fluxos anteriores no servidor em `/opt/keshion/backups/fluxos-20261117/`.

Leia, nesta ordem: `tecnico/RETOMAR-AQUI.md`, `tecnico/n8n/LEIA-ME.md` (seção "Estrutura por clínica"), `tecnico/n8n/gerar_fluxos.py`, `tecnico/n8n/preparar_banco.py`, `tecnico/n8n/schema-clara.sql`, os três `clinica.json` e o modelo, `tecnico/teste-ab/teste_isolamento.py`. Para ver o que mudou no código: `git log` e `git diff` do commit "Estrutura por clínica".

## O que o Claude testou (repita os principais)

1. A demo gerada pelo arquivo novo é igual à anterior (só um comentário e `calendars.primary` virou `calendars['primary']`).
2. Teste de isolamento no servidor: `python3 teste_isolamento.py <caminho demo> <caminho clinica-teste>` (os caminhos estão em `segredos.local.json`). O mesmo telefone e o mesmo id de mensagem nas duas clínicas; cada uma lembrou só do próprio paciente; mensagem com o canal de outra clínica ignorada. Passou.
3. Usuário `clinica_teste` não consegue abrir o banco `clara`, e `clara` não abre `clinica_teste`.
4. 56 mensagens (`teste_n8n.py`): 56 de 56, sem falha técnica. Pacientes simulados (`paciente_simulado.py`, no PC): notas de 7 a 9 e agenda limpa.

## O que quero que você confira

1. **Vazamento entre clínicas:** algum ponto do gerador ainda tem coisa fixa da demo (nome, fuso, cidade, calendário, número, URL, id de fluxo, id do webhook)? Procure também nos textos dos avisos e no que vai para a conversa.
2. **Fluxos de uma clínica chamando os de outra:** o "Envio" chamado pelo "Atendimento" é sempre o da mesma clínica? O reenvio das mensagens extras vai para o webhook certo?
3. **Ids e webhooks:** dois fluxos de clínicas diferentes podem colidir (id do fluxo, id dos nós, `webhookId`, caminho)? O que acontece se alguém copiar o modelo e esquecer de trocar os ids?
4. **Banco:** `preparar_banco.py` é seguro para rodar de novo numa clínica em produção (não apaga a ficha dos pacientes, guarda a versão anterior das instruções)? O texto vai entre `$tag$`: há caso em que isso quebra? Permissões dos usuários e bancos estão corretas?
5. **Calendário:** a agenda agora vem do campo `agenda.calendario` (URL e resposta do `freeBusy`). Funciona com um calendário que não seja `primary` (id com `@group.calendar.google.com`)? Só revisão de código: não crie calendário.
6. **Passo a passo de clínica nova** no LEIA-ME: dá para seguir? Falta algo para a Dra. Vivian (credenciais do Whapi e do Google dela, avisos indo para o número dela pelo próprio canal dela, `modo_teste` começando em 1)?
7. **O que não foi testado:** avisos para a equipe saindo pelo Whapi de outra clínica (não teste envio real: só aponte), dois canais Whapi de verdade, a clínica de teste usando o mesmo Google da demo (as duas veem a mesma agenda: isso é aceitável para teste?).
8. Repita o teste de isolamento uma vez e confira que nada sobrou nos dois bancos nem na agenda.

## Entrega

Crie `tecnico/n8n/revisao-codex-estrutura-por-clinica-AAAA-MM-DD.md` (data do dia) com:
1. Resumo em 5 linhas: dá para ligar a Dra. Vivian com essa estrutura? O que impede?
2. Tabela de testes: teste, como fez, resultado (ok, falhou, não deu para testar), evidência.
3. Problemas, do mais grave ao mais leve: o que é, por que importa (linguagem simples), como corrigir (técnico).
4. Pontos em que você discorda das decisões (um banco e um par de fluxos por clínica, arquivo JSON, segredos fora do Git).
5. Confirmação de limpeza: linhas de teste apagadas nos dois bancos e nenhum evento de teste na agenda.

Não corrija nada no código nem em produção: só aponte. Eu decido depois o que aplicar.
