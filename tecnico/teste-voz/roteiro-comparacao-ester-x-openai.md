# Roteiro de comparação: Ester (ElevenLabs) x vozes da OpenAI

> Criado em 17/11/2026. Objetivo: descobrir se uma voz da OpenAI (cerca de dez vezes mais barata) chega perto da Ester. Se chegar, vai para o teste cego. Se não chegar, a Ester fica.
> Analogia: a Ester é a padaria premium. A OpenAI é o mercado do bairro. Só provando os dois lado a lado dá para saber se a diferença de preço compensa.

## 1. O que é comparado

| | Ester (ElevenLabs) | OpenAI |
|---|---|---|
| Modelo | Eleven V4 | gpt-4o-mini-tts (site openai.fm) |
| Configuração | Estabilidade 36%, Similaridade 100%, Intensidade 100% | Instrução de estilo (item 3) |
| Vozes | Só a Ester | coral, ballad, sage, nova, shimmer |
| Custo estimado por áudio de 20 s | cerca de R$ 0,30 (confirmar o multiplicador do V4) | cerca de R$ 0,03 |

Os valores são estimativas de terceiros. Confirmar nos sites oficiais antes de contratar.

## 2. Regra de ouro: as mesmas frases nas duas ferramentas

Use sempre a versão "falada" abaixo, escrita do jeito que se fala (números e horários por extenso, "doutora" em vez de "Dra."). Isso serve para a OpenAI e para a Ester. Assim a comparação é justa.

1. **Saudação:** "Oi, Mariana! Tudo bem? Aqui é a Clara, da equipe da doutora Suzana... Vi que você se interessou pelas lentes de contato dental. Posso te contar como funciona a avaliação?"
2. **Tratamentos:** "Aqui na clínica a gente faz clareamento, facetas, lentes de contato dental, alinhadores invisíveis e harmonização orofacial."
3. **Valores:** "A avaliação custa cento e cinquenta reais e dura uns quarenta minutinhos. Se você fechar o tratamento, esse valor é descontado, tá?"
4. **Datas e horários:** "Tenho dois horários livres: quinta-feira, dia quatro, às quatorze e meia, ou sexta, dia cinco, às nove. Qual fica melhor pra você?"
5. **Empatia:** "Entendo totalmente, é um investimento importante. Por isso a doutora Suzana gosta de explicar tudo com calma na avaliação, sem compromisso nenhum."
6. **Lembrete:** "Passando só pra lembrar da sua consulta amanhã, às dez, na Rua Augusta, mil e duzentos. Se precisar remarcar, é só me responder por aqui. Até amanhã!"

Observação: se quiser medir o efeito do texto falado, gere a frase 3 também na versão escrita ("R$ 150", "40 minutos") só com a Ester e compare.

## 3. Como gerar na OpenAI (openai.fm)

1. Abra openai.fm (demonstração grátis).
2. Escolha a voz. Teste uma por vez: coral, ballad, sage, nova, shimmer.
3. No campo de instruções, cole a versão curta:

```
Voice: Friendly Brazilian woman, about 30, chatting casually.
Tone: Warm, relaxed, smiling. Not formal, not a narrator.
Dialect: Native Brazilian Portuguese, neutral São Paulo accent.
Pronunciation: Loose and conversational, like a WhatsApp voice note.
Features: Natural rhythm, small pauses, slight variation in pitch.
```

   Se o campo cortar o texto, use a versão de uma linha:

```
Casual Brazilian woman sending a friendly WhatsApp voice note to a patient. Warm, relaxed, native São Paulo accent, never formal.
```

4. Cole uma frase por vez (o site corta textos longos), gere e baixe.
5. Nome do arquivo: `openai-coral-frase1.mp3`, `openai-sage-frase3.mp3` e assim por diante.

## 4. Como gerar a Ester (ElevenLabs)

1. Text to Speech, voz Ester, modelo Eleven V4.
2. Estabilidade 36%, Similaridade 100%, Intensidade 100%. Não mude nada entre as frases.
3. Nome do arquivo: `ester-frase1.mp3` etc.

## 5. Rodada A: ouvir e dar nota (Erica e Sérgio)

Cada um ouve sozinho, sem combinar as notas antes.

1. Ouça a Ester nas frases 1, 3, 4 e 5. Ela é a régua.
2. Ouça cada voz da OpenAI nas mesmas quatro frases.
3. Preencha a ficha `ficha-notas-rodada-a.csv` (abra no Google Planilhas ou no Excel). Para cada áudio:
   - Naturalidade, de 1 a 5 (1 = robô, 5 = pessoa gravando).
   - Sotaque de outro país: não, um pouco ou muito.
   - Palavra ou número que soou estranho (escreva qual).
4. Preste atenção especial na **frase 3** (valor e minutos) e na **frase 4** (horário). É onde a OpenAI mais costuma tropeçar.

## 6. Regra para uma voz da OpenAI passar para o teste cego

Uma voz da OpenAI só vai para a rodada B se cumprir tudo:

- Naturalidade média de pelo menos 4 (somando as notas de vocês dois, nas quatro frases).
- Média no máximo 0,7 ponto abaixo da Ester.
- Nenhuma frase com "sotaque: muito".
- Nenhuma frase com número ou horário lido errado.

Se nenhuma passar, a Ester está escolhida e o teste acaba aqui. Se duas passarem, leve só a melhor.

## 7. Rodada B: teste cego (só se uma voz da OpenAI passou)

Igual ao que já foi definido no roteiro original:

- 5 a 8 pessoas, de preferência mulheres de 30 a 55 anos. Ninguém sabe quais ferramentas estão sendo comparadas.
- 10 arquivos: frases 1, 3, 4, 5 e 6, nas duas vozes ("Frase 1 - Voz A", "Frase 1 - Voz B"). Troque a ordem de uma frase para outra. O gabarito fica só com a Erica.
- Envie pelo WhatsApp como áudio, para ter a mesma compressão que o paciente vai ouvir.
- Perguntas por áudio: naturalidade de 1 a 5, se percebeu sotaque de outro país, e se alguma palavra ou número soou estranho.
- Pergunta final: "Se uma clínica te mandasse um desses áudios, qual você preferiria receber? Por quê?"

**Decisão final:**
- A Ester vence se tiver 1 ponto ou mais de média de naturalidade, ou 70% ou mais da preferência.
- Caso contrário, vence a voz da OpenAI (mais barata e usa a chave que já temos).

## 8. Antes de decidir pelo preço

Confirmar duas coisas, pois mudam a conta:

1. Qual multiplicador de créditos o modelo V4 cobra por caractere (o leve gasta metade).
2. Se a licença da Ester permite uso comercial por API.

Conta de referência: cerca de 300 áudios por mês por clínica são uns R$ 10 na OpenAI e uns R$ 100 na ElevenLabs. Pese isso contra a mensalidade de R$ 1.200 a 2.500 da clínica.

## 9. Registro do resultado

Anotar aqui depois do teste:

- Voz da OpenAI que mais se aproximou: ____________
- Média da Ester: ______  Média dessa voz: ______
- Passou para o teste cego? sim / não
- Decisão final: ____________
- Data: ____________

Depois, atualizar a tarefa "Teste cego de vozes" no Notion (responsável Erica).
