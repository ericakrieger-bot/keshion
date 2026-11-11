# CRM, agenda e painel da Keshion

> Desenho de 01/11/2026. Vale para a clínica demo (Dra. Suzana) e serve de modelo para cada cliente real. Tudo fica na conta Google **da clínica**: agenda, planilha e painel.

## 0. Versão 2 (01/11/2026): celular primeiro, pacientes antigos e lições dos concorrentes

**Princípio de UX:** a secretária e a doutora usam o CRM no celular, com uma mão, entre um paciente e outro. Toda ação comum leva no máximo dois toques: abrir o WhatsApp do paciente, ligar, mudar a etapa, registrar o orçamento, marcar como fechou ou perdeu. Nada de digitar em célula de planilha no celular.

**Como entregar isso:** a planilha do Google continua sendo o banco de dados (o Make escreve nela). Por cima dela, um app de celular sem código, ligado à mesma planilha: Google AppSheet ou Glide (os dois montam app a partir de planilha; confirmar preço e limite de usuários de cada um antes de escolher). O protótipo navegável de como as telas devem funcionar está em `app-crm-painel/prototipo-crm-mobile.html`.

**Telas do app**
1. **Hoje** (tela inicial): o que fazer agora, em cartões com um botão de ação cada. Esperando resposta da equipe (rascunhos e pedidos de pessoa), orçamentos para acompanhar hoje, confirmações de amanhã sem resposta, pacientes quentes, aniversariantes e reativações sugeridas.
2. **Funil:** colunas por etapa que rolam para o lado; tocar no cartão abre o paciente; mudar de etapa por botões, sem arrastar.
3. **Pacientes:** busca por nome ou telefone, filtros por etapa, tratamento e temperatura.
4. **Ficha do paciente:** botões grandes de WhatsApp e ligar; etapa; orçamento; próxima ação com data; linha do tempo (mensagens, avaliação, orçamento, acompanhamentos); etiquetas.
5. **Reativar:** pacientes antigos que voltaram a ser elegíveis (limpeza vencida, manutenção do clareamento, retorno do alinhador), com envio em lote aprovado pela equipe.
6. **Resultados:** atalho para o painel da clínica.

**Lições dos concorrentes (AtendeJá, Secretária Odonto, Secretária IA):** os três prometem CRM e painel, mas nenhum mostra a tela real, nenhum acompanha o orçamento formal, nenhum calcula valor recuperado com regra explícita e nenhum tem aprovação antes do envio. Ideias que valem copiar: lista de pacientes quentes, reativação por tempo parado, lembrete 2 horas antes, resumo do dia no WhatsApp do gestor, integração com sistemas odontológicos (Clinicorp, Dental Office, Feegow) mais adiante.

### Regras de UX para o app real (revisão de 01/11/2026, protótipo versão 2)
1. **Tela Hoje é uma fila de tarefas**, não um relatório: cada cartão tem o botão da ação principal e some quando a tarefa é feita. Ordem: pediram uma pessoa, aprovar resposta, confirmar, acompanhar orçamento; dentro de cada grupo, quem espera há mais tempo primeiro. Mais de 15 minutos de espera fica em destaque.
2. **Aprovar sem abrir a ficha:** o rascunho da IA aparece no próprio cartão, com "Aprovar e enviar" e "Editar".
3. **Desfazer em vez de "tem certeza?":** ações reversíveis (aprovar, mudar etapa, adiar) executam na hora e mostram "Desfazer" por 5 segundos.
4. **Funil por filtro de etapa**, sem quadro arrastável: no celular, chips com a contagem de cada etapa e uma lista; botão "Mover para a próxima etapa" em cada paciente.
5. **Dados obrigatórios no momento certo:** ir para "Orçamento enviado" pede o valor; ir para "Perdido" pede o motivo (6 opções em botões). Sem esses dados o painel não calcula valor recuperado nem motivo de perda.
6. **Próxima ação com um toque:** chips Amanhã, Em 3 dias, Em 1 semana.
7. **Cadastro manual curto** (nome, WhatsApp, origem) para quem ligou ou chegou pela recepção, com erro escrito embaixo do campo.
8. **Acessibilidade e toque:** botões com pelo menos 48 px de altura, texto base de 16 px, contraste mínimo de 4,5:1 nos dois temas (claro e escuro), foco visível, sem ícone sem nome, animações curtas e desligadas para quem pede menos movimento.
9. **No AppSheet ou Glide:** Hoje vira uma visão de cartões filtrada por `tarefa` não vazia e ordenada por prioridade e espera; Funil vira uma visão de lista com filtro por `etapa`; cada botão vira uma ação que grava na planilha; "Desfazer" vira a ação inversa.

