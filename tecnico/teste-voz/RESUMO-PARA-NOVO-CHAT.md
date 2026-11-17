# Resumo completo dos testes de voz (17/11/2026)

Copie tudo a partir da linha abaixo e cole como primeira mensagem do novo chat.

---

Contexto: sou a Erica, da Keshion IA (assistente de IA no WhatsApp para clínicas odontológicas de alto valor; sócio: Sérgio). Estou testando qual voz usar quando a assistente responder em áudio. Abaixo, tudo o que já foi decidido e testado. Responda sempre em português do Brasil, sem travessão, com exemplos e analogias.

## 1. Onde isso entra no produto
- Voz no roadmap: 2º semestre de 2027. Etapa 1: a assistente responde em áudio no WhatsApp (texto da IA convertido em voz), só quando o paciente mandou áudio ou a clínica quiser. Etapa 2 (depois): ligação telefônica com agente de voz.
- O teste de voz está sendo feito AGORA para já escolher o fornecedor e ter isso como diferencial ("voz de alto padrão" está entre os diferenciais aprovados).
- Assistente da demo: Clara, da clínica fictícia da Dra. Suzana. Em cada cliente real a assistente tem o nome que a clínica escolher.
- Pilha atual: Clara roda no n8n num servidor próprio (Contabo), respostas escritas pelo Claude Haiku 5.5, áudios do paciente transcritos pela OpenAI (gpt-4o-mini-transcribe), WhatsApp pelo Whapi.Cloud.

## 2. O que queremos da voz
- Voz genérica (não clonada), feminina, natural, português do Brasil, sem sotaque estrangeiro.
- Deve soar como uma pessoa mandando áudio no WhatsApp, não como locutora ou menu de telefone.
- Voz clonada de alguém real (ex.: a doutora) só com autorização por escrito, e não é o plano agora.

## 3. Fornecedores e custos
| Fornecedor | Como cobra | Custo por áudio de ~20 s (300 caracteres) |
|---|---|---|
| OpenAI gpt-4o-mini-tts | Só pelo uso, sem assinatura (cerca de US$ 0,015 por minuto) | cerca de R$ 0,03 |
| ElevenLabs | Assinatura mensal com cota de caracteres + excedente | cerca de R$ 0,07 a 0,13 |
| Azure Neural / Google Chirp 3 HD / Cartesia | Por uso | na mesma faixa (não testados ainda) |
| Modelos abertos (Chatterbox, Kokoro) | Grátis, mas precisam de servidor com placa de vídeo | mais caro no nosso volume; evitar XTTS e F5-TTS (licença não comercial) |
- A OpenAI usa a MESMA chave/conta que já usamos para transcrever áudio. O servidor do n8n já tem essa chave.
- Exemplo de volume: 1.000 áudios por mês saem por uns R$ 30 na OpenAI e uns R$ 70 a 130 na ElevenLabs.
- Valores são estimativas de terceiros; confirmar no site oficial antes de contratar.

## 4. O "leve sotaque" da OpenAI
- As vozes da OpenAI foram treinadas principalmente em inglês. Em português às vezes soam como um estrangeiro que fala muito bem: entonação de pergunta meio americana, números, valores e abreviações (R$, Dra., 14h30) lidos de forma estranha.
- Ajuda: instrução de estilo pedindo sotaque brasileiro, e escrever o texto do jeito que se fala (números e "doutora" por extenso).

## 5. Como gerar os áudios sem programar
- OpenAI: site openai.fm (demonstração grátis). Escolher a voz, colar a instrução de estilo no campo de instruções, colar a frase, gerar e baixar.
  - Vozes para testar: coral, ballad, sage (costumam soar mais soltas em português), nova, shimmer.
- ElevenLabs: conta grátis em elevenlabs.io (cota de cerca de 10 mil caracteres por mês; o grátis NÃO permite uso comercial, só teste). Text to Speech, modelo multilíngue mais recente (Multilingual v2 ou v3), Voice Library filtrada por Portuguese/Brazilian, voz feminina de 25 a 40 anos.
  - A ElevenLabs não tem campo de instrução: o tom vem da voz escolhida e do controle Stability (mais baixo = mais expressivo; mais alto = mais estável).
- Este ambiente do Claude não consegue gerar os áudios da OpenAI (acesso bloqueado), então a Erica gera pelos sites.

## 6. Instruções de estilo para o openai.fm (histórico)
- Versão longa (5 blocos: Voice, Tone, Dialect, Pronunciation, Features): DESCARTADA. Problemas: era cortada no meio pelo campo do site e a voz ficou robótica (muitas regras deixam a fala dura).
- Versão curta (em uso):
```
Voice: Friendly Brazilian woman, about 30, chatting casually.
Tone: Warm, relaxed, smiling. Not formal, not a narrator.
Dialect: Native Brazilian Portuguese, neutral São Paulo accent.
Pronunciation: Loose and conversational, like a WhatsApp voice note.
Features: Natural rhythm, small pauses, slight variation in pitch.
```
- Versão de uma linha (se ainda cortar):
```
Casual Brazilian woman sending a friendly WhatsApp voice note to a patient. Warm, relaxed, native São Paulo accent, never formal.
```
- Se o ÁUDIO cortar no meio: o site tem limite de tamanho do texto; gerar uma frase por vez.

