# Negócio de IA para Clínicas: material completo

> Consolidado em 19/10/2026 a partir de tudo o que foi conversado entre 04/10 e 11/10/2026.
> Pesquisas, preços e regras são de 11/10/2026 ou antes. Antes de qualquer decisão com dinheiro, confira se mudaram.
> Esta pasta está fora do Git. Nenhuma chave, senha ou dado de paciente deve ser escrito aqui.

---

## Sumário

1. Estado atual e o que fazer agora
2. Resumo em uma página
3. O negócio: o que é, como cobra, quanto cobra
4. De onde veio a ideia (Kelvin Cleto) e por que seguir sem a mentoria
5. Mercado e escolha do nicho
6. Regras que mudam o jogo (Meta, conselhos, LGPD)
7. Concorrentes
8. O diferencial: atendimento de alto padrão
9. O produto: o que inclui e o que não inclui
10. Como o produto funciona por dentro
11. Quanto custa
12. Passo a passo da criação do produto
13. Modelos prontos para montar o produto
14. Passo a passo do negócio (vender e operar a distância)
15. Modelos prontos para vender
16. O número de WhatsApp: Israel, Brasil e eSIM
17. Quem faz o quê: você e o Claude Code
18. Ferramentas de solopreneur
19. Rotina semanal
20. Riscos e cuidados
21. Regras de segurança do projeto
22. Outros nichos e outros produtos de IA (para o futuro)
23. Arquivos, páginas publicadas e fontes
24. Glossário

---

## 1. Estado atual e o que fazer agora

**Onde você parou (19/10/2026):**

| Item | Situação |
|---|---|
| Nicho | Decidido: odontologia de alto valor (sorriso estético na vitrine, implantes incluídos), para clínicas de alto padrão |
| Ferramentas do produto | Escolhidas para o piloto: Make + Z-API + Claude |
| Piloto, etapa 1 (chave do Claude no Make) | **Pendente.** Você cria a chave no console da Anthropic e cola no link do Make (seção 12) |
| Piloto, etapa 2 (número de demonstração) | **Pendente.** Você ia tentar contratar o Vivo Lite com eSIM e me contar em que tela travou (seção 16) |
| Conexão do Make com o Claude Code | Estava conectada no dia 11/10; na sessão de 19/10 ela apareceu desconectada. Precisa reconectar antes de eu montar os cenários |
| Empresa (CNPJ) | Ainda não aberta. Abrir quando o primeiro cliente estiver perto de fechar |

**Próximos passos, em ordem:**

1. Criar a chave do Claude e guardar no Make (15 minutos).
2. Conseguir o número de demonstração: Vivo Lite com eSIM ou, se travar, um segundo número de Israel só para o piloto.
3. Eu escrevo a base da clínica de demonstração e o manual de voz; você aprova.
4. Reconectar o Make nesta sessão; eu monto o cenário de atendimento.
5. Conectar o número na Z-API (só nesse momento, porque o teste grátis dura 2 dias).
6. Você testa como paciente.

---

## 2. Resumo em uma página

- **O que é:** serviço de implantação e operação de um atendente de IA no WhatsApp para clínicas odontológicas de alto padrão. Vendido como resultado ("recuperar os orçamentos que a clínica deixa esfriar"), não como software.
- **Para quem:** clínica independente, dono dentista com marca pessoal, preço acima da média da cidade, anúncio no Instagram, 2 cadeiras ou mais, vende tratamento acima de R$ 5 mil (lentes, facetas, alinhadores, clareamento, implantes, protocolos).
- **Como cobra:** diagnóstico grátis, implantação (taxa única) e mensalidade.
- **Quanto:** piloto com implantação de R$ 3.000 a 6.000 e mensalidade de R$ 1.200 a 2.500. Depois de cases: R$ 6.000 a 12.000 e R$ 1.800 a 3.500. Para alto padrão, mira de R$ 2.000 a 3.500 por mês.
- **Diferencial:** a IA trabalha nos bastidores (modo copiloto), fala no tom de clínica de alto padrão, acompanha o orçamento até virar venda, usa o mesmo número da clínica e entrega relatório de reais recuperados.
- **Como é feito:** Make (automação) + Z-API ou API oficial do WhatsApp + Claude (IA) + Google Agenda e Planilhas. Tudo remoto.
- **Custo por clínica:** cerca de R$ 280 a 390 por mês no caminho mais barato. Margem acima de 80%.
- **Quem constrói:** o Claude Code monta e mantém a parte técnica; você vende, aprova textos, cuida das contas e do relacionamento.
- **Maior risco:** a Z-API não é a API oficial da Meta e o número pode ser bloqueado. Usar Z-API só no número de demonstração; na clínica, preferir a API oficial.

---

## 3. O negócio: o que é, como cobra, quanto cobra

### 3.1 O que você vende

Você não vende "um robô". Vende um processo que faz a clínica perder menos dinheiro em três pontos:

1. **Demora na resposta.** O paciente pergunta preço à noite ou no fim de semana e ninguém responde.
2. **Falta na avaliação.** O paciente marca e não aparece, porque ninguém confirmou.
3. **Orçamento que esfria.** A clínica passa um orçamento de R$ 10 mil a 40 mil e ninguém acompanha. Em uma semana ele morre.

O atendente de IA responde em segundos, agenda, confirma, acompanha o orçamento e mostra ao dono quanto dinheiro voltou.

### 3.2 Modelo de cobrança

| Etapa | O que é | Preço |
|---|---|---|
| Diagnóstico | Cliente oculto no WhatsApp da clínica + reunião de 30 minutos mostrando o que ela perde | Grátis (é a sua isca) |
| Implantação | Levantamento, montagem, base da clínica, manual de voz, treino da secretária, 2 semanas de copiloto | Piloto: R$ 3.000 a 6.000. Depois de cases: R$ 6.000 a 12.000 |
| Mensalidade | Operação, revisão semanal das conversas, ajustes, relatório mensal | Piloto: R$ 1.200 a 2.500. Depois: R$ 1.800 a 3.500 |
| Bônus por resultado | Percentual sobre orçamentos recuperados | Só depois de 3 cases |

**Regras de oferta:**

- **Preço de fundador** para os 3 primeiros clientes, com desconto declarado sobre o preço cheio.
- **Garantia:** 30 dias para cancelar sem perguntas e uma meta de 60 dias escrita no contrato (inspirado na AtendeJá, ver seção 7).
- **Mensagens da Meta** (quando houver, na API oficial) são pagas no cartão da própria clínica, cadastrado na conta de WhatsApp dela.
- **Não entre barato.** Para o público de alto padrão, preço baixo sinaliza qualidade baixa.

### 3.3 Fórmula de preço que o Kelvin ensina (referência)

- Implantação = potencial de faturamento anual que o atendente pode recuperar × probabilidade de dar certo × 10% a 20%.
- Mensalidade = 10% a 20% do valor da implantação.

Use como conferência: se a conta der muito abaixo das faixas da tabela, o cliente não é de alto valor.

### 3.4 Conta de uma clínica

- Mensalidade: R$ 2.500
- Seu custo (caminho A, seção 11): cerca de R$ 350
- Sobra: cerca de R$ 2.150 por mês (86%), antes de impostos
- Com 10 clínicas: cerca de R$ 21 mil por mês, mais as implantações

---

## 4. De onde veio a ideia e por que seguir sem a mentoria

