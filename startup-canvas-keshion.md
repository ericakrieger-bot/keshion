# Startup Canvas da Keshion

> Versão 2, 22/11/2026. Revisada com a Erica: o cliente é o dentista, o nicho é a odontologia inteira e a Keshion oferece um rol de pacotes e funções por tipo de clínica. Página para mostrar ao Sérgio: https://claude.ai/artifact/KKxQZCjDmMqnG6eZgWYKDd (fonte em `estrategia/canvas-page/startup-canvas.html`). Fontes: `plano-estrategico-keshion.md`, `comercial/piloto/estrutura-piloto-conhecidos.md`, `historico-e-estrategia.md`.
> Valores marcados como **estimativa** (tíquetes, custos por clínica, preços dos pacotes) não vieram dos documentos: servem para discutir e testar, não para decidir.

---

## Parte 1. Estratégia

### 1. Visão

**Nenhum paciente sem resposta, nenhum dentista respondendo WhatsApp de madrugada.**

A Keshion quer ser a referência em automações e agentes de IA para pequenos e médios negócios, começando pela odontologia no Brasil. Valores:

- **O dentista no controle:** ele aprova o que a assistente pode dizer e assume a conversa quando quiser.
- **Transparência com o paciente:** a assistente diz que é virtual, não dá diagnóstico e não fala preço sem autorização.
- **Resultado medido:** a gente mostra em números o que mudou (tempo de resposta, consultas marcadas, faltas, orçamentos fechados).

### 2. Mercado: a odontologia e suas especialidades

**O cliente é o dentista.** O nicho é a odontologia inteira. Dentro dela, cada especialidade tem um tíquete, uma rotina de agenda e um jeito de o paciente chegar, e é isso que define qual pacote e quais funções fazem sentido. A segmentação serve para montar o rol de produtos, não para excluir clínicas.

#### 2.1 Mapa das especialidades

| Especialidade | Procedimentos típicos | Tíquete por procedimento (estimativa) | Como é a agenda | Como o paciente chega | O que mais dói para o dentista |
|---|---|---|---|---|---|
| Clínica geral | Limpeza, obturação (restauração), extração simples, avaliação | R$ 150 a 400 | Consultas curtas, muitas por dia; limpeza a cada 6 meses | Paciente antigo, indicação, Google, WhatsApp | Volume de mensagens enquanto atende; paciente que não volta para a limpeza |
| Endodontia (canal) | Tratamento de canal, retratamento | R$ 600 a 1.500 por dente | 1 a 3 sessões, encaixe de urgência | Dor (urgência) e encaminhamento de outro dentista | Paciente com dor que precisa de horário hoje; sessões seguintes esquecidas |
| Ortodontia | Aparelho fixo, alinhadores, manutenção mensal | Instalação R$ 800 a 2.500; manutenção R$ 150 a 300 por mês; alinhador R$ 6.000 a 15.000 | Manutenção mensal por 18 a 30 meses | Indicação, Instagram, pais de pacientes | Falta e remarcação em volume; inadimplência da mensalidade |
| Implantodontia | Implante unitário, protocolo, enxerto | Implante R$ 2.500 a 5.000; protocolo R$ 15.000 a 35.000 | Etapas longas (cirurgia, 3 a 6 meses de espera, prótese) | Anúncio, indicação, avaliação gratuita | Orçamento alto que esfria; dúvidas e medo antes de decidir |
| Prótese | Coroa, prótese fixa e removível | R$ 1.000 a 4.000 | Várias sessões de ajuste | Encaminhamento, paciente antigo | Sequência de consultas e retornos de ajuste |
| Periodontia | Raspagem, tratamento de gengiva, manutenção | R$ 300 a 1.000 por sessão | Manutenção a cada 3 ou 4 meses | Encaminhamento | Paciente que abandona a manutenção |
| Odontopediatria | Consulta, prevenção, restauração em criança | R$ 150 a 400 | Retorno a cada 6 meses | Pais, indicação | Quem conversa é o responsável; remarcação por agenda da família |
| Estética | Clareamento, lentes e facetas, resina estética | Clareamento R$ 600 a 1.500; lente R$ 1.500 a 3.500 por dente | Avaliação, planejamento, sessões | Instagram e anúncio | Muitos curiosos, orçamento que esfria |
| Cirurgia oral | Siso, cirurgias menores | R$ 400 a 1.500 por dente | Cirurgia e pós-operatório em 7 dias | Encaminhamento, dor | Pós-operatório e dúvidas depois da cirurgia |
| Harmonização orofacial | Toxina, preenchimento | R$ 800 a 2.500 | Retorno a cada 4 a 6 meses | Instagram | Regras do conselho e do anúncio mudam: entrar com cuidado |
| DTM e dor orofacial | Placa, tratamento de dor | R$ 500 a 1.500 | Sessões e retorno | Encaminhamento, dor | Paciente ansioso, muitas dúvidas |

