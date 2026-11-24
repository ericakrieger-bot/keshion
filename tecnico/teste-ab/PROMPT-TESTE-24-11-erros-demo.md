# Prompt de teste de 24/11/2026: correções do teste da Erica na demo

Publicado na demo (`ClaraEnvio000001` e `ClaraAtendimento`) em 24/11 às 07h20 do horário do servidor. Versão anterior guardada em `/opt/keshion/versoes/clinica-demo/*-20261124-0719.json`.

Antes de colar, a Erica confere o saldo da Anthropic (acima de US$ 3) e deixa o PC ligado sem suspender.

**Teste manual da Erica, no WhatsApp dela (fora da conversa de testes):** mande `#reiniciar`. Tem que chegar "Conversa reiniciada...". Depois mande "oi": a Clara tem que tratar como primeiro contato, sem lembrar nome nem conversa anterior. Se a mensagem "Conversa reiniciada" não chegar, o número dela não está em `numeros_keshion` (`clientes/clinica-demo/clinica.json`) e isso volta para a conversa de correções.

---

Projeto Keshion. Quero testar as correções de 24/11 da Clara da demo. Leia `CLAUDE.md` e `tecnico/teste-ab/2026-11-24-erros-teste-demo-erica.md`. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado. Só números com prefixo `554199900`, um teste por vez.

Antes de começar: confirme que nenhum outro teste está rodando (fichas `554199900%` mexidas nos últimos 10 minutos no banco `clara`).

O que mudou e o que conferir:

1. **Espera de 20 s (era 7 s).** Rode `tecnico/teste-ab/teste_n8n.py`. Nos casos com 2 ou 3 mensagens seguidas, tem que sair **uma resposta só**, cobrindo todas. Traga o tempo ("segundos") de cada resposta: nenhuma pode chegar antes de 20 s. Faça também um caso à parte: 2 mensagens com 12 s entre elas (use a função `enviar` do `teste_n8n.py` com um número `554199900` novo). Tem que sair uma resposta só, uns 20 s depois da segunda.
2. **"Digitando" mais longo.** Na tabela `saidas_teste` do banco `clara`, traga `typing_time` e o tamanho do texto das mensagens desta rodada. A regra nova: 1 s a cada 4 letras, mínimo 4 e máximo 50 (antes o máximo era 30). Confira que as mensagens com mais de 120 letras passam de 30 s e nenhuma passa de 50 s, e que as mensagens de uma mesma resposta saem na ordem certa.
3. **Respostas em sequência não se misturam.** Com o "digitando" maior, a Clara espera o envio anterior terminar (até 180 s). Confira em `teste_n8n.py` se alguma resposta saiu fora de ordem ou se apareceu "SEM RESPOSTA EM 300 s" (o limite dos scripts subiu de 150/160 s para 300 s).
4. **Marcação.** Nos casos de marcar, remarcar e cancelar do `teste_n8n.py`: evento criado, mudado e apagado no Google Agenda, aviso para a equipe e despedida 1 minuto depois. No cancelamento, conte quantas vezes a Clara pergunta se quer cancelar (tem que ser uma vez só, correção de 23/11).
5. **Paciente simulado.** Rode `tecnico/teste-ab/paciente_simulado.py` (22 perfis). Compare a média com 17/11 (7,23), 18/11 (7,05) e Codex 19/11 (7,32). Traga os perfis com nota abaixo de 6.

Horário de Curitiba e se a clínica estava aberta em cada rodada, como sempre. Se o teste parar de ler as respostas ("ERRO DE LEITURA"), não conte as notas: me diga e repita o que faltou.

Ao fim, atualize `tecnico/testes-checklist.md` (Registro de rodadas) e `tecnico/RETOMAR-AQUI.md`, e faça commit só dos seus arquivos. Push só com OK da Erica.