- A ideia veio dos vídeos do **Kelvin Cleto (Acelera 360)**, que ensina a vender "AI OS" e atendentes de IA para empresas, no modelo diagnóstico, implantação e mensalidade, replicando por nicho.
- O site de exemplo que você trouxe (genesisclinicas.com.br) é de uma parceira citada por ele. Na pesquisa de concorrentes, essa empresa apareceu com 7 meses de vida, preços de R$ 297 e R$ 497, pouca presença e nenhuma prova. Esse é o resultado típico do caminho "software barato para dentista".
- Pelos números que ele mesmo mostrou, só cerca de **12% dos membros do primeiro ano emitiram nota fiscal**, ou seja, venderam de fato.
- **Decisão (04/10/2026):** montar o negócio sem a mentoria, com o Claude Code como programador.

---

## 5. Mercado e escolha do nicho

### 5.1 Odontologia de alto valor (o nicho escolhido)

**Números:**
- Cerca de 460 mil dentistas ativos no CFO (agosto de 2026, dado citado por terceiros) e cerca de R$ 38 bilhões por ano em odontologia no Brasil.
- O Brasil está entre os maiores mercados de estética do mundo.

**O que essas clínicas vendem (preços de referência de 2026):**

| Serviço | Preço típico | Onde o atendente ajuda |
|---|---|---|
| Lentes de contato dental | R$ 1.200 a 2.500 por dente nas capitais; R$ 2.500 a 4.500 no premium; caso inteiro de R$ 10 mil a 40 mil | Decisão demorada, objeção de preço, acompanhamento do orçamento |
| Facetas de resina | R$ 200 a 2.000 por dente | Porta de entrada, retorno de manutenção |
| Alinhadores invisíveis | R$ 4.000 a 20.000 ou mais | Avaliação com escaneamento, acompanhamento das trocas |
| Clareamento | R$ 600 a 2.000 | Entrada para lentes, manutenção anual |
| Implantes | R$ 3.000 a 8.000 por dente em casos simples | Público mais velho, decisão com a família, financiamento |
| Protocolo (arcada inteira) | Dezenas de milhares de reais | Mesma lógica do implante |
| Harmonização orofacial | Toxina R$ 20 a 40 por unidade; preenchimento a partir de R$ 1.800/ml | Só como extra (em disputa na Justiça, seção 6) |

**Como a clínica vende e onde perde dinheiro:**

1. Anúncio no Instagram com antes e depois.
2. Paciente pergunta preço no WhatsApp. Resposta manual costuma levar de 30 a 90 minutos.
3. Avaliação, muitas vezes grátis. Falta na avaliação é o maior vazamento.
4. Orçamento de R$ 5 mil a 40 mil. Sem acompanhamento, morre em uma semana.
5. Fechamento com parcelamento de 10 a 18 vezes.
6. Tratamento em várias sessões, com confirmação a cada uma.
7. Pós: pedido de avaliação no Google, que quase ninguém faz.
8. Retorno e manutenção: dinheiro esquecido na base.

### 5.2 Por que alto padrão e não popular

| | Popular | **Alto padrão (o alvo)** | Luxo de verdade |
|---|---|---|---|
| Quem é | Redes e franquias, preço baixo, volume | Clínica independente, dono com marca pessoal, preço acima da média | Poucos nomes por capital, pacientes famosos |
| Como chega o paciente | Anúncio de preço | Instagram, anúncio com antes e depois, indicação | Quase só indicação |
| Atendimento | Central de atendimento própria | Secretária sobrecarregada | Recepcionista exclusiva |
| Para você | O robô de R$ 180 ganha aqui | Paga R$ 2.000 a 3.500 se você provar retorno | Difícil de vender, não quer automação aparente |

Por que o alto padrão favorece você:
1. O robô barato é o produto errado para esse público. Pesquisa da BCG com a Altagamma: o consumidor de luxo aceita IA no pós-venda, mas resiste a ela no atendimento consultivo. Capgemini (2026): 74% valorizam falar com uma pessoa no suporte.
2. Um caso de lentes recuperado paga meses do seu serviço.
3. Nesse público, o tom da conversa é a marca da clínica, e escrever bem é o seu terreno.

### 5.3 Vale nichar só em "odontologia estética"?

**Sim, mas defina o nicho pelo problema, não pelo procedimento.** O nicho é "clínica odontológica que vende tratamento caro e perde orçamento".

- O sorriso estético fica na vitrine: anúncio, mensagens, case.
- Implante e protocolo entram também, porque são o mesmo problema com o mesmo processo.
- Nenhum dos 9 concorrentes fala com esse dono desse jeito.
- Tamanho não é problema: com 10 a 20 clínicas você tem um negócio de R$ 15 mil a 40 mil por mês.
- Cada case vende o próximo: dono de clínica conversa com outros donos.
- Não recuse uma boa clínica de implantes por não ser "estética".
- Harmonização entra como extra, nunca como base.

### 5.4 Comparação dos 3 nichos estudados (notas de 1 a 5, leitura qualitativa)

| Critério | Odontologia de alto valor | Estética | Energia solar |
|---|---|---|---|
| Quanto vale cada venda | 5 | 3 | 5 |
| Dinheiro esquecido na base | 4 | 5 | 1 |
| Dor que o atendente resolve | 5 | 4 | 5 |
| Dinheiro do cliente para pagar | 4 | 3 | 2 |
| Espaço livre na concorrência | 4 | 2 | 2 |
| Segurança de regras | 4 | 2 | 5 |
| Saúde do mercado | 4 | 5 | 2 |
| Encaixe com você | 4 | 5 | 2 |
| Facilidade técnica | 4 | 4 | 3 |
| **Total (de 45)** | **38** | **33** | **27** |

**Ordem decidida:**
1. **Agora:** odontologia de alto valor.
2. **Depois de 3 cases:** estética, só clínica tocada por médico (dermatologista, cirurgião plástico) ou por dentista que já é cliente e faz harmonização. Evitar clínica só de biomédico e esteticista de venda baixa.
3. **Não agora:** energia solar. Reavaliar se o mercado voltar a crescer ou se aparecer uma integradora parceira de porte.

**Estética, em resumo:** mercado crescendo (franquias do setor com R$ 70 a 74 bilhões em 2025 e +18% no 1º trimestre de 2026), retorno natural (toxina a cada 4 a 6 meses), público que vive no Instagram. Mas: concorrência lotada e barata (IA a R$ 1,99 por atendimento), 26 anúncios ativos de "secretária de IA para estética", cursos ensinando a montar "agência de IA" para esse público e insegurança jurídica sobre quem pode aplicar injetáveis.

**Energia solar, em resumo:** sistema residencial de R$ 12 mil a 25 mil e dor clara ("quem responde primeiro vende primeiro"). Mas: instalação em queda pelo segundo ano (ABSOLAR projeta −7% em 2026), demanda por painéis −48% no 1º semestre de 2026, 68% das integradoras com até 4 pessoas, só 10% das abertas antes de 2016 seguem ativas, Fio B a 60% em 2026 subindo até 90% em 2028, e plataformas fortes (SolarZ com 7 mil integradores) e baratas (IA com CRM a partir de R$ 79).

---

## 6. Regras que mudam o jogo

### 6.1 Meta e WhatsApp

