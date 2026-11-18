# Prompt de teste: avisos, idioma, clínica fechada e hora em inglês (18/11/2026)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet.

---

Projeto Keshion. Quero testar correções publicadas na Clara da demo em 18/11 de manhã. Leia `CLAUDE.md` e a parte "Custo dos testes (18/11)" de `tecnico/RETOMAR-AQUI.md`. **Não mude nada no fluxo, nas instruções nem no servidor:** só rode os testes, confira e me traga o resultado. Se achar problema, descreva; quem corrige é outra conversa.

## O que mudou

1. **Avisos:** quando o motivo é parecido com o do último aviso (até 90 min), antes o aviso era engolido. Agora, se a mensagem do paciente traz pergunta ou informação nova, sai um aviso curto começando com `*Complemento do aviso anterior*`. Só "ok", "obrigada" e mensagens curtas sem pergunta continuam sem aviso.
2. **Idioma:** o pedido para a IA termina com "Responda no idioma em que o paciente está escrevendo, inclusive ao oferecer horários."
3. **Clínica fechada:** a base diz "Com a clínica fechada, nunca fale em encaixe."
4. **Hora em inglês:** antes de marcar, o fluxo confere se o dia e a hora apareceram na conversa. Antes só reconhecia "9h", "9:00", "às 9". Agora também "9am", "4 pm", "4:00 p.m.", "at 4" e "a las 9".

## Antes de começar

- Confirme que nenhum outro teste está rodando. Fichas dos números de teste atualizadas nos últimos 10 minutos indicam outro teste em andamento; nesse caso, pare e me avise:
  `select telefone, atualizado from pacientes where telefone like '5541999%' and atualizado > now() - interval '10 minutes'` no banco `clara`.
- Rode um teste por vez, nunca dois juntos.
- Anote a hora de Curitiba: com a clínica aberta (seg a sex, 8h às 19h) e fechada, a Clara segue regras diferentes.

## Testes, nesta ordem

1. **Paciente simulado, 5 perfis** (custo perto de US$ 0,15 mais a Clara):
   `python tecnico/teste-ab/paciente_simulado.py 801 803 807 811 815`
   Para comparar, as notas anteriores (`historico-notas.csv`) foram:
   - 17/11 à tarde: Bia 9 e 8, Camila 8 e 8, Fernanda 9 e 9, Patrícia 9,5 e 9, Emily 8 e 7,5.
   - 18/11 às 22h37 de Curitiba: 8, 7, 6, 7 e 7.

   Confira no relatório `.md`:
   - **Emily:** a Clara oferece os horários em inglês, e a avaliação é **marcada** (a ficha termina com avaliação). A frase "Esse horário não está disponível" não pode aparecer para um horário que a Clara mesma ofereceu. Se marcou, confira que foi cancelada no fim ou cancele.
   - **Fernanda e Camila:** toda vez que a Clara diz que vai verificar ou passar para a Dra. Suzana algo novo, existe aviso (normal ou complemento). Conte quantos avisos e complementos cada uma recebeu e se algum se repete sem nada novo.
   - **Camila com a clínica fechada:** nenhuma menção a "encaixe" nem a "vir hoje".
   - Qualquer "(SEM RESPOSTA EM 160 s)": anote em qual paciente e turno.
2. **Se o passo 1 estiver bom, rodada completa de 22 perfis**, se possível em horário comercial de Curitiba (custo perto de US$ 0,60 mais a Clara):
   `python tecnico/teste-ab/paciente_simulado.py`
3. **56 mensagens fixas**, porque o fluxo mudou: `teste_n8n.py`, que roda no servidor. Veja como rodar em `tecnico/testes-checklist.md`. Precisa dar 56 de 56 sem falha técnica.
4. **Agenda da demo:** depois de cada rodada, liste os eventos dos próximos 30 dias na agenda da demo e apague os de teste que sobraram. O script só limpa o que a ficha lembra.

## O que me trazer

- Tabela com as notas de cada perfil comparadas às anteriores, o custo que o script mostrou e a hora de Curitiba da rodada.
- Para Emily, Fernanda e Camila: marcou ou não, quantos avisos e complementos, e se apareceu "encaixe".
- Resultado das 56 mensagens.
- Problemas novos, do mais grave ao mais leve, em linguagem simples.
- Confirmação de limpeza (fichas de teste e agenda).
- Atualize `tecnico/testes-checklist.md` e acrescente uma linha em `tecnico/RETOMAR-AQUI.md` com o resultado. Faça commit e push.
