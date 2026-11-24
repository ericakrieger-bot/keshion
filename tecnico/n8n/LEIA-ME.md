# Clara no n8n · como está montada

Montada em 12/11/2026, a partir das cópias do Make em `arquivo/make/make-cenarios/`. Sem chaves neste arquivo.

## Os dois fluxos

| Fluxo no n8n | id | Substitui | O que faz |
|---|---|---|---|
| `Clara · Atendimento (WhatsApp)` | `ClaraAtendimento` | 1A + 1B + 1C | Recebe do Whapi, separa texto, áudio, foto e outros, pausa 12 h quando a doutora responde, `#reiniciar`, fila de 20 s (era 7 s até 24/11), ficha, agenda, Claude Haiku, marcar, remarcar, cancelar, avisos, despedida 1 minuto depois de marcar |
| `Clara · Envio (até 3 mensagens)` | `ClaraEnvio000001` | 1D | Envia até 3 mensagens com "digitando" e avisa a Erica se o Whapi falhar. Não envia, e grava na tabela `saidas_teste`, quando `modo_teste = 1` ou quando o lote envolve um número que começa com `prefixo_teste` (554199900). O prefixo permite testar com a Clara no ar, sem mandar nada real, nem os avisos para a equipe |

**No ar desde 12/11/2026:** o Whapi chama o n8n e `modo_teste = 0`. Revisão independente: `PROMPT-CODEX-REVISAO.md`.

Endereço do webhook: `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`. **Desde 12/11/2026 (tarde) o caminho é secreto** e fica só em `segredos.local.json`, fora do Git (o antigo `clara-whapi-...` foi desativado depois da revisão do Codex). Ele também aparece no painel do Whapi (webhook 1) e no nó de webhook do n8n. Se perder o arquivo, copie o caminho de um desses lugares.

## Arquivos desta pasta

- `gerar_fluxos.py <slug>`: gera o par de fluxos de uma clínica a partir de `clientes/<slug>/clinica.json`. **Para mudar um fluxo, mude aqui e rode de novo para cada clínica**, para o repositório continuar sendo a fonte da verdade. Sem slug, gera a demo.
- `preparar_banco.py <slug>`: gera o SQL do banco da clínica (tabelas + tabela `config` com instruções, base, aprovador etc.). Pode rodar de novo depois de mudar instruções ou base: guarda a versão anterior com data.
- `segredos.local.json` (fora do Git): caminho secreto do webhook de cada clínica, `{"<slug>": {"webhook_path": "..."}}`.
- `gerados/<slug>/`: `atendimento.json`, `envio.json` e `banco.sql`. Fora do Git, porque contêm o caminho secreto.
- `schema-clara.sql`: as tabelas (iguais em todas as clínicas).
- Revisões do Codex e planos de correção: os de 12 a 18/11 estão em `arquivo/codex/`; o mais recente em `codex-19-11/`. Prompt de revisão em uso: `PROMPT-CODEX-REVISAO.md`.

Para atualizar no servidor (mesmo id substitui o fluxo antigo):
```bash
python gerar_fluxos.py clinica-demo
```
Depois copiar os JSON de `gerados/clinica-demo/` para o servidor, `n8n import:workflow --input=...` e `n8n publish:workflow --id=ClaraAtendimento` dentro do contêiner do n8n.

## Estrutura por clínica (17/11/2026)

Cada clínica tem: uma pasta em `clientes/<slug>/` com `clinica.json` (sem chaves), instruções e base; um banco próprio no Postgres; um par de fluxos próprio no n8n (ids diferentes); credenciais próprias de Whapi, Google e Postgres (Anthropic e OpenAI podem ser as da Keshion); um caminho de webhook próprio. Nada é compartilhado entre clínicas além do servidor.