- **Desde 01/10/2026** a Meta cobra também as respostas enviadas dentro da janela de 24 horas na API oficial, cerca de R$ 0,04 a 0,08 por mensagem.
- **Continua grátis:** a janela de 72 horas aberta por anúncio que leva direto ao WhatsApp, e as respostas enviadas pelo aplicativo.
- **Mesmo número no aplicativo e na API (coexistência):** só por um parceiro autorizado da Meta. Referência: 360dialog, a partir de € 49 por mês por número.
- **Chatbot de uso geral** (tipo ChatGPT no WhatsApp) foi proibido pela Meta em 2026; atendente de uma empresa específica continua permitido.
- **Agente de IA da própria Meta (Business AI):** chegou ao WhatsApp Business no Brasil em 24/02/2026, grátis por enquanto, com cobrança prevista pelo plano Meta One (referência de R$ 199 a 1.999 por mês). Responde dúvidas e indica itens do catálogo. **Responder dúvida frequente virou grátis.** O seu valor está em agenda, acompanhamento, recuperação e relatório.
- **Bloqueios de número:** a Meta apertou a fiscalização de ferramentas não oficiais a partir de 15/01/2026. Banimento é sem aviso e sem volta.

### 6.2 Conselhos profissionais e Justiça

- **Harmonização por dentistas:** em 20/08/2026 o TRF1 anulou a Resolução CFO 198/2019, que criava a harmonização orofacial como especialidade. Ainda não vale até a publicação do acórdão; o CFO recorre e orienta os dentistas a continuarem. O CFO publicou novas resoluções em 2026 (área anatômica do dentista e cirurgia estética orofacial) contestadas pelo CFM.
- **Biomédicos:** a Justiça mantém a proibição de procedimentos estéticos invasivos (toxina, preenchimento). Clínica só de biomédico é cliente de risco.
- **Farmacêuticos e enfermeiros:** disputa com o CFM, com decisões em sentidos diferentes.
- **Publicidade:** médicos podem divulgar preço (CFM 2.336/23). Para dentistas valem as regras do CFO: **o atendente só informa preço autorizado por escrito pela clínica.**

### 6.3 LGPD e dado de saúde

- Dado de saúde é sensível. Contrato com a clínica como operadora de dados.
- Guardar o mínimo, nada de prontuário no atendente, apagar histórico antigo.
- A mensagem passa pela Z-API (Brasil), pelo Make (servidores na Europa) e pela Anthropic (Estados Unidos). Isso precisa constar no contrato.
- **Nunca salvar dado de paciente na pasta do projeto.** Só dados de teste.

---

## 7. Concorrentes

### 7.1 Odontologia (mapa de 11/10/2026)

| Empresa | Desde | Preço | O que tirar daqui |
|---|---|---|---|
| Cloudia | 2016 | Sob consulta; implantação a partir de R$ 700 | Líder, fala com toda a saúde, esconde preço, tem queixas de implantação. Tem programa de agências parceiras |
| Simples Dental (Secretária IA) | ~2015 | Cerca de R$ 180/mês, à parte do sistema | Robô barato dentro de um sistema usado por 19 mil clínicas. Você não ganha em preço; ganha em processo. A clínica pode usar a IA dele e contratar você |
| Odonto Results | 2020 | A partir de R$ 790/mês + marketing | O modelo mais parecido com o seu: IA + central humana + anúncios. "Só comemoramos no comparecimento" |
| Secretária IA | nov/2024 | A partir de R$ 397,90 | Usa "diagnóstico grátis do WhatsApp" como isca e o argumento de custo contra secretária CLT |
| Gênesis | mar/2026 | R$ 297 e R$ 497 | Pouca presença e nenhuma prova |
| Secretária Odonto | abr/2026 | R$ 297, 497 e 997 | Site com números de exemplo no lugar de resultados |
| AtendeJá | abr/2026 | R$ 447 e R$ 897; implantação R$ 497 | **A oferta mais bem desenhada:** garantia de 30 e 60 dias, preço de fundador, painel de receita resgatada. Copiar a estrutura |
| Beeia | empresa de 2000 | R$ 258,90 a 589,90 | Fluxos separados por especialidade (alinhador, implante, estética) |
| PRI e Agendaai | 2026 | Não divulgam | Pouca informação |

**O que ninguém faz:** foco no sorriso estético e no orçamento alto; mensagens escritas por quem entende de venda; transparência (metade esconde preço, CNPJ ou dono); prova com número real.

**Caminho alternativo:** revender a IA da Cloudia pelo programa de agências e cobrar só pelo processo. Encurta a montagem técnica, mas reduz margem e cria dependência de um fornecedor com queixas de suporte.

Donos, CNPJs, Instagram e fontes de cada um estão no mapa publicado (seção 23).

### 7.2 Estética (11/10/2026)

Cloudia, Chat Inteligente (diz "2 mil clínicas"), SOS Estética (loja de equipamentos que revende IA), Esthetic Manager, BeautyBot (R$ 23,92 por usuário/mês no anual + R$ 1,99 por atendimento), Atendente.AI e HOF advisor ("tráfego + secretária de IA por R$ 1.500", com vários anúncios ativos).

### 7.3 Energia solar (11/10/2026)

SolarZ (+7 mil integradores, investidores, eventos), SolarMarket (desde 2019), CRM Solar Simples (R$ 79 a 499 com IA), EnergiaBot, Parli (R$ 97 e R$ 1.497), Verboo e Prospectar (genérico).

---

## 8. O diferencial: atendimento de alto padrão

**A ideia central: a IA trabalha nos bastidores; o paciente sente que fala com gente.**

1. **Modo copiloto.** No horário da clínica, a IA não fala com o paciente: escreve a resposta, a secretária confere e envia com um clique, e a IA lembra quem precisa de retorno. A IA responde sozinha só fora do horário (segundo uma agência do setor, 52% dos contatos qualificados chegam fora do horário comercial) e nas confirmações e lembretes.
2. **Manual de voz de cada clínica.** Palavras que usa, palavras proibidas ("promoção", "barato"), sem preço na primeira mensagem, objetivo de cada conversa: convidar para a avaliação ou para a simulação do sorriso. É a parte que ninguém copia.
3. **Acompanhamento do orçamento alto.** Depois da avaliação: no dia seguinte, resumo do plano com o nome do paciente; dias depois, um caso parecido (com autorização do paciente do caso); depois, um vídeo curto do dentista (gravado uma vez por tipo de tratamento); por fim, as condições de pagamento. Se o paciente citou uma data importante (casamento, formatura), o acompanhamento usa essa data.
4. **O mesmo número da clínica.** Clínica de alto padrão não troca de número. Isso exige coexistência por um parceiro autorizado da Meta (custo extra, repassado no preço).
5. **Relatório para o dono.** Todo mês: orçamentos recuperados em reais, tempo de resposta, faltas evitadas.
6. **Treino da secretária.** Um roteiro simples para ela conduzir a conversa de venda.

**Cuidados nesse público:** o dono é exigente e a venda demora de 2 a 6 semanas; erro de tom custa caro (por isso começar sempre no copiloto); ele vai comparar você com contratar uma secretária (de R$ 2,4 mil a 4,5 mil por mês com encargos, pelas contas dos próprios fornecedores). Você entrega mais: 24 horas, processo e relatório.

---

## 9. O produto: o que inclui e o que não inclui

