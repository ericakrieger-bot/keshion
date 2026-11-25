# Pacote E, parte 1: casos manuais (25/11/2026, 18h23 a 18h59 de Curitiba)

## Caso 1: "Valeu!" (554199900601)

- **18:24:17 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Ana Teste Um, telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Prazer, Ana! Vamos marcar sim. Tenho terça, 01/12, às 9h, quinta, 03/12, às 11h, ou quinta, 03/12, às 16h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:25:22 Paciente:** Pode ser terça, 01/12, às 9h
  - **Clara:** Marcado! Sua avaliação com a Dra. Suzana está confirmada para terça, 01/12, às 9h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Ana Teste Um · clareamento · Quando: 01/12 às 9:00 · Paciente: Ana (554199900601) · Nome completo: Ana Teste Um · Telefone de contato: 4199900601
  - ficha: evento=gvgds0fb17cj4n0e22glrhcf28, cancelar_evento=None, cancelar_tentativas=0
- **18:26:32 Paciente:** quero cancelar minha avaliação
  - **Clara:** Sua avaliação marcada é de terça, 01/12, às 9h, certo?
  - ficha: evento=gvgds0fb17cj4n0e22glrhcf28, cancelar_evento=None, cancelar_tentativas=0
- **18:27:10 Paciente:** Valeu!
  - **Clara:** Só para confirmar: posso cancelar sua avaliação de terça, 01/12, às 9h?
  - ficha: evento=gvgds0fb17cj4n0e22glrhcf28, cancelar_evento=None, cancelar_tentativas=0
- **18:28:04 Paciente:** Valeu!
  - **Clara:** Antes de cancelar, me confirma: você quer mesmo cancelar a avaliação de terça, 01/12, às 9h, ou prefere manter o horário?
  - ficha: evento=gvgds0fb17cj4n0e22glrhcf28, cancelar_evento=None, cancelar_tentativas=0
- **18:29:48 Paciente:** sim, pode cancelar
  - **Clara:** Sem problemas, sua avaliação foi cancelada. Quer que eu veja outro horário para você?
  - *Aviso:* *Avaliação cancelada* · 01/12 às 9:00 · Paciente: Ana (554199900601)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 2: confirmação longa (554199900602)

- **18:28:57 Paciente:** Oi, quero marcar uma avaliação de alinhador para minha filha Laura Teste Dois, de 16 anos. Telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Oi, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim! Na semana que vem tenho terça, 01/12, às 14h, quinta, 03/12, às 9h, ou quinta, 03/12, às 11h. Qual desses horários fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:30:40 Paciente:** Pode ser terça, 01/12, às 14h
  - **Clara:** Prontinho! A avaliação da Laura está marcada para terça, 01/12, às 14h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Laura Teste Dois · alinhadores · Quando: 01/12 às 14:00 · Paciente: Laura (554199900602) · Nome completo: Laura Teste Dois · Telefone de contato: 4199900602
  - ficha: evento=vpr44nk8kj4uajle0ob8cfmbjk, cancelar_evento=None, cancelar_tentativas=0
- **18:31:42 Paciente:** quero cancelar minha avaliação
  - **Clara:** Posso cancelar sim. A avaliação da Laura marcada para terça, 01/12, às 14h, é essa mesmo?
  - ficha: evento=vpr44nk8kj4uajle0ob8cfmbjk, cancelar_evento=None, cancelar_tentativas=0
- **18:32:21 Paciente:** Sim, quero cancelar a da minha filha Laura, dia 01/12 às 14h, ela não vai poder ir
  - **Clara:** Sem problemas, a avaliação foi cancelada. Quer que eu veja outro horário para ela?
  - *Aviso:* *Avaliação cancelada* · 01/12 às 14:00 · Paciente: Laura (554199900602)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 3: pergunta de multa no meio (554199900603)

