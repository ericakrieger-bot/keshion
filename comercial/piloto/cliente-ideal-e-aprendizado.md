# Cliente ideal novo e o que aprender nos pilotos (rascunho para a Erica)

Rascunho de 21/11/2026. Nada aplicado no Notion, no plano estratégico, no `CLAUDE.md` nem nos agentes. Tudo aqui é hipótese: o piloto existe para confirmar ou derrubar. Feito com os agentes de estratégia e técnico. As skills do `pm-product-strategy` e do `pm-product-discovery` não apareceram nesta sessão, então serviram só de roteiro.

---

## 1. Cliente ideal (hipótese)

**Quem é:** clínica odontológica de bairro, do próprio dentista, com 1 a 3 dentistas. Vive de limpeza, obturação, extração, canal e manutenção. Pode ter um pouco de estética, mas não vive dela.

**Sinais para reconhecer**
1. 1 a 3 dentistas, dono presente, não é rede nem franquia.
2. WhatsApp é o canal principal, num número só.
3. Quem responde é o próprio dentista ou uma secretária que também faz a recepção.
4. Muito paciente antigo, que volta a cada 6 meses ou quando sente dor.
5. Agenda no papel, no Google Agenda ou num sistema simples.
6. Particular, ou particular com alguns convênios.
7. Paciente novo chega por indicação e pelo Google, quase nunca por anúncio.

**O que dói no WhatsApp dela**
1. Mensagem sem resposta enquanto o dentista está com paciente na cadeira.
2. Paciente que escreve à noite ou no fim de semana e marca em outro lugar.
3. Falta e remarcação de última hora, que deixam buraco na agenda.
4. Paciente que não volta para a limpeza porque ninguém lembrou.
5. As mesmas perguntas o dia todo: preço da limpeza, endereço, convênio, horário.
6. Dor e urgência chegando no meio do atendimento.

**Novo filtro A, B, C para o Funil**

| Nota | Quando | Critérios (dá para checar numa conversa, no Google ou no Instagram) |
|---|---|---|
| **A** (convidar já) | Encaixa bem no piloto | 1 a 3 dentistas; WhatsApp num número só; agenda no Google ou topa usar uma agenda Google no piloto; responde a gente em menos de 1 dia; diz que perde mensagem ou tem falta toda semana |
| **B** (talvez, depois) | Encaixa, mas com algo que ainda não resolvemos | Usa Clinicorp ou Simples Dental (sem integração); vive principalmente de convênio; recebe poucos contatos pelo WhatsApp (menos de 5 por dia, a confirmar na conversa) |
| **C** (não agora) | Não encaixa nesta fase | Rede ou franquia; já usa a IA do Simples Dental; agenda cheia só de convênio; mais de um número sem dono claro do WhatsApp |

**Recomendação:** usar este filtro A, B, C para escolher os pilotos e, depois do OK, o PM troca o filtro antigo no Funil. **Sim ou não?**

---

## 2. Proposta de valor

**Em palavras de dentista:**
> Você atende em paz, e nenhum paciente fica sem resposta. A Clara responde no WhatsApp da sua clínica, de dia e de noite, marca na sua agenda e só chama você quando é dor, tratamento ou algo que só você resolve. Ela lembra o paciente da consulta para ele não faltar e chama de volta quem está devendo a limpeza. Ela só fala o que você aprovou.

**O que muda em relação à clínica estética**

| | Clínica estética (antes) | Clínica do dia a dia (agora) |
|---|---|---|
| Valor de cada caso | Alto: lente de R$ 1.800 a 2.600 por dente, alinhador de R$ 5.500 a 9.000 | Baixo: limpeza de R$ 280 a 350 |
| Volume de mensagens | Poucas, mas caras | Muitas, todo dia |
| Paciente volta? | Pouco (compra uma vez) | Sim, a cada 6 meses |
| Falta | Na avaliação | Em todo tipo de consulta |
| Orçamento | Acompanhar até fechar é o centro | Pesa pouco (canal, prótese) |
| A frase que vende | "Um caso recuperado paga meses" | "Agenda cheia, menos falta, paciente que volta, e você para de responder WhatsApp" |

