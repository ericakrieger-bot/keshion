# Prompt de teste: Pacote C do fluxo da Clara (19/11/2026)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. **Só use depois que a Erica confirmar que o Pacote C foi publicado na demo e na clínica de teste** (a conversa que corrigiu avisa). A rodada de 5 e de 22 perfis e as 56 mensagens têm de ser rodadas num terminal da Erica, com o PC acordado (sem suspender, sem fechar o Claude).

---

Projeto Keshion. Quero testar o Pacote C publicado na Clara (itens C1 a C7 de `tecnico/n8n/codex-19-11/PLANO-CORRECOES-2.md`). Leia `CLAUDE.md` e esse plano. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode os testes, confira e me traga o resultado. Se achar problema, descreva; quem corrige é outra conversa.

## O que mudou (em uma linha cada)

- **C1 cancelar:** só cancela se a última fala da Clara fala de cancelar e é pergunta, e a resposta da paciente é um "sim" curto, sem pergunta nem outro assunto. "Sim, esse é meu telefone" e "isso é só uma dúvida, pode dizer o preço?" não cancelam.
- **C2 horário negado:** "não posso 24/11 às 11h", "não marque ainda", "I can't do...", "no puedo...", "aún no" invalidam o par dia e hora, mesmo que a IA monte a marcação.
- **C3 urgência:** vale para pergunta ("estou sangrando, o que faço?") e para qualquer ação da IA (se ela ia marcar ou cancelar, a mensagem é trocada por "avisei a equipe"). Negação ("não estou com febre", "no tengo fiebre", "I don't have a fever") não avisa. Dúvida geral ("clareamento faz a gengiva sangrar?") continua respondida pela Clara.
- **C4 pausa:** antes de cada mensagem para a paciente, o envio relê a pausa. Se a Dra. assumiu pelo celular, as mensagens da Clara que ainda estavam na fila são descartadas. Avisos para a equipe continuam saindo.
- **C5 aviso de falha:** o alerta para a Keshion traz só clínica, código do erro e ID da execução (sem texto livre, sem final do telefone).
- **C6 áudio:** só vira `.ogg` o que é oga, opus ou sem extensão. WAV, MP3 e M4A mantêm nome e tipo.
- **C7 cadastro:** `numeros_keshion` vazio é aceito em clínica real (só o número preenchido fora da demo e do teste continua recusado). Já testado localmente de ponta a ponta com uma clínica fictícia.

Testes locais já passaram (sem custo; repita depois de `python tecnico/n8n/gerar_fluxos.py clinica-demo`): `node tecnico/n8n/teste_validacao_data_hora.js` (61 + 32), `node tecnico/n8n/teste_pacote_a.js` (48), `node tecnico/n8n/teste_pacote_c.js` (70), `python tecnico/n8n/teste_pacote_c_cadastro.py` (7) e os dois do Codex em `tecnico/n8n/codex-18-11/` (leem o fluxo gerado pela entrada padrão).

## Antes de começar

- Confirme que nenhum outro teste está rodando: `select telefone, atualizado from pacientes where telefone like '554199900%' and atualizado > now() - interval '10 minutes'` no banco `clara`. Se houver, pare e me avise.
- Confirme que o fluxo publicado tem o nó "Ler a pausa agora" no envio (conferir publicado = gerado).
- Um teste por vez. Só números com prefixo `554199900`. Anote a hora de Curitiba e se a clínica estava aberta.
- Os casos abaixo são conversas sintéticas, uma mensagem por vez, pelo mesmo caminho do `teste_n8n.py` (webhook da demo, número de teste novo para cada caso, finais **961 em diante**). Espere a resposta da Clara (`saidas_teste`) antes da próxima mensagem. Para cada caso, guarde as saídas (paciente e equipe) e a ficha no fim.

## Casos, nesta ordem

