# Plano de correções depois da revisão do Codex (18/11/2026)

Relatórios do Codex nesta pasta (cópia; o original ficou em `OneDrive\Documentos\ChatGPT\KESHION\tecnico\n8n`, porque o Codex foi aberto numa pasta antiga: da próxima vez, abrir o Codex em `Documents\Claude Code\keshion`). Cada achado abaixo foi conferido no código pelo Claude na conversa de testes: **todos procedem**.

Regras: corrigir aqui, publicar só com OK da Erica (import e publish, sem reiniciar o n8n), não rodar teste da Clara (vai para a conversa de testes), testes locais sem custo podem rodar. Os dois scripts do Codex (`testes_data_hora_extras_2026_11_18.js`, `testes_locais_revisao_2026_11_18.js`) servem de teste de regressão.

## Pacote A: fluxo da Clara (`tecnico/n8n/gerar_fluxos.py`), antes do piloto

| # | Problema (simples) | Onde | Como corrigir |
|---|---|---|---|
| A1 | Informação nova curta some sem aviso ("Agora comecei a sangrar muito" depois de um aviso de recibo) | `RESULTADO_JS`, caso `humano`, linhas `idade < 15 * 60000 && pend.length < 60 && !pend.includes('?')` e a mesma condição no ramo de 90 min | Só deixar de avisar quando a mensagem é confirmação pura (lista fechada: ok, obrigado/a, valeu, blz, beleza, certo, combinado, 👍, thanks, ok thanks, gracias, perfecto, vale). Qualquer outra coisa gera aviso ou complemento. Palavras de urgência (sangr, bleed, sangrad, inchad, swell, hinchad, febre, fever, fiebre, dor forte, muita dor, severe pain, mucho dolor, pus, desmai) sempre geram aviso novo, nunca complemento. Limitar complementos a 1 a cada 15 min por paciente (Camila recebeu 5), exceto urgência. |
| A2 | Ciclo de recusa: "Esse horário não está disponível" repete sem chamar ninguém ("amanhã às 11h" recusado 3 vezes; Emily 10 vezes) | caso `invalido` | Contador de recusas seguidas na ficha (coluna nova, por exemplo `recusas_agenda`, zera ao marcar, remarcar ou cancelar com sucesso). Na 2ª recusa: aviso para a equipe com o motivo técnico e o pedido da paciente, e mensagem para a paciente dizendo que a equipe vai confirmar o horário (sem repetir a recusa). Na 1ª recusa por formato não reconhecido, pedir a data por extenso ("me confirma o dia e o mês, por exemplo 19/11?") em vez de dizer indisponível. |
| A3 | Datas relativas não reconhecidas | `temDataNaConversa` | Aceitar hoje/amanhã/depois de amanhã, today/tomorrow, hoy/mañana/pasado mañana, calculados pela data da clínica (fuso `__FUSO__`) no momento da mensagem em que aparecem (usar a data de hoje é aceitável para o piloto). |
| A4 | Data de uma opção junto com a hora de outra; minutos ignorados; "dia 19 de dezembro" aceito como novembro; ano não conferido | `temDataNaConversa` e `temHora` | Exigir data e hora **na mesma mensagem** (mesmo bloco de fala da assistente ou da paciente), e de preferência na mensagem mais recente que fala de horário. Hora: minutos precisam bater (9:30 não prova 9h). "dia 19" seguido de outro mês, ou ano diferente do candidato, não vale. Segundos do candidato diferentes de zero: inválido. Acrescentar esses casos ao `teste_validacao_data_hora.js`. |
| A5 | Cancelar: a trava aceita "cancel" em qualquer frase e não confere o "sim" da paciente; em inglês exige uma confirmação a mais, em português | `Decidir a ação`, regex `/certo\s*\?\|cancel/i` | Cancelar só se a última fala da assistente foi pergunta de confirmação de cancelamento (certo?, correct?, right?, confirm, ¿correcto?, ¿confirmas?) **e** a mensagem nova da paciente é afirmativa (sim, pode, confirmo, isso, yes, confirm, sí, claro) e não negativa (não, quero manter, no, keep). Senão, perguntar de novo no idioma da paciente. |
| A6 | Frases fixas sempre em português (recusa, ocupado, dados, falha, confirmação de cancelamento, "só um instante") | `RESULTADO_JS` e `Decidir a ação` | Campo `idioma` (pt, en, es) na resposta da IA (pedir no prompt e no formato JSON). Catálogo das frases fixas nos 3 idiomas; desconhecido = português. |
| A7 | A defesa "prometeu encaminhar, então avisa a equipe" só entende português | regex `promete` | Acrescentar inglês e espanhol: I'll (forward\|pass\|check\|ask\|confirm), let me check, I will check, will get back, voy a (pasar\|consultar\|verificar\|confirmar), le paso, te confirmo, te aviso. |
| A8 | Trava de vaga dura 2 min, mas as chamadas ao Google podem levar até 120 s cada | `Reservar o horário` e nós HTTP | Trava de 5 min e tempo limite de 30 s nas chamadas ao Google da marcação. (Idempotência e sobreposição de horários: depois do piloto.) |

