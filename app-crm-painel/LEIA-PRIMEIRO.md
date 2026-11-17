# App, CRM e painel da Keshion IA

> Tudo sobre o dashboard, o CRM e o app da clínica está nesta pasta. Estado em 17/11/2026, com as decisões de 16/11/2026. Para o contexto geral do negócio, leia também `../CLAUDE.md` e `../SESSAO-2026-11-01-RESUMO.md`.

## 0. Decisões de 16/11/2026 (valem sobre o resto deste guia)

Detalhe em `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md`. Onde este guia disser outra coisa, valem estas:

- **O app deixa de ser planilha + AppSheet/Glide + Looker Studio.** Vira app web em Next.js, que abre no computador e se instala no celular (PWA), com Netlify (telas) e Supabase (login, banco e arquivos), na região São Paulo, com backup diário para o Contabo e cada clínica vendo só os próprios dados.
- **Público:** dentista solo ou clínica com 2 ou 3 dentistas, sem software de gestão.
- **Piloto real:** Dra. Vivian, a partir de 01/12/2026. A Dra. Suzana continua sendo a clínica fictícia de demonstração.
- **Dezembro:** Pendências, Conversas, Agenda do dia (nova, com compareceu e faltou) e Pacientes.
- **Janeiro:** Orçamentos (nova, com PDF e envio pelo WhatsApp), Resultados e Retornos.
- **Fora:** prontuário, nota fiscal, financeiro, integrações.
- **Reais recuperados:** nova regra na seção 3, aba Resultados.
- **Domínio:** keshion.com, com o app em app.keshion.com.
- **Em aberto:** o banco "clara" vai para o Supabase ou o app lê os dados do Contabo.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `LEIA-PRIMEIRO.md` | Este guia: decisões, histórico e o que falta |
| `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md` | Decisões de 16/11/2026: tecnologia, hospedagem, custos, o que entra em dezembro e janeiro, regra de reais recuperados |
| `prototipo-crm-mobile.html` | **Protótipo atual, versão 3.** Publicado em https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr |
| `previa-painel.html` | Primeira prévia do painel, com dados fictícios. Publicada em https://claude.ai/artifact/PTMcbDMS6ZhU4CibshYiGS. Ficou antes das decisões da versão 3: usar só como referência |
| `crm-agenda-painel.md` | Desenho técnico: colunas da planilha, painel, cenários de Agenda e Confirmações, importação de pacientes antigos. **Feito para a planilha do Google, que saiu em 16/11/2026.** Serve só de referência de campos e regras |
| `modelo-crm-keshion.xlsx` | Modelo da planilha do CRM. **Superado em 16/11/2026** pelo banco no Supabase. Serve só de referência de campos |

Para republicar o protótipo no mesmo link, publique este arquivo passando a URL do artifact. Sem a URL, o publish cria um link novo, porque o arquivo mudou de pasta em 04/11/2026.

## 1. Como chegamos até aqui

1. **Prévia do painel:** indicadores, gráficos e orçamentos parados, com dados fictícios.
2. **Protótipo versão 1:** abas Hoje, Funil, Pacientes, Reativar e Resultados.
3. **Versão 2:** revisão de UX (fila de tarefas, Desfazer, dados pedidos na hora certa).
4. **Crítica da Erica à versão 2:**
   - visual feio e com cara de antigo;
   - termos comerciais demais ("funil");
   - abas Funil e Pacientes repetidas;
   - a IA não deveria pedir aprovação para o que já sabe responder;
   - "enviar acompanhamento" não ficou claro;
   - mensagem de retorno robotizada;
   - "faltas evitadas" não é medível;
   - faltavam avisos e lembretes para a equipe.
5. **Versão 3:** 5 abas novas, visual refeito a partir das 7 referências da Erica. **Ela aprovou: "ficou ótimo".** Disse que ainda tem alterações a fazer, mas não listou quais.
6. **16/11/2026:** decisões de tecnologia, hospedagem e calendário (seção 0). O protótipo ainda não foi ajustado a elas: faltam Agenda do dia e Orçamentos, e a regra de reais recuperados mudou.

## 2. Decisões que valem hoje

- **Estilo visual: Oliva** (creme e verde-oliva). Menta e Lavanda foram vistos e descartados. O seletor de estilos ainda está no protótipo e pode sair.
- **Direção visual, vinda das referências:** cantos bem arredondados, cartões leves, títulos grandes, muito espaço, avatares com iniciais, etiquetas de status coloridas, barra de navegação escura e flutuante, com a aba ativa em destaque. No computador, vira barra lateral com conteúdo em duas colunas. As imagens originais não ficaram salvas.
- **Fonte:** Plus Jakarta Sans.
- **Celular primeiro,** mas funcionando também no computador da recepção.
- **Linguagem de recepção:** nada de "funil", "lead", "etapa" ou "temperatura".
- **A IA responde sozinha** tudo o que está na base da clínica, incluindo agendar, confirmar e lembrar do orçamento. Opção combinada: 1 semana inicial com aprovação antes do envio, para a clínica ganhar confiança.
- **A equipe só entra em:** pedido de pessoa, dor ou urgência, reclamação, desconto ou condição especial, pergunta fora da base.
- **CRM e painel usam os mesmos dados**, no banco do Supabase, dentro do próprio app (seção 0). Planilha, AppSheet, Glide e Looker Studio saíram em 16/11/2026.
- **Anotação clínica fica no prontuário** do sistema da clínica, não no CRM (LGPD).

## 3. As abas