Na prática, a maioria das clínicas mistura várias especialidades (a clínica geral faz canal e às vezes implante). Por isso a assistente trabalha com uma **tabela de procedimentos da clínica**: nome, duração da consulta, se pode ser encaixe, faixa de preço que pode ser dita e retorno programado.

#### 2.2 As três jornadas que o produto precisa cobrir

| Jornada | Especialidades | O que a assistente precisa fazer |
|---|---|---|
| **Rotina e retorno** | Clínica geral, periodontia, odontopediatria, manutenção de ortodontia | Responder rápido, marcar, confirmar, lembrar do retorno (6 meses, 3 meses, mensal) |
| **Urgência e etapas** | Endodontia, cirurgia oral, prótese, DTM | Reconhecer dor e chamar o dentista, oferecer encaixe, marcar a próxima sessão, acompanhar o pós-operatório |
| **Orçamento alto e decisão longa** | Implante, protocolo, alinhador, estética | Tirar dúvidas aprovadas, acompanhar o orçamento (dias 3, 10, 17 e 30), mostrar o valor recuperado |

#### 2.3 Por onde começar e quem fica de fora

| Perfil de clínica | Quando | Por quê |
|---|---|---|
| **Clínica geral multidisciplinar** (limpeza, obturação, extração, algum canal) | Piloto 1, agora | É a mais fácil de trabalhar e a mais comum; usa as três jornadas em escala pequena; a Erica e o Sérgio conhecem dentistas assim |
| **Clínica de especialista** (ortodontia, endodontia, implante) | Pilotos 2 e 3, até 15/12 | Testa a jornada de rotina em volume (ortodontia) ou a de urgência e orçamento (endodontia, implante) |
| **Clínica de alto valor** (implante, protocolo, estética) | Desde já em venda, com o pacote completo e o módulo de orçamento | Paga mais; o lembrete de orçamento e o relatório de valor recuperado ficam prontos até 31/12/2026 |
| Franquias e redes | **Fora por enquanto** | Decisão centralizada, compra lenta, exige integração com sistema próprio e personalização da rede, não da clínica |

**Observação sobre o endodontista que só faz canal:** grande parte dos pacientes chega encaminhada por outro dentista. O valor pode estar em marcar a urgência no mesmo dia e avisar o dentista que encaminhou. Hipótese a conferir com um endodontista conhecido.

### 3. Custos relativos

**Valor único, com operação de custo baixo.** A Keshion não vende uma assinatura de R$ 180 com um produto genérico que qualquer clínica usa igual. Vende um serviço feito sob medida: base da clínica montada com o dentista, tabela de procedimentos, voz da clínica, regras aprovadas por escrito e acompanhamento semanal. Esse é o diferencial do começo e é o que justifica o preço.

O custo fica baixo por dentro: n8n no servidor próprio, IA barata (Claude Haiku) e uma estrutura única que lê a configuração de cada clínica.

#### 3.1 Pacotes de serviço (proposta para discutir com o Sérgio)

O dentista escolhe o pacote. Os preços abaixo são **estimativa** para testar nos pilotos.