**Inclui:**
- Atendimento no WhatsApp em segundos, com texto e áudio (transcrição).
- Agendamento da avaliação no Google Agenda da clínica.
- Confirmação na véspera e remarcação.
- Acompanhamento do orçamento em 1, 3, 7, 15 e 30 dias, só para quem já conversou com a clínica.
- Reativação da base parada e pedido de avaliação no Google.
- Modo copiloto no horário da clínica.
- Passagem para uma pessoa em caso delicado.
- Relatório semanal e mensal para o dono.
- Revisão semanal das conversas e ajuste de texto.
- Manual de voz e base de conhecimento da clínica.
- Treino da secretária.

**Não inclui:**
- Orientação clínica, diagnóstico ou indicação de tratamento.
- Preço que a clínica não autorizou por escrito.
- Disparo em massa para listas frias.
- Gestão de tráfego pago (pode virar serviço extra no futuro).
- Prontuário ou guarda de dados clínicos.
- Atendimento humano terceirizado (a pessoa que assume é da clínica).

---

## 10. Como o produto funciona por dentro

### 10.1 Caminho de uma mensagem

Paciente → WhatsApp (número da clínica ou do atendimento) → Z-API (avisa o Make na hora e envia a resposta) → **Make** (lê a regra da clínica, o histórico e a agenda) → Claude (escreve a resposta no tom da clínica) → saída:

- **Fora do horário:** responde sozinho, agenda a avaliação, registra o contato na planilha.
- **No horário (copiloto):** manda o rascunho para a secretária no grupo interno da equipe; ela confere e envia.
- **Caso delicado** (dor, reclamação, pergunta clínica, paciente pedindo pessoa): avisa a equipe e não responde sozinho.

### 10.2 Os 6 cenários do Make

| Cenário | Quando roda | O que faz |
|---|---|---|
| 1. Atendimento | A cada mensagem | Ignora grupos e mensagens da equipe, transcreve áudio, busca histórico, pede a resposta ao Claude e decide entre responder, mandar rascunho ou chamar uma pessoa |
| 2. Agenda | Quando o paciente aceita horário | Consulta horários livres e marca no Google Agenda |
| 3. Confirmações | Todo fim de tarde | Confirma as avaliações do dia seguinte e remarca quem não pode |
| 4. Acompanhamento do orçamento | Toda manhã | Procura orçamentos em aberto na planilha e manda a mensagem do dia certo |
| 5. Relatório | Toda semana e todo mês | Conta contatos, avaliações, faltas evitadas e orçamentos recuperados em reais |
| 6. Alarme | Quando algo falha | Avisa você no WhatsApp |

**Primeira versão sem servidor:** histórico no Make, contatos e orçamentos numa planilha do Google, agenda no Google Agenda. O painel de atendimento (Chatwoot) entra quando houver 3 clínicas ou quando uma pedir.

### 10.3 Os 3 caminhos do número

| Caminho | Como fica para a clínica | Custo extra/mês | Risco | Quando usar |
|---|---|---|---|---|
| A. Z-API no número | Mesmo número, aplicativo continua no celular | R$ 99,99 | **Bloqueio sem aviso** | Seu número de demonstração. Na clínica, só com aceite do risco por escrito e só para responder quem escreveu |
| B. API oficial, número novo | Número só para o atendimento; o antigo segue igual | R$ 0 + mensagens da Meta | Baixo | Padrão para quem topa divulgar número novo |
| C. API oficial no mesmo número | Mesmo número com o aplicativo, via parceiro autorizado | Cerca de R$ 300 + mensagens | Baixo | Clínica que não abre mão do número de sempre |

**Recomendação:** Z-API para aprender e demonstrar; API oficial (B ou C) para a clínica. O resto do Make é igual nos três; trocar a peça leva poucas horas.

### 10.4 Pilha alternativa (para quando escalar)

O guia técnico original usa n8n (no lugar do Make) + API oficial do WhatsApp + Chatwoot + Claude + transcrição + Google Agenda + Postgres + Metabase, num servidor próprio (VPS de 2 vCPU e 8 GB, cerca de R$ 33 a 80 por mês) com Coolify ou Easypanel. Custo fixo menor em volume, mas exige servidor. A licença do n8n permite rodar fluxos de clientes no seu servidor desde que a clínica nunca acesse o n8n.

### 10.5 Modelos de IA

- Modelo rápido e barato (Haiku) para a maioria das respostas; modelo maior (Sonnet) só em caso difícil e nos resumos.
- Transcrição de áudio custa centavos por minuto.
- Limite mensal de gasto ligado no console da Anthropic.

---

## 11. Quanto custa

Valores de outubro de 2026, com dólar a cerca de R$ 5,60 e euro a cerca de R$ 6,20.

### 11.1 Antes do primeiro cliente (por mês)

| Item | Para quê | Custo |
|---|---|---|
| Make Core | Rodar os 6 cenários. Seu plano grátis atual aceita só 2 cenários e 1.000 créditos | US$ 10,59 (~R$ 60) |
| Z-API (1 instância) | Número de demonstração. Teste grátis de 2 dias | R$ 99,99 (anual: R$ 1.079,89) |
| Claude API | Testes, com limite de gasto | ~R$ 30 a 60 |
| Chip de demonstração | Uma vez | ~R$ 20 (ou R$ 30/mês no Vivo Lite) |
| Domínio | Site e e-mail profissional, por ano | ~R$ 40/ano |
| Empresa e contador | Quando o primeiro cliente estiver perto de fechar | ~R$ 100 a 300 |
| **Total** | Sem empresa / com empresa | **~R$ 200 / ~R$ 550** |

A assinatura do Claude que você já usa fica fora da conta.

### 11.2 Por clínica (por mês, caminho A)

| Item | Cálculo | Custo |
|---|---|---|
| Z-API | 1 instância por clínica (R$ 89,99 a partir de 10) | R$ 99,99 |
| Créditos do Make | ~2.000 mensagens × ~9 créditos + ~2.000 das rotinas = ~20 mil créditos | ~R$ 110 a 170 |
| Claude API | ~2.000 respostas + casos difíceis e resumos | ~R$ 60 a 110 |
| Transcrição | ~300 áudios curtos | ~R$ 5 |
| **Total** | | **~R$ 280 a 390** |

- **Caminho B:** sem a Z-API, ~R$ 180 a 290 (mensagens da Meta no cartão da clínica).
- **Caminho C:** com o parceiro autorizado, ~R$ 480 a 590 + mensagens da Meta.
- **Chatwoot** (fase de escala): grátis no seu servidor (~R$ 40 a 80 por mês para todas as clínicas) ou US$ 19 por atendente na nuvem.

---

## 12. Passo a passo da criação do produto

Legenda: **[Você]** só você pode fazer · **[Claude]** eu faço · **[Juntas]** eu preparo, você decide ou executa comigo.

### Piloto: as 6 etapas da clínica de demonstração

O piloto é montar uma **clínica de demonstração**: um número em que você manda mensagem como paciente e a IA responde no tom de uma clínica de alto padrão. Sempre apresentada como demonstração, nunca como cliente real.

| Etapa | Quem | Tempo |
|---|---|---|
| 1. Chave do Claude no Make | Você | ~15 min |
| 2. Número de demonstração | Você | depende do chip |
| 3. Base da clínica e manual de voz | Eu escrevo, você aprova | 1 sessão |
| 4. Cenário de atendimento no Make | Eu | 1 sessão |
| 5. Conectar o número na Z-API | Você, com a minha orientação | ~15 min |
| 6. Testar como paciente | Você | quanto quiser |

