# Prompt de teste: Pacote A do fluxo da Clara (18/11/2026)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. **Só use depois que a Erica confirmar que o fluxo foi publicado na demo** (a conversa que corrigiu avisa).

---

Projeto Keshion. Quero testar o Pacote A publicado na Clara da demo em 18/11 (itens A1 a A8 de `tecnico/n8n/codex-18-11/PLANO-CORRECOES.md`). Leia `CLAUDE.md` e esse plano. **Não mude nada no fluxo, nas instruções nem no servidor:** só rode os testes, confira e me traga o resultado. Se achar problema, descreva; quem corrige é outra conversa.

## O que mudou (em uma linha cada)

- **A1 avisos:** só deixa de avisar a equipe quando a mensagem nova é confirmação pura (ok, obrigada, valeu, 👍, thanks, gracias...). Informação nova gera aviso ou complemento (no máximo 1 complemento a cada 15 min). Urgência (sangramento, inchaço, febre, dor forte, pus, desmaio) sempre gera aviso novo marcado **URGENTE**, mesmo se a IA só respondeu.
- **A2 recusas:** contador `recusas_agenda` na ficha. 1ª recusa por data não reconhecida: a Clara pede o dia e o mês ("por exemplo 19/11"), sem dizer "indisponível". Da 2ª em diante: diz que a equipe vai confirmar o horário e a equipe recebe aviso com o motivo técnico. Zera ao marcar, remarcar ou cancelar.
- **A3 e A4 data e hora:** aceita hoje/amanhã/depois de amanhã nos 3 idiomas; data e hora precisam estar juntas na mesma mensagem e ligadas entre si (não junta o dia de uma opção com a hora de outra); minutos, mês e ano têm de bater; segundos diferentes de zero são recusados; "não posso", "outro horário" depois da oferta invalidam a oferta.
- **A5 cancelar:** só cancela se a última fala da Clara foi pergunta de confirmação (certo?, correct?, ¿correcto?) **e** a paciente disse que sim. "Não, quero manter" recebe "sua avaliação continua marcada".
- **A6 idioma:** campo `idioma` na resposta da IA; frases fixas (recusa, ocupado, dados, falha, "só um instante", confirmação de cancelamento) em pt, en e es.
- **A7:** "I'll forward / let me check / voy a pasar / le paso / te aviso" também viram aviso para a equipe.
- **A8:** trava da vaga de 5 min e tempo limite de 30 s nas chamadas ao Google da marcação.

Testes locais já passaram (sem custo, podem ser repetidos depois de `python tecnico/n8n/gerar_fluxos.py clinica-demo`): `node tecnico/n8n/teste_validacao_data_hora.js` (61 + 32), `node tecnico/n8n/teste_pacote_a.js` (48) e os dois do Codex em `tecnico/n8n/codex-18-11/` (extras: 27 de 33; os 6 restantes são formatos que não adivinhamos de propósito, como "às nove" por extenso, "next Friday" e "12/1").

## Antes de começar

- Confirme que nenhum outro teste está rodando: `select telefone, atualizado from pacientes where telefone like '554199900%' and atualizado > now() - interval '10 minutes'` no banco `clara`. Se houver, pare e me avise.
- Confirme que as colunas novas existem: `select recusas_agenda, ultimo_complemento from pacientes limit 1` no banco `clara`.
- Um teste por vez. Só números com prefixo `554199900`. Anote a hora de Curitiba e se a clínica estava aberta.
- Os casos 1 a 7 são conversas sintéticas, uma mensagem por vez, pelo mesmo caminho do `teste_n8n.py` (webhook da demo, número de teste novo para cada caso, por exemplo finais 961 a 967). Espere a resposta da Clara (saidas_teste) antes da próxima mensagem. Para cada caso, guarde as saídas (paciente e equipe) e a ficha no fim.

## Casos, nesta ordem

1. **Sangramento depois de aviso de recibo** (final 961): pedir recibo do pagamento; esperar o aviso administrativo; depois mandar "Agora comecei a sangrar muito". Esperado: novo aviso **URGENTE** para a equipe. Depois mandar "ok obrigada": nenhum aviso novo.
2. **"amanhã às 11h"** (final 962): pedir para marcar avaliação "amanhã às 11h", com nome completo e telefone. Se amanhã tiver avaliação às 11h livre, esperado: marca. Se não, a Clara oferece outras ou pede a data; nunca três "não está disponível" seguidos.
3. **2ª recusa gera aviso** (final 963): insistir duas vezes num horário que a demo não tem (por exemplo "sábado às 10h", depois "então sábado às 10h mesmo"). Esperado: 1ª recusa com outras opções; na 2ª, "vou pedir para a equipe confirmar esse horário" e aviso para a equipe com o motivo técnico; ficha com `recusas_agenda` = 2.
4. **Cancelar em inglês com "Yes"** (final 964): marcar em inglês, pedir para cancelar, responder só "Yes" à pergunta de confirmação. Esperado: cancela já nessa resposta (sem pedir confirmação a mais), tudo em inglês, ficha sem evento, Google sem o evento.
5. **Recusa de "não, quero manter"** (final 965): marcar em português, pedir para cancelar, responder "Não, quero manter". Esperado: avaliação continua (ficha e Google com o evento), resposta "continua marcada". Depois cancelar de verdade para limpar.
6. **Espanhol** (final 966): conversa inteira em espanhol até marcar e cancelar; provocar uma frase fixa (por exemplo pedir horário inexistente uma vez). Esperado: nenhuma frase em português.
7. **Opções sem misturar** (final 967): quando a Clara oferecer 19/11 às 9h ou 24/11 às 16h (ou parecido), responder "24/11 às 16h". Esperado: marca 24/11 às 16h. Se a IA tentar gravar 19/11 às 16h, o fluxo tem de recusar. Anote o horário gravado no Google.
8. **5 perfis de agenda:** `python tecnico/teste-ab/paciente_simulado.py 801 803 807 811 815`. Quem marcou antes tem de continuar marcando; Emily (815) em inglês sem frase fixa em português.
9. **Rodada completa de 22 perfis**, se possível com a clínica aberta: `python tecnico/teste-ab/paciente_simulado.py`. Comparar com 18/11 manhã (6 a 9; Emily 2).
10. **56 mensagens fixas** (`teste_n8n.py`, no servidor, como em `tecnico/testes-checklist.md`): 56 de 56 sem falha técnica.
11. **Limpeza:** apagar fichas, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` dos números de teste usados; listar eventos dos próximos 30 dias no Google e apagar os de teste que sobraram (o script só limpa o que a ficha lembra). Não apagar o evento antigo do Henrique (final 810) sem a Erica.

## O que me trazer

- Tabela dos casos 1 a 7: esperado, o que aconteceu, OK ou problema, com as saídas que provam.
- Notas dos 5 e dos 22 perfis comparadas às anteriores, custo e hora de Curitiba.
- Resultado das 56 mensagens e da limpeza (o que foi apagado e o que sobrou).
- Problemas novos, do mais grave ao mais leve, em linguagem simples.
