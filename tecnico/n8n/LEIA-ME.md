# Clara no n8n · como está montada

Montada em 12/11/2026, a partir das cópias do Make em `tecnico/make-cenarios/`. Sem chaves neste arquivo.

## Os dois fluxos

| Fluxo no n8n | id | Substitui | O que faz |
|---|---|---|---|
| `Clara · Atendimento (WhatsApp)` | `ClaraAtendimento` | 1A + 1B + 1C | Recebe do Whapi, separa texto, áudio, foto e outros, pausa 12 h quando a doutora responde, `#reiniciar`, fila de 7 s, ficha, agenda, Claude Haiku, marcar, remarcar, cancelar, avisos, despedida 1 minuto depois de marcar |
| `Clara · Envio (até 3 mensagens)` | `ClaraEnvio000001` | 1D | Envia até 3 mensagens com "digitando" e avisa a Erica se o Whapi falhar. Não envia, e grava na tabela `saidas_teste`, quando `modo_teste = 1` ou quando o lote envolve um número que começa com `prefixo_teste` (554199900). O prefixo permite testar com a Clara no ar, sem mandar nada real, nem os avisos para a equipe |

**No ar desde 12/11/2026:** o Whapi chama o n8n e `modo_teste = 0`. Revisão independente: `PROMPT-CODEX-REVISAO.md`.

Endereço do webhook: `https://n8n.169-58-41-107.sslip.io/webhook/<caminho secreto>`. **Desde 12/11/2026 (tarde) o caminho é secreto** e fica só em `segredos.local.json`, fora do Git (o antigo `clara-whapi-...` foi desativado depois da revisão do Codex). Ele também aparece no painel do Whapi (webhook 1) e no nó de webhook do n8n. Se perder o arquivo, copie o caminho de um desses lugares.

## Arquivos desta pasta

- `gerar_fluxos.py`: gera os dois fluxos. **Para mudar um fluxo, mude aqui e rode de novo**, para o repositório continuar sendo a fonte da verdade. Exige `segredos.local.json` (`{"webhook_path": "..."}`).
- `clara-atendimento.json` e `clara-envio.json`: o que o script gera (para importar). Fora do Git, porque contêm o caminho secreto.
- `schema-clara.sql`: as tabelas do banco `clara`.
- `revisao-codex-2026-11-12.md` e `plano-pos-revisao-codex.md`: revisão independente e o que foi feito com ela.

Para atualizar no servidor (mesmo id substitui o fluxo antigo):
```bash
python gerar_fluxos.py
```
Depois copiar o JSON para o servidor, `n8n import:workflow --input=...` e `n8n publish:workflow --id=ClaraAtendimento` dentro do contêiner do n8n.

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