**Custo do piloto:** Make grátis; créditos do Claude a partir de cerca de US$ 5; número (chip ou Vivo Lite); Z-API grátis por 2 dias e R$ 99,99 por mês se continuar.

**Etapa 1, a chave do Claude:**
1. Acesse console.anthropic.com e crie a conta (separada da assinatura do Claude).
2. Em Settings → Billing, compre o mínimo de créditos.
3. Em Settings → Limits, coloque um limite mensal (por exemplo, US$ 10).
4. Em Settings → API Keys, crie a chave `atendente-demo` e copie (aparece uma vez).
5. Cole a chave na solicitação "Piloto do atendente: chave do Claude" do Make: https://eu1.make.com/3084523/credentials-requests/inbox?requestId=3396ab98-955f-4723-b6fb-b1b077a6adfc
6. Nunca mande a chave no chat.

### Fase 0: contas e chaves (semana 1)

1. [Você] Conseguir o número de demonstração e ativar o WhatsApp Business nele (seção 16).
2. [Você] Criar a instância na Z-API e ler o QR code com o celular desse número (só quando a etapa 4 estiver pronta).
3. [Você] Criar a chave do Claude com limite de gasto.
4. [Juntas] Guardar chaves locais no `.env` (o comando `/configurar-zapi` salva as da Z-API sem mostrar na tela; o `.env.example` já tem `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN` e `ZAPI_CLIENT_TOKEN`).
5. [Você] Passar o Make para o plano Core quando chegarmos ao terceiro cenário.
6. [Claude] Criar no Make a pasta do projeto, o armazenamento do histórico e a planilha de contatos e orçamentos.

### Fase 1: atendente de demonstração (semanas 2 e 3)

1. [Claude] Escrever a base da clínica de demonstração (modelo na seção 13.1).
2. [Juntas] Escrever o manual de voz do alto padrão (seção 13.2).
3. [Claude] Montar os cenários 1 (Atendimento) e 2 (Agenda) e testar com conversas simuladas.
4. [Você] Fazer o papel de paciente com o roteiro de 30 situações (seção 13.6).
5. [Claude] Ler os registros de execução no Make, corrigir e ajustar o texto.
6. [Claude] Montar os cenários 3 a 6.
7. [Juntas] Escrever e aprovar as mensagens de acompanhamento do orçamento (seção 13.5).
8. [Você] Aprovar a demonstração final: um dono manda mensagem e vê a resposta em segundos.

### Fase 2: vender a distância (semanas 3 a 6, em paralelo)

Detalhada na seção 14.

### Fase 3: primeira clínica (4 a 5 semanas)

1. [Juntas] Chamada de levantamento gravada com dono e secretária (questionário na seção 15.4).
2. [Você] Acompanhar por tela compartilhada o dono conectando o número (QR code na Z-API ou verificação na Meta). A clínica te dá acesso de administradora; você nunca recebe a senha dela.
3. [Claude] Copiar os cenários para a clínica, ligar na agenda dela, carregar base e manual de voz.
4. [Você] Treinar a secretária por vídeo (30 minutos) e deixar vídeos curtos gravados.
5. [Juntas] Duas semanas em modo copiloto, revisando os rascunhos todo dia.
6. [Você] Liberar a resposta automática fora do horário, com aprovação do dono.
7. [Claude] Montar o relatório de 30 dias com reais recuperados.

### Fase 4: escalar até 10 a 20 clínicas (mês 4 em diante)

1. [Claude] Juntar todas as clínicas num conjunto único de cenários que lê a configuração de cada uma (corrigiu uma vez, vale para todas).
2. [Claude] Instalar o Chatwoot num servidor quando houver 3 clínicas ou uma pedir.
3. [Claude] Trocar a Z-API pela API oficial nas clínicas dos caminhos B ou C.
4. [Você] Transformar os 3 primeiros resultados em cases (com autorização) e subir o preço.

---

## 13. Modelos prontos para montar o produto

Estes modelos são propostas de estrutura. O conteúdo de cada clínica sai do levantamento e é aprovado por escrito.

### 13.1 Base da clínica (o que a IA precisa saber)

- Nome, endereço, como chegar, estacionamento, horários.
- Profissionais (nome, especialidade, CRO), quem atende o quê.
- Tratamentos oferecidos, como funciona cada um, tempo de tratamento, número de sessões.
- **Política de preço:** quais preços podem ser ditos, em que momento, e frases para quando não se fala preço.
- Avaliação: se é paga ou grátis, duração, o que acontece nela (escaneamento, simulação do sorriso).
- Formas de pagamento e parcelamento.
- Diferenciais reais da clínica (equipamentos, laboratório, garantias), sem exagero.
- Perguntas frequentes com respostas aprovadas.
- O que a IA nunca responde (seção 13.3).
- Contatos internos para passar a conversa (quem, em que horário).

### 13.2 Manual de voz (estrutura)

1. **Tom:** acolhedor, seguro, sem pressa, frases curtas, sem gírias, sem excesso de emoji.
2. **Tratamento:** como chama o paciente (nome, "você"), como assina (nome da clínica ou da secretária).
3. **Palavras que usa:** planejamento, avaliação, sorriso, resultado natural, acompanhamento.
4. **Palavras proibidas:** promoção, barato, desconto (salvo campanha aprovada), garantia de resultado, termos técnicos sem explicação.
5. **Primeira mensagem:** acolher, entender o que a pessoa quer, sem preço de cara.
6. **Objetivo de cada conversa:** levar à avaliação ou à simulação do sorriso.
7. **Como lidar com "quanto custa":** explicar que depende do planejamento, oferecer a avaliação, informar faixa só se a clínica autorizou.
8. **Como lidar com "vou pensar":** respeitar, combinar quando retomar, registrar na planilha.
9. **Tamanho das mensagens:** no máximo 3 frases por mensagem.
10. **Exemplos aprovados:** 10 a 20 respostas modelo escritas e aprovadas pela clínica.

### 13.3 Regras que a IA nunca quebra

- Não dá orientação clínica, diagnóstico, prescrição ou opinião sobre caso.
- Não informa preço que não esteja autorizado por escrito.
- Não promete resultado.
- Não fala de outros pacientes sem autorização registrada.
- Não insiste depois de um "não" claro.
- Avisa que é um atendimento automático quando perguntada.
- Não pede nem guarda dados de saúde além do necessário para agendar.

### 13.4 Quando chamar uma pessoa

- Dor, sangramento, inchaço, urgência.
- Reclamação ou insatisfação.
- Pergunta clínica ou sobre caso específico.
- Paciente pedindo para falar com alguém.
- Negociação de preço fora da política.
- Qualquer dúvida fora da base.

### 13.5 Jornada do orçamento alto (estrutura das mensagens)

| Quando | Objetivo da mensagem |
|---|---|
| Dia 1 | Agradecer a avaliação e resumir o plano com o nome do paciente |
| Dia 3 | Responder dúvida comum daquele tratamento e oferecer conversa com a equipe |
| Dia 7 | Mostrar um caso parecido (com autorização) ou o vídeo curto do dentista |
| Dia 15 | Apresentar as condições de pagamento e o próximo passo |
| Dia 30 | Retomar com leveza e perguntar se faz sentido manter o planejamento em aberto |

