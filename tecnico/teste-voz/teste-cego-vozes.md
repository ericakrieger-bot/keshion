# Teste cego de vozes: OpenAI x ElevenLabs (16/11/2026)

> Objetivo: escolher a voz dos áudios da assistente (Clara na demo). Voz genérica, natural, feminina, português do Brasil sem sotaque estrangeiro.
> Custo do teste: zero (sites de demonstração e planos grátis). Ninguém precisa programar.

## Resumo para levar a outro chat

```
Teste cego de vozes da Keshion (decidido em 16/11/2026).
- Objetivo: escolher a voz dos áudios da assistente no WhatsApp (etapa 1 da voz, previsto para o 2º semestre de 2027, teste agora).
- Concorrentes: OpenAI gpt-4o-mini-tts (por uso, cerca de R$ 0,03 por áudio de 20 s, mesma chave da OpenAI que já usamos para transcrever áudio) x ElevenLabs (assinatura com cota de caracteres, cerca de R$ 0,07 a 0,13 por áudio).
- "Leve sotaque" da OpenAI: vozes treinadas sobretudo em inglês; em português às vezes soam como estrangeiro que fala muito bem (entonação de pergunta, números, "Dra."). Corrige em parte com instrução de sotaque e números por extenso.
- Como gerar sem código: OpenAI no site openai.fm (campo de instruções + download); ElevenLabs no plano grátis (Text to Speech, modelo multilíngue, voz brasileira da Voice Library).
- Rodada 1: Erica e Sérgio escolhem a melhor voz de cada empresa. Rodada 2: teste cego com 5 a 8 pessoas, 5 frases x 2 vozes, arquivos chamados A e B, enviados como áudio no WhatsApp.
- Critérios: naturalidade (1 a 5), sotaque estrangeiro (não, um pouco, muito), números e nomes bem lidos, parece pessoa ou robô, preferência final.
- Regra de decisão: ElevenLabs só se ganhar por 1 ponto ou mais de naturalidade, ou 70% ou mais da preferência. Senão, OpenAI (2 a 4 vezes mais barata).
- Arquivo completo no repositório: tecnico/teste-voz/teste-cego-vozes.md
```

## As 6 frases (iguais nas duas ferramentas)

Cada frase testa uma coisa diferente. Copie exatamente, inclusive a pontuação.

| Nº | Testa | Texto |
|---|---|---|
| 1 | Saudação e simpatia | Oi, Mariana! Tudo bem? Aqui é a Clara, da equipe da Dra. Suzana. Vi que você se interessou pelas lentes de contato dental. Posso te contar como funciona a avaliação? |
| 2 | Nomes de tratamentos | Aqui na clínica a gente faz clareamento, facetas, lentes de contato dental, alinhadores invisíveis e harmonização orofacial. |
| 3 | Números escritos com algarismos (o caso difícil) | A avaliação custa R$ 150 e dura uns 40 minutos. Se você fechar o tratamento, esse valor é descontado. |
| 4 | Datas e horários | Tenho dois horários livres: quinta-feira, dia 4, às 14h30, ou sexta, dia 5, às 9h. Qual fica melhor para você? |
| 5 | Empatia (objeção de preço) | Entendo totalmente, é um investimento importante. Por isso a Dra. Suzana gosta de explicar tudo com calma na avaliação, sem compromisso nenhum. |
| 6 | Lembrete com endereço | Passando só para lembrar da sua consulta amanhã às 10h, na Rua Augusta, 1200. Se precisar remarcar, é só me responder por aqui. Até amanhã! |

Bônus (só na rodada 1): gere a frase 3 também por extenso ("cento e cinquenta reais", "quarenta minutos") para ver quanto melhora. Se melhorar muito, a Clara passa a escrever números por extenso antes de gerar o áudio.

## Como gerar os áudios

### OpenAI (site openai.fm)

1. Abra openai.fm no computador.
2. Escolha a voz. Testar pelo menos: **coral, nova, shimmer e sage**.
3. No campo de instruções (Vibe ou Instructions), cole:
   > Fale em português do Brasil, com sotaque brasileiro neutro, como uma recepcionista simpática de clínica. Tom acolhedor e natural, ritmo calmo, sem parecer locutora de rádio. Leia valores em reais e horários do jeito que um brasileiro fala.
4. Cole a frase, gere e baixe (Download). Nome do arquivo: `openai-coral-frase1.mp3`, e assim por diante.

### ElevenLabs (plano grátis)

1. Crie uma conta grátis em elevenlabs.io (a cota grátis é de cerca de 10 mil caracteres por mês, suficiente para o teste).
2. Vá em Text to Speech. Modelo: o multilíngue mais recente que aparecer (Multilingual v2 ou v3).
3. Em Voices, abra a Voice Library e filtre por Portuguese / Brazilian, voz feminina. Escolha 2 ou 3 vozes com cara de 25 a 40 anos.
4. Gere as mesmas frases e baixe. Nome: `eleven-NOMEDAVOZ-frase1.mp3`.

O plano grátis da ElevenLabs não permite uso comercial. Para o teste, tudo bem; para usar com cliente, teria que assinar.

