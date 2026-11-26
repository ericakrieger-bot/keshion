# Prompt de teste: Jev em modo sombra (para colar na conversa de testes, só DEPOIS da publicação)

Colar o texto abaixo na conversa de testes da Erica. Só vale depois que o Jev em modo sombra estiver publicado (tabela `jev_sombra` criada, credencial "TypeSafe" no n8n e fluxo importado).

---

Projeto Keshion. Teste do **Jev em modo sombra** na clínica demo (plano: `tecnico/n8n/PLANO-JEV-SOMBRA.md`). Um teste por vez, só números com prefixo `554199900`.

1. Antes: `cd tecnico/n8n && python gerar_fluxos.py clinica-demo --jev-teste && node teste_jev_sombra.js` (tem de dar 40 de 40).
2. Rodar `teste_n8n.py` normal na demo e conferir que **as respostas são as mesmas de sempre** (o Jev não pode mudar nada para o paciente nem atrasar a resposta).
3. Mandar, com números `554199900...` diferentes, estas conversas curtas pelo webhook (como o `teste_n8n.py` faz):
   - "não consigo engolir direito, a garganta está fechando" (esperado na tabela: `decide_urgencia = true`);
   - "a limpeza dói?" (esperado: `decide_dor = pergunta`);
   - "quanto custa o implante?" (esperado: `decide_fora = nao_fazemos`);
   - marcar uma avaliação, pedir para cancelar e responder "Isso, pode cancelar sim. Valeu!" à pergunta de confirmação (esperado na linha da resposta: `perguntou_cancelar = true` e `decide_cancelar = cancela`).
4. Conferir no banco `clara`: `SELECT criado_em, right(telefone,4), ok, erro, ms, regra_rota, regra_urgencia, decide_urgencia, decide_dor, decide_fora, perguntou_cancelar, decide_cancelar FROM jev_sombra ORDER BY id DESC LIMIT 10;`
   - toda resposta da Clara tem uma linha; `ok = true`; `ms` abaixo de 3000;
   - no n8n, a execução fica verde e os nós "Jev: ..." aparecem **depois** de "Enviar ao paciente e à equipe".
5. Queda do Jev (com OK da Erica, só na clínica de teste): trocar por alguns minutos a credencial "TypeSafe" da clínica de teste por uma chave errada, mandar uma mensagem e conferir que a Clara responde normal e a linha fica com `ok = false` e o motivo em `erro`. Voltar a chave certa.
6. Rodar `python tecnico/jev-bancada/comparar_sombra.py clara 1` e colar o resultado.
7. Registrar em `tecnico/testes-checklist.md` e apagar os eventos de teste da agenda.
