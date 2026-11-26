# Cancelar e Jev: casos manuais (26/11/2026, 07h31 a 08h05 de Curitiba)


## Caso 1: "Valeu!" (554199900701)

- **07:31:51 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Nina Teste Um, telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim, Nina! Na semana que vem tenho terça, 01/12, às 9h, terça, 01/12, às 14h, ou quinta, 03/12, às 9h. Qual fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **07:33:13 Paciente:** Pode ser terça, 01/12, às 9h
  - **Clara:** Prontinho! Sua avaliação com a Dra. Suzana está marcada para terça, 01/12, às 9h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Nina Teste Um · clareamento · Quando: 01/12 às 9:00 · Paciente: Nina (554199900701) · Nome completo: Nina Teste Um · Telefone de contato: 554199900701
  - ficha: evento=960af2rgb9pc887enavhjfs154, cancelar_evento=None, cancelar_tentativas=0
- **07:36:08 Paciente:** quero cancelar minha avaliação
  - **Clara:** A sua avaliação de terça, 01/12, às 9h, é essa que você quer cancelar?
  - ficha: evento=960af2rgb9pc887enavhjfs154, cancelar_evento=960af2rgb9pc887enavhjfs154, cancelar_tentativas=0
- **07:38:05 Paciente:** Valeu!
  - **Clara:** Sem problemas, sua avaliação de terça, 01/12, às 9h, foi cancelada. Quer que eu veja outro horário para você?
  - *Aviso:* *Avaliação cancelada* · 01/12 às 9:00 · Paciente: Nina (554199900701)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Caso 6: três respostas sem decisão (554199900702)

- **07:40:15 Paciente:** Oi, quero marcar uma avaliação de clareamento. Meu nome completo é Olga Teste Dois, telefone pode ser este número. Tem horário na semana que vem?
  - **Clara:** Oi, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Vamos marcar sim, Olga! Tenho terça, 01/12, às 9h, quinta, 03/12, às 9h, ou quinta, 03/12, às 14h. Qual desses horários fica melhor para você?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0
- **07:42:49 Paciente:** Pode ser terça, 01/12, às 9h
  - **Clara:** Prontinho! Sua avaliação de clareamento está marcada para terça, 01/12, às 9h. Fica na Rua Desembargador Motta, 2000, sala 1404, no Batel. A avaliação custa R$ 150, valor abatido se você fechar o tratamento em até 30 dias.
  - *Aviso:* *Nova avaliação marcada* · Avaliação · Olga Teste Dois · clareamento · Quando: 01/12 às 9:00 · Paciente: Olga (554199900702) · Nome completo: Olga Teste Dois · Telefone de contato: 554199900702
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=None, cancelar_tentativas=0
- **07:45:38 Paciente:** quero cancelar minha avaliação
  - **Clara:** Tudo bem, posso cancelar. Só para confirmar: sua avaliação de clareamento é terça, 01/12, às 9h, certo?
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_tentativas=0
- **07:47:28 Paciente:** hmm
  - **Clara:** Só para confirmar, quer que eu cancele a avaliação de terça, 01/12, às 9h?
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_tentativas=1
- **07:49:16 Paciente:** deixa eu ver
  - **Clara:** Tudo bem, pode ver com calma. Só me confirma: posso cancelar sua avaliação de terça, 01/12, às 9h?
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_tentativas=2
- **07:51:08 Paciente:** não sei
  - **Clara:** Vou pedir para a equipe confirmar o cancelamento com você por aqui, tá bom?
  - *Aviso:* *Chamar uma pessoa* · Paciente: Olga (554199900702) · Mensagem: não sei · Motivo: Paciente falou em cancelar a avaliação de 01/12 às 9:00, mas não confirmou depois de 3 respostas. Confirme com o paciente antes de cancelar ·  · O que a Clara respondeu: · Vou pedir para a equipe confirmar o cancelamento com você por aqui, tá bom?
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_tentativas=99
- **07:52:59 Paciente:** ok, obrigada
  - **Clara:** Imagina! Tenha um ótimo dia.
  - ficha: evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_evento=bqqlmao4c69i0ro08j0nloh76s, cancelar_tentativas=99