| | **Essencial** | **Completo** | **Completo com app** |
|---|---|---|---|
| Para quem | Consultório pequeno, dentista que atende sozinho | Clínica com secretária ou com muito volume | Clínica que quer ver tudo no celular e medir resultado |
| Horário da assistente | Fora do horário: noite, almoço, fim de semana e feriado | 24 horas | 24 horas |
| Responde, marca, remarca e cancela | Sim | Sim | Sim |
| Chama o dentista em dor, remédio e tratamento em andamento | Sim | Sim | Sim |
| Copiloto (o dentista aprova antes de enviar, no horário de atendimento) | Não | Sim | Sim |
| Confirmação e lembrete de consulta | Não | Sim | Sim |
| Retorno programado (limpeza, manutenção, próxima sessão) | Não | Sim | Sim |
| Aplicativo exclusivo da clínica (conversas, agenda do dia, "Precisa de você", pacientes) | Não | Não | Sim |
| Relatório mensal | Simples | Simples | Completo, com valor recuperado |
| Mensalidade (estimativa) | R$ 590 | R$ 1.190 | R$ 1.690 |
| Implantação (estimativa) | R$ 1.500 | R$ 2.500 | R$ 3.500 |

**Plano Start (a partir de abril de 2027):** R$ 349 por mês (testar 299 e 399), implantação de R$ 490, base pronta por especialidade ajustada por questionário, só fora do horário, até 300 conversas por mês, sem reunião. Só entra quando houver bases prontas e implantação sem reunião. Estratégia completa de preço em `comercial/estrategia-de-preco.md`; proposta de valor de cada plano em `comercial/proposta-de-valor-planos.md`.

**Módulos que podem ser somados a qualquer pacote:** acompanhamento de orçamento (dias 3, 10, 17 e 30), reativação de pacientes antigos (só com a conexão oficial ou em pequena escala), pós-operatório e orientações aprovadas, pedido de avaliação no Google. Depois: agente de voz e Instagram.

A oferta de fundador do plano (implantação de R$ 3.000 e mensalidade de R$ 1.500 congelada por 12 meses) equivale ao pacote **Completo com app**.

#### 3.2 "Software exclusivo" ou "aplicativo exclusivo"?

**Recomendação: "aplicativo exclusivo da sua clínica".**

- O dentista pensa no celular. "Aplicativo" diz que é fácil e está no bolso.
- "Software" lembra sistema de gestão (Clinicorp, Simples Dental). Cria a expectativa de prontuário e financeiro, que a Keshion não faz, e coloca a Keshion na comparação com esses sistemas.
- "Exclusivo" funciona melhor quando o app aparece com o nome e o logo da clínica.

Como testar: nas demonstrações dos pilotos, mostrar o app e perguntar "como você chamaria isso?". Nos convites para quem não é conhecido, alternar as duas palavras e ver qual gera mais resposta.

### 4. Proposta de valor

**Para todos os dentistas**

- **Antes:** o paciente escreve enquanto o dentista atende e espera horas. Mensagem das 22h fica para o dia seguinte. O dentista responde no intervalo e à noite. Parte dos contatos desiste e marca em outro lugar.
- **Como:** assistente no WhatsApp da própria clínica, com nome escolhido pela clínica e base montada com o dentista. Responde a qualquer hora, marca no Google Agenda sem horário em dobro, chama o dentista quando precisa.
- **Depois:** nenhum paciente sem resposta, agenda preenchida sem parar o atendimento, noites livres.

**Por jornada**

| Jornada | Antes | Como | Depois |
|---|---|---|---|
| Rotina e retorno | Falta sem aviso, paciente que some depois da limpeza | Confirmação 48 h, véspera e 2 h antes; lembrete de retorno no prazo certo de cada procedimento | Menos buracos na agenda, retorno em dia |
| Urgência e etapas | Paciente com dor espera resposta e procura outro; segunda sessão esquecida | Reconhece dor, chama o dentista, oferece encaixe; marca a próxima sessão antes de o paciente sair | Urgência atendida no dia, tratamento concluído |
| Orçamento alto | Orçamento passado e esquecido | Lembretes aprovados nos dias 3, 10, 17 e 30; dúvidas respondidas com o texto do dentista | Mais orçamentos fechados, com o valor em reais no relatório |