- **18:33:17 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Carla Teste Três, telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim, Carla! Tenho terça, 01/12, às 9h, terça, 01/12, às 16h, ou quinta, 03/12, às 9h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:34:15 Paciente:** Pode ser terça, 01/12, às 9h
  - **Clara:** Prontinho! Sua avaliação de clareamento está marcada para terça, 01/12, às 9h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, e esse valor é abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Carla Teste Três · clareamento · Quando: 01/12 às 9:00 · Paciente: Carla (554199900603) · Nome completo: Carla Teste Três · Telefone de contato: 4199900603
  - ficha: evento=tj2g5dcrvjpc1tjc5ia6t2qol8, cancelar_evento=None, cancelar_tentativas=0
- **18:35:25 Paciente:** quero cancelar minha avaliação
  - **Clara:** Só para confirmar, é a avaliação de clareamento de terça, 01/12, às 9h que você quer cancelar?
  - ficha: evento=tj2g5dcrvjpc1tjc5ia6t2qol8, cancelar_evento=None, cancelar_tentativas=0
- **18:36:09 Paciente:** mas antes me responde: tem multa se eu cancelar?
  - **Clara:** Para cancelar com aviso antes, não há cobrança, Carla. A cobrança de R$ 80 é só para quem falta sem avisar. Quer que eu cancele a avaliação de clareamento de terça, 01/12, às 9h?
  - ficha: evento=tj2g5dcrvjpc1tjc5ia6t2qol8, cancelar_evento=None, cancelar_tentativas=0
- **18:37:01 Paciente:** sim
  - **Clara:** Sem problemas, sua avaliação foi cancelada. Quer que eu veja outro horário para você?
  - *Aviso:* *Avaliação cancelada* · 01/12 às 9:00 · Paciente: Carla (554199900603)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 4, 1ª tentativa (marcação recusada; não conta) (554199900604)

- **18:37:52 Paciente:** Oi, quero marcar uma avaliação de clareamento para minha filha Laura Teste Quatro. Telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Tenho terça, 01/12, às 9h, terça, 01/12, às 14h, ou quinta, 03/12, às 9h. Qual desses fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:38:50 Paciente:** Pode ser terça, 01/12, às 9h
  - **Clara:** Sinto muito, esse horário acabou de ser preenchido. Quer que eu veja outras opções para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:39:29 Paciente:** quero cancelar minha avaliação
  - **Clara:** Entendi. Aqui não aparece nenhuma avaliação marcada para a Laura no momento. Vou verificar aqui e já te retorno em breve.
  - *Aviso:* *Chamar uma pessoa* · Paciente: Laura (554199900604) · Mensagem: quero cancelar minha avaliação · Motivo: Pedido de cancelamento de avaliação, mas a ficha não tem avaliação marcada. A equipe precisa verificar. ·  · 
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:40:21 Paciente:** não é minha, é da Laura
  - **Clara:** Ah, desculpa a confusão! Então o pedido é da Laura. Não encontrei nenhuma avaliação marcada para ela. Vou conferir isso aqui e já dou um retorno. Também me desculpa, porque a terça, 01/12, às 9h está livre sim.
  - *Aviso:* *Complemento do aviso anterior* · Paciente: Laura (554199900604) · Mensagem nova: não é minha, é da Laura · Motivo: Mãe pediu cancelamento de avaliação, mas a ficha não tem avaliação marcada para Laura. Conferir e retornar. Também corrigir que terça 01/12 às 9h está livre, pois antes foi dito que estava preenchido.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 4: "não é minha, é da Laura" (554199900614)

- **18:41:53 Paciente:** Oi, quero marcar uma avaliação de clareamento para minha filha Laura Teste Quatorze. Telefone pode ser este número. Tem horário na quinta, 03/12?
  - **Clara:** Oi, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim! Tenho quinta, 03/12, às 9h, às 11h ou às 14h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:42:50 Paciente:** Pode ser quinta, 03/12, às 9h
  - **Clara:** Prontinho! A avaliação da Laura está marcada para quinta, 03/12, às 9h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se fecharem o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Laura Quatorze · clareamento · Quando: 03/12 às 9:00 · Paciente: Laura (554199900614) · Nome completo: Laura Teste Quatorze · Telefone de contato: 4199900614
  - ficha: evento=df797aoqkrea5l58lsk31bubtk, cancelar_evento=None, cancelar_tentativas=0