## 7. As 6 frases do teste (iguais nas duas ferramentas)
1. Saudação: "Oi, Mariana! Tudo bem? Aqui é a Clara, da equipe da Dra. Suzana. Vi que você se interessou pelas lentes de contato dental. Posso te contar como funciona a avaliação?"
2. Nomes de tratamentos: "Aqui na clínica a gente faz clareamento, facetas, lentes de contato dental, alinhadores invisíveis e harmonização orofacial."
3. Números com algarismos (a mais difícil): "A avaliação custa R$ 150 e dura uns 40 minutos. Se você fechar o tratamento, esse valor é descontado."
4. Datas e horários: "Tenho dois horários livres: quinta-feira, dia 4, às 14h30, ou sexta, dia 5, às 9h. Qual fica melhor para você?"
5. Empatia (objeção de preço): "Entendo totalmente, é um investimento importante. Por isso a Dra. Suzana gosta de explicar tudo com calma na avaliação, sem compromisso nenhum."
6. Lembrete com endereço: "Passando só para lembrar da sua consulta amanhã às 10h, na Rua Augusta, 1200. Se precisar remarcar, é só me responder por aqui. Até amanhã!"
- Variação "falada" para testar contra a robotização (texto escrito como se fala):
  - Frase 1: "Oi, Mariana! Tudo bem? Aqui é a Clara, da equipe da doutora Suzana... Vi que você se interessou pelas lentes de contato dental. Posso te contar como funciona a avaliação?"
  - Frase 3: "A avaliação custa cento e cinquenta reais e dura uns quarenta minutinhos. Se você fechar o tratamento, esse valor é descontado, tá?"
  - Se a versão falada melhorar muito, a assistente passa a escrever o texto do áudio já no jeito falado (números por extenso, "doutora", "tá", "pra", reticências) antes de gerar a voz.

## 8. Rodada 1: Erica e Sérgio
- Ouvir todas as vozes nas frases 1, 3 e 5 (e a versão falada).
- Escolher a melhor voz da OpenAI e a melhor da ElevenLabs, anotando o porquê. Essas duas vão para a rodada 2.

## 9. Rodada 2: teste cego
- 5 a 8 pessoas, de preferência mulheres de 30 a 55 anos (público de lentes e alinhadores). Ninguém sabe quais ferramentas estão sendo comparadas.
- 10 arquivos: frases 1, 3, 4, 5 e 6 nas duas vozes. Nomes "Frase 1 - Voz A", "Frase 1 - Voz B" etc. Trocar a ordem em cada frase (às vezes a OpenAI é A, às vezes B). Gabarito guardado só com a Erica.
- Enviar pelo WhatsApp como áudio (mesma compressão que o paciente vai ouvir).
- Perguntas para cada áudio:
  - De 1 a 5, quanto soa natural? (1 = robô, 5 = pessoa gravando)
  - Percebeu sotaque de outro país? (não, um pouco, muito)
  - Alguma palavra ou número soou estranho? Qual?
- Pergunta final: "Se uma clínica te mandasse um desses áudios, qual você preferiria receber? Por quê?"
- Ficha (planilha): Pessoa | Frase | Voz | Naturalidade 1 a 5 | Sotaque | Palavra estranha | Preferida.

## 10. Regra de decisão
- ElevenLabs vence se tiver 1 ponto ou mais de média de naturalidade, ou 70% ou mais da preferência final.
- Senão, OpenAI (2 a 4 vezes mais barata e usa a chave que já temos).
- Voz com "sotaque: muito" em mais de um terço das respostas é eliminada, mesmo sendo mais barata.
- Se as duas ficarem robóticas, testar as alternativas: Azure, Google Chirp 3 HD e Cartesia.

## 11. Depois do teste (para lembrar)
- Registrar o resultado no arquivo do teste e na tarefa "Teste cego de vozes" do Notion (responsável Erica; prazo original 30/06/2027, pode adiantar).
- Integração futura no n8n: quando o paciente mandar áudio, a Clara escreve a resposta, converte em voz e envia como mensagem de voz (formato ogg/opus, que é o do WhatsApp).
- Riscos já levantados: paciente estranhar áudio de IA, sotaque, custo variável, dependência do fornecedor, LGPD (aviso de uso de IA se perguntarem). Para ligação (etapa 2): demora na resposta, aviso de gravação, erro de agenda, custo por minuto.

## 12. Arquivos no repositório (GitHub ericakrieger-bot/keshion)
- tecnico/teste-voz/teste-cego-vozes.md (roteiro completo, instruções longa e curtas)
- tecnico/teste-voz/RESUMO-PARA-NOVO-CHAT.md (este resumo)
- plano-produto-diferenciais.md (seção "Voz e áudio")
