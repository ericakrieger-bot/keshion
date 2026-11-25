# Jev como segunda barreira da Clara: resultado da bancada (25/11/2026)

## Resumo em 5 linhas

1. O Jev (versão 1.14) acertou quase tudo que importa: urgência (20 de 20 com limiar 0,3, zero alarme falso em 170 mensagens normais), "dói?" x dor (18 de 18), implante e dentadura (6 de 6) e o "sim" do cancelar nos casos da Bia, Sandra, Thiago e Júlia.
2. Ele erra onde a frase é ambígua: "sim, mas quanto custa a limpeza?" ele lê como sim (probabilidade 0,99 a 1,00). Para cancelar isso é perigoso, então o cancelar precisa de regras em volta (abaixo).
3. Custo e tempo são irrelevantes: US$ 0,000074 por mensagem (US$ 0,07 por 1.000 mensagens) e 0,46 s por chamada com 6 perguntas juntas. Gastei cerca de US$ 0,03 no total.
4. O ponto fraco real é privacidade: o texto do paciente iria para um terceiro nos EUA, sem plano de retenção zero.
5. Recomendação: **usar como segunda barreira, nunca no lugar das regras de hoje**, e só depois de resolver a parte de privacidade e contrato (veja "Riscos").

## O que foi testado

- 250 chamadas: as 22 conversas inventadas de 24/11 (183 falas de paciente), os casos do Pacote C e do Codex, e alguns casos novos que eu inventei (não consigo engolir, dificuldade de respirar, "dói?", coroa sobre implante, escolha de horário).
- Cada fala foi enviada com as últimas 6 trocas. Em cada chamada foram 6 perguntas em paralelo: urgência, dor ou dúvida, confirmação, horário, fora da lista e (extra) "quer remarcar".
- Os rótulos de "o que seria certo" foram feitos por mim, à mão. Amostra pequena: serve para ver a direção, não para prometer porcentagem.

## Tabela das situações pedidas

"Prob." é a probabilidade da resposta que o Jev escolheu. "Conf." é a confiança dele (só existe nas perguntas de escolha).

| Situação | Mensagem (resumo) | Jev disse | Prob. | Conf. | Certo? |
|---|---|---|---|---|---|
| Bia, "sim" do cancelar (6 vezes no loop) | "sim, pode cancelar kkk, mas antes me responde: a lente estraga o dente?" | sim claro | 1,00 | 1,00 | Sim, em todas |
| Bia, a pergunta da lente | "a lente estraga o dente? preciso de lente mesmo?" | não é dor | 0,70 | 0,55 | Sim |
| Sandra, "sim" para a avaliação da filha | "Isso mesmo, é a da Laura Duarte. Pode cancelar" | sim claro | 1,00 | 1,00 | Sim |
| Sandra, corrige o "sua avaliação" (4 testes) | "Não é minha, é da minha filha. Pode cancelar a dela" | não | 0,99 a 1,00 | 0,99 a 1,00 | Sim, em todas (não sai como sim) |
| Thiago, "Valeu!" | "Isso, pode cancelar sim. Valeu!" | sim claro | 1,00 | 1,00 | Sim |
| Thiago, depois de cancelado | "Não, valeu! Por enquanto deixa assim" | não | 1,00 | 1,00 | Sim |
| Júlia, "dói?" | "quanto custa? e dói? tenho muita sensibilidade" | pergunta sobre o procedimento | 0,70 | 0,55 | Sim (mas é o menos firme) |
| Júlia, "e se ela falar que dói muito?" | idem | pergunta sobre o procedimento | 1,00 | 1,00 | Sim |
| Dona Lourdes, implante e dentadura | "quanto custa o implante ou a dentadura?" | fora da lista | 0,94 e 0,98 | n/a | Sim |
| Diego, remarcar depois de faltar | "perdi a avaliação de ontem, vocês conseguem remarcar?" | quer remarcar | 0,99 e 0,95 | n/a | Sim |
| Urgência 3: "I am bleeding, what should I do?" | | urgente | 0,83 | n/a | Sim |
| Urgência 4: "mi cara está hinchada, ¿qué hago?" | | urgente | 0,74 | n/a | Sim |
| Urgência 5: "tengo mucho dolor, ¿qué puedo hacer?" | | urgente | 0,67 | n/a | Sim (no limite do 0,67) |
| Urgência 6: "estou com febre e dor forte" | | urgente | 0,69 | n/a | Sim |
| "não consigo engolir direito, a garganta fechando" (a lista de palavras não pega) | | urgente | 0,90 | n/a | Sim |
| "depois da anestesia estou com dificuldade de respirar" | | urgente | 0,93 | n/a | Sim |
| "minha gengiva está sangrando muito, é normal?" | | urgente | 0,59 | n/a | Sim, mas baixo |
| "não estou com febre", "I don't have a fever", "no tengo fiebre" e 8 parecidos | | não urgente | 0,02 a 0,03 | n/a | Sim, todos |
| "clareamento faz a gengiva sangrar?" | | não urgente | 0,02 | n/a | Sim |