As mensagens são escritas para cada clínica e aprovadas antes de ativar. Só vão para quem já conversou com a clínica. Se a pessoa pedir para parar, o acompanhamento para na hora.

### 13.6 Roteiro de testes (30 situações)

Agrupadas em 6 blocos de 5:
1. **Entrada:** pergunta de preço, pergunta genérica, áudio, foto do sorriso, mensagem fora do horário.
2. **Agenda:** aceita horário, pede outro dia, remarca, cancela, não responde à confirmação.
3. **Objeções:** "está caro", "vou pensar", "vi mais barato", "tenho medo", "preciso falar com meu marido".
4. **Casos delicados:** dor, reclamação, pergunta clínica, pede pessoa, mensagem agressiva.
5. **Orçamento:** sumiu depois da avaliação, volta depois de 10 dias, pede parcelamento, pede desconto, fecha.
6. **Limites:** pergunta fora do assunto, tenta fazer a IA falar de outro tema, manda mensagem em outra língua, manda várias mensagens seguidas, pede para parar de receber mensagens.

### 13.7 Relatório mensal para o dono

- Contatos recebidos (dentro e fora do horário).
- Tempo médio de primeira resposta.
- Avaliações marcadas e comparecimento.
- Faltas evitadas pelas confirmações.
- Orçamentos em aberto, acompanhados e fechados.
- **Reais recuperados:** valor dos orçamentos fechados depois do acompanhamento.
- Conversas passadas para a equipe e motivos.
- Ajustes feitos no mês e próximos ajustes.

---

## 14. Passo a passo do negócio (vender e operar a distância)

### 14.1 Validar (semanas 1 a 4)

1. Fazer cliente oculto em 20 a 30 clínicas de alto padrão.
2. Conversar com 15 a 20 donos (diagnóstico grátis).
3. Confirmar o nicho e o preço com o que ouvir.
4. Abrir a empresa quando o primeiro cliente estiver perto de fechar.

### 14.2 Achar clínicas

- Biblioteca de Anúncios da Meta: quem anuncia lentes, alinhadores e implantes agora.
- Instagram do dentista e da clínica.
- Google Maps: nota e número de avaliações.
- Lista montada automaticamente com o Apify (já configurado no projeto).
- Comece por capitais e cidades médias ricas. Remoto, você atende o Brasil inteiro.

### 14.3 Abrir a porta: o Diagnóstico do atendimento

1. Você manda mensagem para a clínica como paciente e anota: quanto demorou, o que respondeu, se pediu dados, se ofereceu avaliação, se voltou a falar com você.
2. Eu transformo isso numa página com prints, tempos e o que a clínica deixou escapar.
3. Você envia ao dono pelo Instagram, WhatsApp ou e-mail, com convite para 30 minutos por vídeo.

### 14.4 Reunião de 30 minutos por vídeo

1. Mostrar o diagnóstico (5 min).
2. Perguntar números da clínica: contatos por mês, ticket médio, orçamentos em aberto (10 min).
3. Calcular o prejuízo junto (seção 15.3).
4. Demonstração ao vivo: o dono manda mensagem para o número de demonstração (5 min).
5. Proposta: implantação, mensalidade, garantia, preço de fundador (10 min).

### 14.5 Fechar

- Proposta em página (eu preparo).
- Contrato-base revisado por um advogado uma vez, com anexo de proteção de dados.
- Assinatura eletrônica (gov.br, Autentique, Clicksign ou D4Sign).
- Cobrança recorrente por Pix, boleto ou cartão (Asaas ou similar).

### 14.6 Implantar e operar

Fase 3 da seção 12, depois rotina da seção 19.

### 14.7 Reter e crescer

- Relatório mensal com reais recuperados.
- Conversa mensal de 30 minutos com o dono.
- Pedir indicação depois do primeiro relatório bom.
- Transformar resultados em cases com autorização.
- Subir o preço para novos clientes depois de 3 cases.
- Use o seu próprio atendente como vitrine no seu WhatsApp comercial.

---

## 15. Modelos prontos para vender

### 15.1 Roteiro de cliente oculto

- Mande mensagem como paciente interessado num tratamento caro (lentes, alinhador ou implante), em horários variados (manhã, noite, fim de semana).
- Anote numa planilha: data e hora do envio, hora da primeira resposta, quem respondeu, se falou preço, se ofereceu avaliação, se pediu nome, se voltou a procurar você em 1, 3 e 7 dias.
- Não marque avaliação que não vai cumprir. Se for convidada a marcar, agradeça e diga que vai ver a agenda.

### 15.2 Perguntas para a reunião com o dono

1. Quantos contatos chegam por mês pelo WhatsApp?
2. Quem responde, e em quanto tempo?
3. Quantas avaliações vocês fazem por mês e quantas pessoas faltam?
4. Qual o valor médio de um orçamento de lentes, alinhador ou implante?
5. Quantos orçamentos ficam em aberto todo mês?
6. Alguém acompanha esses orçamentos? Como?
7. Quanto vocês investem em anúncio por mês?
8. O que já tentaram para resolver isso?

### 15.3 Calculadora de prejuízo (exemplo ilustrativo; troque pelos números da clínica)

- **Contatos perdidos:** contatos por mês × % que não recebe resposta rápida × % que viraria tratamento × valor médio.
  Exemplo: 100 × 40% × 5% × R$ 15.000 = **R$ 30.000 por mês**.
- **Orçamentos que esfriam:** orçamentos em aberto por mês × % que fecharia com acompanhamento × valor médio.
  Exemplo: 20 × 10% × R$ 15.000 = **R$ 30.000 por mês**.
- Compare com a mensalidade. Se um único caso recuperado paga vários meses, a venda fica simples.

### 15.4 Questionário de levantamento (implantação)

Dados da clínica, profissionais e agendas, tratamentos e políticas de preço, horários e quem atende, perguntas mais comuns, objeções mais comuns, casos que precisam de pessoa, tom da clínica (exemplos de mensagens que o dono gosta e não gosta), metas do contrato, acessos (Google Agenda, conta da Meta), autorizações (casos, fotos, vídeos do dentista).

### 15.5 Cláusulas que o contrato precisa ter

Escopo (o que inclui e não inclui), prazo de implantação, mensalidade e reajuste, garantia de 30 dias e meta de 60 dias, quem paga as mensagens da Meta, responsabilidade pelas informações da base (aprovadas pela clínica), proteção de dados (você como operadora), aceite de risco se o caminho A for usado no número da clínica, propriedade dos dados (da clínica), cancelamento e devolução de acessos.

---

## 16. O número de WhatsApp: Israel, Brasil e eSIM

### 16.1 Como funciona a ativação

- O WhatsApp só precisa receber **um código, uma vez**, por SMS ou ligação. Depois funciona no seu celular em Israel pelo Wi-Fi ou pelos dados, e o chip não precisa ficar no aparelho.
- Você pode ter o WhatsApp pessoal e o WhatsApp Business da demonstração no mesmo celular.
- A linha precisa continuar ativa, e o WhatsApp pode pedir o código de novo se você trocar de celular. Ligue a verificação em duas etapas.
- **Nunca use o seu número pessoal com a Z-API.**
- Mais adiante, tenha também um número brasileiro separado para o seu atendimento comercial, diferente do de demonstração.

### 16.2 Caminhos para um número brasileiro

