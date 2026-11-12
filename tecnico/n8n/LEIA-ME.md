# Clara no n8n · como está montada

Montada em 12/11/2026, a partir das cópias do Make em `tecnico/make-cenarios/`. Sem chaves neste arquivo.

## Os dois fluxos

| Fluxo no n8n | id | Substitui | O que faz |
|---|---|---|---|
| `Clara · Atendimento (WhatsApp)` | `ClaraAtendimento` | 1A + 1B + 1C | Recebe do Whapi, separa texto, áudio, foto e outros, pausa 12 h quando a doutora responde, `#reiniciar`, fila de 7 s, ficha, agenda, Claude Haiku, marcar, remarcar, cancelar, avisos, despedida 1 minuto depois de marcar |
| `Clara · Envio (até 3 mensagens)` | `ClaraEnvio000001` | 1D | Envia até 3 mensagens com "digitando" e avisa a Erica se o Whapi falhar. Não envia, e grava na tabela `saidas_teste`, quando `modo_teste = 1` ou quando o lote envolve um número que começa com `prefixo_teste` (554199900). O prefixo permite testar com a Clara no ar, sem mandar nada real, nem os avisos para a equipe |

**No ar desde 12/11/2026:** o Whapi chama o n8n e `modo_teste = 0`. Revisão independente: `PROMPT-CODEX-REVISAO.md`.

Endereço do webhook (vai no Whapi na hora da virada):
`https://n8n.169-58-41-107.sslip.io/webhook/clara-whapi-7f3c9a2e51b84d06`

## Arquivos desta pasta

- `gerar_fluxos.py`: gera os dois fluxos. **Para mudar um fluxo, mude aqui e rode de novo**, para o repositório continuar sendo a fonte da verdade.
- `clara-atendimento.json` e `clara-envio.json`: o que o script gera (para importar).
- `schema-clara.sql`: as tabelas do banco `clara`.

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
| `saidas_teste` | O que teria sido enviado, quando o modo teste está ligado |

Para mudar tom ou regras da Clara, altere `_instrucoes` ou `_base` na tabela `config`, sem mexer no fluxo. A credencial "Postgres Clara" do n8n usa o usuário `clara`, com senha só no `.env` do servidor (`CLARA_DB_PASSWORD`).

## Diferenças em relação ao Make

- Tudo num fluxo só (no n8n não há fila de execução como no Make, então a espera de 1 minuto da despedida não trava as outras conversas).
- As mensagens da própria Clara que voltam do Whapi são descartadas logo no início, sem custo.
- `#reiniciar` só funciona para os números de `numeros_keshion` (no Make valia para qualquer número).
- Proteção contra chamada sem telefone (não envia nada).
- Se a agenda do Google não responder, a Clara é instruída a não oferecer horários e a chamar uma pessoa.
- Áudio que não der para transcrever: a Clara pede com gentileza que a pessoa escreva.
- A ação da agenda é feita antes de salvar a conversa, então a conversa guarda o que foi enviado de fato (horário ocupado, falha etc.).

## Testes feitos em 12/11/2026 (modo teste, números fictícios)

Funcionaram: primeira mensagem, fila de 7 s (2 mensagens, 1 resposta), pedido de nome, marcação com evento criado no Google Agenda, aviso de marcação para o aprovador, despedida 1 minuto depois, cancelamento (evento apagado e aviso), pausa de 12 h quando a doutora responde, `#reiniciar`, leitura de foto.

Passo 8 (12/11/2026, manhã): as 56 mensagens do teste A/B passaram pelo fluxo inteiro, todas respondidas (14 a 19 s cada), incluindo marcar, remarcar (evento mudado no Google), cancelar e 6 avisos de "chamar uma pessoa". Respostas muito próximas às do Haiku na rodada 2. Comparação mensagem por mensagem em `tecnico/teste-ab/relatorio-n8n.md`.

Ainda não testados: áudio (precisa de um áudio real do Whapi), horário que ficou ocupado no meio da conversa, falha da IA, envio real pelo Whapi.
