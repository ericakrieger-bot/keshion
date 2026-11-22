# Plano: modo copiloto e modo "só fora do horário" (21 e 22/11/2026)

Status: **aprovado pela Erica em 22/11** (pelo PM). Construído na branch local `feat/copiloto-e-fora-do-horario`, sem publicar.

## Decisões da Erica (22/11)

1. Aprovação pelo **WhatsApp pessoal do dentista** (o número `aprovador` da clínica), vinda do número da clínica.
2. **Nunca envia sozinha por tempo esgotado:** a resposta espera a aprovação o tempo que for. Níveis com envio automático podem vir depois, como opção.
3. **Sem marcação na agenda durante o copiloto:** a Clara pergunta dia e período de preferência, nome e telefone, e o dentista decide o horário (respondendo com o texto certo, por exemplo "Confirmado, terça 25/11 às 15h").
4. Prioridade: o modo "só fora do horário" vem antes, porque o 1º piloto começa com ele.

## Achado

O modo "só fora do horário de atendimento" não existia no fluxo: só a IA sabia, pelo texto da base, se a clínica estava aberta, e a Clara respondia sempre.

## Como funciona

**Duas chaves por clínica**, na tabela `config` do banco (vêm de `config_no_banco` do `clinica.json`):

| Chave | Valores | Efeito |
|---|---|---|
| `no_horario` | `sim` / `copiloto` / `nao` | o que a Clara faz com a clínica aberta |
| `fora_do_horario` | `sim` / `copiloto` / `nao` | o que a Clara faz com a clínica fechada |

`sim` = responde sozinha (como hoje); `copiloto` = escreve e espera o dentista aprovar; `nao` = fica quieta e só guarda a conversa (a equipe responde pelo celular). Sem as chaves, vale `sim` e `sim`: a demo não muda.

Semana 1 do piloto: `no_horario` = nao, `fora_do_horario` = sim. Semana 2: `no_horario` = copiloto. Mudar de modo é uma linha de SQL (ou `preparar_banco.py`), sem republicar o fluxo.

**Horário de atendimento** no `clinica.json` (vai para dentro do fluxo; feriados de `agenda.regras` contam como fechado):

```json
"horario_atendimento": { "1": ["08:00", "19:00"], "2": ["08:00", "19:00"], "6": ["08:00", "12:00"] }
```

Dias: 0 = domingo ... 6 = sábado. Pode ter dois turnos: `"1": [["08:00", "12:00"], ["14:00", "19:00"]]`. Obrigatório quando alguma chave não for `sim`.

**Aprovação.** Do número da clínica chega no WhatsApp do aprovador:

> *Aprovar resposta C7* · Maria (final 4521)
> Paciente: quanto custa a limpeza?
> Sugestão da Clara: A limpeza fica entre R$ 280 e R$ 350...
> Responda *ok* para enviar, *não* para não enviar nada, ou escreva o texto certo. Com mais de uma pendente, comece pelo código (ex.: "C7 ok").

- "ok" envia a sugestão; um texto envia o texto do dentista no lugar (e ele fica na conversa, para a Clara seguir dali); "não" descarta (o dentista responde por conta própria).
- Mensagem nova do paciente antes da aprovação: a sugestão antiga vira "substituída" e chega uma nova, que leva tudo em conta.
- A equipe respondeu o paciente pelo celular da clínica: a aprovação não envia nada (a pausa de 12 h continua valendo) e o dentista é avisado.
- Avisos para a equipe (urgência, chamar uma pessoa) continuam saindo na hora.
- Só o número do aprovador entra no caminho de aprovação, e só com o copiloto ligado.

## Risco e como voltar atrás

🟡 Médio: mexe na entrada das mensagens e no fim do atendimento. Voltar atrás: `no_horario` e `fora_do_horario` em `sim` (efeito na hora) ou reimportar a cópia do fluxo anterior. Tabela nova `copiloto_pendentes` (só acrescentada; precisa existir no banco antes de ligar o copiloto: rodar `preparar_banco.py`).
