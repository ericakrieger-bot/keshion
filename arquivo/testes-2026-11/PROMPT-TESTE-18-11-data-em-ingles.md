# Prompt de teste: data escrita em inglês na conferência de horário (18/11/2026)

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. **Só use depois que a Erica confirmar que o fluxo foi publicado** (a conversa que corrigiu avisa).

---

Projeto Keshion. Quero testar uma correção publicada na Clara da demo em 18/11: a conferência de horário antes de marcar agora entende datas escritas em inglês e espanhol. Leia `CLAUDE.md` e a seção "Resultado dos testes de 18/11" de `tecnico/RETOMAR-AQUI.md`. **Não mude nada no fluxo, nas instruções nem no servidor:** só rode os testes, confira e me traga o resultado. Se achar problema, descreva; quem corrige é outra conversa.

## O que mudou

Antes de marcar, o fluxo confere se o dia e a hora apareceram na conversa. Em 18/11 a data só era reconhecida como "19/11" ou "dia 19". Quando a Clara escrevia "Thursday, Nov 19" para a Emily (inglês), a conferência não achava a data e a Clara respondia 10 vezes, em português, "Esse horário não está disponível para avaliação", sem avisar a equipe (Emily tirou 2). Agora também aceita: "Nov 19", "November 19th", "19 Nov", "19th of November", "the 19th", "Thursday 19", "11/19" (formato dos EUA, só com dia acima de 12), "19 de noviembre", "el jueves 19", além do português de sempre. Um número solto (11:19, R$ 1.019, 19h) não vale como dia.

O teste local de expressões (61 casos) já passou. Para repetir, sem custo: `node tecnico/n8n/teste_validacao_data_hora.js` (precisa do fluxo gerado em `tecnico/n8n/gerados/clinica-demo/`).

## Antes de começar

- Confirme que nenhum outro teste está rodando: `select telefone, atualizado from pacientes where telefone like '554199900%' and atualizado > now() - interval '10 minutes'` no banco `clara`. Se houver fichas atualizadas, pare e me avise.
- Um teste por vez, nunca dois juntos. Anote a hora de Curitiba e se a clínica estava aberta (seg a sex, 8h às 19h) ou fechada.

## Testes, nesta ordem

1. **Emily sozinha, 2 vezes** (inglês; ficha 815, custo perto de US$ 0,05 cada):
   `python tecnico/teste-ab/paciente_simulado.py 815`
   Confira no relatório `.md`:
   - A Clara oferece horários em inglês e a avaliação é **marcada** (a ficha termina com avaliação).
   - A frase "Esse horário não está disponível" **não aparece** para um horário que a Clara mesma ofereceu.
   - Anote **como a Clara escreveu a data** (por exemplo "Thursday, Nov 19" ou "19/11") e como a Emily respondeu. Se na segunda vez a data saiu em outro formato, melhor ainda.
   - Depois de marcar, a Emily cancela: confirme que o cancelamento foi feito.
2. **Os 5 perfis de agenda** (confirma que o português continua funcionando): `python tecnico/teste-ab/paciente_simulado.py 801 803 807 811 815`
   Notas anteriores (18/11 manhã): Bia 8, Camila 8, Fernanda 6, Patrícia 9, Emily 6. Quem marcou antes tem de continuar marcando.
3. **Rodada completa de 22 perfis**, se possível com a clínica aberta: `python tecnico/teste-ab/paciente_simulado.py`. Na rodada de 18/11 (manhã) as notas foram de 6 a 9, menos Emily 2.
4. **56 mensagens fixas**, porque o fluxo mudou: `teste_n8n.py`, que roda no servidor (como rodar em `tecnico/testes-checklist.md`). Precisa dar 56 de 56 sem falha técnica.
5. **Agenda da demo:** depois de cada rodada, liste os eventos dos próximos 30 dias e apague os de teste que sobraram. O script só limpa o que a ficha lembra.

## O que me trazer

- Tabela com as notas por perfil, comparadas às anteriores, o custo que o script mostrou e a hora de Curitiba.
- Emily: marcou ou não, formato da data que a Clara usou, quantas vezes apareceu "Esse horário não está disponível" (a meta é zero para horário oferecido por ela).
- Resultado das 56 mensagens.
- Problemas novos, do mais grave ao mais leve, em linguagem simples.
- Confirmação de limpeza (fichas de teste e agenda).
- Atualize `tecnico/testes-checklist.md` ("Registro de rodadas") e acrescente uma linha em `tecnico/RETOMAR-AQUI.md` com o resultado. Faça commit e push só dos seus arquivos.
