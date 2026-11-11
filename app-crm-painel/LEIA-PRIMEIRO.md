# App, CRM e painel da Keshion IA

> Tudo sobre o dashboard, o CRM e o app da clínica está nesta pasta. Estado em 04/11/2026. Para o contexto geral do negócio, leia também `../CLAUDE.md` e `../SESSAO-2026-11-01-RESUMO.md`.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `LEIA-PRIMEIRO.md` | Este guia: decisões, histórico e o que falta |
| `prototipo-crm-mobile.html` | **Protótipo atual, versão 3.** Publicado em https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr |
| `previa-painel.html` | Primeira prévia do painel, com dados fictícios. Publicada em https://claude.ai/artifact/PTMcbDMS6ZhU4CibshYiGS. Ficou antes das decisões da versão 3: usar só como referência |
| `crm-agenda-painel.md` | Desenho técnico: colunas da planilha, painel, cenários de Agenda e Confirmações, importação de pacientes antigos. **A seção 0 e as regras de UX foram escritas para a versão 2.** Onde houver conflito, vale este guia |
| `modelo-crm-keshion.xlsx` | Modelo da planilha do CRM: abas Contatos, Mensagens, Agenda, Configuração e Pacientes antigos. **Ainda usa as etapas antigas**; precisa ser trocado para as situações da seção 3 abaixo |

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

## 2. Decisões que valem hoje

- **Estilo visual: Oliva** (creme e verde-oliva). Menta e Lavanda foram vistos e descartados. O seletor de estilos ainda está no protótipo e pode sair.
- **Direção visual, vinda das referências:** cantos bem arredondados, cartões leves, títulos grandes, muito espaço, avatares com iniciais, etiquetas de status coloridas, barra de navegação escura e flutuante, com a aba ativa em destaque. No computador, vira barra lateral com conteúdo em duas colunas. As imagens originais não ficaram salvas.
- **Fonte:** Plus Jakarta Sans.
- **Celular primeiro,** mas funcionando também no computador da recepção.
- **Linguagem de recepção:** nada de "funil", "lead", "etapa" ou "temperatura".
- **A IA responde sozinha** tudo o que está na base da clínica, incluindo agendar, confirmar e lembrar do orçamento. Opção combinada: 1 semana inicial com aprovação antes do envio, para a clínica ganhar confiança.
- **A equipe só entra em:** pedido de pessoa, dor ou urgência, reclamação, desconto ou condição especial, pergunta fora da base.
- **CRM e painel usam os mesmos dados.** Planilha do Google como banco. App de celular sem código por cima (AppSheet ou Glide, **ainda não comparados**). Painel completo no Looker Studio.
- **Anotação clínica fica no prontuário** do sistema da clínica, não no CRM (LGPD).

## 3. As 5 abas

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
- **Valor recuperado:** fechamentos em que o paciente chegou fora do horário, fechou depois de lembrete da IA ou voltou por mensagem de retorno.
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

1. **Ouvir da Erica as alterações** que ela ainda quer no protótipo.
2. Fechar o conteúdo da aba Resultados.
3. Atualizar `modelo-crm-keshion.xlsx` e `crm-agenda-painel.md` para a versão 3 (situações, campo de pendências, tratamento, sessões).
4. Comparar AppSheet e Glide (preço, limite de usuários, uso no celular, avisos) e escolher.
5. Criar a planilha na conta da clínica demo (kashion.ai.2026@gmail.com) e o painel no Looker Studio.
6. Montar o app real sobre a planilha.
7. Ajustar o tom da mensagem de retorno quando chegarem as respostas da clínica fictícia da Dra. Suzana.

O estado da automação no Make fica em `../SESSAO-2026-11-01-RESUMO.md`, seções 3 e 4. Confira na conta do Make antes de confiar nele, porque pode ter mudado depois de 01/11/2026.
