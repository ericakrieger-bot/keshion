# Erros do teste da demo (Erica, 24/11/2026)

Teste feito pela Erica no WhatsApp dela, com a Clara da Dra. Suzana. Sem dados de pacientes.
Status: itens 1, 2 e 5 aprovados pela Erica e aplicados no `gerar_fluxos.py` em 24/11 (testes locais: Pacote C 75/75, Pacote A 48/48, data e hora 61/61 e 32/32). Ainda não publicados. Itens 3 e 4 esperam a resposta da Erica sobre o valor dos retornos.

Detalhe aplicado: o reinício também aceita `# reiniciar` e `reiniciar` sem o #; a espera do envio anterior subiu de 60 s para 180 s, para acompanhar o "digitando" mais longo.

| # | Erro | Prioridade | Tipo de correção |
|---|---|---|---|
| 1 | "#reiniciar" não começa conversa nova | 🔴 | fluxo |
| 2 | Clara responde rápido demais (paciente ainda está escrevendo) | 🔴 | fluxo |
| 3 | Base não diz se os retornos são pagos nem o valor | 🟡 | texto (base) |
| 4 | Questionário não pergunta sobre retornos pagos | 🟡 | texto (questionário da Erica) |
| 5 | "Digitando" curto em mensagem comprida | 🟡 | fluxo |
| 6 | Marcação: parece ok, a Erica vai testar de novo | ⚪ | nenhuma por enquanto |

## 1. Reiniciar não funciona 🔴

**O que a Erica viu:** depois de reiniciar, a Clara continua lembrando da conversa anterior.

**Causa (achada no `gerar_fluxos.py`, nó "Apagar a conversa de teste"):**
- O reinício apaga a conversa, o nome, o tratamento e a avaliação, mas **não apaga** o nome completo, o telefone de contato, o último aviso para a equipe e o horário do último envio. O nome completo e o telefone vão para a Clara em toda mensagem, então ela "sabe" quem é a pessoa e age como se a conversa continuasse.
- O comando só vale se for exatamente `#reiniciar` (com o #) e vier de um número da lista `numeros_keshion` em `clinica.json` (hoje 2 números). De outro número, ou sem o #, a mensagem vai para a Clara como texto normal e o histórico fica.
- Se o `#reiniciar` chegar enquanto a Clara ainda está respondendo a mensagem anterior, essa resposta pode ser gravada depois e trazer a conversa velha de volta.

**Correção proposta (fluxo):** o reinício passa a apagar todos os campos da ficha; aceitar também `reiniciar` sem o # e com espaço depois do #; e a resposta que estava em andamento é descartada se a ficha foi reiniciada no meio.

**Dúvida para a Erica:** você recebeu a mensagem "Conversa reiniciada..."? Se não recebeu, o número do seu WhatsApp precisa entrar na lista.

## 2. Espera antes de responder 🔴

**O que a Erica viu:** a paciente manda 2 ou 3 mensagens seguidas e a Clara responde antes de ela terminar.

**Causa:** a Clara espera só 7 segundos depois da última mensagem (nó "Esperar 7 s"). Cada mensagem nova recomeça a contagem, mas 7 s é pouco para quem digita devagar.

**Correção proposta (fluxo):** subir para 20 segundos depois da última mensagem. Se chegar outra mensagem nesse tempo, a contagem recomeça, e a Clara responde tudo junto.

## 3. Retornos pagos na base 🟡

**O que falta:** a base diz que no alinhador a visita à clínica é a cada 2 meses, mas não diz se essas visitas são pagas nem quanto custam. O mesmo vale para retornos de outros tratamentos.

**Correção proposta (texto da base, `base-clinica.md`):** acrescentar uma linha por tratamento com retorno, por exemplo: "Retornos do alinhador (a cada 2 meses): incluídos no valor do tratamento" ou "pagos, R$ X por visita". Depois, rodar `preparar_banco.py clinica-demo` e aplicar no banco (com OK).

**Dúvida para a Erica:** na demo, os retornos do alinhador são incluídos ou pagos? Se pagos, qual valor?

## 4. Pergunta no questionário 🟡

O questionário modelo (`clientes/_modelo/questionario-curto-clinica-dia-a-dia.md`) é da Erica e não foi editado. Pergunta sugerida para ela incluir:

> "Os retornos e as manutenções dos tratamentos (por exemplo, alinhador, aparelho, implante) são pagos à parte ou já estão incluídos no valor? Se forem pagos, qual o valor de cada retorno?"

## 5. Tempo de "digitando" 🟡

**O que a Erica viu:** em mensagem comprida, o "digitando" dura pouco.

**Causa:** o tempo é 1 segundo a cada 5 letras, com mínimo de 3 e **máximo de 30 segundos** (nó "Separar em mensagens", fluxo de envio). Toda mensagem com mais de 150 letras fica nos 30 s.

**Correção proposta (fluxo):** 1 segundo a cada 4 letras, mínimo de 4 e máximo de 50 segundos. Exemplos: 100 letras, 25 s; 200 letras, 50 s. Junto com a espera do item 2, uma resposta longa pode levar perto de 1 minuto e meio para chegar inteira.

## 6. Marcação ⚪

A Erica achou que a Clara marca, mas vai testar de novo. Entra no prompt de teste.
