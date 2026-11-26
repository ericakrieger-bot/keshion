# Prompt de teste de 20/11/2026: Pacote C, rodada completa (versão de hoje)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. Esta versão substitui o cabeçalho do `PROMPT-TESTE-19-11-pacote-c.md` (os casos 1 a 16 e o "O que me trazer" continuam os de lá).

Antes de colar, a Erica faz três coisas (15 min):

1. Cria a chave da Anthropic só para os testes no console e cola no `.env` da pasta `keshion` do PC (variável `ANTHROPIC_API_KEY`). Nunca no chat. A chave da Clara no servidor não muda.
2. Confere o saldo da conta da Anthropic. Se estiver abaixo de US$ 3, recarrega antes: sem saldo a Clara responde "Só um instante" e a rodada fica inválida.
3. Deixa o PC ligado na tomada, sem suspender, e não fecha o Claude até a rodada acabar (a rodada de 19/11 às 08h20 foi perdida porque o teste parou de ler as respostas).

---

Projeto Keshion. Quero testar o Pacote C da Clara, publicado na demo e na clínica de teste em 20/11 às 10h42 de Curitiba. Leia `CLAUDE.md`, `tecnico/n8n/codex-19-11/PLANO-CORRECOES-2.md` e `tecnico/teste-ab/PROMPT-TESTE-19-11-pacote-c.md`, e siga os casos 1 a 16 desse arquivo, nesta ordem, um teste por vez. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado.

Mudanças desta versão:

- **Antes de qualquer teste:** confira o saldo da Anthropic pelo console (ou peça à Erica o valor). Abaixo de US$ 3, pare e avise. Confirme também que nenhum outro teste está rodando (consulta de fichas `554199900%` mexidas nos últimos 10 minutos no banco `clara`).
- **Chave nova:** o `paciente_simulado.py` lê a chave do `.env` da raiz. Confirme que ela é a chave de testes (não mostre o valor) e que o custo mostrado no fim bate com o consumo no console.
- **Rodada de 22 perfis e 56 mensagens:** a Codex já rodou as duas em 19/11 (56 de 56, média 7,32 nos 22 perfis), mas antes do Pacote C. Rode de novo agora para valer sobre o fluxo publicado. Compare com 17/11 (7,23), 18/11 (7,05) e Codex 19/11 (7,32).
- **Se o teste parar de ler as respostas** (aviso "ERRO DE LEITURA" do Pacote D3, rodada marcada INVÁLIDA), não conte as notas: me diga e repita o que faltou.
- **Cancelamento perguntado duas vezes (achado de 18/11):** no caso 2, conte quantas vezes a Clara pergunta se quer cancelar e traga a conversa completa. Está em investigação em outra conversa; só registre.
- Horário de Curitiba e se a clínica estava aberta em cada rodada, como sempre.

Ao fim, atualize `tecnico/testes-checklist.md` (Registro de rodadas) e `tecnico/RETOMAR-AQUI.md`, e faça commit só dos seus arquivos. Push só com OK da Erica.
