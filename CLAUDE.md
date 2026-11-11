# Negócio de IA para Clínicas

> Projeto paralelo da Erica, separado dos infoprodutos da Mamãe Planejada. Iniciado em 04/10/2026.
> Esta pasta está no `.gitignore` e não sobe para o GitHub do curso.

## O que é

**Make no plano Core desde 01/11/2026. Conta Google da clínica demo: keshion.ai.2026@gmail.com (grafia com "e", corrigido em 01/11/2026).**

**Empresa: Keshion IA** (nome definido em 29/10/2026, nome completo em 01/11/2026; domínio keshion.com.br; sócio: Sérgio).

Serviço B2B de implantação e operação de atendente de IA no WhatsApp para clínicas, vendido como resultado ("recuperar o faturamento que a clínica perde com lead sem resposta, falta e paciente que não volta"), não como ferramenta.

- **Modelo:** diagnóstico grátis, implantação (setup) e mensalidade. Bônus por resultado só depois de 3 cases.
- **Preço inicial de referência:** implantação de R$ 3.000 a 6.000 (piloto) e mensalidade de R$ 1.200 a 2.500. Depois de cases: R$ 6.000 a 12.000 e R$ 1.800 a 3.500.
- **Mensagens da Meta:** cobradas direto no cartão da clínica, cadastrado na conta de WhatsApp dela.
- **Inspiração:** vídeos do Kelvin Cleto (Acelera 360). A Erica decidiu montar o negócio sem a mentoria dele.

## Nicho

Foco inicial: **clínicas de estética e clínicas odontológicas com foco em estética** (lentes de contato dental, facetas, alinhadores invisíveis, clareamento, implantes, harmonização orofacial). A decisão final entre os dois sai das conversas de validação.

Atenção regulatória (verificada em 04/10/2026):
- TRF1 (20/08/2026) anulou a Resolução CFO 198/2019, que criava a harmonização orofacial como especialidade odontológica. Ainda não tem efeito até a publicação do acórdão. O CFO recorre e orienta os dentistas a continuarem.
- TRF1 (2026) manteve a proibição de biomédicos fazerem procedimentos estéticos invasivos (toxina botulínica, intradermoterapia etc.). Clínica de estética tocada só por biomédico é cliente de risco.

## Decisões técnicas