A tabela completa (todas as linhas) está em `analise.txt`.

## Onde o Jev acertou

- **Urgência por sentido, não por palavra.** Pegou "não consigo engolir" e "dificuldade de respirar", que a lista de palavras de hoje não pega, e não deu alarme em nenhuma negação ("não estou com febre") nem em dúvida geral ("clareamento faz sangrar?").
- **"Dói?" é pergunta, não relato.** 18 de 18 na separação entre "estou com dor" e "isso dói?", inclusive os casos da Júlia.
- **Fora da lista.** Implante, dentadura e coroa sobre implante: 6 de 6 (menor probabilidade 0,86), sem nenhum alarme falso nas outras 179 mensagens.
- **Confirmação do cancelar nas conversas reais de teste.** Todos os "sim" da Bia, Paula, Sandra (filha), Júlia, Rafaela, Emily e Thiago saíram como sim claro (1,00). Todos os "não, é da minha filha" da Sandra saíram como não. Ou seja, o loop da Bia e da Sandra não aconteceria com o Jev lendo a resposta.
- **Horário.** 11 de 12 (o erro é discutível: "tem outro dia? esses não dão" ele leu como recusa, 0,90).

## Onde o Jev errou ou ficou fraco

- **"Sim" com outro assunto junto.** "sim, mas quanto custa a limpeza?", "sim, mas qual o endereço?" e "sim. aliás, vocês atendem sábado": o Jev deu sim claro com 0,99 a 1,00. É a mesma forma da frase da Bia ("sim, cancela, mas antes me responde..."), que deve cancelar. Só pelo sentido, os dois casos são quase iguais. Isso é decisão de regra, não erro de leitura: precisa de código em volta (veja a regra mista).
- **"sim, mas não cancela ainda".** Com a pergunta de confirmação sozinha, saiu sim com 0,55 e 0,56. Com uma pergunta separada ("o paciente pede para esperar ou manter?") saiu 0,97 e foi resolvido.
- **Urgência em dor forte que continua.** Camila (dor insuportável, depois de clareamento): 0,63 na primeira mensagem, 0,85 na segunda, e 0,32 a 0,54 nas mensagens seguintes em que ela só repete que está com medo. Dor forte relatada de forma indireta fica entre 0,3 e 0,7. Por isso o limiar de urgência precisa ser baixo (0,3).
- **Sem filtro do código, a confirmação é perigosa.** Em 158 falas em que a Clara NÃO tinha perguntado de cancelar, o Jev deu "sim claro" com mais de 0,67 em 30 e com mais de 0,93 em 15 (por exemplo, "Valeu, vou esperar a doutora"). A pergunta de confirmação só pode ser usada quando o código sabe que a última fala da Clara foi uma pergunta de cancelar.
- **Limite do teste.** Wagner ("a clínica não faz implante, mas...") ficou em 0,41 a 0,52 em "fora da lista". Deixei esses casos de fora das contas por serem discutíveis.

## Limiares sugeridos

| Decisão | Regra sugerida | Resultado no teste |
|---|---|---|
| **Urgência** (avisar a equipe, ação que se desfaz) | avisar se o Jev der 0,3 ou mais **OU** se a regra de hoje pegar | 0 urgências perdidas em 20 e 0 alarmes falsos em 170 mensagens normais |
| Urgência, com 0,67 | só 0,67 ou mais | perde 2 de 20: as de 0,59 e 0,63. Não usar 0,67 sozinho para urgência. |
| **Fora da lista** (responder que não fazemos) | 0,7 ou mais | 6 de 6, 0 alarmes falsos. Entre 0,3 e 0,7: mandar para a equipe. |
| **"Dói?" x relato de dor** | usar a escolha do Jev se a probabilidade for 0,67 ou mais; abaixo disso, tratar como relato (lado seguro) | 18 de 18 |
| **Cancelar** (ação sem volta) | só cancelar se **todas** valerem: a última fala da Clara foi pergunta de cancelar (código); P(sim claro) 0,93 ou mais; P(pede para esperar ou manter) menor que 0,3; e (a mensagem não tem "?" ou P(pede explicitamente para cancelar) 0,7 ou mais) | 1 cancelamento indevido em 18 casos que não podem cancelar ("sim. aliás, vocês atendem sábado"), 0 pedidos reais perdidos em 23 |
| Cancelar, só com P(sim claro) | qualquer limiar de 0,5 a 0,99 | **não dá zero erro**: 3 de 18 cancelariam sem dever (os "sim, mas..." com P de 0,99 a 1,00). Subir o limiar para 0,93 não resolve, porque o Jev está muito seguro do sim. |
| Cancelar, sem nenhuma dúvida | caso não passe nas regras acima, a Clara pergunta de novo, uma vez, "só para confirmar: responda SIM para cancelar" | evita o loop e evita cancelar sem querer |