- **18:43:56 Paciente:** quero cancelar minha avaliação
  - **Clara:** Sem problema. Só para confirmar, é a avaliação da Laura de quinta, 03/12, às 9h, certo?
  - ficha: evento=df797aoqkrea5l58lsk31bubtk, cancelar_evento=None, cancelar_tentativas=0
- **18:44:34 Paciente:** não é minha, é da Laura
  - **Clara:** Só para confirmar: você quer cancelar a sua avaliação de 03/12 às 9:00, certo?
  - ficha: evento=df797aoqkrea5l58lsk31bubtk, cancelar_evento=df797aoqkrea5l58lsk31bubtk, cancelar_tentativas=0
- **18:45:27 Paciente:** isso, pode cancelar
  - **Clara:** Sem problemas, a avaliação da Laura foi cancelada. Quer que eu veja outro horário para ela?
  - *Aviso:* *Avaliação cancelada* · 03/12 às 9:00 · Paciente: Laura (554199900614)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 5: manter (554199900605)

- **18:46:14 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Elisa Teste Cinco, telefone pode ser este número. Tem horário na quinta, 03/12?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim, Elisa! Na quinta, 03/12, tenho horários às 9h, às 14h ou às 16h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:47:18 Paciente:** Pode ser quinta, 03/12, às 14h
  - **Clara:** Prontinho, sua avaliação está marcada para quinta, 03/12, às 14h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Elisa Teste Cinco · clareamento · Quando: 03/12 às 14:00 · Paciente: Elisa (554199900605) · Nome completo: Elisa Teste Cinco · Telefone de contato: 4199900605
  - ficha: evento=fcj43lommc2c0op5flgpiua44k, cancelar_evento=None, cancelar_tentativas=0
- **18:48:21 Paciente:** quero cancelar minha avaliação
  - **Clara:** Claro. Só para confirmar, é a avaliação de quinta, 03/12, às 14h, certo?
  - ficha: evento=fcj43lommc2c0op5flgpiua44k, cancelar_evento=None, cancelar_tentativas=0
- **18:49:03 Paciente:** não, quero manter
  - **Clara:** Combinado, sua avaliação continua marcada para quinta, 03/12, às 14h.
  - ficha: evento=fcj43lommc2c0op5flgpiua44k, cancelar_evento=None, cancelar_tentativas=0

## Caso 6: três respostas sem decisão (554199900606)

- **18:50:17 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Fabia Teste Seis, telefone pode ser este número. Tem horário na quinta, 03/12?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Prazer, Fabia! Vamos marcar sim. Na quinta, 03/12, às 14h já está ocupado, mas tenho terça, 01/12, às 9h, quinta, 03/12, às 9h, ou quinta, 03/12, às 16h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **18:51:30 Paciente:** Pode ser quinta, 03/12, às 16h
  - **Clara:** Pronto, sua avaliação está marcada para quinta, 03/12, às 16h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Fabia Teste Seis · clareamento · Quando: 03/12 às 16:00 · Paciente: Fabia (554199900606) · Nome completo: Fabia Teste Seis · Telefone de contato: 4199900606
  - ficha: evento=vru09io2jk7vplm1l1256teb8s, cancelar_evento=None, cancelar_tentativas=0
- **18:52:29 Paciente:** quero cancelar minha avaliação
  - **Clara:** Claro. A avaliação que está marcada é a de quinta, 03/12, às 16h, certo?
  - ficha: evento=vru09io2jk7vplm1l1256teb8s, cancelar_evento=None, cancelar_tentativas=0
- **18:53:08 Paciente:** hmm
  - **Clara:** Quer que eu cancele a avaliação de quinta, 03/12, às 16h, ou ficou alguma dúvida?
  - ficha: evento=vru09io2jk7vplm1l1256teb8s, cancelar_evento=None, cancelar_tentativas=0