**Alternativas e onde a Keshion ganha**

| Alternativa | Preço | O que ela não entrega |
|---|---|---|
| Dentista responde sozinho | Grátis em dinheiro, caro em tempo | Resposta rápida, noite e fim de semana |
| Secretária | Salário mais encargos (estimativa: R$ 2.500 a 3.500 por mês) | Atendimento 24 h; em consultório pequeno nem existe |
| Business AI da Meta | Grátis hoje | Agenda integrada, voz da clínica, confirmação, retorno, acompanhamento |
| Secretária IA da Simples Dental | Cerca de R$ 180 por mês, só para quem usa o sistema | Ajuste por clínica e acompanhamento humano |
| Cloudia e novatos (Gênesis, AtendeJá, PRI) | R$ 259 a 997 por mês | Configuração feita para a clínica; é software genérico de saúde |
| Odonto Results | Agência: tráfego, IA e central humana | Preço de agência; o foco é anúncio |

### 5. Escolhas: o que a Keshion NÃO faz

1. Só odontologia até ter 10 clientes pagantes e 2 cases com números.
2. Franquias e redes ficam fora por enquanto.
3. Sem integração com sistemas de gestão por enquanto: só Google Agenda. Quem usa Clinicorp ou Simples Dental vira aprendizado, não promessa.
4. Sem prontuário e sem financeiro: a Keshion cuida da conversa e da agenda.
5. Sem mensagem em massa nem propaganda pelo WhatsApp. Reativação só com a conexão oficial ou em pequena escala combinada com a clínica.
6. Sem tráfego pago para a clínica: a Keshion não é agência.
7. Sem software para a clínica configurar sozinha: a implantação é feita pela Keshion.
8. Sem anúncio pago da própria Keshion antes de 3 cases.
9. Nenhuma função nova sem pedido de cliente ou de reunião de venda.
10. A assistente não dá diagnóstico, não fala preço sem autorização e não finge ser humana.

### 6. Pacientes que já são da clínica

O paciente novo nunca fica esperando: isso já está resolvido. O trabalho agora é o paciente que a clínica já tem. Exemplo: "minha obturação caiu, tem horário?" A assistente precisa reconhecer o paciente, entender o procedimento, saber quanto tempo ele leva, perguntar se tem dor e oferecer o horário do tipo certo.

| Função | Clínica geral | Ortodontia | Endodontia | Implante | Situação hoje |
|---|---|---|---|---|---|
| Reconhecer quem já conversou (pelo telefone) | Sim | Sim | Sim | Sim | Já funciona |
| Marcar, remarcar e cancelar sem horário em dobro | Sim | Sim | Sim | Sim | Já funciona |
| Regra para paciente antigo (oferecer marcar, faixa de preço da limpeza) | Sim | Sim | Sim | Sim | Ajustar antes do piloto (testes deram 5 a 6 de 10) |
| Tabela de procedimentos com duração e encaixe ("a obturação caiu") | Sim | Sim | Sim | Sim | Construir até 30/11 |
| Lista de pacientes da clínica (nome, telefone, último atendimento) | Sim | Sim | Sim | Sim | Construir em janeiro (dado no sistema da clínica, nunca em arquivo da Keshion) |
| Confirmação e lembrete de consulta | Sim | Essencial | Sim | Sim | Construir até 15/12 |
| Aviso de falta e oferta de remarcar | Sim | Essencial | Sim | Sim | Com o app, até 31/12 |
| Retorno programado | Limpeza a cada 6 meses | Manutenção mensal | Próxima sessão do canal | Controle anual do implante | Janeiro de 2027 |
| Pós-operatório com orientação aprovada | Extração | Não | Sim | Sim | 1º trimestre de 2027 |
| Acompanhamento de orçamento | Às vezes | Alinhador | Coroa depois do canal | Sim | Até 31/12/2026 |
| Reativação (mais de 6 meses sem vir) | Sim | Abandono do tratamento | Não | Sim | Só com a conexão oficial |

