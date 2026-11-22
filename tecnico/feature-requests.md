# Pedido ao dev: recontato de pacientes que faltaram e de pacientes sem voltar

Data: 18/11/2026. Origem: copy do site (`site/copy-v3.html`, seção 5, "Pacientes atuais"). A Erica quer que o dev avalie se estas duas funções cabem no roadmap.

## O que o site promete (se as funções entrarem)

1. **Quem faltou.** O paciente que não compareceu recebe uma mensagem da assistente para remarcar, e a vaga volta a ser ocupada.
2. **Quem está sem voltar.** Pacientes que passaram do prazo de revisão ou de retorno aparecem em uma lista no app (tela Reativar e Retornos), e a assistente os chama de volta.

## Situação hoje

- A tela **Agenda do dia** do app prevê marcar "compareceu" ou "faltou" (decisões de 16 a 18/11, dezembro).
- A tela **Reativar e Retornos** do app prevê a lista de quem está sem voltar (janeiro).
- Falta decidir se a **assistente envia a mensagem sozinha** nos dois casos. Isso não está no roadmap de `RETOMAR-AQUI.md`. Só estão previstas as confirmações (48 h, véspera e 2 h antes), depois do piloto.

## Perguntas para o dev

- Dá para disparar a mensagem de remarcação quando o app marcar "faltou"? Em que prazo depois da falta?
- Como definir "sem voltar" (prazo por tipo de tratamento, por clínica)? Sugestão: um prazo configurável em `clinica.json`.
- A mensagem ativa fora da janela de 24 h do WhatsApp exige modelo aprovado pela Meta. Hoje, com o Whapi, isso muda? E na API oficial?
- Limite de envios por dia, para não parecer spam nem arriscar o número.
- A conversa deve voltar para o app em "Precisa de você" quando o paciente responder?

## Decisão pendente da Erica

Se as duas funções não entrarem na construção, o texto da seção 5 do site perde os cartões "Quem faltou" e "Quem está sem voltar".