- **07:54:50 Paciente:** já falei que pode cancelar
  - **Clara:** Sem problemas, sua avaliação foi cancelada. Quer que eu veja outro horário para você?
  - *Aviso:* *Avaliação cancelada* · 01/12 às 9:00 · Paciente: Olga (554199900702)
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Urgência 1 (554199900711)

- **07:56:55 Paciente:** não consigo engolir direito desde ontem
  - **Clara:** Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900711) · Mensagem: não consigo engolir direito desde ontem · Motivo: Paciente relatou possível urgência (Paciente relata dificuldade para engolir desde ontem. Orientado a procurar pronto-socorro e passado para a Dra. Suzana, com retorno hoje assim que a clínica abrir.) ·  · O que a Clara respondeu: · Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Urgência 2 (554199900712)

- **07:58:44 Paciente:** estou com falta de ar e o rosto inchando
  - **Clara:** Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900712) · Mensagem: estou com falta de ar e o rosto inchando · Motivo: Paciente relatou possível urgência (Paciente relata falta de ar e inchaço no rosto. Clínica fechada agora, abre hoje às 8h. Orientado a procurar pronto-socorro imediatamente.) ·  · O que a Clara respondeu: · Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Urgência 3 (554199900713)

- **08:00:37 Paciente:** tô com dificuldade pra respirar, é normal?
  - **Clara:** Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - *Aviso:* *URGENTE: chamar uma pessoa agora* · Paciente: Teste (554199900713) · Mensagem: tô com dificuldade pra respirar, é normal? · Motivo: Paciente relatou possível urgência (Paciente relata dificuldade para respirar. Orientada a procurar pronto-socorro imediatamente. Mensagem repassada à Dra. Suzana para retorno.) ·  · O que a Clara respondeu: · Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Controle 1 (554199900714)

- **08:02:28 Paciente:** o clareamento dói?
  - **Clara:** Oi, tudo bem? Aqui é a Clara, da clínica da Dra. Suzana. A Dra. Suzana explica as sensações e os cuidados de cada etapa na avaliação, para você saber o que esperar antes de começar. Como é seu nome?
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Controle 2 (554199900715)

- **08:04:59 Paciente:** dói pra engolir depois da extração?
  - **Clara:** Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Puxa, sinto muito. Vou passar sua mensagem para a Dra. Suzana agora, para ver a possibilidade de um encaixe ainda hoje. Retornamos em instantes. Como a dificuldade para engolir é um sinal de alerta, procure um pronto-socorro odontológico agora, sem esperar o nosso retorno. Espero que você melhore logo.
  - *Aviso:* *Chamar uma pessoa* · Paciente: Teste (554199900715) · Mensagem: dói pra engolir depois da extração? · Motivo: Paciente com dor e dificuldade para engolir após extração, com a clínica aberta. Passar para a Dra. Suzana para avaliar encaixe ainda hoje. ·  · O que a Clara respondeu: · Olá, tudo bem? Aqui é a Clara, assistente da clínica da Dra. Suzana. Puxa, sinto muito. Vou passar sua mensagem para a Dra. Suzana agora, para ver a possibilidade de um encaixe ainda hoje. Retornamos em instantes. Como a dificuldade para engolir é um sinal de alerta, procure um pronto-socorro odontológico agora, sem esperar o nosso retorno. Espero que você melhore logo.
  - ficha: evento=None, cancelar_evento=None, cancelar_tentativas=0

## Quadro "a Clara fez X, o Jev faria Y"