1. **"Sim, esse é meu telefone" sem cancelar** (final 961): marcar uma avaliação em português; quando a Clara pedir ou confirmar o telefone, responder "sim, esse é meu telefone". Esperado: a avaliação continua marcada (ficha e Google com o evento), nenhuma pergunta de cancelamento.
2. **Dúvida depois de pedir para cancelar** (final 962): marcar; pedir para cancelar; quando a Clara perguntar "só para confirmar, você quer cancelar...", responder "isso é só uma dúvida, pode dizer o preço?". Esperado: não cancela. Depois responder "sim" de verdade para cancelar e limpar.
3. **Urgência com "?" em português** (final 963): "estou sangrando muito depois da limpeza, o que faço?". Esperado: aviso **URGENTE** para a equipe e a paciente recebe a resposta da Clara.
4. **Urgência com "?" em inglês** (final 964): "I am bleeding a lot, what should I do?". Esperado: aviso URGENTE, resposta em inglês.
5. **Urgência com "?" em espanhol** (final 965): "tengo la cara muy hinchada, ¿qué hago?". Esperado: aviso URGENTE, resposta em espanhol.
6. **Urgência no meio de uma marcação** (final 966): pedir para marcar e, antes de escolher horário, mandar "estou com febre e dor forte". Esperado: aviso URGENTE; a Clara não marca nada nessa mensagem.
7. **Negação não avisa** (finais 967, 968 e 969): "não estou com febre" (pt), "no tengo fiebre" (es), "I don't have a fever" (en), um número para cada. Esperado: nenhum aviso URGENTE.
8. **Dúvida geral continua respondida** (final 970): "clareamento faz a gengiva sangrar?". Esperado: a Clara responde sozinha, sem aviso URGENTE.
9. **Horário negado** (final 971): pedir para marcar; a Clara oferece horários; responder "não posso 24/11 às 11h" e depois "não marque ainda". Esperado: nada marcado (ficha e Google sem evento). Repetir em inglês ("I can't do Nov 24 at 11am, don't book it yet") e espanhol ("no puedo el 24/11 a las 11h, no lo agende todavía") nos finais 972 e 973.
10. **Pausa humana com mensagens saindo** (final 974): mandar uma pergunta que gere 2 ou 3 mensagens da Clara; enquanto a primeira está saindo, simular a Dra. respondendo pelo celular (mensagem da própria clínica para o número, como no teste 2.2 do `testes-checklist.md`). Esperado: a ficha fica pausada (`pausado_ate` com cerca de 12 h) e as mensagens da Clara que ainda não tinham saído **não aparecem** em `saidas_teste` depois da mensagem da Dra. (confira a hora de cada linha). Avisos para a equipe, se houver, continuam. Anote quantas mensagens saíram antes e depois.
11. **Áudio em WAV e em Ogg** (finais 975 e 976): mandar um áudio fictício em português em WAV (o do Codex: `midia-integrada-audio-pt.json`, execução 5257) e um em Ogg/Opus (voz normal do WhatsApp). Esperado: os dois são transcritos e a Clara responde ao conteúdo; nenhuma resposta do tipo "escreva por texto".
12. **Cadastro vazio** (sem número de paciente): rodar `python tecnico/n8n/teste_pacote_c_cadastro.py` (7 de 7) e conferir que `clientes/dra-vivian/clinica.json` ainda tem campos para preencher (não é para preencher aqui). Nada é publicado.
13. **5 perfis de agenda:** `python tecnico/teste-ab/paciente_simulado.py 801 803 807 811 815`, num terminal da Erica com o PC acordado. Quem marcou antes tem de continuar marcando; Emily (815) em inglês sem frase fixa em português.
14. **Rodada completa de 22 perfis** (a de 19/11 às 08h20 foi inválida; esta vale): `python tecnico/teste-ab/paciente_simulado.py`, em segundo plano, com a clínica aberta. Comparar com 17/11 (7,23), 18/11 (7,05) e Codex 19/11 (7,32).
15. **56 mensagens fixas** (`teste_n8n.py`, como em `tecnico/testes-checklist.md`): 56 de 56 sem falha técnica.
16. **Limpeza:** apagar fichas, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` dos números de teste usados; listar eventos dos próximos 30 dias no Google da demo e apagar os de teste que sobraram. Não apagar o evento antigo do Henrique (final 810) sem a Erica.

## O que me trazer

- Tabela dos casos 1 a 12: esperado, o que aconteceu, OK ou problema, com as saídas que provam.
- Notas dos 5 e dos 22 perfis comparadas às anteriores, custo e hora de Curitiba.
- Resultado das 56 mensagens e da limpeza (o que foi apagado e o que sobrou).
- Problemas novos, do mais grave ao mais leve, em linguagem simples.
- Atualize `tecnico/testes-checklist.md` e `tecnico/RETOMAR-AQUI.md`; commit e push só dos seus arquivos.
