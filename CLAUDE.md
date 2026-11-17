# Keshion IA (Negócio de IA para Clínicas)

> Projeto da Erica, separado dos infoprodutos. Pasta própria `Documents\Claude Code\keshion` desde 17/11/2026 (antes ficava dentro do fluxo-criativo e depois em `Documents\keshion`), com `.env` próprio. Git: `ericakrieger-bot/keshion`.
> Histórico completo de decisões, Make, nicho e concorrentes: `historico-e-estrategia.md` (abrir só quando precisar).

## O que é

Keshion IA (sócio: Sérgio; domínio keshion.com, app em app.keshion.com). Serviço B2B: implantação e operação de atendente de IA no WhatsApp para clínicas odontológicas de alto valor, vendido como resultado (lead sem resposta, falta e paciente que não volta). Modelo: diagnóstico grátis, implantação e mensalidade. Piloto com a Dra. Vivian em 01/12/2026 (`clientes/dra-vivian/BRIEFING-NOVO-CHAT.md`).

## Estado técnico (17/11/2026)

- **Começar por `tecnico/RETOMAR-AQUI.md`**: onde está cada peça, o que foi feito, roadmap e próxima feature.
- A Clara (assistente da clínica demo da Dra. Suzana) roda no **n8n próprio** (Contabo 169.58.41.107, `/opt/keshion`). Fluxos gerados por `tecnico/n8n/gerar_fluxos.py`; instruções e base em `clientes/clinica-demo/` e na tabela `config` do Postgres `clara`. Make desativado.
- IA das respostas: Claude Haiku 5.5. Áudio e foto: OpenAI. WhatsApp: Whapi (canal GRNLTR-4K8ZF, pago até 12/12/2026). Conta Google da demo: keshion.ai.2026@gmail.com.
- App, CRM e painel: `app-crm-painel/LEIA-PRIMEIRO.md` (Next.js + Netlify + Supabase).

## Regras

- Português do Brasil com acentos, sem travessão. A Erica não é programadora: linguagem simples.
- Chaves só no `.env` desta pasta (PC) ou em `/opt/keshion/.env` (servidor). Nunca no chat nem no Git.
- Pedir OK antes de mudar produção, criar contas, gastar dinheiro ou mexer em número de WhatsApp de cliente.
- Testes com a Clara no ar: só números com prefixo `554199900` (nada sai pelo WhatsApp).
- Dados de pacientes reais nunca nesta pasta.
- Material visual da Keshion segue `branding/guia-de-marca.md`.
- Commit e push dentro desta pasta; memória `keshion-migracao-n8n` com cópia no segundo cérebro (`Documents\segundo-cerebro`).

## Padrões de trabalho (pedidos da Erica em 17/11/2026)

1. **Respostas curtas por padrão:** só o resultado e o que ela precisa decidir. Explicação longa só quando ela pedir.
2. **Resumo ou nova conversa:** atualizar `tecnico/RETOMAR-AQUI.md` e terminar com a frase pronta para colar: "Projeto Keshion. Leia `tecnico/RETOMAR-AQUI.md` e vamos para [próxima feature]." (conversa aberta na pasta `Documents\Claude Code\keshion`)
3. **Uma feature por conversa.** Ao terminar, atualizar o RETOMAR-AQUI e sugerir abrir conversa nova.
4. **Revisão pelo Codex:** ao fechar cada feature que mexa no fluxo, nas instruções ou no servidor, lembrar a Erica de rodar a revisão no Codex com `tecnico/n8n/PROMPT-CODEX-REVISAO.md` (dizer qual feature revisar).
5. **Testes:** depois de mudar instruções, rodar `tecnico/teste-ab/paciente_simulado.py`; depois de mudar o fluxo, também `teste_n8n.py`. Lista completa em `tecnico/testes-checklist.md`.
6. **Modelo:** Opus para desenhar feature nova, decisão difícil e revisão; Sonnet para rodar teste, ajustar texto, documentar e tarefas repetidas.

## Mapa curto

| Onde | O quê |
|---|---|
| `tecnico/` | n8n, servidor, testes, revisões |
| `clientes/` | uma pasta por clínica (sem dados de pacientes) |
| `comercial/` | oferta, proposta, contrato |
| `app-crm-painel/` | app da clínica, CRM e painel |
| `pesquisa/` | mercado, nichos, concorrentes |
| `plano-estrategico-keshion.md` | plano de longo prazo (metas até 2030) |