Preços da tabela vêm da clínica demo (`clientes/clinica-demo/base-clinica.md`), que é fictícia: servem de ordem de grandeza.

**Atenção:** a parte "lembra da consulta" e "chama de volta quem deve a limpeza" ainda não existe (seção 5). No piloto, prometer só o que já funciona e apresentar o resto como "construímos junto com você".

**Recomendação:** usar esta proposta de valor no material e nas conversas do piloto, separando o que já existe do que vem no mês. **Sim ou não?**

---

## 3. Hipóteses de preço (só para testar, nada decidido)

**Referências** (`pesquisa/concorrentes-odonto.html` e `conflitos-e-duplicatas.md`):
- Software com IA: R$ 259 a 997 por mês, implantação de R$ 497 a 700.
- IA do Simples Dental: cerca de R$ 180 por mês. Odonto Results: R$ 790 por mês mais marketing.
- AtendeJá: R$ 447 por mês só fora do horário, R$ 897 em 24 horas, implantação de R$ 497.
- Nosso custo por clínica: R$ 280 a 390 por mês (há outra conta com média de R$ 435; os documentos divergem).

| Hipótese | Preço (estimativa) | Lógica | Risco |
|---|---|---|---|
| **H1. Manter o fundador** | R$ 3.000 de implantação e R$ 1.500 por mês | Equivale a cerca de 5 limpezas por mês | Fica 2 a 6 vezes acima do software barato |
| **H2. Só fora do horário** | R$ 450 a 700 por mês e R$ 500 a 1.000 de implantação | Porta de entrada, perto da AtendeJá | Margem apertada perto do nosso custo |
| **H3. Serviço completo** | R$ 900 a 1.200 por mês e cerca de R$ 1.500 de implantação | 24 horas, confirmação, retorno e relatório, com acompanhamento nosso | Precisa das funções que ainda não existem |
| **H4. Fixo baixo mais variável** | Cerca de R$ 400 fixos mais um valor por consulta marcada ou paciente que voltou | O dentista paga pelo que vê | Difícil de medir; a Meta cobra por mensagem desde 01/10/2026 |

**O que observar no piloto para validar**
- Contatos por dia e quantos chegam fora do horário (diz se H2 já resolve).
- Faltas por mês, antes e depois.
- Quantos pacientes estão há mais de 6 meses sem voltar.
- Consultas que a Clara marcou no mês.
- Quem responde hoje o WhatsApp e quanto custa essa pessoa.
- Se o dentista compara a Clara com "um software" ou com "uma pessoa da recepção". Isso decide se o preço fica perto de H2 ou de H3.
- Na semana 4: mostrar H2 e H3 lado a lado e ver qual ele escolhe e por quê.

**Ponto de atenção:** o plano estratégico conta com cerca de R$ 2.500 por clínica para chegar em R$ 100 mil por mês com 40 clínicas em junho de 2028. Com H2 ou H3, seriam 2 a 5 vezes mais clínicas (estimativa). Ou a meta muda depois do piloto, ou o público pagante fica misto. Não precisa decidir agora.

**Recomendação:** levar H2 e H3 como as duas faixas da conversa da semana 4 e guardar H1 só para piloto que tiver parte de estética. Não falar preço antes da semana 4. **Sim ou não?**

---

## 4. Plano de aprendizado por piloto

### As 7 hipóteses mais arriscadas

