# Prompt de teste de 24/11/2026: Pacote C + cancelar + correções do teste da Erica (rodada única)

Substitui, para a próxima rodada, o `PROMPT-TESTE-20-11-pacote-c-rodada-completa.md` (que nunca chegou a rodar). Os casos 1 a 16 continuam os de `PROMPT-TESTE-19-11-pacote-c.md`.

No ar na demo: Pacote C (20/11), correção do cancelar (23/11) e correções de 24/11 (reiniciar, espera de 20 s, "digitando" de até 50 s), publicadas às 07h20 do servidor. Cópia anterior em `/opt/keshion/versoes/clinica-demo/*-20261124-0719.json`.

## Antes de colar (Erica, uns 15 min)

1. **Base com os retornos do alinhador publicada** (conversa de correções de 24/11). Sem isso, o perfil do alinhador testa a base velha.
2. **Fazer antes de 26/11:** a autorização do Google Agenda vence por volta de 26/11. Depois disso, os casos de marcar falham por causa da autorização, não da Clara.
3. Chave de testes da Anthropic no `.env` da pasta `keshion` (nunca no chat) e saldo acima de US$ 3.
4. PC na tomada, sem suspender, e o Claude aberto até o fim. A rodada fica mais lenta que a de 19/11 por causa da espera de 20 s.
5. **Teste manual no seu WhatsApp:** mande `#reiniciar`. Tem que chegar "Conversa reiniciada...". Depois mande "oi": a Clara tem que tratar você como primeiro contato. Se não chegar a mensagem, o seu número não está em `numeros_keshion` e isso volta para a conversa de correções. Por último, mande `#reiniciar` de novo, para não deixar ficha de teste.

---

Projeto Keshion. Quero rodar o teste do Pacote C da Clara da demo junto com a correção do cancelar (23/11) e as correções de 24/11. Leia `CLAUDE.md`, `tecnico/teste-ab/PROMPT-TESTE-19-11-pacote-c.md` e `tecnico/teste-ab/2026-11-24-erros-teste-demo-erica.md`. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado. Só números com prefixo `554199900`, um teste por vez.

**Antes de qualquer teste:** confira o saldo da Anthropic (abaixo de US$ 3, pare e avise) e confirme que nenhum outro teste está rodando (fichas `554199900%` mexidas nos últimos 10 minutos no banco `clara`). Confirme que a chave do `.env` é a de testes (sem mostrar o valor).

**Parte 1: casos 1 a 16 do `PROMPT-TESTE-19-11-pacote-c.md`, nesta ordem.** Mudanças:
- Caso 2 (cancelar): conte quantas vezes a Clara pergunta se quer cancelar. Tem que ser **uma vez só** (correção de 23/11). Traga a conversa completa.
- Caso 9: troque "24/11 às 11h" por um dia útil daqui a pelo menos 3 dias, num horário que a Clara ofereceu.
- Casos 14 (22 perfis) e 15 (56 mensagens): os scripts agora esperam até 300 s por resposta. "SEM RESPOSTA EM 300 s" é falha a registrar.

**Parte 2: critérios novos de 24/11.**
1. **Espera de 20 s.** Nos casos com 2 ou 3 mensagens seguidas do `teste_n8n.py`, tem que sair **uma resposta só**, cobrindo todas, e nenhuma resposta antes de 20 s (traga a coluna "segundos"). Caso à parte: 2 mensagens com 12 s entre elas (função `enviar` do `teste_n8n.py`, número `554199900` novo). Tem que sair uma resposta só, uns 20 s depois da segunda.
2. **"Digitando".** Na `saidas_teste` desta rodada, traga `typing_time` e o tamanho do texto. Regra: 1 s a cada 4 letras, mínimo 4 e máximo 50. Mensagens com mais de 120 letras passam de 30 s, nenhuma passa de 50 s, e as mensagens de uma mesma resposta saem na ordem certa.
3. **Ordem entre respostas seguidas.** Nenhuma resposta fora de ordem (a Clara espera até 180 s o envio anterior terminar).
4. **Retornos do alinhador.** Número `554199900` novo: "oi, os retornos do alinhador são pagos à parte?". Esperado: a Clara diz que as visitas de retorno, a cada 2 meses, já estão incluídas no valor do tratamento.
5. **Marcação.** Nos casos de marcar, remarcar e cancelar: evento criado, mudado e apagado no Google Agenda, aviso para a equipe e despedida 1 minuto depois.

**Como avaliar a média dos 22 perfis:** compare com 17/11 (7,23), 18/11 (7,05) e Codex 19/11 (7,32). Traga à parte a média dos perfis de paciente antigo: a regra nova para eles só entra em 27/11, então nota baixa ali é esperada e não é falha desta rodada. Traga os perfis com nota abaixo de 6 e o motivo.

Horário de Curitiba e se a clínica estava aberta em cada rodada, como sempre. Se aparecer "ERRO DE LEITURA", a rodada é INVÁLIDA: não conte as notas, me diga e repita o que faltou. Faça a limpeza do caso 16 no fim.

Ao fim, atualize `tecnico/testes-checklist.md` (Registro de rodadas) e `tecnico/RETOMAR-AQUI.md`, e faça commit só dos seus arquivos. Push só com OK da Erica. Depois, lembre a Erica da revisão do Codex (`tecnico/n8n/PROMPT-CODEX-REVISAO.md`) sobre o Pacote C, o cancelar e as correções de 24/11.