Importante: o único caso que ainda passa pela regra mista é "sim. aliás, vocês atendem sábado" (sem "?"). Se esse risco não for aceitável, exigir sempre a palavra "cancela" ou "cancelar" na resposta (P(pede explicitamente para cancelar) 0,7 ou mais). Custo disso: respostas curtas como "sim" ou "isso mesmo" deixam de cancelar de primeira e a Clara pede "responda: cancelar". Isso é uma escolha de produto, não do Jev.

## Custo e tempo

| Item | Valor medido |
|---|---|
| Tempo por chamada (6 perguntas juntas) | média 0,46 s; mediana 0,41 s; 95% abaixo de 0,57 s; máximo 1,87 s |
| Tokens de entrada por chamada | média 1.761 (mín. 1.260, máx. 2.748); saída grátis |
| Custo por mensagem do paciente | US$ 0,000074 (menos de um centésimo de centavo) |
| Custo por 1.000 mensagens | US$ 0,074 |
| Gasto total da bancada | cerca de US$ 0,03 (limite era US$ 3) |

Para uma clínica com 3.000 mensagens por mês, o Jev custaria uns US$ 0,22 por mês. O custo de tempo (meio segundo) cabe na pausa humana que a Clara já faz antes de enviar.

## Riscos

- **Privacidade (o maior).** O texto do paciente (que pode ter dor, sintomas, nome) iria para os servidores da TypeSafe nos EUA, e hoje não existe plano de retenção zero. É dado de saúde, protegido pela LGPD. Antes de usar com paciente real: contrato ou aceite de tratamento de dados com a TypeSafe, aviso na política de privacidade, e (se possível) tirar nome e telefone antes de enviar. O teste da bancada usou só conversa inventada.
- **Dependência.** Se a TypeSafe ficar fora do ar ou mudar o modelo ("jev-latest" muda de versão), as respostas mudam. Usar uma versão fixa (hoje `jev-1.14.0`) e testar de novo antes de trocar.
- **Amostra pequena.** São 20 urgências, 6 fora da lista, 41 confirmações. Os pacientes são simulados por IA, e os rótulos foram feitos por mim. Antes de ligar em produção, repetir com os casos reais que aparecerem (sem dado pessoal).
- **Excesso de confiança.** O Jev dá 1,00 em frases ambíguas. Probabilidade alta não prova que a regra de negócio está certa (caso "sim, mas...").
- **Mais uma peça para manter.** Perguntas, regras de código e limiares precisam de revisão a cada mudança, e a chave fica no `.env` do servidor.

## Recomendação

**Usar, como segunda barreira, só depois de resolver privacidade/contrato.** Nunca no lugar das regras de hoje.

Como encaixar no fluxo (n8n), sem mudar nada agora:

1. Um passo novo, antes de "Decidir a ação", chama o Jev com as últimas 6 trocas e as perguntas de urgência, dor, fora da lista e (quando a regra de código disser que a Clara perguntou) confirmação. Uma chamada só, cerca de 0,5 s.
2. **Urgência: OU.** Se a regra de palavras de hoje OU o Jev (0,3 ou mais) apontar urgência, vai para a equipe. Quem nunca tira urgência é o código. O Jev só soma.
3. **Fora da lista e "dói?": o Jev informa, o código decide.** Jev 0,7 ou mais em "fora da lista" vira a resposta fixa de que não fazemos. "Dói?" deixa de ser tratado como relato de dor, a não ser que a probabilidade fique abaixo de 0,67.
4. **Cancelar: E.** Só cancela se a regra de hoje não bloqueou E o Jev passou nas regras mistas. Em caso de dúvida a Clara pergunta de novo uma vez, em frase mais fácil de responder.
5. **Se o Jev falhar** (erro, passou de 3 segundos, chave inválida, resposta estranha): seguir só com as regras de hoje, sem erro para o paciente, e registrar o fato. Nunca tratar falha do Jev como "não".
6. Começar em **modo sombra**: o Jev responde, o fluxo grava o que ele diria, mas quem decide continua sendo a regra de hoje. Depois de 1 a 2 semanas com os dados reais da clínica parceira, comparar e só então ligar.

Próximo passo sugerido para o PM técnico: decidir a política de privacidade (item 1 dos riscos) e, se for em frente, abrir a feature "Jev em modo sombra" (conversa nova, com o plano em `tecnico/n8n/PLANO-PACOTE-E.md`).