| # | Hipótese | Por que é arriscada | Como saber |
|---|---|---|---|
| 1 | O dentista do dia a dia paga por um serviço bem acima do software barato (R$ 180 a 500) | Se ele vê a Clara como software, H1 e H3 caem | Pergunta de preço na semana 4 e com o que ele compara |
| 2 | A dor maior é a mensagem sem resposta (e não a falta, nem o paciente que some) | Define o que vendemos e o que construímos primeiro | Ranking das dores na conversa de 60 min e números reais da semana 2 |
| 3 | Chega contato suficiente fora do horário para valer a pena | Se quase tudo chega no horário, "só fora do horário" vale pouco | Contagem automática de mensagens por horário (semanas 1 e 2) |
| 4 | O valor está em falta e retorno, que ainda não existem | O piloto pode testar uma oferta que ainda não temos | Se confirmação e lembrete ficarem prontos na semana 3, medir faltas antes e depois |
| 5 | O paciente aceita conversar com uma assistente virtual da clínica | Paciente antigo pode estranhar e pedir "a moça de sempre" | Reclamações e pedidos de falar com pessoa, por semana |
| 6 | Dá para funcionar sem integração com o sistema da clínica | Muitas usam Clinicorp ou Simples Dental | Quantas das clínicas A, B, C usam sistema e se toparam a agenda Google |
| 7 | Convênio não atrapalha a Clara | Clínica do dia a dia costuma ter convênio, e a Clara não trata convênio | Quantas perguntas de convênio aparecem e quantas ela precisou passar para a equipe |

### O que medir em cada semana (ligado a `estrutura-piloto-conhecidos.md`)

| Semana | O que liga | O que medir | Hipóteses |
|---|---|---|---|
| **0** (preparação) | Nada no número real | O "antes": contatos por dia, quem responde, tempo médio de resposta (o que o dentista acha), faltas por semana, pacientes sumidos, convênios, sistema de agenda. Ranking das 3 maiores dores. O que ele estranhou no teste | 2, 6, 7 |
| **1** (só fora do horário) | Clara à noite e no fim de semana | Contatos fora do horário, consultas marcadas, quantas vezes chamou a equipe, erros 🔴 e 🟡 apontados, o que o paciente estranhou | 3, 5 |
| **2** (copiloto e mais horário) | Dentista aprova antes de enviar; depois dia todo se for bem | Quantas respostas ele aprovou sem mexer, quantas corrigiu, tempo que gastou aprovando, marcações sozinha | 2, 3, 5 |
| **3** (pacientes antigos e app) | Confirmação e lembrete, app | Faltas comparadas com o "antes", quantos confirmaram ou remarcaram pelo lembrete, o que ele usou no app | 4, 6 |
| **4** (resultado) | Lembrete de orçamento, relatório | Continua ou não, quanto pagaria, H2 contra H3, o que faltou, se indicaria um colega | 1, todas |

**Medido sozinho pelo banco hoje:** contatos e horário de cada mensagem recebida, consultas que a Clara marcou, remarcações e cancelamentos (lendo a conversa).
**Ainda não dá para medir sozinho:** tempo de resposta exato, faltas, quem é paciente antigo, quantas vezes ela chamou a equipe (o banco guarda só o último aviso). Até ajustar, anotar à mão no grupo do piloto.

### Roteiro da conversa de 60 minutos com o dentista (semana 0)

Regra: perguntar sobre o que aconteceu de verdade ("me conta a última vez que..."), não sobre o que ele acha que faria. Não mostrar preço. Gravar ou anotar com as palavras dele.

| Tempo | Bloco | Perguntas |
|---|---|---|
| 0 a 5 min | Abertura | Explicar o objetivo: aprender com a rotina dele, não vender. Pedir licença para anotar |
| 5 a 15 min | A clínica | Quantos dentistas e quem mais trabalha aí? Quais tratamentos mais faz numa semana? Atende convênio, quais, quanto do movimento? Como organiza a agenda hoje? |
| 15 a 30 min | O WhatsApp hoje | Quem responde? Quantas mensagens por dia, mais ou menos? O que mais perguntam? Me conta a última vez que uma mensagem ficou sem resposta e o que aconteceu. E à noite e no fim de semana? |
| 30 a 40 min | Falta e retorno | Quantas faltas numa semana normal? O que faz quando alguém falta? Como lembra o paciente da limpeza de 6 meses hoje? Quantos pacientes você acha que estão sumidos? |
| 40 a 50 min | Dor e casos difíceis | Como chega um paciente com dor? O que a assistente nunca pode dizer? Quais preços e condições podem ser ditos? Quando você quer ser chamado na hora? |
| 50 a 57 min | Prioridade | Destas dores (mensagem sem resposta, falta, paciente sumido, perguntas repetidas, urgência), quais são as 3 que mais pesam? Se resolvesse só uma, qual seria? Já tentou alguma ferramenta ou pessoa para isso? Quanto custou? |
| 57 a 60 min | Fechamento | Combinar questionário, prints e nome da assistente. "Tem algo que eu não perguntei e devia?" |