### 7. Métricas-chave

- **North Star:** consultas marcadas ou confirmadas pela assistente por mês, somando todas as clínicas.
- **OMTM até 31/03/2027:** clínicas piloto que aceitam pagar ao fim do período sem custo. Meta: 1 até 31/01/2027 e 3 até 31/03/2027.
- **Números de apoio, por clínica, toda semana:** tempo de primeira resposta (antes e depois); % das conversas resolvidas sem chamar o dentista; no copiloto, % aprovadas sem edição; erros 🔴 da semana; faltas no mês; retornos marcados; horas da Keshion gastas na clínica.

### 8. Crescimento

**Venda conduzida pelos fundadores agora, indicação depois.** O dentista não assina sozinho num site: ele precisa ver a assistente funcionando e confiar em quem montou.

| Momento | Canal |
|---|---|
| Agora a março de 2027 | Rede de conhecidos da Erica e do Sérgio, convite pessoal, demonstração ao vivo de 30 min |
| 2027 | Indicação de dentista para dentista, com benefício para quem indica; diagnóstico grátis por cliente oculto para quem não é conhecido |
| A partir de dezembro de 2026 | Conteúdo da Erica no LinkedIn e no Instagram: bastidores do piloto, erros de atendimento vistos nos diagnósticos (sem expor clínicas), conteúdo por especialidade |
| 2028 em diante | Parceiros com comissão: agências de marketing odontológico, consultores de gestão de clínica, contadores de clínica |

### 9. Capacidades

| Capacidade | Hoje | Construir ou parceiro |
|---|---|---|
| Assistente, fluxos no n8n, servidor próprio | Tem (Erica) | Construir |
| Venda e relacionamento | Tem (Sérgio) | Construir |
| Copiloto, confirmações, retornos, tabela de procedimentos, app, relatório | Em construção ou ainda não existe | Construir, puxado pelos pilotos (roadmap de produto) |
| Bases prontas por especialidade (geral, ortodontia, endodontia, implante) | Não tem | Construir a partir dos pilotos |
| Conexão oficial do WhatsApp | Não tem (Whapi, não oficial) | Parceiro (provedor oficial da Meta) |
| Integração com sistemas de gestão | Não tem | Parceiro ou API deles, só quando clientes pedirem |
| Contrato e proteção de dados (LGPD) | Não tem | Advogado, com a primeira proposta aceita |
| CNPJ com sócios em Israel | Não tem | Contador |
| Implantação sem a Erica | Não tem | Manual de implantação; pessoa por projeto a partir de 5 clínicas |

### 10. Por que é difícil copiar

- **Simples Dental não quer:** vende software para 19 mil clínicas a cerca de R$ 180. Ajustar a voz de cada clínica e fazer reunião semanal quebra o modelo deles.
- **Meta não quer:** a IA grátis do WhatsApp é genérica para todo tipo de negócio. Agenda de consultório, retorno e acompanhamento por clínica não são o jogo dela.
- **Cloudia não quer:** atende saúde em geral, com mais de 1.000 clínicas. Especializar por especialidade odontológica diminui a escala.
- **Odonto Results não consegue no mesmo preço:** o custo dela é central humana e tráfego; a Keshion roda com IA e base técnica única.
- **Novatos não conseguem rápido:** falta prova e falta a biblioteca de bases por especialidade que os pilotos vão gerar.

**Leitura direta:** hoje a defesa é fraca. Nenhuma peça sozinha protege. O que protege é o conjunto: base sob medida, tabela de procedimentos, copiloto, acompanhamento semanal, relatório de valor e as bases por especialidade que melhoram a cada piloto. Isso só existe depois de alguns clientes, então a velocidade dos pilotos é a defesa de agora.

---

