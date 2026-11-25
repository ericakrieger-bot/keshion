# Retomar aqui (Keshion · automações da Clara)

Atualizado em 24/11/2026. Ler só este arquivo para começar; abrir os outros só quando a tarefa pedir.
Histórico completo até 20/11 (pacotes A a D, resultados de cada rodada, custos): `arquivo/tecnico/RETOMAR-AQUI-ate-2026-11-20.md`.

## Onde estamos

A Clara (assistente de WhatsApp da clínica demo da Dra. Suzana) **roda no n8n próprio desde 12/11/2026**. O Make está desativado (cenários só desligados; cópias em `arquivo/make/`). **Desde 17/11, cada clínica tem banco, fluxos e credenciais próprios**, gerados a partir de um arquivo por clínica.

**Rumo (21 e 22/11):** o piloto da Dra. Vivian foi suspenso em 20/11, mas ela **retomou o contato (24/11)** e o material do piloto é para ela e o Dr. Eduardo Ramina. **Cronograma de 24/11:** copiloto na semana 1, confirmação e lembrete na semana 2, app na semana 3 (abaixo ainda aparece o plano antigo: semana 2 e 3). Os pilotos agora são com clínicas que a Erica e o Sérgio conhecem: o 1º combinado até 30/11, o 2º e o 3º até 15/12, entrando na semana 2 do 1º. O 1º piloto roda de 01 a 31/12, como clínica parceira. Semana 1 com a Clara **só fora do horário**; semana 2 com **copiloto mínimo de 3 dias úteis** (o dentista responde "ok" ou corrige pelo WhatsApp). A regra de paciente antigo entra já no dia 1 (decisões de 22/11). Estrutura completa: `comercial/piloto/estrutura-piloto-conhecidos.md`.

| Peça | Onde |
|---|---|
| Servidor | Contabo 169.58.41.107, `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`, tudo em `/opt/keshion` (n8n 2.47.5, Postgres 16.15, Caddy 2.11.9). Detalhes: `tecnico/servidor-n8n.md` |
| n8n | https://n8n.169-58-41-107.sslip.io · demo: `ClaraAtendimento` e `ClaraEnvio000001` · clínica fictícia de teste: `TesteAtendimento` e `TesteEnvio000001` |
| Clínicas | uma pasta por clínica em `clientes/<slug>/` com `clinica.json` (sem chaves), instruções e base. Modelo em `clientes/_modelo/`. Roteiro de clínica nova: `tecnico/n8n/CLINICA-NOVA.md` |
| Fonte dos fluxos | `tecnico/n8n/gerar_fluxos.py <slug>` (fluxos) e `tecnico/n8n/preparar_banco.py <slug>` (banco). Saída em `tecnico/n8n/gerados/<slug>/`, fora do Git. Como a Clara está montada: `tecnico/n8n/LEIA-ME.md` |
| Caminhos dos webhooks | secretos, um por clínica, em `tecnico/n8n/segredos.local.json` (fora do Git) |
| Dados | Postgres, um banco por clínica (`clara` = demo, `clinica_teste` = teste). Tabelas: `pacientes`, `config`, `mensagens_recebidas`, `saidas_teste`, `reservas_horario` |
| Instruções e base | `clientes/<slug>/` (demo: `instrucoes-sarah.md` e `base-clinica.md`). Depois de mudar, rodar `preparar_banco.py <slug>` e aplicar o SQL no banco da clínica |
| Testes | lista e registro de rodadas em `tecnico/testes-checklist.md`; scripts em `tecnico/teste-ab/`. Números com prefixo `554199900` nunca saem pelo WhatsApp. **Um teste por vez e só na conversa de testes da Erica** |
| Backup | todo dia às 03h, criptografado, no Google Drive da conta da demo (30 dias). Resultado em `/opt/keshion/backups/STATUS-BACKUP.txt`. Restauração: `tecnico/servidor-n8n.md`, seção Backup |

## Teste do Pacote E, parte 1 (25/11, noite): cancelar NÃO passou

Casos 1 ("Valeu!") e 6 (passar para a equipe) falharam; a Júlia ficou em loop (nota 2). Urgência: aviso URGENTE nas 3, sem a resposta fixa. Detalhes e causas: `tecnico/testes-checklist.md`, rodada de 25/11. **Próximo passo:** corrigir a pendência do cancelar (gravar também quando a IA pergunta sozinha; aceitar "sim" com outra pergunta junto; não recomeçar o ciclo depois de passar para a equipe) e repetir os casos 1 e 6 e a Júlia.

## O que já existe (resumo)

Servidor seguro e backup externo; Clara no n8n com fila, ficha, Google Agenda (marcar, remarcar, cancelar), avisos para a equipe, pausa quando a doutora responde, áudio e foto; estrutura por clínica; correções das revisões do Codex nos Pacotes A (18/11), B (18/11) e C (20/11), todos publicados na demo; Pacote D (ferramentas de teste e roteiro de restauração) no Git. Detalhes de cada pacote no histórico.

## Pendente agora, nesta ordem