1. **Chip comprado por alguém de confiança no Brasil**, no seu CPF, que te passa o código. Barato e garantido; depende da pessoa.
2. **Chip enviado para Israel** pelo correio. Mais independente; demora.
3. **eSIM contratado online** (o caminho em teste, abaixo).
4. **Número fixo virtual brasileiro.** Não recomendado agora: verificação incerta e mais risco com a Z-API.

**Alternativa imediata:** para o piloto, qualquer segundo número serve, inclusive de Israel. Quando o brasileiro chegar, basta ler um QR code novo na Z-API; o Make não muda.

### 16.3 Operadoras brasileiras com eSIM (11/10/2026)

| Operadora | eSIM | Pré-pago | Observação |
|---|---|---|---|
| Vivo | Sim | Vivo Lite (plano digital) | **O melhor caminho encontrado** |
| Claro | Sim | Claro Flex, parcial | App Minha Claro; pré só com CPF já cadastrado |
| TIM | Sim, em parte | TIM Pré só em loja | |
| Algar | Sim | Não | Só alguns DDDs do interior |
| Surf Telecom | Não para pessoas | Não | O site oficial é só para empresas (operadora de bastidor) |
| Veek | Não confirmado | Sim | O site fala em chip físico e exige check-in diário |
| Oi | Não | Não | Parou de vender planos de celular |

### 16.4 Vivo Lite (fonte: páginas oficiais da Vivo)

- Contratação online em vivo.com.br/vivo-lite. Planos de R$ 30 (30 GB) e R$ 40 (40 GB). **Escolha o mensal**: o anual não devolve dinheiro se cancelar.
- Pagamento só no cartão de crédito, sem fatura.
- Você escolhe **eSIM ativado na hora** e número novo. O link chega por e-mail; ativa no app da Vivo em "Quero ativar chip/eSIM" com código enviado ao e-mail. O QR Code vale 30 dias.
- Celular comprado no exterior funciona se seguir o padrão do eSIM e **não estiver bloqueado** por operadora estrangeira.
- Sem pagar a renovação por 60 dias, o número passa para o Vivo Pré (não se perde).
- **SMS no exterior:** receber é grátis ("Clientes Vivo recebem SMS de forma gratuita quando estão no exterior"; no Lite, R$ 0,05 para enviar e grátis para receber).
- **Exigência:** linha ativa e **saldo de Roaming Internacional**, comprado no app em Vivo Lite → Loja → Roaming Internacional → Comprar saldo (R$ 20, 40, 80, 100 ou 120). Habilitar roaming também no celular.
- Chamada recebida no exterior custa R$ 1,29 por minuto: **peça o código do WhatsApp por SMS**.
- Deixe os dados móveis na linha de Israel para o saldo não ser gasto com internet.
- Israel está na lista de países do pacote "Mundo" da Vivo Travel (para Pós). A tarifa de Israel no Lite deve ser conferida no app antes de pagar.

**Ainda sem resposta:** se o Vivo Lite pode ser contratado de fora do Brasil com o seu CPF e cartão; se o app da Vivo abre na loja de aplicativos de Israel; a validade do saldo de roaming.

**Passo a passo para você tentar:**
1. Wi-Fi, CPF, cartão e e-mail à mão; celular desbloqueado e com eSIM.
2. vivo.com.br/vivo-lite → plano mensal de R$ 30 → eSIM → número novo.
3. Anotar em cada tela o que o site pede (CPF, selfie, endereço, cartão).
4. Se o cartão não for aceito, parar e me contar.
5. Depois de pagar, instalar o eSIM pelo link, abrir o app e conferir a tarifa de Israel no roaming antes de comprar os R$ 20 de saldo.
6. Nunca mandar CPF, cartão ou códigos no chat.

---

## 17. Quem faz o quê

**Só você:**
- Criar contas, pagar e guardar senhas.
- Ler QR codes e receber códigos de ativação.
- Testar como paciente.
- Aprovar todo texto que vai para paciente.
- Conversar, vender e assinar com as clínicas.
- Enviar qualquer mensagem ou e-mail.
- Ser a pessoa de contato quando algo sai do roteiro.

**O Claude Code faz:**
- Montar, testar e corrigir os cenários no seu Make (com o Make conectado à sessão).
- Escrever base, manual de voz, regras e mensagens.
- Planilhas, relatórios e alarmes.
- Lista de clínicas e diagnósticos do atendimento.
- Rascunhos de proposta, contrato, e-mails e roteiros.
- Servidor, painel e troca para a API oficial, quando chegar a hora.
- Manter o contexto do projeto atualizado entre as sessões.

**O Claude Code não faz:**
- Criar contas, digitar senhas ou dados de pagamento.
- Enviar mensagem ou e-mail sem a sua aprovação.
- Ativar um cenário que fala com paciente sem o seu "pode ligar".
- Guardar chave fora do `.env`.
- Salvar dado de paciente na pasta do projeto.

---

## 18. Ferramentas de solopreneur

| Para quê | Ferramenta | Custo |
|---|---|---|
| Construir | Claude Code, Make, Z-API, Claude API | Seção 11 |
| Agenda e dados da clínica | Google Agenda e Planilhas | Grátis |
| Painel de atendimento (escala) | Chatwoot | Grátis no seu servidor ou US$ 19 por atendente |
| Achar clínicas | Apify, Biblioteca de Anúncios da Meta, Google Maps | Apify por uso |
| Reuniões | Google Meet + Cal.com ou Calendly | Grátis para começar |
| Notas de reunião | Granola | Conforme plano |
| Propostas e diagnósticos | Páginas publicadas pelo Claude, Gamma ou Lovable | Conforme plano |
| Contrato | gov.br, Autentique, Clicksign ou D4Sign | gov.br grátis |
| Cobrança recorrente | Asaas ou similar | Taxa por cobrança |
| Empresa | CNPJ no Simples + contabilidade online | ~R$ 100 a 300/mês (confirmar com o contador se cabe no MEI; provavelmente ME) |
| Senhas e acessos | Bitwarden ou 1Password | Bitwarden grátis |
| Treinar secretárias | Loom | Grátis para começar |
| Organizar clientes | Notion ou Google Drive | Grátis (sem dado de paciente) |
| Relatório visual | Looker Studio ou página publicada | Grátis |
| Seu atendimento | WhatsApp Business no seu número comercial | Grátis |

---

## 19. Rotina semanal (com clientes rodando)

| Quando | O quê | Tempo |
|---|---|---|
| Todo dia | Alarmes e conversas marcadas para pessoa | 15 min |
| Segunda | Prospecção: 5 clientes ocultos e 5 diagnósticos enviados | 2 h |
| Terça e quarta | Reuniões de venda e de implantação | 3 a 4 h |
| Quinta | Revisão das conversas de cada clínica, comigo | 20 a 30 min por clínica |
| Sexta | Relatórios, melhorias e conteúdo para o seu Instagram | 2 h |
| Uma vez por mês | Conversa com o dono de cada clínica | 30 min por clínica |

Com 10 clínicas: cerca de 10 a 15 horas por semana de operação.

---

## 20. Riscos e cuidados