| Clínica | Pasta | Banco | Fluxos |
|---|---|---|---|
| Demo (Dra. Suzana, Clara) | `clientes/clinica-demo` | `clara` | `ClaraAtendimento`, `ClaraEnvio000001` |
| Teste de isolamento (no ar desde 17/11, canal falso) | `clientes/clinica-teste` | `clinica_teste` | `TesteAtendimento`, `TesteEnvio000001` |
| Dra. Vivian (piloto suspenso em 20/11) | `arquivo/dra-vivian-suspenso-2026-11-20` (não preenchida) | `clinica_vivian` | `VivianAtendiment`, `VivianEnvio00001` |

**Clínica nova:** roteiro completo em [`CLINICA-NOVA.md`](CLINICA-NOVA.md) (banco com dois usuários, credenciais, fluxos, WhatsApp, testes e virada para valer).

**#reiniciar** só existe na demo e na clínica de teste: nas outras, `numeros_keshion` fica vazio (o `preparar_banco.py` recusa se tiver número).

## Banco `clara` (Postgres do servidor)

| Tabela | Conteúdo |
|---|---|
| `pacientes` | Uma linha por telefone: conversa, mensagens pendentes (fila), nome dito, tratamento, avaliação (início, texto, id do evento), pausa da doutora |
| `config` | `_instrucoes` e `_base` (iguais aos registros do Make em 12/11/2026), `modelo`, `aprovador`, `modo_teste`, `local_avaliacao`, `numeros_keshion` |
| `saidas_teste` | O que teria sido enviado, quando o modo teste está ligado ou o número tem o prefixo de teste |
| `mensagens_recebidas` | Ids de mensagens do Whapi já recebidas (um reenvio, mesmo horas depois, não ganha nova resposta) |

Para mudar tom ou regras da Clara, altere `_instrucoes` ou `_base` na tabela `config`, sem mexer no fluxo. A credencial "Postgres Clara" do n8n usa o usuário `clara`, com senha só no `.env` do servidor (`CLARA_DB_PASSWORD`).

## Diferenças em relação ao Make

- Tudo num fluxo só (no n8n não há fila de execução como no Make, então a espera de 1 minuto da despedida não trava as outras conversas).
- As mensagens da própria Clara que voltam do Whapi são descartadas logo no início, sem custo.
- `#reiniciar` só funciona para os números de `numeros_keshion` (no Make valia para qualquer número).
- Proteção contra chamada sem telefone (não envia nada).
- Se a agenda do Google não responder (ou responder com erro), e a IA tentar marcar ou oferecer horário, o fluxo troca a resposta por "Vou conferir a agenda aqui e já te retorno com os horários." e avisa a equipe, sem depender da IA. Ação desconhecida da IA vira "chamar uma pessoa".
- Áudio que não der para transcrever: a Clara pede com gentileza que a pessoa escreva. A voz do WhatsApp (`.oga`) é renomeada para `.ogg` antes da transcrição.
- A ação da agenda é feita antes de salvar a conversa, então a conversa guarda o que foi enviado de fato (horário ocupado, falha etc.). Marcar ou remarcar sem id de evento devolvido pelo Google conta como falha.

Proteções acrescentadas depois da revisão do Codex (12/11/2026, tarde):
- Só aceita mensagens do canal `GRNLTR-4K8ZF` (campo `channel_id`) e só baixa mídia de endereços do Whapi (Wasabi). Foto ou áudio de outro endereço vira "conteúdo que não é texto, foto nem áudio".
- Pacote com várias mensagens: a primeira segue; as outras voltam sozinhas ao webhook e entram na fila.
- Avisos para a equipe saem antes das mensagens ao paciente.
- A despedida confere o id da última mensagem, a pausa da doutora e o evento, em vez do tamanho da conversa.
- Execuções do n8n guardadas por 14 dias (`EXECUTIONS_DATA_MAX_AGE`).

**Para testar:** use números com o prefixo `554199900`, mande `"channel_id": "GRNLTR-4K8ZF"` no corpo e, para áudio ou foto, um link do Wasabi do Whapi (links de outros sites são bloqueados de propósito).

## Testes feitos em 12/11/2026 (modo teste, números fictícios)

