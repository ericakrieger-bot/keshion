# Briefing: piloto da Keshion IA com a Dra. Vivian

> Escrito em 10/11/2026 para abrir um chat separado, só sobre o piloto. Ler este arquivo inteiro antes de qualquer ação.
> Contexto geral do negócio: `negocio-ia-clinicas/CLAUDE.md`. Plano de longo prazo: `negocio-ia-clinicas/plano-estrategico-keshion.md` (não é o foco deste chat).

## 1. Quem e o quê

- **Keshion IA:** empresa da Erica e do Sérgio (sócio e pai dela), os dois em Israel, vendendo para o Brasil. Atendente de IA no WhatsApp para clínicas odontológicas de alto padrão.
- **Dra. Vivian Ramina:** dentista, amiga da Erica. É a clínica piloto, numa parceria: não paga durante o piloto e, em troca, avalia a assistente como dona de clínica e como dentista, aponta falhas e diz o que falta. **Não tem secretária: atende sozinha.** Tudo que no material genérico diz "equipe" ou "secretária", para ela é a própria Dra. Vivian.
- **Assistente:** na demo se chama Sarah. Para a Dra. Vivian, **ela escolhe o nome**. O nome fica na base e nas instruções de cada clínica; cada clínica pode ter um nome diferente.

## 2. Decisões já tomadas sobre o piloto (10/11/2026)

| Tema | Decisão |
|---|---|
| Duração | 30 dias de acompanhamento próximo a partir da entrada no ar. Depois disso a assistente continua funcionando na clínica |
| Preço | Não escrever "sem custo" no material. Explicar como parceria: em vez de pagamento, ela contribui com a avaliação de cliente e de dentista |
| Condição depois do piloto | Fica para mais tarde. Não colocar no material agora |
| Conexão do WhatsApp | Não oficial (hoje Whapi.Cloud), no número atual dela. A Erica explica pessoalmente. Regras: só responde quem escreveu, sem propaganda, sem envio em massa. O material diz com honestidade que o risco de bloqueio fica baixo, mas não é zero |
| Automação | O material cita n8n (servidor da Keshion), porque a migração do Make para o n8n está decidida. A IA continua sendo a OpenAI, mas a Erica pode trocar |
| Primeira semana | Proposta: a Dra. Vivian confere as respostas antes do envio. **Não está confirmado** que a rota de rascunho para aprovação ainda funciona no cenário 1B depois das reescritas de 09/11 |
| Etapa seguinte (dezembro, sem data fechada) | Confirmações, lembretes de orçamento, aplicativo com o cadastro dos pacientes (CRM) e primeiro relatório |

## 3. Arquivos deste chat

| Arquivo | O que é |
|---|---|
| `clientes/dra-vivian/apresentacao-piloto.md` | Apresentação do piloto, versão 2 (10/11/2026). Conversa com ela na semana de 16/11, quando volta de férias |
| `clientes/dra-vivian/questionario-dra-vivian.html` | Questionário adaptado para ela (95 perguntas em 15 seções, sem secretária, com pacientes da clínica e avisos). Publicado em https://claude.ai/artifact/RQSUXr6Unojv3enM7pJgXh, com salvamento automático no banco da página (coleção `respostas`, documento `questionario`). Ainda não compartilhado com ela |
| `clientes/dra-vivian/ficha-oferta-piloto.md` | **Ficha da oferta, versão 2**, já com as decisões acima. Base para tudo que for enviado a ela |
| `clientes/clinica-demo/Questionario-Keshion-Dra-Suzana.docx` e `.md` | Questionário da clínica (74 perguntas). Trocar o nome para a Dra. Vivian antes de enviar e tirar as perguntas sobre secretária e equipe |
| `clientes/clinica-demo/base-clinica.md` | Base da clínica demo. Modelo para a base da Dra. Vivian |
| `clientes/clinica-demo/instrucoes-sarah.md` | Instruções da assistente. Trocar nome e regras que citam equipe |
| `tecnico/especificacao-sarah.md` | Como a assistente funciona e o que falta |
| `resumo-sessao-sarah-2026-11-09.md` | Últimos testes e correções da Sarah |
| `app-crm-painel/prototipo-crm-mobile.html` | Protótipo do aplicativo (estilo Oliva). Publicado em https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr |

## 4. O que a Erica quer fazer neste chat

1. **Ajustar a ficha da oferta**, se ainda houver pontos.
2. **Apresentação breve para a Dra. Vivian**, baseada na ficha: o que é, o que ela recebe, como funciona o WhatsApp, o combinado do piloto, próximos passos.
3. **Algo para enviar a ela** (página publicada ou PDF), com fotos e mostras de conversa.
4. **Vídeo ou gravação de conversas reais com a assistente na demo**, para mostrar como ela responde (marcar, remarcar, dúvida de preço, áudio, caso de dor).
5. Depois: preparar o questionário dela, a base da clínica, o termo de parceria e colocar a assistente no ar.

## 5. Estado técnico da assistente (10/11/2026)

**Pronto na demo (cenários 1A, 1B, 1C e 1D ativos no Make, equipe 3084523):** dúvidas da base, áudio e foto sem diagnóstico, até 3 horários reais da agenda e marcação, remarcar e cancelar no mesmo evento, bloqueio de marcação em dobro, fila de mensagens rápidas, resposta em até 3 mensagens com "digitando", aviso para a equipe nos casos delicados, ficha do paciente no data store. Reteste de 09 e 10/11: 9 de 12 respostas Ok.

**Falta antes de entrar no número da Dra. Vivian:**

- Pausar a assistente quando a Dra. Vivian responde pelo celular (hoje a assistente não sabe e pode responder por cima). **É o item mais importante, porque ela atende sozinha e vai entrar nas conversas o tempo todo.**
- Remover o comando #reiniciar.
- Proteção contra chamada sem telefone no 1B.
- Número para onde vão os avisos: o WhatsApp pessoal da Dra. Vivian ou um grupo só com ela (campo `PREENCHER_NUMERO_DE_QUEM_APROVA`).
- Base real da clínica e nome da assistente.
- Conferir a rota de aprovação antes do envio.
- **Créditos do Make:** cada mensagem de paciente gasta 25 a 30 créditos, e restavam cerca de 8 mil em 09/11 (não conferido desde então). Isso não sustenta um piloto de 30 dias. Planejar a migração para o n8n logo depois da primeira semana do piloto, ou antes dela. A Erica já tem o servidor.

## 6. Regras para este chat

- Tudo em português do Brasil, com acentuação correta, sem travessão e sem ponto de exclamação no material para a clínica.
- Nada é enviado à Dra. Vivian sem a Erica aprovar.
- Nunca inventar número, depoimento ou resultado. A clínica demo é sempre apresentada como demonstração.
- Nenhum dado real de paciente nas pastas da Keshion. Prints de conversas reais só sem nome.
- Chaves e tokens só no `.env`.
