# App, CRM e painel da Keshion IA

> Tudo sobre o dashboard, o CRM e o app da clínica está nesta pasta. Estado em 17/11/2026, com as decisões de 16/11/2026. Para o contexto geral do negócio, leia também `../CLAUDE.md` e `../SESSAO-2026-11-01-RESUMO.md`.

## 0. Decisões de 16/11/2026 (valem sobre o resto deste guia)

Detalhe em `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md`. Onde este guia disser outra coisa, valem estas:

- **O app deixa de ser planilha + AppSheet/Glide + Looker Studio.** Vira app web em Next.js, que abre no computador e se instala no celular (PWA), com Netlify (telas) e Supabase (login, banco e arquivos), na região São Paulo, com backup diário para o Contabo e cada clínica vendo só os próprios dados.
- **Público:** dentista solo ou clínica com 2 ou 3 dentistas, sem software de gestão.
- **Piloto real:** Dra. Vivian, a partir de 01/12/2026. A Dra. Suzana continua sendo a clínica fictícia de demonstração.
- **Dezembro:** Conversas (com "Precisa de você" no topo), Agenda do dia (nova, com compareceu e faltou) e Pacientes.
- **Janeiro:** Orçamentos (nova, com PDF e envio pelo WhatsApp), Retornos e Painel.
- **17/11/2026:** Pendências entrou dentro de Conversas, Resultados virou Painel e os lembretes do orçamento passaram a ser nos dias 3, 10, 17 e 30. Estrutura completa na seção 3.
- **Calculadora de perdas e ROI:** vai para o site keshion.com, para o diagnóstico de venda. As respostas dela viram o "antes" no Painel. Ficou em segundo plano em 17/11/2026, depois do protótipo.
- **Fora:** prontuário, nota fiscal, financeiro, integrações.
- **Reais recuperados:** nova regra na seção 3, aba Painel.
- **Domínio:** keshion.com, com o app em app.keshion.com.
- **Em aberto:** o banco "clara" vai para o Supabase ou o app lê os dados do Contabo.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `LEIA-PRIMEIRO.md` | Este guia: decisões, histórico e o que falta |
| `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md` | Decisões de 16/11/2026: tecnologia, hospedagem, custos, o que entra em dezembro e janeiro, regra de reais recuperados |
| `prototipo-crm-mobile.html` | **Protótipo atual, versão 7** (6 abas, marca Keshion, painel com gráficos de disco). Publicado em https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr |
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

- **Visual: marca Keshion AI** (17/11/2026, versão 5 do protótipo). Cores, fontes e logo oficiais de `../branding/guia-de-marca.md`: Manrope 700 nos títulos, Inter no texto, azul intenso #2459A6 nas ações no tema claro, azul #4388E8 no escuro. Segue o tema claro ou escuro do celular. O estilo Oliva e o seletor de estilos saíram.
- **Direção visual "sem cara de IA":** fundo liso, cards com borda fina e cantos de 10 a 12 px, sem degradês nem sombras grandes, títulos de seção como rótulo pequeno em caixa alta, avatares com iniciais numa cor só, etiquetas de status discretas. No celular, barra de abas fixa embaixo com o nome de cada aba sempre visível; no computador, barra lateral com o logo e conteúdo em duas colunas.
- **Celular primeiro,** mas funcionando também no computador da recepção.
- **Linguagem de recepção:** nada de "funil", "lead", "etapa" ou "temperatura".
- **A IA responde sozinha** tudo o que está na base da clínica, incluindo agendar, confirmar e lembrar do orçamento. Opção combinada: 1 semana inicial com aprovação antes do envio, para a clínica ganhar confiança.
- **A equipe só entra em:** pedido de pessoa, dor ou urgência, reclamação, desconto ou condição especial, pergunta fora da base.
- **CRM e painel usam os mesmos dados**, no banco do Supabase, dentro do próprio app (seção 0). Planilha, AppSheet, Glide e Looker Studio saíram em 16/11/2026.
- **Anotação clínica fica no prontuário** do sistema da clínica, não no CRM (LGPD).

## 3. As abas (versão 6 do protótipo, 17/11/2026)

Seis abas: Conversas, Agenda do dia e Pacientes em dezembro; Orçamentos, Reativar e Painel em janeiro. O logo da Keshion aparece na barra lateral, ao lado do nome da clínica e no rodapé de todas as abas (rodapé com 128 px; o guia de marca pede mínimo de 160 px, e a Erica pediu menor), para deixar claro que é um app da Keshion. Os dados de exemplo seguem a base da clínica demo da Dra. Suzana Vidal (lentes, facetas, alinhadores, clareamento e limpeza; sem implante).

**Conversas**
- Em cima, só as conversas encaminhadas para a equipe, numa lista única: urgência, pediu a doutora, a IA não sabe, pedido de desconto, reclamação. Os filtros "Tudo", "Responder agora" e "Decidir" saíram (pedido da Erica).
- Pedido de desconto: botões com respostas prontas e "Outra resposta", em que a equipe escreve o que a IA deve responder.
- "Responder e ensinar a IA": a resposta entra na base da clínica.
- Os botões "Abrir conversa" e "Aceitou" são verdes. Embaixo, todas as conversas, com filtros "Fora do horário" e "A equipe assumiu". "Assumir conversa" pausa a IA; "Devolver para a IA" retoma.