| Hora | Caso | Mensagem | A Clara fez | O Jev faria | Discorda? |
|---|---|---|---|---|---|
| 07h57 | Urgência 1 | não consigo engolir direito | URGENTE | urgência (0,85) | não |
| 07h59 | Urgência 2 | falta de ar e rosto inchando | URGENTE | urgência (0,96) | não |
| 08h01 | Urgência 3 | dificuldade pra respirar | URGENTE | urgência (0,87) | não |
| 08h02 | Controle 1 | o clareamento dói? | respondeu | sem urgência (0,02); pergunta | não |
| 08h05 | Controle 2 | dói pra engolir depois da extração? | chamou a equipe | sem urgência (0,06); leu como pergunta (0,95) | **no "dói?"** |
| 07h38 | Caso 1 | Valeu! | cancelou | perguntaria de novo (sim 0,25) | **sim** |
| 07h47 | Caso 6 | hmm | perguntou de novo | perguntaria de novo | não |
| 07h49 | Caso 6 | deixa eu ver | perguntou de novo | perguntaria de novo | não |
| 07h51 | Caso 6 | não sei | passou para a equipe | não cancelaria | não |
| 07h53 | Caso 6 | ok, obrigada | não cancelou | não cancelaria (mas sim 0,99; barrado por "espera" 0,60) | não |
| 07h55 | Caso 6 | já falei que pode cancelar | cancelou | não opinou (gatilho não ligou) | sem dado |
| 08h08 | Júlia | dói? tenho muita sensibilidade | chamou a equipe | leu como pergunta (0,94) | **no "dói?"** |
| 08h14 | Júlia | não cancela ainda | manteve | não cancelaria | não |
| 08h16 | Júlia | pode cancelar pra mim, por favor? | perguntou "certo?" | não opinou sobre cancelar (primeiro pedido) | sem dado |
| 08h17 | Júlia | Isso, pode cancelar | cancelou | cancelaria (sim 1,00) | não |

## Saída de comparar_sombra.py clara 1

```
25 respostas da assistente no período

## Saúde do Jev
  ok: 25; falhas: 0 (0.0%)
  tempo: mediana 237 ms; 95% abaixo de 289 ms; máximo 291 ms
  custo total: US$ 0.0014

## 1. Urgência (Jev avisa com 0,3 ou mais)
  os dois avisariam: 3
  só o Jev avisaria: 0  (conferir: urgência que a regra perdeu ou alarme falso do Jev?)
  só a regra avisaria: 0  (o Jev nunca tira urgência: com o OU, esses continuam avisando)

## 2. "Dói?" e fora da lista
  "dói?" lido como pergunta (não relato): 5; destes, a regra mandou para a equipe por urgência: 0
    p=1.00 regra=responder 'o clareamento dói?'
    p=0.95 regra=humano 'dói pra engolir depois da extração?'
    p=0.94 regra=humano 'Bom dia! Oi, tudo bem? Queria saber quanto custa o clareamento de dente Ah e dói? Tenho mu'
    p=1.00 regra=agenda 'Ah, hoje às 14h fica bom / Preciso antes do almoço... não, espera, às 14h então / Mas e a '
    p=1.00 regra=responder 'Ok, anotado / Hoje às 14h então, Batel, sala 1404 / Mas e aí, vai doer na avaliação? Não é'
  fora da lista (implante, dentadura, coroa sobre implante): 0

## 3. Cancelar (só quando a assistente tinha perguntado de cancelar)
  7 respostas à pergunta de cancelar
  regra cancelou e o Jev também: 1
    sim=1.00 espera=0.13 pede=0.96 'Isso, pode cancelar / Desculpa a correria Obrigada!'
  regra NÃO cancelou e o Jev cancelaria (loop que o Jev evitaria?): 0
  regra cancelou e o Jev perguntaria de novo (cancelamento indevido?): 1
    sim=0.25 espera=0.11 pede=0.69 'Valeu!'
  nenhum dos dois cancelou: 5
```