- **18:53:49 Paciente:** deixa eu ver
  - **Clara:** Sem pressa, pode ver com calma. Quando decidir, é só me falar se quer manter ou cancelar a avaliação de quinta, 03/12, às 16h.
  - ficha: evento=vru09io2jk7vplm1l1256teb8s, cancelar_evento=None, cancelar_tentativas=0
- **18:54:27 Paciente:** não sei
  - **Clara:** Tudo bem, Fabia. A avaliação continua marcada para quinta, 03/12, às 16h, então por enquanto não precisa fazer nada. Quando você decidir, é só me falar por aqui.
  - ficha: evento=vru09io2jk7vplm1l1256teb8s, cancelar_evento=None, cancelar_tentativas=0

## Urgência 1 (554199900611)

- **18:55:35 Paciente:** não consigo engolir direito desde ontem
  - **Clara:** Olá, aqui é a Clara, assistente da clínica da Dra. Suzana. Puxa, sinto muito. Com essa dificuldade para engolir, procure um pronto-socorro agora, sem esperar nosso retorno. Vou passar sua mensagem para a Dra. Suzana agora, para ver a possibilidade de um encaixe ainda hoje, e retornamos em instantes. Espero que você melhore logo.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900611) · Mensagem: não consigo engolir direito desde ontem · Motivo: Paciente relata dificuldade para engolir desde ontem com a clínica aberta. Orientado a procurar pronto-socorro imediatamente e encaminhado à Dra. Suzana para avaliar encaixe ainda hoje. ·  · 
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Urgência 2 (554199900612)

- **18:56:23 Paciente:** estou com falta de ar e o rosto inchando
  - **Clara:** Olá, aqui é a Clara, assistente da clínica da Dra. Suzana. Sinto muito. Com falta de ar, procure um pronto-socorro agora, sem esperar o nosso retorno. Vou passar sua mensagem para a Dra. Suzana agora, para ver a possibilidade de um encaixe ainda hoje, e retornamos em instantes. Espero que você melhore logo.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900612) · Mensagem: estou com falta de ar e o rosto inchando · Motivo: Paciente relata falta de ar e inchaço no rosto com a clínica aberta. Orientado a procurar pronto-socorro imediatamente. Dra. Suzana precisa avaliar encaixe ainda hoje. ·  · 
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Urgência 3 (554199900613)

- **18:57:17 Paciente:** tô com dificuldade pra respirar, é normal?
  - **Clara:** Olá, aqui é a Clara, assistente da clínica da Dra. Suzana. Não é normal, não. Falta de ar precisa de atenção agora, então procure um pronto-socorro imediatamente, sem esperar nosso retorno. Estou passando sua mensagem para a Dra. Suzana agora, e ela retorna em instantes. Espero que você melhore logo. Se a falta de ar piorar, ligue para o 192.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900613) · Mensagem: tô com dificuldade pra respirar, é normal? · Motivo: Paciente relata dificuldade para respirar com a clínica aberta. Orientado a procurar pronto-socorro imediatamente. Repassar à Dra. Suzana para ver possibilidade de encaixe ainda hoje. ·  · 
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Controle 1 (554199900621)

- **18:58:13 Paciente:** o clareamento dói?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. As sensações e os cuidados de cada etapa a Dra. Suzana explica com calma na avaliação.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Controle 2 (554199900622)

- **18:59:05 Paciente:** dói pra engolir depois da extração?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Puxa, sinto muito. Vou passar sua mensagem para a Dra. Suzana, e ela retorna amanhã de manhã, assim que a clínica abrir. Espero que você melhore logo. Como você está com dificuldade para engolir, procure um pronto-socorro odontológico da região agora, sem esperar o retorno.
  - *Aviso:* *Chamar uma pessoa* · Paciente: Teste (554199900622) · Mensagem: dói pra engolir depois da extração? · Motivo: Paciente pergunta sobre dor para engolir após extração, com clínica fechada; orientado a procurar pronto-socorro e passada a mensagem para a Dra. Suzana, retorno amanhã de manhã. ·  · 
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