1. **Antes de 26/11 (operação):** publicar o app do Google (`tecnico/servidor/PASSO-A-PASSO-ERICA-GOOGLE-OAUTH.md`) ou reconectar o Google Agenda no n8n. A autorização atual, dada em 19/11, vence por volta de 26/11.
2. **Teste ao vivo do Pacote C: rodado em 24/11** (registro em `tecnico/testes-checklist.md`). Passou: urgência, horário negado, pausa humana, espera de 20 s, ordem, alinhador R$ 150, 56 de 56 mensagens. **Falta o caso 11 (áudio WAV e Ogg)**: precisa do arquivo de áudio do Codex hospedado no Whapi. Média dos 22 perfis **6,64** (abaixo de 7,05 a 7,32 das rodadas anteriores).
3. **URGENTE, nova correção do "cancelar":** a correção de 23/11 não cobre o caso em que a pergunta da IA ("é a avaliação de ..., certo?") não tem a palavra "cancelar": o fluxo pergunta de novo e, em alguns perfis, fica em loop (Bia e Sandra com nota 2, nunca cancelaram; Thiago, Júlia e Emily repetiram). Corrigir, publicar sem reiniciar o n8n e repetir os perfis Bia, Sandra, Thiago, Júlia e Emily. Também no radar: caso 8 (dúvida geral de clareamento e gengiva vai para a equipe), Diego (não oferece horário para remarcar) e Dona Lourdes (não diz que a clínica não faz implante nem dentadura; promete retorno depois das 17h). Revisão do Codex (`tecnico/n8n/PROMPT-CODEX-REVISAO.md`) sobre o Pacote C, o cancelar e as correções de 24/11.
4. **Com OK:** instalar no servidor o `backup-postgres.sh` novo (Pacote D1). Teste: `tecnico/teste-ab/PROMPT-TESTE-19-11-pacote-d.md`.
5. **Com OK, antes do 1º piloto:** passar a demo e a clínica de teste para o usuário `_app` do banco (B7).

## Antes do 1º piloto com clínica conhecida (até 30/11)

1. ✅ Estrutura por clínica (17/11) e backup fora do servidor (18/11).
2. **Modo "só fora do horário" e copiloto:** em construção na branch `feat/copiloto-e-fora-do-horario`, na pasta `Documents\Claude Code\keshion-wt-copiloto` (trabalho guardado em commit em 22/11, sem publicar). Plano aprovado pela Erica em 22/11: `tecnico/n8n/PLANO-COPILOTO.md` (nessa branch). O "só fora do horário" vai na publicação de 27/11; o copiloto é a versão mínima (3 dias úteis, "ok" ou correção) para a semana 2.
3. **Regra para paciente antigo** (limpeza e manutenção, retorno, obturação, canal, extração, dor, remarcar e cancelar): nos testes, os perfis de paciente antigo tiraram 5 a 6. Entra na publicação de 27/11, com perfis novos de paciente antigo nos testes; o número real da clínica só conecta com média 7 ou mais (decisão de 22/11).
4. Base, instruções, voz e número da clínica escolhida, seguindo `tecnico/n8n/CLINICA-NOVA.md`.
5. Canal de alerta fora do WhatsApp: Healthchecks.io por e-mail (o script já está preparado; falta a Erica criar a conta, `tecnico/servidor/PASSO-A-PASSO-ERICA-BACKUP.md`).
6. Base da Clara no servidor ainda com os lembretes de orçamento antigos (15 dias; dias 2, 7 e 14). Vale 3, 10, 17 e 30. **Aprovado pela Erica em 21/11 (Notion):** levar junto com a próxima publicação e testar com o paciente simulado.
7. Até o alerta por e-mail existir: a Erica confere o backup (Sérgio de substituto), e o executor das 14h confere o `STATUS-BACKUP.txt` todo dia (decidido em 21/11).

## Durante o piloto (semanas 2 a 4, cronograma de 24/11)

Confirmação e lembrete de consulta (48 h, véspera, 2 h antes) até a semana 2 (adiantado, era semana 3), o copiloto já na semana 1, lembrete de orçamento (dias 3, 10, 17 e 30) e o app (semana 3) com Conversas, Agenda do dia e "Precisa de você" (`app-crm-painel/LEIA-PRIMEIRO.md`).

## Depois

Recontato ativo (pedido de 18/11, ficou em `arquivo/tecnico/feature-requests-2026-11-18.md`): a Clara chamar sozinha quem faltou (disparo quando o app marcar "faltou") e quem está sem voltar (prazo configurável em `clinica.json`). Antes de construir: mensagem ativa fora da janela de 24 h do WhatsApp pode exigir modelo aprovado pela Meta, limite de envios por dia e volta da conversa para "Precisa de você" no app. Decisão pendente da Erica; sem ela, o site perde os cartões "Quem faltou" e "Quem está sem voltar".

Ordem de envio garantida entre respostas próximas, idempotência no Google, Sonnet nas mensagens clínicas, resumo do histórico longo, Postgres 17, usuário de manutenção com sudo no lugar do root, conexão oficial do WhatsApp (plano estratégico: 1º trimestre de 2027).

## Regras de sempre

Português com acentos e sem travessão. Chaves só no `.env` (PC) ou em `/opt/keshion/.env` (servidor), nunca no chat nem no Git. Pedir OK antes de mudar produção, gastar dinheiro ou mexer em número de WhatsApp. Testar só com o prefixo `554199900`, um teste por vez e só na conversa de testes da Erica (as outras conversas corrigem, publicam e entregam um prompt de teste). Publicar fluxo com import e publish, sem reiniciar o n8n. Depois de cada feature que mexa no fluxo, nas instruções ou no servidor, lembrar a revisão do Codex (`tecnico/n8n/PROMPT-CODEX-REVISAO.md`). Commit e push dentro de `Documents\Claude Code\keshion`.