- **Pilha:** API oficial do WhatsApp (Cloud API) + Chatwoot (caixa de entrada) + n8n (automações) + Claude API (Haiku 4.5 para a maioria das conversas, Sonnet 5.5 para as difíceis) + transcrição de áudio (gpt-4o-mini-transcribe) + Google Agenda + Postgres + Metabase, numa VPS com Coolify ou Easypanel.
- **Coexistência** (app + API no mesmo número): só é possível via Solution Partner ou Tech Provider da Meta. No piloto, usar número dedicado à API. Se a clínica exigir manter o app no mesmo número, avaliar um BSP com coexistência (ex.: 360dialog, a partir de € 49/mês por número) ou virar Tech Provider depois.
- **Licença do n8n:** pode rodar fluxos para clientes no servidor da Erica, desde que a clínica nunca acesse o n8n (só o Chatwoot).
- **Cobrança da Meta desde 01/10/2026:** mensagens de serviço (respostas dentro da janela de 24 h) passaram a ser cobradas por mensagem, ao preço de utilidade. Continuam grátis a janela de 72 h aberta por anúncio que leva direto ao WhatsApp e as respostas enviadas pelo app.
- **Chaves e tokens:** só no `.env` da raiz do projeto (regra global do `CLAUDE.md` raiz).
- **Nome da assistente da demo: Clara (desde 11/11/2026, antes Sarah).** Trocado em `_instrucoes`, `_base`, 1B (histórico, avisos, descrição do evento) e 1D (avisos de falha). O arquivo local continua `clientes/clinica-demo/instrucoes-sarah.md`. Onde este arquivo disser Sarah, ler Clara.
- **IA das respostas desde 11/11/2026: Claude Haiku 5.5** (ver o item de instruções abaixo). Áudio e foto no 1A continuam na OpenAI.
- **IA do piloto (decidido em 29/10/2026, substituído em 11/11/2026): só OpenAI**, numa conta e numa chave. Ela escreve as respostas, lê fotos e prints e transcreve os áudios (gpt-4o-mini-transcribe). Escolha da Erica por simplicidade (uma conta, uma conexão no Make). Reavaliar o Claude só na escrita das respostas se o tom não agradar a clínica depois do piloto.
- **Cenário 1 montado no Make em 01/11/2026 (equipe "My Team", id 3084523, ainda inativo):** `Keshion · 1A Entrada (WhatsApp)` (id 8302405: recebe da Z-API, separa áudio, foto e texto, transcreve e lê foto com OpenAI) chama `Keshion · 1B Resposta (IA e modo copiloto)` (id 8302452: base + histórico no data store 240983, OpenAI via chat completions em JSON, rotas responder, rascunho para o aprovador e chamar pessoa). A URL do webhook do 1A vai no campo "Ao receber" da Z-API. A base da clínica fica no registro `_base` do data store. Pendências: conectar OpenAI e Z-API, preencher o número do aprovador e o modelo no módulo "Ajustes" do 1B, preencher a base, e o retorno da aprovação (secretária responde OK e o rascunho vai ao paciente) ainda não existe.
- **WhatsApp da demo: Whapi.Cloud no lugar da Z-API (decidido em 05/11/2026).** Conexão no Make: `Erica's Whapi.Cloud Channel connection` (id 12717425), canal GRNLTR-4K8ZF. A Erica montou e testou o cenário simples `Secretaria IA` (id 8372976, inativo, webhook 4041217). Os cenários 1A e 1B ainda estão com a estrutura da Z-API e precisam ser adaptados. Onde este arquivo citar Z-API para a demo, ler Whapi.
- **Nome da assistente (05/11/2026):** Sarah. Assistente virtual assumida: tem nome, mas nunca diz que é pessoa ou secretária. Sem acesso à agenda, não pode dizer que há vaga nem que marcou. Roteiro de teste em `clientes/clinica-demo/roteiro-teste-respostas.md`; base em `clientes/clinica-demo/base-clinica.md`.
- **Instruções da Sarah (05/11/2026):** ficam no registro `_instrucoes` do data store 240983, e a base no registro `_base`. Para ajustar tom ou regras, altere esses registros, sem mexer no blueprint do 1B. Modelo atual (desde 11/11/2026): Claude Haiku 5.5 (`claude-haiku-5-5`), pela conexão "Anthropic Keshion" (id 12954190) no módulo 6 do 1B, estrutura de pedido "Keshion · Pedido para o Claude" (id 695568). Escolhido no teste A/B da planilha "Teste A/B 2" (Sonnet 1º, Haiku 2º, mas 18 vezes mais barato). Atenção: com as instruções completas, o Haiku devolve primeiro um bloco de pensamento ("thinking", vazio) e só depois o texto, que vem dentro de ```json. Por isso o módulo 7 lê `first(map(6.body.content; "text"; "type"; "text"))` e tira as cercas; ler `content[1].text` dá "resposta ilegível". Para voltar ao Sonnet, basta trocar o valor `modelo` no módulo "Ajustes" do 1B. Scripts do teste em `tecnico/teste-ab/`. Agenda real ligada no 1B; "digitando" via `typing_time` no POST /messages/text.
- **Decisões de 09/11/2026 (comparativo com o prompt mestre):** primeira fase com **uma dentista e uma agenda** (Dr. Rafael, Dra. Camila e implantes saíram da base demo, local e `_base`). Sarah se apresenta como "da clínica" ou "da equipe da Dra. Suzana" e só diz "assistente virtual" se perguntarem (ajustado em `_base` e `_instrucoes`). Remarcar e cancelar entram no fluxo (a fazer). Sem mensagem de "não quero receber mais mensagens": parar de retomar é decidido pela conversa. CRM em Google Planilhas na conta da clínica. Especificação e lista de correções técnicas em `tecnico/especificacao-sarah.md`; roteiro de testes v2 com 38 testes.
- **Correções de 09/11/2026 (depois dos testes da Erica):** 1B reescrito com fila de mensagens (espera 7 s, só a última responde), ficha do paciente no data store (nome_paciente, tratamento, avaliacao_inicio/texto/evento, pendente, ultimo_id), bloqueio de marcação em dobro, ações remarcar e cancelar (PATCH e DELETE no Google Agenda), rotas de erro e resposta da IA em até 3 mensagens (campos mensagem1, mensagem2, mensagem3). Envio pelo novo cenário `Keshion · 1D Envio (até 3 mensagens)` (id 8464848, webhook https://hook.eu1.make.com/txiqa2ndlcyd1jpv2kvihy4dnl3gjj9a). Agenda de 90 dias. Pagamento só Pix, cartão e transferência. Cópia das instruções em `clientes/clinica-demo/instrucoes-sarah.md`. Planilha de testes: "Keshion · Teste da Sarah (Clínica Dra. Suzana)", id 1hvF2r7wvUsax7mZ7m0Ja3sAODjntbpm-HnIOhCNkVyU.
- **Correções de 10/11/2026:** o Sérgio (972552994413) mandou mensagens e a Sarah respondeu, mas o Whapi não entregou (envio terminava em menos de 1 s e o erro era ignorado). Causa confirmada no painel: o teste de 5 dias do Whapi venceu em 10/11 e o canal foi bloqueado; antes disso, os limites do teste (5 conversas por mês) já recusavam contatos novos. Em 11/11 a Erica pagou o plano de US$ 12/mês do canal GRNLTR-4K8ZF (pago até 12/12/2026, conta keshion.ai.2026@gmail.com). Nunca testar o 1B com números fictícios que façam o 1D enviar pelo Whapi: cada número conta como conversa. O 1D agora, quando um envio falha, manda um aviso para a Erica (972584285541) com o número e o texto que não saiu. Regra C das instruções reforçada: se perguntarem só se a clínica faz um tratamento, responder que faz e parar, sem preço e sem oferecer avaliação (exemplo trocado). Histórico do número da Erica apagado (tinha "Joyce" dos testes antigos). O Make não guarda os detalhes das execuções, então o erro exato do Whapi não aparece.
- **Comando #reiniciar (08/11/2026):** no 1A, qualquer número que mandar "#reiniciar" apaga o próprio histórico de conversa (só na demo). Antes de usar o cenário numa clínica real, remover essa rota ou restringir aos números da Keshion.
- **Cenário 1C Fechamento (09/11/2026, id 8463643, webhook 4068828):** recebe do 1B, depois de marcar uma avaliação, o telefone, a despedida e o tamanho da conversa; espera 1 minuto e, se o paciente não respondeu, envia a despedida. Fica separado para o 1B não travar a fila durante a espera (um cenário instantâneo do Make atende uma mensagem por vez). Erros no envio são ignorados.
- **Migração futura para o n8n (decisão de 09/11/2026, ainda NÃO migrar):** o Make cobra por módulo executado. Hoje são uns 25 a 30 créditos por mensagem de paciente: 19 a 24 no 1B e 1 por evento do Whapi no 1A. Os status já estão desligados; o que pesa é cada mensagem enviada pela Sarah voltar como evento "messages". A Erica já tem um VPS para o n8n; avisar a ela quando for a hora de migrar. O plano é ir para o n8n instalado num servidor próprio, com custo fixo. Até lá: não montar funcionalidade grande nova no Make sem perguntar; manter tom e base em texto, fácil de levar; documentar aqui a lógica de cada cenário; evitar recursos que só existem no Make. Momento sugerido: depois dos testes de tom e antes dos fluxos de confirmação e lembrete.
- **Envio com jeito humano (pedido da Erica em 03/11/2026, ainda NÃO aplicado nos cenários; aplicar ao montar os envios):**
  - Antes de cada mensagem, ligar o status "digitando" pela Z-API e deixá-lo ativo por alguns segundos.
  - Nunca responder na hora: módulo Sleep do Make logo após o gatilho, de 4 a 8 segundos (fixo ou aleatório).
  - Texto longo vira 2 ou mais mensagens: digitando, esperar 3 s, mensagem 1; digitando de novo, esperar 4 s, mensagem 2. Pedir à OpenAI a resposta já dividida em partes.
  - Nada de link na primeira mensagem para um contato novo: link (site, agenda, mapa) só depois que a pessoa respondeu pelo menos uma vez.
  - Observação: o Sleep do Make tem limite de 300 s por módulo e o tempo conta na execução do cenário; o 1B já tem `delayTyping: 3` no envio da Z-API.
- **Pilha alternativa em avaliação (11/10/2026), pedida pela Erica:** Make (no lugar do n8n) + Z-API (no lugar da API oficial), sem servidor na primeira versão (histórico no Make, planilha do Google, Google Agenda). A conta do Make da Erica (zona eu1) está conectada por MCP e hoje está no plano Free (1.000 créditos, 2 cenários); o Core é necessário para os 6 cenários. Recomendação: Z-API só no número de demonstração; na clínica, API oficial com número novo (caminho B) ou no mesmo número via parceiro (caminho C). Custo estimado por clínica no caminho A: R$ 280 a 390/mês.

## Como trabalhar nesta pasta

- Aqui o Claude também atua como construtor técnico: monta servidor, fluxos, agente e painel. Sempre explicar em linguagem simples, passo a passo, e pedir aprovação antes de criar contas, gastar dinheiro ou mexer em número de WhatsApp de cliente.
- Toda resposta em português do Brasil com acentuação correta, sem travessão.
- Dados de pacientes das clínicas: nunca salvar nesta pasta. Só dados de teste.

## Mapa de arquivos

| Pasta | Conteúdo |
|---|---|
| `pesquisa/` | Pesquisa de mercado (nichos, preços, concorrentes, regulação) |
| `tecnico/` | Guia técnico, configurações, roteiros de teste |
| `comercial/` | Oferta, proposta, contrato, roteiros de conversa, calculadora |
| `clientes/` | Uma subpasta por clínica (questionário, manual da clínica, métricas). Sem dados de pacientes. |
| `guia-tecnico-e-mercado.html` | Guia visual da parte técnica + pesquisa de odontologia estética e estética |
| `pesquisa/concorrentes-odonto.html` | Mapa de 9 concorrentes (11/10/2026). Publicado em https://claude.ai/artifact/HN1F5p8XKExVSE6edRW9Mc. Dados brutos em `pesquisa/dados/` |
| `app-crm-painel/` | **Tudo do dashboard, CRM e app da clínica.** Começar por `app-crm-painel/LEIA-PRIMEIRO.md` (04/11/2026) |
| `SESSAO-2026-11-01-RESUMO.md` | **Ler primeiro ao retomar.** Estado do projeto em 01/11/2026: decisões, o que está montado no Make (ids, webhooks, links de credenciais), próximos passos da automação, protótipo do app (estilo Oliva aprovado), concorrentes |
| `plano-estrategico-keshion.md` | **Plano de longo prazo (10/11/2026).** Visão: referência em automações e agentes de IA para pequenos e médios negócios, Brasil e depois Estados Unidos. Empresa enxuta, sem investidores. Metas: R$ 100 mil/mês até jun/2028 e R$ 1 milhão/mês até dez/2030. Fases com datas, plano por área e os próximos 40 dias. Primeiro pagante até 31/01/2027. Não citar a Mamãe Planejada nos planos da Keshion (pedido da Erica). Publicado como documento editável em https://claude.ai/artifact/FoYkJBHnu5EPS65aLYZKNB |
| `MATERIAL-COMPLETO.md` | **Ler primeiro.** Tudo consolidado em 19/10/2026: negócio, nicho, concorrentes, diferencial, produto, custos, passo a passo do produto e da venda, modelos prontos, número e eSIM, ferramentas, riscos, pendências |
| `tecnico/plano-make-zapi.html` | Plano de montagem com Make + Z-API: 6 cenários, 3 caminhos de número, custos, passo a passo com dono de cada tarefa, ferramentas e rotina (11/10/2026). Publicado em https://claude.ai/artifact/T6ZGnAMdYSuNkGThwG4BPw |
| `clientes/dra-vivian/` | **Piloto com a Dra. Vivian (10/11/2026).** Começar por `BRIEFING-NOVO-CHAT.md`. Ficha da oferta v2 em `ficha-oferta-piloto.md`. Decisões: ela escolhe o nome da assistente (o nome é por clínica; Sarah é só a demo), não tem secretária (avisos e aprovação vão para ela), conexão não oficial no número atual, 30 dias de acompanhamento e a assistente continua depois, parceria em troca da avaliação dela como cliente e dentista |
| `clientes/clinica-demo/` | Clínica de demonstração da Dra. Suzana (fictícia), montada como se fosse um cliente real. Questionário da clínica em `.md` e `.docx` (01/11/2026), que serve de modelo para clientes reais |
| `app-crm-painel/crm-agenda-painel.md` + `app-crm-painel/modelo-crm-keshion.xlsx` | Desenho do CRM (Google Planilhas), painel (Looker Studio), cenários de Agenda e Confirmações e ajuste no 1B (01/11/2026). A Erica quer agenda e CRM já na primeira versão |
| `app-crm-painel/prototipo-crm-mobile.html` | Protótipo do CRM para celular (Hoje, Funil, Pacientes, Reativar, Resultados), publicado em https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr. Prévia do painel em https://claude.ai/artifact/PTMcbDMS6ZhU4CibshYiGS. App real planejado em AppSheet ou Glide sobre a planilha |
| `tecnico/comparacao-make-n8n-vps.md` | Make x n8n Cloud x n8n em VPS, e Hostinger x Contabo (29/10/2026). Recomendação: Make no piloto, n8n na Hostinger a partir de 3 clínicas ou US$ 50/mês no Make |
| `pesquisa/comparacao-nichos.html` | Odontologia x estética x energia solar: placar, raio-x, concorrentes de estética e solar, recomendação (11/10/2026). Publicado em https://claude.ai/artifact/Bz25YzNk66cizhSYzeY1vh |

## Concorrentes (resumo de 11/10/2026)

- **Mais fortes:** Cloudia (desde 2016, +1.000 clínicas, saúde em geral, tem programa de agências parceiras), Odonto Results (agência desde 2020, IA + central humana + tráfego, modelo mais parecido com o da Erica), Simples Dental (lançou Secretária IA por cerca de R$ 180/mês para 19 mil clínicas da base).
- **Novatos de 2026:** Gênesis, Secretária Odonto, AtendeJá, PRI. Pouca presença, sem prova.
- **Faixa de preço do software:** R$ 259 a R$ 997/mês; implantação de R$ 497 a R$ 700.
- **Espaço livre:** ninguém se posiciona para o sorriso estético (lente, faceta, alinhador, clareamento) nem coloca o acompanhamento do orçamento alto no centro da oferta.
- **Ameaça de base (Meta):** desde 24/02/2026 o WhatsApp Business tem o Business AI, agente de IA gratuito dentro do próprio app (responde dúvidas, indica itens do catálogo e passa para humano). A Meta prevê cobrança futura pelo plano Meta One. Responder dúvida frequente virou grátis: o valor da oferta precisa estar em agenda integrada, acompanhamento de orçamento, recuperação de lead e relatório de resultado.

## Decisão de nicho (comparação de 11/10/2026)

- **Nicho 1, agora:** odontologia de alto valor. Definido pelo problema (tratamento caro e orçamento que esfria), não pelo procedimento: sorriso estético na vitrine e na mensagem, implantes e protocolos incluídos. Filtro de cliente: vende tratamento acima de R$ 5 mil e recebe contato por anúncio. Placar: 38/45.
- **Em avaliação (11/10/2026):** foco em clínicas de alto padrão (independentes, dono com marca pessoal, preço acima da média, anúncio no Instagram), não em redes populares nem no luxo de indicação. Diferencial proposto: IA nos bastidores ("modo copiloto": a IA escreve, a secretária aprova; resposta automática só fora do horário e em confirmações), manual de voz por clínica, jornada do orçamento alto, mesmo número da clínica (coexistência via BSP) e relatório de reais recuperados. Operação 100% remota.
- **Nicho 2, depois de 3 cases:** estética, só clínica tocada por médico ou por dentista que já é cliente e faz harmonização. Mercado cresce (+18% no 1º tri de 2026), mas é lotado (BeautyBot R$ 1,99/atendimento, HOF advisor "tráfego + IA por R$ 1.500", 26 anúncios ativos) e juridicamente instável. Placar: 33/45.
- **Nicho 3, não agora:** energia solar. Venda alta, mas mercado em queda pelo 2º ano (ABSOLAR −7% em 2026, demanda −48% no 1º semestre), 68% das integradoras com até 4 pessoas, SolarZ com 7 mil integradores e IA com CRM a partir de R$ 79. Placar: 27/45.

## Outros nichos e produtos de IA (pesquisa de 11/10/2026)

- **Nichos com a mesma lógica do odonto estético (orçamento alto + lead de anúncio):** energia solar (ticket de R$ 15 mil a 50 mil, ciclo de 30 a 60 dias), imobiliárias, estética médica. Infoprodutores (recuperação de Pix, boleto e cartão recusado + suporte ao aluno) é o nicho mais próximo da experiência da Erica.
- **Com ressalva:** advocacia (Provimento OAB 205/2021: só atender quem procurou, sem promessa de resultado), veterinárias (lembrete de vacina e retorno, ticket menor).
- **Evitar no começo:** restaurantes, salões, varejo de catálogo simples (ticket baixo e o Business AI grátis da Meta já cobre).
- **Produtos de IA em alta que se encaixam:** criativos e vídeos com IA para anúncio de clique para WhatsApp, GEO (aparecer nas respostas do ChatGPT e do Gemini), tutor de IA treinado no conteúdo de um curso, treinamento de IA para equipes, agente de voz (módulo futuro), apps sob medida feitos com IA.

## Fases do plano

0. Validar (semanas 1 a 4): abrir ME, cliente oculto em 30 clínicas, 15 a 20 conversas de diagnóstico, decidir o nicho.
1. Demonstração (semanas 3 a 6): montar a estrutura técnica num número de teste da Erica.
2. Piloto (semanas 6 a 12): 1 ou 2 clínicas com preço reduzido e meta no contrato.
3. Vender o modelo (meses 4 a 6): chegar a 5 clínicas e padronizar.
4. Escalar (depois do mês 6).
