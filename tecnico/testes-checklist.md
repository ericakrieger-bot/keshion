# Testes da Clara (checklist completo)

Regras: números de teste com prefixo `554199900` (nada sai pelo WhatsApp). A agenda do Google é real: todo teste que marca precisa cancelar no fim e conferir que não sobrou evento. Quem executa: **C** = Claude (conversa de testes), **X** = Codex (revisão independente), **E** = Erica (celular real), **V** = Dra. Vivian.

## Portão 1: a cada mudança publicada (fluxo, instruções ou base)

| # | Teste | Quem | Como | Situação |
|---|---|---|---|---|
| 1.1 | Teste rápido (5 conversas: oi, preço, marcar e cancelar, dor, foto) em 2 minutos | C | script `teste_rapido.py` | **criar** |
| 1.2 | 56 mensagens fixas (tom e regras) | C | `teste_n8n.py` no servidor + `comparar_antes_depois.py` | pronto |
| 1.3 | Pacientes simulados (8 perfis, nota de outra IA) | C | `paciente_simulado.py` no PC | pronto |
| 1.4 | Agenda limpa e banco de teste limpo depois dos testes | C | consulta no banco `clara` | pronto (os scripts limpam) |
| 1.5 | Revisão independente da feature | X | `PROMPT-CODEX-REVISAO.md` com a feature indicada | pronto |

## Portão 2: antes de ligar uma clínica real (piloto Dra. Vivian, 01/12)

| # | Teste | Quem | Situação |
|---|---|---|---|
| 2.1 | Mídia real pelo celular: áudio, foto, documento, figurinha, vídeo, localização | E | áudio corrigido em 12/11; refazer todos no número da clínica |
| 2.2 | Doutora respondendo pelo celular: Clara fica 12 h em silêncio naquela conversa | E | testado com simulação; falta no celular real |
| 2.3 | Falhas simuladas: IA fora, lenta ou com resposta quebrada; Google fora ou sem permissão; Whapi recusando envio. Conferir "só um instante", aviso para a equipe, ficha certa e nada de resposta errada | C, X | **por fazer** (cópia do fluxo apontando para endereços falsos) |
| 2.4 | Agenda: fora do expediente, sábado, domingo, feriado, recesso, mais de 90 dias, mesmo dia, horário que acabou de passar | C | parcial; **criar roteiro próprio** |
| 2.5 | Concorrência: duas pessoas pegando o mesmo horário; 3 mensagens seguidas; reenvio do Whapi; resposta rápida antes da Clara terminar | C, X | parcial (ordem entre respostas ainda pode trocar) |
| 2.6 | Segurança: canal errado, caminho antigo do webhook, mídia de site de fora, grupo, mensagem da própria Clara voltando | C, X | feito em 12/11; repetir a cada mudança na entrada |
| 2.7 | Isolamento por clínica: mesmo telefone na demo e na Vivian; fichas, agendas e avisos separados | C, X | quando a estrutura por clínica existir |
| 2.8 | Autorização do Google renovando sozinha (app publicado) | E, C | depende da página e da política de privacidade |
| 2.9 | Carga: 20 conversas ao mesmo tempo (tempo de resposta e erros) | C | **por fazer** |
| 2.10 | Custo por conversa (tokens da IA e mensagens) para fechar o preço | C | **por fazer** |
| 2.11 | Recuperação: reiniciar o servidor; restaurar o backup numa cópia; backup fora do servidor | C | **por fazer** |
| 2.12 | Aceite da clínica: roteiro com os casos reais da Vivian; ela aprova tom, regras e avisos | V, E | antes de 01/12 |
| 2.13 | Avisos chegando no número certo da clínica (não no da Erica) | E | quando a estrutura por clínica existir |

## Portão 3: durante o piloto (toda semana)

| # | Teste | Quem |
|---|---|---|
| 3.1 | Ler 10 conversas reais da semana e anotar erros de tom ou de regra | E, C |
| 3.2 | Conferir avisos para a doutora: chegaram, eram necessários, nenhum faltou | V, E |
| 3.3 | Conferir agenda x ficha: marcações da Clara batem com a agenda | C |
| 3.4 | Rodar os pacientes simulados depois de cada ajuste pedido pela clínica | C |
| 3.5 | Conferir a autorização do Google e o vencimento do plano do Whapi | E |

## Melhorias nos scripts

1. Criar `teste_rapido.py` (1.1).
2. Pacientes simulados: perfis novos (3 mensagens seguidas, some e volta no dia seguinte, pergunta de outro paciente, reclamação de tratamento feito na clínica, pessoa que só manda áudio na vida real), critérios lidos da base de cada clínica, e um histórico de notas para ver a evolução.
3. Roteiro de datas difíceis (2.4).
4. Cópia do fluxo com endereços falsos para as falhas (2.3).