Depois: gerar, rodar os testes locais (os 61 casos + os do Codex + casos novos dos itens A1 a A7), commit e push, pedir OK para publicar na demo (import e publish, sem reiniciar), conferir publicado = gerado e entregar o prompt de teste para a conversa de testes. Lembrar a revisão do Codex.

## Pacote B: servidor, backup e roteiros (precisa de OK para mexer no servidor)

| # | Problema | Como corrigir |
|---|---|---|
| B1 | Backup pode falhar sem ninguém saber, e às vezes o status antigo continua "OK" | `trap` de erro logo depois de `set -euo pipefail`, antes de `cd`, `.env` e `mktemp`; status "EM ANDAMENTO" no início e "OK" só no fim; `flock` contra duas execuções. |
| B2 | Nenhum alerta fora do WhatsApp | Monitor externo (proposta: Healthchecks.io, grátis, e-mail para a Erica): o backup avisa início, sucesso e falha; se não houver sucesso até as 04h de Curitiba, chega e-mail. O nó de alerta de falha do n8n também chama o endereço de falha do monitor (sem dados de paciente, só clínica, código do erro e ID da execução). **Precisa do OK da Erica para criar a conta.** |
| B3 | Retenção local guarda 7 arquivos, não 7 dias; `.parcial` não é limpo | Apagar por idade (`find -mtime +7`), incluindo `.parcial`. |
| B4 | Roteiro de restauração continua mesmo com erro | `-v ON_ERROR_STOP=1`, `set -o pipefail`, esperar `pg_isready`, comandos completos sem "...", critérios de conferência. |
| B5 | `client_id` compartilhado do rclone vai ser desligado em 2026 | Erica cria um cliente OAuth próprio no Google Cloud da conta da Keshion (app publicado, não em modo Teste), reconectar com escopo `drive.file` e conferir se as cópias antigas continuam visíveis. Passo a passo para a Erica, antes de 01/12. |
| B6 | `CLINICA-NOVA.md` manda reiniciar o n8n e põe senha em argumento de comando | Tirar o `docker compose restart n8n` (import e publish bastam), passar senha por arquivo temporário protegido ou variável, cópia da versão anterior e como voltar. |
| B7 | Usuários limitados do banco (`clara_app`, `clinica_teste_app`) ainda não existem | Aplicar o roteiro do Codex ("Migração para `_app`") com OK, sem reiniciar o n8n. Pode ficar para depois do pacote A. |

## Decisões da Erica (e da Dra. Vivian)

1. Canal de alerta fora do WhatsApp: Healthchecks.io com e-mail (proposta) ou outro.
2. Criar o cliente OAuth próprio do Google para o backup (passo a passo guiado).
3. Base: qual o prazo real de retorno da equipe ("retornamos em instantes" promete demais) e se a avaliação pode ser parcelada.

## Depois do piloto (não bloqueia 01/12)

Fila de envio com confirmação de entrega (ordem das mensagens), idempotência na criação do evento no Google, duas avaliações para a mesma pessoa, horários sobrepostos com inícios diferentes, histórico de cada versão das instruções, validação de fuso e calendário no cadastro, modo copiloto (existir ou sair da lista).