### Dados de cada paciente (campos novos da versão 2)

Além das colunas da aba Contatos abaixo: `temperatura` (quente, morno, frio; calculada pelo Make a partir da conversa e do tempo parado), `etiquetas`, `ultimo_atendimento`, `ultimo_procedimento`, `profissional`, `data_nascimento` (opcional, para aniversário), `proxima_acao_data`, `link_conversa`, `nao_contatar` (sim quando o paciente pediu para não receber mensagens) e `consentimento_origem` (de onde veio o contato e a base para falar com ele).

### Pacientes antigos (importação por planilha)

Sim, dá para puxar. A clínica exporta a lista do sistema que usa (Clinicorp, Dental Office, Simples Dental, Feegow e outros costumam exportar em planilha ou CSV) ou da própria agenda, e a Keshion importa na aba **Pacientes antigos**:

| Coluna | Obrigatória |
|---|---|
| nome | sim |
| telefone (com DDD) | sim |
| ultimo_atendimento (data) | sim |
| ultimo_procedimento | recomendada |
| profissional | opcional |
| data_nascimento | opcional |
| observacao | opcional |

O Make limpa os telefones (só dígitos, com 55), tira duplicados e cruza com a aba Contatos.

**Regras da reativação**
- Limpeza e revisão: elegível 6 meses depois do último atendimento.
- Clareamento: manutenção depois de 12 meses. Alinhador: retorno conforme o plano de tratamento.
- No máximo uma mensagem de reativação a cada 90 dias por paciente; nunca para quem tem `nao_contatar` = sim.
- A lista do dia vai para a tela **Reativar**; a equipe aprova antes do envio (modo copiloto).
- Toda mensagem traz a opção de não receber mais ("responda SAIR"); quem responde SAIR vira `nao_contatar` = sim automaticamente.

**Cuidados**
- **Dados e LGPD:** a lista é da clínica e fica na conta Google da clínica. A clínica é a controladora e a Keshion IA atua como operadora; o contrato precisa dizer isso. Falar com quem já é paciente se apoia na relação existente, mas a clínica precisa autorizar o uso da lista por escrito.
- **Risco do WhatsApp:** mandar mensagem ativa para muita gente pela Z-API (número não oficial) é o jeito mais rápido de ter o número bloqueado. Reativação em volume só pela API oficial, com modelo de mensagem aprovado pela Meta (categoria marketing, cobrada por mensagem no cartão da clínica), e em lotes pequenos por dia.

## 1. Planilha do CRM

Arquivo: `Keshion · CRM · {nome da clínica}` (modelo em `app-crm-painel/modelo-crm-keshion.xlsx`, para importar no Google Planilhas).

### Aba Contatos (uma linha por paciente)

| Coluna | O que guarda | Quem preenche |
|---|---|---|
| telefone | Número com DDI e DDD, só dígitos (chave da linha) | Make |
| nome | Nome que aparece no WhatsApp | Make |
| origem | Anúncio, Instagram, indicação, Google, outro | Make (anúncio) ou equipe |
| primeiro_contato | Data e hora da primeira mensagem | Make |
| ultima_mensagem | Data e hora da última mensagem | Make |
| etapa | Novo, Conversando, Avaliação marcada, Compareceu, Orçamento enviado, Fechou, Perdido | Make até "Avaliação marcada"; equipe depois |
| tratamento_interesse | Lente, faceta, alinhador, clareamento, implante, outro | Make (IA identifica) |
| avaliacao_data | Data e hora da avaliação | Make |
| avaliacao_status | Marcada, Confirmada, Remarcar, Compareceu, Faltou, Cancelada | Make e equipe |
| orcamento_valor | Valor do orçamento em reais | Equipe |
| orcamento_data | Data em que o orçamento foi entregue | Equipe |
| fechou_valor | Valor fechado | Equipe |
| fechou_data | Data do fechamento | Equipe |
| motivo_perda | Preço, medo, tempo, outra clínica, sem resposta, outro | Equipe |
| acompanhamento | Data da última mensagem de acompanhamento do orçamento | Make |
| proxima_acao | O que fazer e quando | Equipe |
| observacoes | Livre | Equipe |

A secretária só mexe nas colunas de orçamento, fechamento e perda. O resto o Make preenche sozinho.

### Aba Mensagens (registro de cada mensagem)

data_hora, telefone, nome, direcao (recebida ou enviada), tipo (texto, áudio, foto), texto, acao_ia (responder, rascunho, humano), tempo_resposta_min, aprovado_por.

Serve para medir tempo de resposta, volume por hora do dia (mostra quanto chega fora do horário) e para auditar o que a IA respondeu.

### Aba Agenda (cópia das avaliações marcadas pela IA)