## Parte 2. Modelo de negócio

### 11. Estrutura de custos

**Fixos (dos documentos)**

| Item | Valor | Recorrente? |
|---|---|---|
| Ferramentas (servidor, IA, Whapi da demo, número) | R$ 250 a 400 por mês | Sim |
| Domínio e e-mail | Cerca de R$ 40 por ano mais o e-mail | Sim |
| Contador | R$ 100 a 300 por mês, depois do CNPJ | Sim |
| Abertura do CNPJ | Até R$ 1.000 | Uma vez |
| Contrato revisado por advogado | R$ 1.000 a 3.000 | Uma vez |
| Marketing | R$ 0 até 3 cases; depois teto de R$ 500 a 1.000 por mês | Sim, depois |

**Variáveis por clínica (estimativa a medir no piloto)**

| Item | Estimativa |
|---|---|
| Número de WhatsApp (Whapi hoje, cerca de US$ 12; a conexão oficial cobra por conversa) | R$ 70 a 150 por mês |
| IA das respostas, áudio e foto | R$ 30 a 100 por mês, conforme o volume |
| Fatia do servidor | Pequena enquanto couber no servidor atual |
| **Horas da Keshion** (implantação e acompanhamento) | **O maior custo real.** Meta: até 7 dias de implantação e menos de 3 h por semana por clínica |

**Como escala:** ferramentas crescem devagar; o que cresce com os clientes são as horas. Por isso o manual de implantação, as bases por especialidade e a estrutura única no n8n vêm antes da contratação.

### 12. Fontes de receita

**Modelo:** implantação mais mensalidade por pacote, mais módulos somados. Depois, receita de parceiros.

| Fonte | Como cobra |
|---|---|
| Implantação | Por pacote, uma vez (estimativa: R$ 490 no Start, R$ 1.500 a 3.500 nos outros) |
| Mensalidade | Por pacote (estimativa: R$ 349, 590, 1.190 e 1.690) |
| Módulos | Valor fixo por mês por módulo (a definir com os pilotos) |
| Fundador (3 vagas, jan a mar/2027) | R$ 3.000 de implantação e R$ 1.500 por mês congelados por 12 meses, em troca de depoimento e case |
| Preço cheio do plano (a partir de abr/2027) | Implantação de R$ 6.000 e mensalidade de R$ 2.200 a 2.800: vira o teto, para o Completo com app mais módulos |

**Margem:** com custo variável de R$ 100 a 250 por clínica (estimativa), o Essencial fica perto de 70% e os outros pacotes passam de 80%, como o plano já previa. O que pode derrubar a margem são as horas, não as ferramentas.

**Como os pacotes mudam a conta do plano:** com tíquete médio de R$ 1.200 por mês (estimativa de mistura entre pacotes), R$ 100 mil por mês pedem cerca de 85 clínicas, contra 40 no preço único de R$ 2.500. Os módulos e a subida de pacote são o caminho para aproximar esse número de 40.

**Maiores incertezas:** quanto o dentista de cada perfil paga de fato, qual pacote ele escolhe e quantas horas cada pacote consome.

---

## Parte 3. Execução

### 13. Roadmap de produto (dono: Erica, com o especialista técnico)

| Prazo | Entrega | Para qual pacote |
|---|---|---|
| Até 30/11/2026 | Piloto 1 no ar fora do horário; regra para paciente antigo; tabela de procedimentos com duração e encaixe | Todos |
| Até 07/12/2026 | Copiloto: o dentista aprova antes de enviar (semana 2 do piloto 1) | Completo |
| Até 15/12/2026 | Confirmação e lembrete de consulta; pilotos 2 e 3 no ar | Completo |
| Até 31/12/2026 | App v1 (Conversas, Agenda do dia, Precisa de você, Pacientes); lembrete de orçamento; relatório mensal | Completo com app; módulo de orçamento |
| Janeiro de 2027 | Lista de pacientes da clínica; retorno programado por procedimento; liga e desliga de funções por pacote | Completo |
| 1º trimestre de 2027 | Conexão oficial do WhatsApp nas clínicas pagantes; pós-operatório; aviso de falta no app | Todos |
| 2º e 3º trimestres de 2027 | Bases prontas por especialidade; implantação em até 2 semanas; relatório de valor recuperado | Todos |
| 2028 | Módulos de reativação, agente de voz e Instagram | Módulos |

