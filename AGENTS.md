# Keshion IA: contexto para o Codex

> O Codex lê este arquivo sozinho ao abrir esta pasta. Não precisa repetir nada disso nos prompts. Quem mantém: a conversa do Claude Code do projeto (mesmas regras do `CLAUDE.md`).

## O que é o projeto

Keshion IA (Erica e Sérgio) implanta e opera uma atendente de IA no WhatsApp para clínicas odontológicas, vendida como resultado: lead sem resposta, falta e paciente que não volta. A atendente da clínica demo (Dra. Suzana) se chama **Clara** e **fala só português do Brasil** Os pilotos são com clínicas conhecidas, tratadas como clínicas parceiras.

## Como a Clara funciona (resumo; detalhe em `tecnico/RETOMAR-AQUI.md` e `tecnico/n8n/LEIA-ME.md`)

- **n8n próprio** no servidor Contabo (`/opt/keshion`), Postgres 16 (um banco por clínica: `clara` = demo, `clinica_teste` = teste), Whapi (WhatsApp), Google Agenda, IA Claude Haiku 5.5. Áudio e foto: OpenAI.
- Os fluxos **não são editados no n8n**: são gerados por `tecnico/n8n/gerar_fluxos.py <slug>` (saída em `tecnico/n8n/gerados/<slug>/`, fora do Git). Banco e instruções: `tecnico/n8n/preparar_banco.py <slug>`. Por isso **a fonte da verdade é o `gerar_fluxos.py`**, não o JSON gerado.
- Por clínica: `clientes/<slug>/` com `clinica.json` (sem chaves), instruções (`instrucoes-sarah.md` na demo) e `base-clinica.md` (a base de conhecimento da Clara).
- Dois fluxos por clínica: atendimento (recebe, espera 20 s, monta a conversa, chama a IA, decide a ação, marca/remarca/cancela no Google, avisa a equipe) e envio (mensagens com "digitando", 1 s a cada 4 letras, mínimo 4, máximo 50).
- Tabelas: `pacientes` (ficha), `config`, `mensagens_recebidas`, `saidas_teste`, `reservas_horario`. Números com prefixo `554199900` são de teste: nada sai pelo WhatsApp, as saídas vão para `saidas_teste`.

## Regras que valem sempre

- Português do Brasil com acentos, sem travessão. A Erica não é programadora: linguagem simples e respostas curtas.
- **Chaves nunca no chat, nos arquivos nem no Git.** Só no `.env` da pasta (PC) ou `/opt/keshion/.env` (servidor). Nunca mostrar valores.
- **Revisão (seu papel principal):** ler, achar problemas e descrever. **Não corrigir, não publicar, não mudar o fluxo, as instruções, o banco nem o servidor, e não reiniciar o n8n.** Quem corrige é a conversa do Claude Code. Formato do pedido: `tecnico/n8n/PROMPT-CODEX-REVISAO.md`. **Salve todo relatório de revisão em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion\tecnico\codex\revisao-codex-AAAA-MM-DD.md`**, nunca só no chat.
- Pedir OK antes de mudar produção, gastar dinheiro, criar conta ou mexer em número de WhatsApp de cliente.
- Dados de pacientes reais nunca nesta pasta.
- Commit só dos seus arquivos; push só com OK da Erica.

## Testes

- Lista completa e registro de rodadas: `tecnico/testes-checklist.md`. Scripts em `tecnico/teste-ab/` (`paciente_simulado.py` = 22 perfis com nota de outra IA; `teste_n8n.py` = 56 mensagens fixas, roda no servidor) e testes locais em `tecnico/n8n/` (`teste_pacote_a.js`, `teste_pacote_c.js`, `teste_validacao_data_hora.js`, `teste_pacote_c_cadastro.py`), que leem o fluxo gerado.
- **Um teste por vez, só números `554199900…`, e só na conversa de testes.** Antes de rodar: conferir que nenhum outro teste está rodando (fichas `554199900%` mexidas nos últimos 10 minutos no banco `clara`), saldo da Anthropic suficiente (o limite mínimo está no pedido de teste) e que a chave do `.env` é a de testes.
- Sempre registrar hora de Curitiba (UTC-3; o PC da Erica fica no fuso de Israel) e se a clínica estava aberta (segunda a sexta 8h às 19h, sábado 8h às 12h).
- "ERRO DE LEITURA" ou "ERRO DE ENVIO" no relatório = rodada INVÁLIDA: não contar as notas, avisar e repetir.
- A agenda do Google é real: todo teste que marca precisa cancelar no fim e conferir que não sobrou evento. Limpar fichas, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` dos números usados.
- Para comparar notas dos 22 perfis, usar as rodadas anteriores do Registro de rodadas em `tecnico/testes-checklist.md`.
- O PC precisa ficar na tomada, sem suspender, com o app aberto até o fim das rodadas longas.

## Onde olhar primeiro

1. `tecnico/RETOMAR-AQUI.md` (estado atual e pendências, nesta ordem).
2. `CLAUDE.md` e `MAPA-DO-PROJETO.md` (regras e onde está cada coisa).
3. `tecnico/n8n/PROMPT-CODEX-REVISAO.md` (como revisar) e `tecnico/testes-checklist.md` (o que já foi testado).