Funcionaram: primeira mensagem, fila de 7 s (2 mensagens, 1 resposta), pedido de nome, marcação com evento criado no Google Agenda, aviso de marcação para o aprovador, despedida 1 minuto depois, cancelamento (evento apagado e aviso), pausa de 12 h quando a doutora responde, `#reiniciar`, leitura de foto.

Passo 8 (12/11/2026, manhã): as 56 mensagens do teste A/B passaram pelo fluxo inteiro, todas respondidas (14 a 19 s cada), incluindo marcar, remarcar (evento mudado no Google), cancelar e 6 avisos de "chamar uma pessoa". Respostas muito próximas às do Haiku na rodada 2. Comparação mensagem por mensagem em `tecnico/teste-ab/relatorio-n8n.md`.

Depois da virada: áudio real do Whapi corrigido e testado; Codex testou horário ocupado, remarcar, documento, figurinha, histórico longo (ver o relatório dele). Testes das correções (12/11, tarde, todos ok): canal errado recusado, caminho antigo com 404, pacote com 2 mensagens, reenvio atrasado sem nova resposta, foto de fora bloqueada, áudio do Whapi, aviso de urgência antes do paciente, marcar com despedida e cancelar.

Ainda não testados: falha da IA e da agenda (precisam de simulação isolada).


## 16/11/2026: instruções novas, nome completo e telefone

- Instruções com as 8 mudanças de tom (`clientes/clinica-demo/proposta-humanizer-instrucoes.md`) e a regra nova: antes de marcar, a Clara pede nome e sobrenome e um telefone de contato ("pode ser este mesmo número"). Os dois vão para a ficha (`pacientes.nome_completo`, `pacientes.telefone_contato`), para a descrição do evento na agenda e para o aviso de nova avaliação. Versão anterior das instruções guardada em `config._instrucoes_anterior_20261112`.
- `max_tokens` da IA de 2000 para 6000: o pensamento interno do Haiku cortava o JSON em respostas longas (2 de 56 no primeiro teste).
- O leitor da resposta também entende o formato "mensagem1: ..." (1 de 56). JSON cortado continua indo para falha técnica.
- Falha técnica agora registra o turno na conversa e esvazia a fila (antes a mensagem seguinte se misturava com a anterior).
- Resultado (`tecnico/teste-ab/relatorio-instrucoes-novas.md`): 53 respostas, nenhuma falha técnica; "Entendo", elogios e frases de enchimento sumiram; "aqui na clínica" caiu de 7 para 4; a ressalva de preço só aparece na primeira pergunta de preço de cada conversa. A conversa C7 parou na 4ª mensagem por erro de rede do script de teste, não da Clara. Marcação com nome completo e telefone testada à parte: ok, com evento criado e cancelado.
- Dor de dente, remédio, inchaço, sangramento ou trauma: sempre ação humano, inclusive com a clínica fechada (pedido da Erica em 16/11; regra H das instruções e parte 11 da base). Testado: aviso para a Dra. antes da resposta ao paciente. Base anterior guardada em `config._base_anterior_20261116`.

- Voz da clínica (16/11, pedido da Erica): a base (parte 10, "Registro") diz se a Clara pode espelhar o paciente e quais abreviações usar; a regra Q e um exemplo de paciente informal nas instruções ensinam o jeito solto e correto, sem erro de grafia. Preço, data, horário, endereço e saúde sempre por extenso. Teste lado a lado (informal x formal): com o exemplo, a Clara passou a usar "Oi", "pq", "pensa com calma" com quem escreve solto e ficou formal com quem escreve formal. Sem o exemplo, quase não espelhava.
- Segunda tentativa da IA: se a resposta vier sem texto (o Haiku às vezes devolve só o pensamento) ou ilegível, o fluxo pede de novo uma vez antes da falha técnica. Rodada das 56 com tudo isso: 56 de 56 respondidas, 1 segunda tentativa usada e nenhuma falha técnica (`tecnico/teste-ab/relatorio-voz.md`). Instruções anteriores em `config._instrucoes_anterior_20261116`.

## 17/11/2026: teste com paciente simulado

