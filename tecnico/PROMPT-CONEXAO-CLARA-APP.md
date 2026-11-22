# Prompt para abrir a conversa da feature "Conexão Clara e app"

Abrir conversa nova na pasta `Documents\Claude Code\keshion`, de preferência com Opus (desenho de feature nova), e colar o texto abaixo.

---

Projeto Keshion. Feature desta conversa: **conexão entre a Clara (n8n, no Contabo) e o app (Next.js, Netlify e Supabase)**. Leia `tecnico/RETOMAR-AQUI.md` e, para esta feature, também:

- `app-crm-painel/LEIA-PRIMEIRO.md` e `app-crm-painel/RESUMO-HOSPEDAGEM-E-DECISOES-APP.md` (telas, decisões e regras do app)
- `app/supabase/schema.sql` (rascunho do banco do app, com RLS por clínica)
- `tecnico/n8n/LEIA-ME.md` e `tecnico/n8n/gerar_fluxos.py` (como os fluxos por clínica são gerados)
- `tecnico/servidor-n8n.md` (servidor e banco da Clara)

**Já decidido (18/11):** a Clara fica no Contabo (Postgres, um banco por clínica) e o app fica no Supabase (região São Paulo), com os dois trocando avisos. Falta escrever o desenho dessa troca.

**Meta desta conversa:** primeiro o desenho, depois a implementação do primeiro pedaço, nesta ordem:

1. Escrever o contrato de eventos entre os dois lados, em `tecnico/conexao-clara-app.md`: quais eventos, em que formato, como cada lado autentica o outro (webhook secreto, chave por clínica), o que acontece se um lado estiver fora do ar (repetir, sem perder nem duplicar) e como cada clínica fica isolada.
2. Dizer qual dado tem dono em qual lado (proposta inicial: pacientes, orçamentos e status da consulta no app; histórico das conversas na Clara) e confirmar ou corrigir comigo.
3. Implementar o menor pedaço que já mostra valor, a combinar comigo depois do desenho (sugestão: a Clara gravar no app os avisos "Precisa de você" e as conversas, e o botão "Assumir conversa" e "Devolver para a IA" pausar e retomar a Clara).

**Proposta inicial de eventos (revisar, não é decisão):**

- Clara para o app: conversas e mensagens, avisos "Precisa de você", paciente novo ou atualizado, consulta marcada, remarcada ou cancelada.
- App para a Clara: assumir e devolver conversa, resposta que ensina a IA (entra na base da clínica), Compareceu e Faltou (para pedir novo horário), orçamento aceito ou recusado (para parar o follow-up), aprovação de rascunho do modo copiloto.

**Decidido em 18/11:** lembretes do orçamento nos dias 3, 10, 17 e 30, com validade de 30 dias, igual ao app. Em aberto: quem registra que o orçamento saiu (sugestão: o app, na aba Orçamentos, prevista para janeiro) e quem dispara os lembretes (sugestão: a Clara, lendo o app).

**Cuidados:**

- Isolamento por clínica é regra: nenhum evento pode cruzar dados entre clínicas (o `teste_isolamento.py` deve continuar passando).
- Dados de saúde: anotação clínica não vai para o app (LGPD). Conferir o que a Clara grava na ficha antes de enviar.
- Pedir OK antes de mudar produção, criar conta, gastar dinheiro ou publicar fluxo. Publicar com import e publish, sem reiniciar o n8n.
- Testes: não rodar aqui. Ao terminar, entregar o prompt de teste pronto para colar na conversa de testes (`paciente_simulado.py` depois de mudar instruções, `teste_n8n.py` e `teste_isolamento.py` depois de mudar fluxo).
- Respostas curtas, português com acentos, sem travessão, linguagem simples.

**Ao terminar:** atualizar `tecnico/RETOMAR-AQUI.md`, lembrar da revisão no Codex (`tecnico/n8n/PROMPT-CODEX-REVISAO.md`, dizendo qual feature revisar) e sugerir abrir conversa nova para a próxima feature.
