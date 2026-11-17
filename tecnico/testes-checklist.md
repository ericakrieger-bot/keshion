# Testes da Clara (checklist)

Números de teste: prefixo `554199900` (nada sai pelo WhatsApp). Agenda do Google é real: cancelar o que marcar.

## Já automatizados

| Teste | Quando rodar | Como |
|---|---|---|
| 56 mensagens fixas (tom e regras, 7 conversas) | depois de mudar o fluxo | `tecnico/teste-ab/teste_n8n.py <caminho do webhook>` no servidor; comparar com `comparar_antes_depois.py` |
| Pacientes simulados (8 perfis, conversa livre, nota de outra IA) | depois de mudar instruções, base ou fluxo | `python tecnico/teste-ab/paciente_simulado.py` no PC (~15 min) |
| Revisão independente | ao fechar cada feature | Codex com `tecnico/n8n/PROMPT-CODEX-REVISAO.md` |

## Ainda manuais ou por fazer

| # | Teste | Por que | Situação |
|---|---|---|---|
| 1 | Teste rápido depois de cada publicação (5 mensagens: oi, preço, marcar e cancelar, dor, foto) | pegar quebra em 2 minutos | **criar script** |
| 2 | Falhas simuladas: Anthropic fora ou lenta, Google fora ou sem permissão, Whapi falhando no envio | conferir "só um instante" + aviso + ficha certa | **por fazer** (precisa de cópia do fluxo apontando para endereços falsos) |
| 3 | Mídia real pelo celular: áudio, foto, documento, figurinha, vídeo, localização | só o Whapi real manda os links verdadeiros | Erica testa pelo celular |
| 4 | Doutora respondendo pelo celular (pausa de 12 h) | só o número real gera esse evento | Erica testa |
| 5 | Agenda: fora do expediente, sábado, feriado, recesso de fim de ano, além de 90 dias | regras de data são o ponto mais frágil | parcial (nas 56 e simulados) |
| 6 | Concorrência: duas pessoas pegando o mesmo horário; 3 mensagens seguidas; reenvio do Whapi | evitar marcação dupla e resposta repetida | parcial |
| 7 | Segurança: canal errado, caminho antigo, mídia de site de fora, grupo | ninguém de fora aciona a Clara | feito em 12/11; repetir depois de mudar a entrada |
| 8 | Isolamento por clínica: mesmo telefone em duas clínicas | dados e avisos não podem se misturar | quando a estrutura por clínica existir |
| 9 | Carga: 20 conversas ao mesmo tempo | tempo de resposta e custo | por fazer |
| 10 | Custo por conversa (tokens da IA) | preço da mensalidade | por fazer |
| 11 | Recuperação: reiniciar servidor, restaurar backup numa cópia | saber se dá para voltar em caso de pane | por fazer |
| 12 | Aceite da clínica: roteiro com os casos da própria Dra. Vivian, ela aprova o tom | piloto | antes de 01/12 |
| 13 | Renovação da autorização do Google | expira em 7 dias até publicar o app | conferir toda semana |

## Melhorias sugeridas nos scripts

- Pacientes simulados: perfis novos (manda 3 mensagens seguidas, some e volta no dia seguinte, pergunta sobre outro paciente, reclama de tratamento feito na clínica), critérios lidos da base de cada clínica, e um arquivo com o histórico das notas para ver a evolução.
- Criar o teste rápido do item 1.