Em dezembro: Pendências, Conversas, Agenda do dia e Pacientes. Em janeiro: Orçamentos, Resultados e Retornos. Agenda do dia e Orçamentos foram definidas em 16/11/2026 e ainda não estão desenhadas no protótipo.

**Pendências:** só o que precisa de uma pessoa.
- Resumo de quantos esperam e há quanto tempo.
- Responder agora: urgência, pediu a doutora, a IA não sabe.
- Decidir: desconto, com botões de resposta.
- "Responder e ensinar a IA": a resposta entra na base da clínica.
- Avaliações de hoje e amanhã, com status.
- Quantas conversas a IA resolveu.

**Conversas:** caixa de entrada para acompanhar a IA.
- Selos: IA respondeu, Agendou, Aguardando a equipe, A equipe assumiu.
- Filtro "Fora do horário".
- "Assumir conversa" pausa a IA para aquele paciente; "Devolver para a IA" retoma.

**Pacientes:** o CRM, juntando as antigas Funil e Pacientes.
- Busca, Novos contatos ou Já pacientes, e filtro por situação.
- Situações: Novo contato, Em conversa, Avaliação marcada, Avaliou aguardando orçamento, Orçamento em aberto, Em tratamento, Tratamento concluído, Não fechou (pede o motivo).
- Ficha editável: dados, tratamento, sessões feitas (exemplo: 3 de 6), próxima sessão, valor, pagamento, anotações da equipe e histórico.

**Retornos:** pacientes antigos no tempo da revisão, da manutenção ou do retorno. A Erica achou a aba excelente.
- Seleção, prévia da conversa e aprovação do envio.
- Regras: autorização escrita da clínica, no máximo 1 mensagem a cada 90 dias, opção SAIR, lotes pequenos pela API oficial (Z-API em volume arrisca bloqueio).
- Tom aprovado como exemplo: "Olá, Sônia, tudo bem? Aqui é a Erica, da clínica da Dra. Suzana. Vi que já faz um tempo da sua última visita e queria saber se você quer marcar sua revisão. Quer que eu veja os horários livres da doutora?"
- Se a pessoa disser que sim, a IA consulta a agenda, oferece horários e marca.

**Resultados:** só o que dá para medir, dizendo de onde vem cada número.
- Medido pelo sistema: mensagens respondidas, fora do horário, tempo de resposta, avaliações marcadas pela IA, remarcações, confirmações, lembretes de orçamento, retornos que agendaram.
- Depende de a equipe marcar: valor fechado, comparecimento, orçamentos em aberto, motivos de não fechar.
- **Reais recuperados (regra de 16/11/2026):**
  - *Recuperado pela assistente* (entra no total): paciente parado há 7 dias ou mais sem contato da equipe, que respondeu à assistente e aceitou em até 30 dias.
  - *Influenciado*: linha separada, fora do total.
  - *Orgânico*: não conta.
  - A clínica confirma o valor e pode contestar.
  - A regra antiga (chegou fora do horário, fechou depois de lembrete ou voltou por retorno) foi substituída. O "R$ 48 mil" e o "Como calculamos" do protótipo ainda usam a antiga.
- **Faltas:** mostrar a taxa de antes (informada pela clínica) ao lado da de agora, rotulada como comparação. Nunca chamar de "faltas evitadas".
- A Erica pediu para definir esta aba com calma: ela disse "estamos no caminho".

**Lembrete do orçamento** é o nome da antiga "enviar acompanhamento": mensagens automáticas nos dias 1, 3, 7, 15 e 30 depois da entrega do orçamento.

## 4. Avisos para a equipe

- Aviso imediato no grupo de WhatsApp da clínica a cada pendência, com paciente, motivo e link.
- Sem resolução em 10 minutos no horário comercial: novo aviso à recepção.
- Em 30 minutos: aviso direto à doutora.
- Fora do horário: o paciente recebe o horário de retorno, e o aviso sai na abertura da clínica.
- No app: número vermelho na aba e cronômetro em cada item.
- Os tempos são ajustáveis por clínica.

## 5. O que os concorrentes mostram

AtendeJá, Secretária Odonto e Secretária IA prometem painel ou CRM, mas nenhum mostra a tela real. Nenhum cita orçamento formal, valor recuperado com regra explicada ou aprovação antes do envio. Ideias aproveitadas: pacientes quentes, reativação por tempo parado, lembrete 2 horas antes, resumo do dia no WhatsApp da doutora. Detalhes na seção 6 de `../SESSAO-2026-11-01-RESUMO.md`.

## 6. O que falta

1. **Calculadora de perdas e ROI** (próximo passo combinado em 16/11/2026; as perguntas estão no outro chat).
2. Decidir se o banco "clara" vai para o Supabase ou se o app lê os dados do Contabo.
3. Ajustar o protótipo às decisões de 16/11: desenhar Agenda do dia e Orçamentos, aplicar a nova regra de reais recuperados e ouvir da Erica as outras alterações.
4. Criar o Supabase (região São Paulo) e o Netlify, com o backup diário para o Contabo e a regra de acesso por clínica.
5. Montar as telas de dezembro a tempo do piloto da Dra. Vivian em 01/12/2026.
6. Montar as telas de janeiro: Orçamentos, Resultados e Retornos.
7. Ajustar o tom da mensagem de retorno quando chegarem as respostas da clínica fictícia da Dra. Suzana.

Saíram da lista em 16/11/2026: comparar AppSheet e Glide, criar a planilha e o painel no Looker Studio, atualizar a planilha modelo.

O estado da automação no Make fica em `../SESSAO-2026-11-01-RESUMO.md`, seções 3 e 4. Confira na conta do Make antes de confiar nele, porque pode ter mudado depois de 01/11/2026.
