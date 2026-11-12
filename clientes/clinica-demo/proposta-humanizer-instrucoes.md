# Proposta: instruções da Clara com menos cara de robô

Feita em 12/11/2026 com a skill humanizer (padrões de "texto de IA" da Wikipédia), aplicada às instruções (`instrucoes-sarah.md`, registro `_instrucoes`) e às respostas reais da Clara no teste das 56 mensagens (`tecnico/teste-ab/relatorio-n8n.md`). **Nada foi aplicado ainda.** Nenhuma proposta muda fato, preço, regra clínica ou ação: só a forma de escrever.

Achado principal: a Clara quase não tem os vícios clássicos de IA (travessão, palavras infladas, listas com negrito). O que soa robótico é **repetição de frases prontas**, e várias delas vêm dos exemplos das próprias instruções, que ela copia ao pé da letra.

## 1. O tique "aqui na clínica"

**O que acontece:** a expressão aparece em quase toda resposta, às vezes no lugar errado. "Não atendemos no dia 24 de dezembro, aqui na clínica." "Aqui na clínica, o clareamento não é recomendado durante a gestação" (parece regra da clínica, e não cuidado com a gestante).
**Causa:** a primeira linha manda dizer "aqui na clínica", e o exemplo ensina "Fazemos sim, aqui na clínica.".
**Proposta:**
- Linha 1, trocar `quando citar a clínica, diga "nossa equipe" ou "aqui na clínica".` por `quando precisar citar a clínica, diga "nossa equipe" ou "aqui na clínica", no máximo uma vez por resposta, e só se a frase ficar confusa sem isso.`
- No EXEMPLO, trocar `mensagem2: Fazemos sim, aqui na clínica.` por `mensagem2: Fazemos, sim.`

## 2. A ressalva de preço repetida em toda resposta

**O que acontece:** "O valor exato a Dra. Suzana define na avaliação, porque depende de cada caso." sai igual em respostas seguidas (alinhador logo depois do clareamento; lente e depois clareamento).
**Proposta:** na regra D, trocar `diga a faixa e que o valor exato a Dra. Suzana define na avaliação, porque depende de cada caso.` por `diga a faixa. Na primeira vez que falar de preço na conversa, diga também que o valor exato a Dra. Suzana define na avaliação, porque depende de cada caso. Nas perguntas de preço seguintes, diga só a faixa, a não ser que a pessoa pergunte por que varia.` E no EXEMPLO, na resposta do alinhador, deixar só `Os alinhadores ficam entre R$ 5.500 e R$ 9.000.`

## 3. "Entendo." como abertura pronta

**O que acontece:** "Entendo. Infelizmente não consigo oferecer desconto por aqui." e "Entendo. Cada caso é um caso..." saem idênticos em conversas diferentes (Renata, Sérgio, a armadilha do 50%).
**Causa:** os exemplos das regras H2 e I começam com "Entendo.".
**Proposta:**
- Regra I, trocar o exemplo por `"Desconto eu não consigo dar por aqui, mas vou passar seu pedido para a Dra. Suzana e te dou um retorno em breve."`
- Regra H2, trocar `"Entendo. Cada caso é um caso, e o valor exato...` por `"Cada caso é um caso, e o valor exato...`
- Regra L, acrescentar: `Não comece respostas com "Entendo", "Puxa" ou "Claro" mais de uma vez na mesma conversa.`

## 4. Elogio e entusiasmo de assistente

**O que acontece:** "Que bom que você quer cuidar do sorriso!", "Ótima escolha!", "Que bom que você gostou desse resultado!" (numa foto que ela não podia saber se a pessoa gostou), "Que ótimo que você quer melhorar o seu sorriso! ✨". É o padrão de chatbot que elogia antes de responder.
**Proposta:** na regra L, acrescentar: `Não elogie a pergunta nem a escolha da pessoa ("Ótima escolha", "Que bom que você quer..."). No máximo um ponto de exclamação por resposta, e nenhum emoji em assunto de saúde, preço ou foto.`

## 5. Voz passiva e frase de manual

**O que acontece:** "Bitcoin e outras criptomoedas não são aceitas aqui na clínica." Ninguém fala assim no WhatsApp.
**Proposta:** na regra G, trocar o exemplo por `"Bitcoin a gente não aceita, só Pix, cartão e transferência."` (as formas de pagamento são as da base).

## 6. Frases que só enchem

**O que acontece:** "Aqui está o link do nosso site: ... Lá você encontra mais informações sobre a clínica e os tratamentos." e "Se ficou alguma dúvida sobre o clareamento, é só me perguntar." A segunda frase não acrescenta nada.
**Proposta:** na regra L, acrescentar: `Corte frases que só anunciam ou completam o óbvio ("Lá você encontra mais informações", "Se tiver dúvida, é só perguntar"). Oferecer ajuda só no encerramento (regra K).`

## 7. Encerramento sempre igual

**O que acontece:** "Eu que agradeço! Tenha um ótimo dia. Qualquer dúvida, estou por aqui." sai quase igual em todas as conversas, porque é o exemplo da regra K.
**Proposta:** na regra K, trocar o exemplo por dois, para ela variar: `"Eu que agradeço! Tenha um ótimo dia." ou "Imagina! Qualquer coisa, me chama aqui."`

## 8. Remarcar só depois do "sim" (achado do Codex, não da humanizer)

**O que acontece:** a pessoa perguntou se um horário estava livre e a Clara já mudou a avaliação, antes de a pessoa confirmar.
**Proposta:** na regra 9, trocar `Quando ela escolher, use a ação remarcar` por `Quando ela escolher um horário de forma clara ("pode ser quinta às 14h", "quero esse"), use a ação remarcar. Se ela só perguntar se um horário está livre, responda que está e pergunte se pode trocar, sem usar remarcar ainda.`

## Como aplicar, se aprovado

1. Atualizar `instrucoes-sarah.md` e o registro `_instrucoes` no banco `clara` (tabela `config`), sem mexer no fluxo.
2. Rodar de novo as 56 mensagens com o prefixo de teste e comparar com a rodada de hoje (`relatorio-n8n.md`), para conferir que melhorou o tom sem piorar nenhuma regra.
