# Prompt de teste de 25/11/2026: Pacote E, parte 1 (cancelar, urgência, só português)

No ar na demo e na clínica de teste desde 25/11, às 09h26 do servidor:
- **Cancelar:** a ficha guarda qual avaliação espera o "sim" (colunas `cancelar_evento`, `cancelar_pedido_em` e `cancelar_tentativas`, que valem 24 h). Na 3ª resposta sem decisão, a equipe assume.
- **Urgência:** dificuldade de engolir, de respirar, falta de ar e não conseguir abrir a boca.
- **Só português:** sem frases fixas em inglês ou espanhol. O perfil Emily virou Larissa, que manda várias mensagens curtas seguidas.

Cópia anterior dos fluxos: `/opt/keshion/versoes/clinica-demo/*-20261125-0926.json` e `/opt/keshion/versoes/clinica-teste/*-20261125-0926.json`.

Ainda **não** entrou (fica para as próximas partes do Pacote E): Diego (remarcar depois de falta), listas "fazemos / não fazemos", mensagem padrão de confirmação, tom único, espera maior e juíza nova. Nota baixa nesses pontos não é falha desta rodada.

## Antes de colar (Erica, uns 5 min)

1. Chave de testes da Anthropic no `.env` da pasta `keshion` e saldo acima de US$ 3.
2. PC na tomada e o Claude aberto até o fim.

---

Projeto Keshion. Quero testar a parte 1 do Pacote E da Clara da demo: cancelar, urgência e só português. Leia `CLAUDE.md` e `tecnico/n8n/PLANO-PACOTE-E.md`. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado. Só números com prefixo `554199900`, um teste por vez.

**Antes de qualquer teste:**
- Confira o saldo da Anthropic. Se estiver abaixo de US$ 3, pare e avise.
- Confirme que nenhum outro teste está rodando: nenhuma ficha `554199900%` mexida nos últimos 10 minutos no banco `clara`.
- Confirme que a chave do `.env` é a de testes, sem mostrar o valor.

**Parte 1: casos manuais de cancelar** (função `enviar` do `teste_n8n.py`, um número `554199900` novo por caso). Em cada caso, primeiro marque uma avaliação num dia útil daqui a pelo menos 3 dias, num horário que a Clara ofereceu. Depois mande "quero cancelar minha avaliação" e, na resposta à pergunta de confirmação, mande:
1. "Valeu!" → cancela, e o evento some do Google Agenda.
2. "Sim, quero cancelar a da minha filha Laura, dia DD/MM às HHh, ela não vai poder ir" → cancela.
3. "mas antes me responde: tem multa se eu cancelar?" → a Clara responde e pergunta de novo se pode cancelar, citando dia e hora. Depois mande "sim": cancela.
4. "não é minha, é da Laura" → **não** cancela, **não** diz "continua marcada" e segue confirmando. Depois mande "isso, pode cancelar": cancela.
5. "não, quero manter" → não cancela e diz que continua marcada. O evento continua na agenda.
6. Três respostas sem decisão seguidas ("hmm", "deixa eu ver", "não sei") → na 3ª, a Clara diz que a equipe vai confirmar, e chega o aviso "Chamar uma pessoa" com o dia da avaliação. O evento **não** é apagado.

Em cada caso, traga:
- a conversa completa;
- quantas vezes a Clara perguntou se podia cancelar (no máximo 2, fora o caso 6);
- se o evento existe no Google Agenda no fim;
- os campos `cancelar_evento` e `cancelar_tentativas` da ficha no fim. Têm que estar vazio e 0 depois de cancelar ou manter.

**Parte 2: urgência** (um número novo por frase, sem marcar nada):
- "não consigo engolir direito desde ontem"
- "estou com falta de ar e o rosto inchando"
- "tô com dificuldade pra respirar, é normal?"

Esperado nas três: aviso **URGENTE** para a equipe e a resposta fixa de urgência.

Controles, que não podem virar urgência: "o clareamento dói?" e "dói pra engolir depois da extração?".

**Parte 3: paciente simulado, só estes perfis:**

```
python tecnico/teste-ab/paciente_simulado.py 801 803 806 809 815 820
```

São Bia, Camila, Sandra, Júlia, Larissa e Thiago.
- Compare a nota de cada um com a rodada de 24/11: Bia 2, Camila 7, Sandra 2, Júlia 6, Thiago 5. A Larissa é nova.
- Bia, Sandra e Thiago não podem entrar em loop de cancelar.
- Na Larissa, tem que sair uma resposta só para as mensagens picadas, sem frase repetida.
- Em nenhuma conversa pode aparecer inglês ou espanhol.

Horário de Curitiba e se a clínica estava aberta, como sempre. Se aparecer "ERRO DE LEITURA", a rodada é INVÁLIDA: me diga e repita o que faltou.

**Limpeza no fim:** mande `#reiniciar` nos números usados e confira no Google Agenda que não ficou nenhum evento desta rodada. Traga a lista do que apagou.

Ao fim, atualize `tecnico/testes-checklist.md` (Registro de rodadas) e `tecnico/RETOMAR-AQUI.md`, e faça commit só dos seus arquivos. Push só com OK da Erica.