### 14. Roadmap de vendas (dono: Sérgio, com o especialista de vendas)

| Prazo | Entrega | Pronto quando |
|---|---|---|
| 23 a 30/11/2026 | Convite e demonstração do piloto 1 (clínica geral conhecida); implantação | Piloto 1 no ar |
| Até 15/12/2026 | Pilotos 2 e 3, de preferência um de especialidade (ortodontia, endodontia ou implante) | 3 pilotos rodando |
| 16 a 19/12/2026 | Fechar pacotes e preços com o que os pilotos disseram; conversa com o contador sobre CNPJ | Tabela de pacotes aprovada pelos dois |
| Janeiro de 2027 | Conversa final do piloto 1 e oferta de fundador; contrato revisado por advogado | 1º pagante até 31/01/2027 |
| Fevereiro e março de 2027 | Fim dos pilotos 2 e 3; volta a prospecção fora da rede (lista, diagnóstico, reunião) | 3 pagantes até 31/03/2027 |
| Abril a setembro de 2027 | Preço cheio por pacote; programa de indicação; 1 a 2 clínicas novas por mês | 10 clientes |
| Outubro de 2027 a junho de 2028 | Vendedor comissionado; primeiros parceiros | 40 clientes, R$ 100 mil por mês |

### 15. Roadmap de marketing (dona: Erica, com o especialista de marketing)

| Prazo | Entrega |
|---|---|
| Até 30/11/2026 | Site de uma página, Instagram, LinkedIn e WhatsApp comercial no ar (o que ainda faltar) |
| Dezembro de 2026 | Material do piloto em PDF (fundo claro); 2 publicações por semana da Erica com bastidores do piloto |
| Janeiro a março de 2027 | Material de venda por pacote; página de proposta; calculadora de prejuízo; primeiro depoimento |
| 2º trimestre de 2027 | Primeiro case com números; conteúdo por especialidade (ortodontia, implante, clínica geral) |
| 2º semestre de 2027 | Estudo "Como as clínicas respondem no WhatsApp", com os dados dos diagnósticos |
| 2028 | Congressos e eventos de gestão de clínica, podcasts; anúncio só depois de 3 cases, com teto de R$ 500 a 1.000 por mês |

### 16. Quem faz o quê (2 pessoas)

| Área | Erica | Sérgio | Juntos |
|---|---|---|---|
| Produto e tecnologia | Monta a base de cada clínica, constrói as funções, corrige 🔴 no mesmo dia, cuida do servidor | Leva para a Erica as objeções e os pedidos dos dentistas | Decidem a prioridade da semana |
| Pilotos | Implantação técnica, testes, leitura das conversas na semana 1 | Convite (quando conhece), grupo de feedback, conversa semanal de 20 min | Conversa final e pergunta de preço |
| Vendas | Entra na demonstração ao vivo | Lista de clínicas, convites, follow-up, propostas, objeções registradas | Oferta de fundador e tabela de pacotes |
| Marketing e marca | Site, conteúdo 2 vezes por semana, materiais | Pede depoimentos e indicações | Aprovam cases antes de publicar |
| Empresa | Contrato e termos (redação) | Contador, advogado, CNPJ | Acordo de sócios, teto de gasto |

**Ritmo fixo:** daily do PM às 9h; reunião semanal de 45 min com os 5 números do plano (diagnósticos, reuniões, propostas em aberto, pagantes e receita, horas por clínica); tempo da Erica meio a meio entre produto e venda. Cada roadmap tem um especialista do PM acompanhando: técnico (produto), vendas, marketing e estratégia (este canvas, preço e pacotes).

---

## Coerência: as peças se reforçam?