## Rodada 1: Erica e Sérgio (cerca de 1 hora)

Ouçam todas as vozes nas frases 1, 3 e 5 e escolham **a melhor da OpenAI e a melhor da ElevenLabs**. Anotem por que escolheram. Essas duas vão para a rodada 2.

## Rodada 2: teste cego (5 a 8 pessoas)

1. **Quem:** de preferência mulheres de 30 a 55 anos (o público de lentes e alinhadores). Ninguém pode saber quais ferramentas estão sendo comparadas.
2. **Preparo:** gere as frases 1, 3, 4, 5 e 6 nas duas vozes escolhidas (10 arquivos). Renomeie para `Frase 1 - Voz A`, `Frase 1 - Voz B`, e assim por diante. **Troque a ordem em cada frase** (na frase 1 a OpenAI é a A; na frase 2 é a B), para ninguém pegar o padrão. Guarde o gabarito só com você.
3. **Envio:** mande pelo WhatsApp como áudio (encaminhar o arquivo). Assim a pessoa ouve com a mesma compressão que o paciente vai ouvir.
4. **Perguntas para cada áudio:**
   - De 1 a 5, quanto soa natural? (1 = robô, 5 = parece uma pessoa gravando)
   - Percebeu sotaque de outro país? (não, um pouco, muito)
   - Alguma palavra ou número soou estranho? Qual?
5. **Pergunta final:** "Se uma clínica te mandasse um desses áudios, qual você preferiria receber? Por quê?"

## Ficha de votação (copiar para uma planilha)

| Pessoa | Frase | Voz | Naturalidade (1 a 5) | Sotaque (não, um pouco, muito) | Palavra estranha | Preferida |
|---|---|---|---|---|---|---|
| | 1 | A | | | | |
| | 1 | B | | | | |

## Regra de decisão

- Média de naturalidade de cada voz, depois do gabarito revelado.
- **ElevenLabs vence** se tiver 1 ponto ou mais de média, ou 70% ou mais da preferência final.
- **Caso contrário, OpenAI**, que custa de 2 a 4 vezes menos e usa a chave que já temos.
- Se "sotaque: muito" aparecer em mais de um terço das respostas de uma voz, ela sai, mesmo que seja mais barata.
- Anotar o resultado neste arquivo e na tarefa "Teste cego de vozes" do Notion.

## Instrução de voz no formato do openai.fm (16/11/2026)

Colar no campo de instruções. A versão em inglês costuma ser seguida com mais precisão; a fala sai em português porque o texto está em português. Testar as duas na rodada 1.

### Em inglês (principal)

```
Voice: Warm, clear and natural female voice in her early thirties, like a friendly receptionist at a high-end dental clinic in São Paulo. Calm and confident, never sounding like a radio announcer or a recorded menu.

Tone: Welcoming, attentive and reassuring. Sounds genuinely happy to help, with a light smile in the voice. Professional but close, as if talking to a patient she already likes.

Dialect: Native Brazilian Portuguese with a neutral Southeast (São Paulo) accent. No European Portuguese, Spanish or English influence. Everyday spoken Brazilian Portuguese, natural contractions like "tá", "pra" and "a gente" when they appear in the text.

Pronunciation: Clear and relaxed. Read currency in Brazilian style ("R$ 150" as "cento e cinquenta reais"), times like a Brazilian ("14h30" as "duas e meia da tarde" or "catorze e trinta"), and "Dra." as "doutora". Soft Brazilian "r" and "s", no rolled English "r". Natural Brazilian question intonation, rising gently at the end.

Features: Medium-slow pace with short natural pauses between ideas. Slightly warmer and slower on empathetic sentences. Never rushed, never exaggerated or theatrical. Sounds like a real person sending a WhatsApp voice message, not reading a script.
```

### Em português (para comparar)

```
Voz: Feminina, quente, clara e natural, de uma mulher de uns 30 anos, como uma recepcionista simpática de clínica odontológica de alto padrão em São Paulo. Calma e segura, nunca com cara de locutora de rádio ou de menu gravado.

Tom: Acolhedor, atento e tranquilizador. Soa feliz em ajudar, com um leve sorriso na voz. Profissional, mas próxima, como quem fala com uma paciente de quem gosta.

Sotaque: Português do Brasil nativo, sotaque neutro do Sudeste (São Paulo). Nada de português de Portugal, espanhol ou inglês. Fala do dia a dia, com contrações naturais como "tá", "pra" e "a gente" quando aparecerem no texto.

Pronúncia: Clara e relaxada. Lê valores do jeito brasileiro ("R$ 150" como "cento e cinquenta reais"), horários como um brasileiro ("14h30" como "duas e meia da tarde") e "Dra." como "doutora". "R" e "s" suaves do Brasil. Entonação de pergunta natural, subindo de leve no fim.

Características: Ritmo médio para calmo, com pausas curtas e naturais entre as ideias. Um pouco mais lenta e calorosa nas frases de empatia. Nunca apressada, exagerada ou teatral. Parece uma pessoa de verdade mandando áudio no WhatsApp, não alguém lendo um texto.
```
