# Decisões do app Keshion (16/11/2026)

> Reconstruído em 17/11/2026 a partir do resumo colado pela Erica. O arquivo completo, com o detalhamento da conversa, ficou no outro chat e não chegou a ser salvo nesta pasta. Se ele aparecer, substituir este pelo completo.

## Produto

- App web em Next.js que abre no computador e se instala no celular (PWA).
- Público: dentista solo ou clínica com 2 ou 3 dentistas, sem software de gestão.
- Piloto: Dra. Vivian, a partir de 01/12/2026.

## O que entra e quando

| Quando | Telas |
|---|---|
| Dezembro | Pendências, Conversas (assumir e devolver para a IA), Agenda do dia (compareceu e faltou), Pacientes |
| Janeiro | Orçamentos (PDF e envio pelo WhatsApp), Resultados (reais recuperados), Retornos |
| Fora | Prontuário, nota fiscal, financeiro, integrações |

## Hospedagem

- **Netlify grátis:** as telas. 300 créditos por mês; se acabarem, o site pausa.
- **Supabase grátis:** login, banco e arquivos. 500 MB; pausa com 7 dias sem uso; sem backup.
- Criar o Supabase na região São Paulo.
- Backup diário próprio para o Contabo.
- Cada clínica só vê os próprios dados (RLS, regra de acesso por linha no banco).

**Quando pagar:**
- Supabase Pro (US$ 25 por mês) no primeiro cliente pagante.
- Netlify Personal (US$ 9 por mês) quando os créditos passarem de 80%.

**Em aberto:** o banco "clara" vai para o Supabase ou o app lê os dados do Contabo.

## Domínio

keshion.com, com o app em app.keshion.com.

## Relatório de reais recuperados

- **Recuperado pela assistente (entra no total):** paciente parado há 7 dias ou mais sem contato da equipe, que respondeu à assistente e aceitou o tratamento em até 30 dias.
- **Influenciado:** fica em linha separada, fora do total.
- **Orgânico:** não conta.
- A clínica confirma o valor e pode contestar.

## Próximo passo

Calculadora de perdas e ROI. As perguntas estão no outro chat.