**Agenda do dia**
- Consultas de hoje e amanhã, confirmação, botões Compareceu e Faltou, "Pedir à IA para remarcar" para quem faltou.
- Comparecimento do mês: marcadas, quantas vieram e quantas faltaram. Depois de marcar Faltou, o app pergunta "Pedir à IA para oferecer novo horário?" com Sim ou Não. O "antes e agora" das faltas saiu do app e vai para a reunião semanal ou mensal com a clínica (pedido da Erica).

**Pacientes (CRM)**
- Lista com telefone, como conheceu, situação, progresso do tratamento e aviso de aniversário nos próximos 7 dias.
- Ficha com dados do paciente: WhatsApp, e-mail, aniversário (dd/mm/aaaa, sem idade), endereço, como conheceu e quem indicou, primeiro contato, última e próxima consulta. Botão para editar os dados.
- Situação, tratamento (valor, pagamento, sessões), orçamento do paciente, anotações da equipe e histórico.
- Cadastro novo com nome, WhatsApp, aniversário, e-mail, endereço, como conheceu e indicação.
- Anotação clínica continua no prontuário do sistema da clínica, não no CRM (LGPD).

**Orçamentos**
- Em aberto, aceitos e recusados; lembretes da IA nos dias 3, 10, 17 e 30; Aceitou ou Recusou (pede o motivo).
- **Textos padrão do orçamento** por tratamento (como é o tratamento, etapas, prazo, o que está incluído), tirados da base da clínica e editáveis pela doutora.
- **PDF com a marca da clínica** (não a da Keshion, que aparece só no rodapé como "Gerado pelo app Keshion AI"): número, emissão e validade, dados do paciente (CPF a preencher), plano de tratamento, abatimento da avaliação, formas de pagamento (5% no Pix, 12 vezes sem juros), como é o tratamento, o que está incluído, observações e assinaturas.
- Validade do orçamento: 30 dias (decidido pela Erica em 17/11/2026, para combinar com os lembretes até o dia 30). A base da clínica demo foi atualizada no arquivo; falta levar para a Clara no servidor.

**Reativar** (antiga Retornos; o nome mudou porque "retorno" parecia consulta já marcada)
- Lista "Contatar Sônia: limpeza vencida há 7 meses", seleção, prévia da mensagem e aprovação do envio.
- Regras: autorização escrita da clínica, no máximo 1 mensagem a cada 90 dias, opção SAIR, lotes pequenos.

**Painel**: primeiro os números da clínica, depois onde a assistente ajudou (pedido da Erica: controle da clínica, sem parecer exibição). Versão 7, de 17/11/2026.
1. Valor fechado no mês com gráfico de barras dos últimos 6 meses, e 4 números: tratamentos fechados, ticket médio, pacientes atendidos, comparecimento.
2. **Do contato ao tratamento** (interativo): contatos novos, avaliações, orçamentos e fechados, com a porcentagem sobre os contatos novos. Tocar numa etapa muda o gráfico "De onde vieram".
3. **De onde vieram** (gráfico de disco com ícones de Google, anúncio, Instagram, indicação e outros), que muda conforme a etapa do funil. Tocar numa fatia destaca o valor.
4. **Resumo financeiro** (disco: fechado, em aberto, recusado) e **Faturamento por procedimento** (disco: lentes, facetas, alinhadores, clareamento).
5. Mais abaixo, "Onde a assistente ajudou": recuperado pela assistente (com "Conferir valores" e "Como calculamos"), influenciado fora do total, trabalho da IA e mensagens por hora.
- "Em tratamento agora" saiu do Painel e foi para o topo da aba Pacientes.
- Cores dos gráficos validadas com o script da skill dataviz, nos temas claro e escuro. Verde não fica ao lado de âmbar (confunde quem tem daltonismo).
- **Reais recuperados (regra de 16/11/2026):** recuperado pela assistente (entra no total) é o paciente parado há 7 dias ou mais sem contato da equipe, que respondeu à assistente e aceitou em até 30 dias. Influenciado fica fora do total. Orgânico não conta. A clínica confirma e pode contestar.
- Saíram do app e vão para o relatório da reunião com a clínica: "quantas vezes a mensalidade" e o comparativo com a calculadora.

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

1. **Calculadora de perdas e ROI** para o site (em segundo plano desde 17/11/2026; as perguntas estão no outro chat).
2. Decidir se o banco "clara" vai para o Supabase ou se o app lê os dados do Contabo.
3. Ouvir da Erica as outras alterações no protótipo (a versão 4, de 17/11/2026, já tem as 6 abas).
4. Criar o Supabase (região São Paulo) e o Netlify, com o backup diário para o Contabo e a regra de acesso por clínica.
5. Montar as telas de dezembro a tempo do piloto da Dra. Vivian em 01/12/2026.
6. Montar as telas de janeiro: Orçamentos, Retornos e Painel.
7. Ajustar o tom da mensagem de retorno quando chegarem as respostas da clínica fictícia da Dra. Suzana.

Saíram da lista em 16/11/2026: comparar AppSheet e Glide, criar a planilha e o painel no Looker Studio, atualizar a planilha modelo.

O estado da automação no Make fica em `../SESSAO-2026-11-01-RESUMO.md`, seções 3 e 4. Confira na conta do Make antes de confiar nele, porque pode ter mudado depois de 01/11/2026.