evento_id, telefone, nome, data_hora, duracao_min, status, confirmado_em, marcado_por (IA ou equipe).

### Aba Configuração (regras da clínica, lidas pelo Make)

| Campo | Exemplo |
|---|---|
| dias_avaliacao | seg, ter, qua, qui, sex |
| horario_inicio / horario_fim | 09:00 / 18:00 |
| intervalo_almoco | 12:00 a 13:30 |
| duracao_avaliacao_min | 50 |
| intervalo_entre_min | 10 |
| antecedencia_minima_h | 4 |
| dias_a_frente | 10 |
| fuso | America/Sao_Paulo |
| aprovador | número de quem aprova os rascunhos |
| hora_confirmacao | 17:00 (véspera) |

Mudar uma regra é mudar uma célula, sem mexer nos cenários.

## 2. Painel (Looker Studio, gratuito)

Fonte: a planilha acima. A clínica abre por um link, inclusive no celular. Filtro de período no topo.

**Linha de números**
- Contatos novos no período
- Tempo médio da primeira resposta e % respondidos em até 5 minutos
- Avaliações marcadas e taxa de agendamento (marcadas ÷ contatos novos)
- Comparecimento (compareceu ÷ marcadas) e faltas evitadas (confirmadas ou remarcadas na véspera)
- Orçamentos em aberto: quantidade e soma em reais
- Valor fechado no período

**Gráficos**
- Funil por etapa (Novo até Fechou)
- Contatos por semana, separados por origem
- Mensagens por hora do dia (destaque para fora do horário comercial)
- Tabela de orçamentos em aberto, com dias parados e data do último acompanhamento

**Valor recuperado (para o relatório mensal):** soma dos fechamentos de pacientes que (a) fizeram o primeiro contato fora do horário comercial ou (b) fecharam depois de pelo menos uma mensagem de acompanhamento automática. A regra fica escrita no próprio painel, para a clínica entender de onde vem o número.

## 3. Ajuste no cenário 1B (Resposta)

A IA passa a devolver, além de resposta, ação e motivo:
- `etapa` sugerida (Novo, Conversando, Avaliação marcada)
- `tratamento_interesse`
- `quer_agendar` (sim ou não)
- `horario_escolhido` (data e hora, quando o paciente escolheu uma das opções oferecidas)
- `confirmacao` (confirmou, remarcar ou vazio, para respostas à mensagem de véspera)

Módulos novos no 1B:
1. Google Planilhas: procurar o telefone na aba Contatos
2. Atualizar a linha (ou criar, se for novo)
3. Registrar a mensagem na aba Mensagens
4. Se `quer_agendar` = sim ou `horario_escolhido` preenchido: chamar o cenário de Agenda
5. Se `confirmacao` preenchida: atualizar o evento e o status na planilha

Consumo estimado: 12 a 15 créditos por mensagem.

## 4. Cenário 2: Agenda

Gatilho: webhook chamado pelo 1B. Dois caminhos:

**Oferecer horários**
1. Ler a aba Configuração
2. Google Agenda: buscar os compromissos dos próximos dias (até `dias_a_frente`)
3. OpenAI: com a lista de horários ocupados e as regras, escolher 3 horários livres em dias diferentes (resposta em JSON)
4. Guardar as opções na conversa do paciente (data store)
5. Enviar ao paciente: "Tenho estes horários para a sua avaliação com a Dra. Suzana: ..." (envio direto, sem aprovação, porque só oferece horários livres)

**Marcar o horário escolhido**
1. Conferir de novo se o horário continua livre
2. Google Agenda: criar o evento "Avaliação · {nome} · {telefone}"
3. Planilha: etapa = Avaliação marcada, preencher avaliacao_data, linha na aba Agenda
4. Enviar a confirmação com endereço e orientações da base
5. Se o horário foi ocupado no meio do caminho: oferecer novos horários

## 5. Cenário 3: Confirmações

Gatilho: todo dia no horário de `hora_confirmacao`, horário de Brasília.
1. Google Agenda: buscar as avaliações do dia seguinte
2. Para cada uma: enviar "Sua avaliação com a Dra. Suzana está confirmada para amanhã às 14h? Responda SIM para confirmar ou REMARCAR"
3. Planilha: avaliacao_status = aguardando confirmação
4. A resposta do paciente volta pelo 1B, que identifica confirmou ou remarcar e atualiza a agenda e a planilha. Em caso de remarcar, o 1B chama a Agenda para oferecer novos horários.

## 6. O que falta para ligar
- Conta Google da clínica demo conectada no Make (Agenda e Planilhas)
- Make no plano Core (mais de 2 cenários)
- Regras de agenda da clínica da Dra. Suzana (aba Configuração)
- Conexões da OpenAI e da Z-API