**Recomendação:** usar estas 7 hipóteses e este roteiro já no piloto 1, e repetir o mesmo roteiro nos pilotos 2 e 3 para poder comparar. **Sim ou não?**

---

## 5. O que a Clara precisa ganhar para esse público

**Achado do técnico:** a clínica demo é de estética. A base não faz canal, siso nem implante e diz "não atendemos convênio". A agenda só marca um tipo de consulta (avaliação de 60 min, terça e quinta, em 4 horários fixos, `clientes/_modelo/clinica.json`). Para o dia a dia, isso pesa mais do que qualquer ajuste de texto.

| # | O que | Situação hoje | Tamanho | Precisa estar pronto |
|---|---|---|---|---|
| 1 | 🔴 **Responder só fora do horário** (combinado para a semana 1) | Não existe | Pequeno | Semana 1 |
| 2 | 🔴 **Regra de paciente antigo:** retorno e limpeza. Informar a faixa de preço, nunca falar de prontuário, oferecer horário | Parcial: a base manda passar a marcação para a equipe, por isso ela não oferece marcar (tirou 5 a 6 nos testes) | Pequeno | Semana 0 |
| 3 | 🔴 **Base da clínica do dia a dia:** canal, extração, obturação, prótese simples, "o que faço em caso de..." | Parcial: o questionário já pergunta | Médio | Semana 0 |
| 4 | 🔴 **Convênio:** quais aceita, se precisa de carteirinha ou autorização, passar cobertura para a equipe | Não existe | Pequeno (só texto) | Semana 0 |
| 5 | 🔴 **Vários tipos de consulta na agenda** (limpeza de 40 min, retorno, extração, cada um com sua duração) | Não existe | Grande | Semana 2 |
| 6 | 🟡 **Urgência e dor:** acolher, avisar URGENTE e encaixar | Existe; falta a regra de encaixe da clínica real | Pequeno | Semana 0 |
| 7 | 🟡 **Copiloto:** o dentista aprova antes de enviar | Não existe | Grande | Semana 2 |
| 8 | 🟡 **Confirmação e lembrete** (48 h, véspera e 2 h antes, com "confirmo" ou "remarcar") | Não existe | Grande | Semana 3 |
| 9 | 🟡 **Falta:** registrar compareceu ou faltou e oferecer remarcar | Parcial: remarcar funciona, não há registro de falta | Médio | Semana 3 |
| 10 | 🟡 **Lista de pacientes da clínica** (nome, telefone, último atendimento) | Não existe: ela só reconhece quem já falou com ela | Médio | Semana 3 |
| 11 | ⚪ **Lembrete de orçamento** (dias 3, 10, 17 e 30) | Decidido, não construído | Médio | Semana 4 |
| 12 | ⚪ **Medição:** registrar cada aviso à equipe e o horário de cada resposta enviada | Parcial | Pequeno | Semana 1, se possível |
| 13 | ⚪ Outros: "quero falar com a secretária", lista de retornos pós-procedimento, relatório semanal | Não existe | Pequeno a médio | Semana 4 |

**O que isso quer dizer para o calendário:** os itens 1 a 4 e 6 são pequenos ou médios e cabem antes do piloto 1. Os itens 5, 7 e 8 são grandes e chegam juntos nas semanas 2 e 3. Se apertar, o item 5 (vários tipos de consulta) vem antes do copiloto, porque sem ele a Clara não marca limpeza sozinha, que é a conversa mais comum desse público.

**Recomendação:** o técnico faz os itens 1, 2, 3, 4 e 6 antes do piloto 1 e coloca o item 5 na frente do copiloto. **Sim ou não?**