**Reforçam:**
- Serviço sob medida, copiloto e "dentista no controle" combinam com a venda pela rede de confiança.
- Os pacotes deixam o consultório pequeno entrar pelo Essencial e a clínica de alto valor comprar o Completo com app e o módulo de orçamento, sem trocar de nicho.
- A tabela de procedimentos é a mesma peça para todas as especialidades; só muda o conteúdo.
- O acompanhamento semanal gera os números que viram case, que alimentam a indicação.

**Ainda não fecham:**
- **Preço do Essencial x horas:** se a implantação do Essencial consumir tantas horas quanto a do Completo, a margem some. O Essencial precisa de base mais padronizada.
- **Defesa x Meta grátis:** no Essencial, o valor precisa estar em marcar na agenda e chamar o dentista, não em responder dúvida.
- **Conexão não oficial x crescimento:** dá para pilotar; cliente pagante pede a conexão oficial (1º trimestre de 2027).

## Hipóteses que precisam ser verdade

| # | Hipótese | Risco se for falsa |
|---|---|---|
| H1 | Cada perfil de clínica paga pelo pacote certo para ele (consultório pequeno o Essencial; clínica com volume o Completo) | Muda os pacotes ou os preços |
| H2 | Depois de 2 semanas, 80% das respostas do copiloto saem sem edição | O produto não se sustenta sem a Erica lendo tudo |
| H3 | O valor percebido está em agenda, confirmação, retorno e falta, não em responder dúvida | A Meta grátis basta |
| H4 | A implantação cabe em 7 dias e o acompanhamento em menos de 3 h por semana por clínica | A margem some nas horas |
| H5 | A maioria das clínicas conhecidas usa Google Agenda ou aceita usar | Precisa de integração antes do previsto |
| H6 | O dentista topa conectar o número atual (conexão não oficial) | Atrasa o piloto ou antecipa a conexão oficial |
| H7 | Cada piloto satisfeito indica pelo menos 1 colega | A indicação não vira canal |
| H8 | "Aplicativo exclusivo" atrai mais que "software exclusivo" | Troca o nome no material |
| H9 | No endodontista, o valor está na urgência do dia e no aviso ao dentista que encaminhou | Muda o pacote para especialistas |

## Experimentos de pouco esforço

| # | Testa | Experimento | Critério de sucesso |
|---|---|---|---|
| 1 | H1 | Na conversa final de cada piloto, mostrar os 3 pacotes, fazer as 4 perguntas de preço e oferecer o mês 2 pago | 2 de 3 pilotos aceitam pagar |
| 2 | H2 | Contar no copiloto aprovadas sem edição, editadas e reescritas, por semana | 80% sem edição na semana 2 |
| 3 | H3 | Pergunta da semana 4: "se desligássemos amanhã, do que você sentiria mais falta?" | A resposta cita agenda, confirmação, retorno ou noite livre |
| 4 | H4 | Cronometrar cada passo da implantação e as horas semanais no piloto 1 | Até 7 dias e menos de 3 h por semana |
| 5 | H5 | Mensagem curta para 10 a 15 dentistas conhecidos: "onde fica sua agenda hoje?" | 60% no Google Agenda, papel ou aceitam migrar |
| 6 | H6 | Contar quantos convidados aceitam conectar o número na hora do sim | 2 de 3 aceitam |
| 7 | H7 | Pedir indicação no fim de cada piloto, com benefício claro (ex.: 1 mês grátis) | 1 indicação por piloto satisfeito |
| 8 | H8 | Nas demonstrações: "como você chamaria isso?"; nos convites frios, alternar as duas palavras | Uma das palavras gera claramente mais resposta |
| 9 | H9 | Conversa de 30 min com um endodontista conhecido sobre como os pacientes chegam | Confirmar ou descartar a hipótese |

**Primeiro a rodar:** experimento 5 (custa uma mensagem e responde em dias) e 4 (já cabe no piloto 1). O experimento 1 decide pacotes e preços: é o mais importante do trimestre.
