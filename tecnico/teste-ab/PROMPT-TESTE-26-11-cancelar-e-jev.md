# Prompt de teste de 26/11/2026: correção do cancelar e Jev em modo sombra (um teste só)

O que entrou na publicação de 26/11 (demo e clínica de teste), o "Jeito 1" aprovado pela Erica:
- **Cancelar:**
  - (a) a pendência também é gravada quando a própria IA pergunta ("é a de terça, 01/12, às 9h, certo?");
  - (b) "sim", "isso" ou "já falei / já confirmei" valem mesmo com outra pergunta junto;
  - (c) depois de passar para a equipe na 3ª resposta sem decisão, a Clara não recomeça a perguntar (a ficha fica "com a equipe", `cancelar_tentativas = 99`);
  - "não sei" conta como dúvida e não como "manter"; "prefiro reagendar" não cancela.
- **Urgência:** a resposta fixa sai sempre, sem promessa de encaixe. Para engolir, respirar e falta de ar, ela manda procurar pronto-socorro ou ligar para o 192.
- **Jev em modo sombra:** o Jev dá a opinião em cada resposta e grava na tabela `jev_sombra`. Ele não muda nada para o paciente.

Cópia anterior dos fluxos: `/opt/keshion/versoes/clinica-demo/ClaraAtendimento-20261126-HHMM.json` e `/opt/keshion/versoes/clinica-teste/TesteAtendimento-20261126-HHMM.json` (horário no `tecnico/RETOMAR-AQUI.md`).

**Fora desta rodada:** os itens 3 a 14 do Pacote E (Diego, listas da base, tom, espera, juíza) e o horário que fica reservado por 5 minutos. Nota baixa nesses pontos não é falha desta rodada.

## Antes de colar (Erica, uns 5 min)

1. Chave de testes da Anthropic no `.env` da pasta `keshion` e saldo acima de US$ 2.
2. PC na tomada e o Claude aberto até o fim.
3. **Um teste só.** O limite semanal do plano Pro está em 82%: não repita a rodada inteira se um caso falhar. Traga o resultado e pare.

---

Projeto Keshion. Quero testar a correção do cancelar de 26/11 e o Jev em modo sombra na Clara da demo. Leia `CLAUDE.md`, `tecnico/n8n/PLANO-PACOTE-E.md` e `tecnico/n8n/PLANO-JEV-SOMBRA.md`. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado. Só números com prefixo `554199900`, um teste por vez. **É um teste só, sem rodada dupla:** se algo falhar, registre e pare, sem repetir.

**Antes de qualquer teste:**
- Confira o saldo da Anthropic. Se estiver abaixo de US$ 2, pare e avise.
- Confirme que nenhum outro teste está rodando: nenhuma ficha `554199900%` mexida nos últimos 10 minutos no banco `clara`.
- Confirme que a chave do `.env` é a de testes, sem mostrar o valor.
- Anote quantas linhas a tabela `jev_sombra` do banco `clara` tem agora (esperado: 0).

**Parte 1: cancelar** (função `enviar` do `teste_n8n.py`, um número `554199900` novo por caso, diferente dos usados em 25/11). Em cada caso, primeiro marque uma avaliação num dia útil daqui a pelo menos 3 dias, num horário que a Clara ofereceu. Depois mande "quero cancelar minha avaliação".
1. **Caso 1, "Valeu!":** à pergunta de confirmação (com ou sem a palavra "cancelar"), responda "Valeu!". Esperado: cancela já nessa resposta e o evento some do Google Agenda. A Clara pergunta no máximo 1 vez.
2. **Caso 6, três respostas sem decisão:** responda "hmm", depois "deixa eu ver", depois "não sei". Esperado:
   - na 3ª, a Clara diz que a equipe vai confirmar o cancelamento, e chega o aviso "Chamar uma pessoa" com o dia da avaliação;
   - o evento **não** é apagado;
   - a ficha fica com `cancelar_evento` preenchido e `cancelar_tentativas = 99`.
   - Depois mande "ok, obrigada". Esperado: a Clara **não** pergunta de novo se pode cancelar e não cancela.
   - Por fim mande "já falei que pode cancelar". Esperado: cancela, o evento some e a ficha volta para `cancelar_evento` vazio e 0.

Em cada caso, traga a conversa completa, quantas vezes a Clara perguntou se podia cancelar, se o evento existe no Google Agenda no fim, e os campos `cancelar_evento` e `cancelar_tentativas` da ficha a cada passo.

**Parte 2: urgência** (um número novo por frase, sem marcar nada):
- "não consigo engolir direito desde ontem"
- "estou com falta de ar e o rosto inchando"
- "tô com dificuldade pra respirar, é normal?"

Esperado nas três:
- aviso **URGENTE** para a equipe;
- a resposta é a frase fixa: "Sinto muito que você esteja assim. Com esse sintoma, procure agora um pronto-socorro ou ligue para o 192, sem esperar o nosso retorno. Já avisei a nossa equipe.";
- **nenhuma** promessa de encaixe, de horário ou de retorno da Dra.

Controles, que não podem virar urgência: "o clareamento dói?" e "dói pra engolir depois da extração?". Diga também a hora de Curitiba e se a clínica estava aberta.

**Parte 3: Júlia** (só este perfil):

```
python tecnico/teste-ab/paciente_simulado.py 809
```

- Compare com 25/11 (nota 2, loop de cancelar).
- Esperado: sem loop. Ela confirma uma vez com clareza e cancela. Se passar para a equipe, a Clara não volta a perguntar.
- A ficha não pode terminar com a avaliação marcada se ela pediu para cancelar.
- Nenhum inglês ou espanhol.

**Parte 4: o quadro do Jev** (a Clara fez X, o Jev faria Y):
1. Confira no banco `clara`:
   `SELECT criado_em, right(telefone,4), ok, erro, ms, regra_rota, regra_urgencia, decide_urgencia, decide_dor, decide_fora, perguntou_cancelar, decide_cancelar FROM jev_sombra ORDER BY id DESC LIMIT 40;`
   - toda resposta da Clara desta rodada tem uma linha;
   - `ok = true` na maioria, com `ms` abaixo de 3000. Diga quantas deram falha e o motivo em `erro`.
2. Rode e cole o resultado inteiro:

```
python tecnico/jev-bancada/comparar_sombra.py clara 1
```

3. Monte o quadro "a Clara fez X, o Jev faria Y" para:
   - as 3 frases de urgência e os 2 controles;
   - as respostas dos casos 1 e 6 e da Júlia em que o cancelar estava em jogo.
   - Marque onde os dois discordam.
   - Lembrete: o Jev só opina, e quem decide continua sendo a regra.
4. Na execução do n8n, confira que os nós "Jev: ..." ficam verdes ou com `ok = false` sem parar o fluxo, e que rodam **depois** de "Enviar ao paciente e à equipe".

**Limpeza no fim:** mande `#reiniciar` nos números usados (lembrete: o `#reiniciar` não vale para os números `554199900`; nesse caso apague as fichas de teste pelo roteiro de sempre) e confira no Google Agenda que não ficou nenhum evento desta rodada. Traga a lista do que apagou. **Não apague** as linhas da `jev_sombra`: elas são a comparação.

Ao fim, atualize `tecnico/testes-checklist.md` (Registro de rodadas) e `tecnico/RETOMAR-AQUI.md`, e faça commit só dos seus arquivos de teste. O commit do Pacote E e o do Jev ficam para a conversa técnica, com OK da Erica. Push só com OK da Erica.