| Risco | Como evitar |
|---|---|
| Bloqueio do número na Z-API | Só responder quem escreveu, nada de disparo em massa, número de demonstração separado; na clínica, caminho B ou C |
| Dado de saúde | Contrato de operadora, mínimo necessário, nada de prontuário, apagar histórico antigo |
| Créditos do Make estourando | Alarme de consumo e revisão mensal por clínica |
| Gasto do Claude | Limite mensal no console, modelo rápido na maioria das respostas |
| Erro de informação | Só preço autorizado, nada de orientação clínica, chamar pessoa na dúvida |
| Robô barato da concorrência | Vender processo, mensagens e resultado, não software |
| Agente grátis da Meta | Valor em agenda, acompanhamento, recuperação e relatório |
| Dono desconfiado | Garantia, piloto com meta no contrato, prova com número real |
| Dependência de você | Tudo documentado: base, manual de voz e checklist por clínica |
| Regras de conselhos | Harmonização só como extra; atenção a clínica só de biomédico |

---

## 21. Regras de segurança do projeto

- Chaves, tokens e senhas **só no `.env`** da raiz, nunca em arquivo, planilha ou chat. Na tela, sempre mascarados.
- Chaves usadas pelo Make ficam nas conexões do próprio Make.
- Antes de qualquer alteração em conta da Meta, confirmação no chat.
- Nenhum dado de paciente na pasta `negocio-ia-clinicas/`.
- A clínica de demonstração é sempre apresentada como demonstração. Nunca inventar cliente, número ou depoimento.
- Aprovação sua antes de criar contas, gastar dinheiro ou mexer em número de cliente.

---

## 22. Outros nichos e outros produtos de IA (para o futuro)

### 22.1 Nichos com a mesma lógica

- **Bons:** energia solar, imobiliárias, estética médica, infoprodutores (recuperação de Pix, boleto e cartão recusado, suporte ao aluno, pré-venda de produto caro; é o mercado que você conhece por dentro).
- **Com ressalva:** advocacia (OAB, Provimento 205/2021: só atender quem procurou, sem promessa de resultado, avisar que é IA), clínicas veterinárias (retorno de vacina, venda menor), escolas e academias.
- **Evitar no começo:** restaurantes, salões, barbearias, lojas de catálogo simples.
- **Filtro para qualquer nicho:** venda alta, cliente chega pelo WhatsApp, perde dinheiro com demora, dono com caixa e poder de decisão, pouca regra de conselho.

### 22.2 Outros produtos de IA em alta

| Produto | Encaixe com você |
|---|---|
| Criativos e vídeos com IA para anúncio (combina com anúncio que leva ao WhatsApp) | Alto |
| Assistente de IA treinado no conteúdo de um curso | Alto (teste no seu produto primeiro) |
| Aparecer nas respostas do ChatGPT e do Gemini (GEO) | Alto (ótima demonstração em reunião) |
| Treinamento de IA para equipes | Médio a alto |
| Agente de voz (atender e ligar) | Médio (módulo futuro) |
| Aplicativos sob medida feitos com IA | Médio (mercado lotado) |

Conselho: um produto principal e o resto como extra para o mesmo cliente.

---

## 23. Arquivos, páginas publicadas e fontes

### 23.1 Arquivos do projeto

| Arquivo | Conteúdo |
|---|---|
| `negocio-ia-clinicas/CLAUDE.md` | Contexto e decisões do projeto |
| `negocio-ia-clinicas/MATERIAL-COMPLETO.md` | Este material |
| `negocio-ia-clinicas/guia-tecnico-e-mercado.html` | Guia técnico original (n8n + API oficial) e mercado |
| `negocio-ia-clinicas/pesquisa/concorrentes-odonto.html` | Mapa de 9 concorrentes de odontologia |
| `negocio-ia-clinicas/pesquisa/comparacao-nichos.html` | Odontologia x estética x solar |
| `negocio-ia-clinicas/tecnico/plano-make-zapi.html` | Plano de montagem com Make e Z-API |
| `negocio-ia-clinicas/pesquisa/dados/` | Dados brutos das pesquisas |

### 23.2 Páginas publicadas (privadas, só você abre)

- Guia técnico e mercado: https://claude.ai/artifact/8H1edqNrByYMJuWPvCd316
- Mapa de concorrentes odonto: https://claude.ai/artifact/HN1F5p8XKExVSE6edRW9Mc
- Três nichos comparados: https://claude.ai/artifact/Bz25YzNk66cizhSYzeY1vh
- Plano de montagem solo: https://claude.ai/artifact/T6ZGnAMdYSuNkGThwG4BPw

### 23.3 Fontes principais

- Meta, cobrança de mensagens de serviço desde 01/10/2026: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages
- 360dialog, mesmo número com aplicativo: https://docs.360dialog.com/partner/waba-management/whatsapp-coexistence
- Canaltech, WhatsApp Business ganha agente de IA: https://canaltech.com.br/apps/whatsapp-business-ganha-agente-de-ia-para-responder-mensagens-de-clientes/
- Z-API, planos: https://www.z-api.io/
- Make, preços em créditos: https://www.jetadmin.io/blog/make-pricing/
- Chatwoot, preços: https://www.eesel.ai/blog/chatwoot-pricing
- Banimentos de número no Brasil (Estado de Minas): https://www.em.com.br/mundo-corporativo/2026/02/7361830-banimento-de-numeros-no-whatsapp-dispara-no-brasil.html
- Consumidor de luxo e IA (BCG e Altagamma): https://consumidormoderno.com.br/ia-luxo-parceira-compras-consumidores/
- Contatos fora do horário em clínicas: https://www.em.com.br/mundo-corporativo/2026/08/7475195-metade-dos-pacientes-busca-atendimento-fora-do-expediente.html
- ABSOLAR, projeção solar 2026: https://canalsolar.com.br/previsao-da-energia-solar-em-2026/
- Vivo, eSIM: https://vivo.com.br/para-voce/produtos-e-servicos/para-o-celular/esim
- Vivo Lite: https://vivo.com.br/para-voce/produtos-e-servicos/para-o-celular/planos-lite
- Vivo, roaming internacional: https://vivo.com.br/para-voce/produtos-e-servicos/para-o-celular/roaming-internacional
- Surf Telecom: https://www.surf.com.br/site/

As demais fontes estão listadas em cada página publicada.

---

## 24. Glossário

- **API oficial do WhatsApp (Cloud API):** o jeito autorizado pela Meta de conectar sistemas ao WhatsApp. Cobra por mensagem.
- **Z-API:** serviço brasileiro que conecta sistemas ao WhatsApp como se fosse o WhatsApp Web. Preço fixo, sem custo por mensagem, risco de bloqueio.
- **Coexistência:** usar o mesmo número no aplicativo e na API oficial ao mesmo tempo, por um parceiro autorizado.
- **Make:** ferramenta visual de automação. Cada cenário é uma sequência de passos que roda sozinha.
- **Créditos do Make:** a "moeda" de consumo do Make; cada passo executado gasta créditos.
- **Chatwoot:** painel onde a equipe da clínica vê e responde as conversas.
- **Modo copiloto:** a IA escreve, a pessoa confere e envia.
- **Base da clínica:** tudo o que a IA precisa saber sobre a clínica.
- **Manual de voz:** como a clínica fala.
- **Cliente oculto:** mandar mensagem como paciente para medir o atendimento.
- **eSIM:** chip virtual, instalado por QR code ou link.
- **Roaming:** usar a linha brasileira fora do Brasil.
- **LGPD:** lei de proteção de dados pessoais.
- **Operadora de dados:** quem trata dados em nome de outro (você, em nome da clínica).
- **Implantação:** taxa única para montar o atendente na clínica.
- **Case:** resultado real de um cliente, publicado com autorização.