`tecnico/teste-ab/paciente_simulado.py`: outra IA faz 8 pacientes (informal, formal, dor, desconfiado, troca de horário, mãe marcando para a filha, perguntas fora da base, idosa) e conversa livremente com a Clara; uma terceira IA dá nota. Usa números de teste e cancela o que sobrar na agenda. Roda no computador da Erica (chave da Anthropic do `.env`), cerca de 15 minutos. Horário do teste em UTC-3 fixo (o computador da Erica está no fuso de Israel, o que distorceu duas rodadas).

Ajustes feitos a partir dele (instruções): desconto à vista de 5% no Pix citado antes de passar pedido maior para a Dra.; nunca prometer "eu te aviso"; não repetir frases já ditas; espelhamento decidido pelas mensagens da pessoa, com cuidado com pessoa idosa; pronto-socorro só para dor forte, inchaço, sangramento ou falta de ar, e reforçado se a dor piorar; saudação de horário só repetindo a do paciente. No fluxo: aviso "chamar uma pessoa" não se repete em 15 minutos quando a mensagem nova é só um "ok". Instruções anteriores em `config._instrucoes_anterior_20261117`.

Notas finais (rodada 20261117-1043): Bia 9, Paula 9, Fernanda 9, Ricardo 8, Camila 8, Sandra 8, Dona Lourdes 8, Marcos 7. Todos atingiram o objetivo.


## 17/11/2026 (noite): correções da revisão do Codex

Feitas no gerador (`gerar_fluxos.py`), no banco (`schema-clara.sql`), nas instruções e na base da demo. Importadas e publicadas na demo e na clínica de teste.

- **A agenda não depende só da IA.** Antes de criar ou mudar um evento, o fluxo confere sozinho: dia da semana, horário de avaliação, prazo de 90 dias, antecedência mínima, feriados e recesso (regras em `agenda.regras` do `clinica.json` de cada clínica; conferir com a clínica nova), nome e sobrenome e telefone (ao marcar) e se aquele dia e hora apareceram na conversa. Fora disso, a resposta é "Esse horário não está disponível para avaliação" ou o pedido de nome e telefone.
- **Trava de vaga (5 min):** tabela `reservas_horario`. Duas conversas pedindo a mesma vaga: só a primeira segue, a outra recebe "esse horário acabou de ser preenchido". Depois de 5 minutos a trava expira (o evento criado já aparece na agenda).
- **Cancelar só depois de confirmar:** se a IA tentar cancelar sem a assistente ter perguntado "certo?", o fluxo troca por "Só para confirmar: é a sua avaliação de ..., certo?".
- **Aviso sempre que a Clara promete encaminhar:** se a resposta diz "vou passar", "vou verificar", "já te retorno" e a ação veio como `responder`, o fluxo muda para `humano` (aviso para a equipe). O aviso não se repete: 15 min quando a mensagem nova é só "ok", e 90 min quando o motivo é parecido com o do último aviso (colunas novas `ultimo_motivo_humano` e `envio_ate`).
- **Ordem das mensagens:** cada turno grava até quando suas mensagens ainda estão saindo (`envio_ate`); o turno seguinte espera (no máximo 60 s) antes de responder. Evita a pergunta da oferta chegar depois da confirmação.
- **Outro dia:** quando o paciente volta em outro dia, a conversa ganha a linha `--- dd/mm/aaaa (outro dia) ---`.
- **Instruções novas (demo):** regra R (idioma do paciente desde a primeira mensagem), S (quem já é paciente: sem prontuário inventado, faixa da limpeza, sem avaliação de R$ 150, restante vai para a equipe), T (não prometer o que a base não diz), confirmação sem pergunta de horário, cancelamento com menos de 24 h. Base: anestesia "quando é preciso", sem promessa de lembretes e de acompanhamento do orçamento, que ainda não existem.
- **Ainda não existem (próxima feature):** lembretes de confirmação (48 h, véspera 18h, 2 h), acompanhamento do orçamento (dias 3, 10, 17 e 30, decidido em 18/11, igual ao app), reengajamento por silêncio e estado "cancelou".
