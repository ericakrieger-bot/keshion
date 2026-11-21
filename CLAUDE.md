# Keshion IA (Negócio de IA para Clínicas)

> Projeto da Erica, separado dos infoprodutos. Pasta própria `Documents\Claude Code\keshion` desde 17/11/2026 (antes ficava dentro do fluxo-criativo e depois em `Documents\keshion`), com `.env` próprio. Git: `ericakrieger-bot/keshion`.
> Histórico completo de decisões, Make, nicho e concorrentes: `historico-e-estrategia.md` (abrir só quando precisar).

## O que é

Keshion IA (sócio: Sérgio; domínio keshion.com, e-mail contato@keshion.com, app em app.keshion.com). Serviço B2B: implantação e operação de atendente de IA no WhatsApp para clínicas odontológicas de alto valor, vendido como resultado (lead sem resposta, falta e paciente que não volta). Modelo: diagnóstico grátis, implantação e mensalidade. Piloto com a Dra. Vivian em 01/12/2026 (`clientes/dra-vivian/BRIEFING-NOVO-CHAT.md`).

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
- Marca disponível em qualquer sessão pela skill global `keshion-marca` (em `~/.claude/skills`), que aponta para esta pasta: se mover a pasta, atualizar o caminho na skill.
- Material visual da Keshion (site, app, redes, propostas, contratos, apresentações, SOPs) segue `branding/guia-de-marca.md`; arquivos oficiais (logos, ícones, fontes, CSS) em `branding/kit/`. PDF e contrato: sempre fundo claro. Nunca digitar "KESHION AI" no lugar do logo.
- Commit e push dentro desta pasta; memória `keshion-migracao-n8n` com cópia no segundo cérebro (`Documents\segundo-cerebro`).

## Padrões de trabalho (pedidos da Erica em 17/11/2026)

1. **Respostas curtas por padrão:** só o resultado e o que ela precisa decidir. Explicação longa só quando ela pedir.
2. **Resumo ou nova conversa:** atualizar `tecnico/RETOMAR-AQUI.md` e terminar com a frase pronta para colar: "Projeto Keshion. Leia `tecnico/RETOMAR-AQUI.md` e vamos para [próxima feature]." (conversa aberta na pasta `Documents\Claude Code\keshion`)
3. **Uma feature por conversa.** Ao terminar, atualizar o RETOMAR-AQUI e sugerir abrir conversa nova.
4. **Revisão pelo Codex:** ao fechar cada feature que mexa no fluxo, nas instruções ou no servidor, lembrar a Erica de rodar a revisão no Codex com `tecnico/n8n/PROMPT-CODEX-REVISAO.md` (dizer qual feature revisar).
5. **Testes (regra de 18/11/2026):** os testes da Clara rodam só na conversa de testes da Erica, um por vez. Nas outras conversas: corrigir, publicar e entregar um prompt de teste pronto para colar lá (depois de mudar instruções, `tecnico/teste-ab/paciente_simulado.py`; depois de mudar o fluxo, também `teste_n8n.py`). Não rodar teste fora dela. Para publicar fluxo, import e publish bastam: não reiniciar o n8n, que derruba conversas em andamento. Lista completa em `tecnico/testes-checklist.md`.
6. **Modelo:** Opus para desenhar feature nova, decisão difícil e revisão; Sonnet para rodar teste, ajustar texto, documentar e tarefas repetidas.

## Project Manager

- Agente `project-manager` (`.claude/agents/project-manager.md`): daily, status, prioridades, riscos e organização no GitHub e no Notion. Quando a Erica pedir "daily", "status" ou "o que eu faço hoje", usar esse agente e o formato de daily dele (10 blocos, do Termômetro ao que o PM atualizou). O PM também mantém o Notion em dia todo dia.
- Especialistas que o PM consulta (e que a Erica pode chamar direto): `estrategia`, `tecnico`, `marketing` e `vendas`, em `.claude/agents/`. Cada um tem a lista do que resolve sozinho, do que exige OK e das ferramentas do pm-skills que usa (plugins ligados em `.claude/settings.json`).
- Daily automático todo dia às 9h (tarefa agendada `keshion-pm-daily` no app do Claude; roda só com o app aberto).
- Executor todo dia às 14h (tarefa `keshion-executor-14h`): faz o que o daily marcou em "Para o executor das 14h" (só o que os especialistas resolvem sozinhos) e registra na seção "✅ Executor 14h" da página do daily no Notion.

## Mapa curto

| Onde | O quê |
|---|---|
| `tecnico/` | n8n, servidor, testes, revisões |
| `clientes/` | uma pasta por clínica (sem dados de pacientes) |
| `comercial/` | oferta, proposta, contrato |
| `app-crm-painel/` | app da clínica, CRM e painel |
| `pesquisa/` | mercado, nichos, concorrentes |
| `plano-estrategico-keshion.md` | plano de longo prazo (metas até 2030) |
