# Prompt para a conversa técnica: decisões de 26/11 (dor, encaixe, cancelar e Jev)

Colar numa conversa nova, aberta na pasta `Documents\Claude Code\keshion`.

---

Projeto Keshion. Leia `tecnico/RETOMAR-AQUI.md`, principalmente a seção "Decisões da Erica em 26/11", e o registro de 26/11 em `tecnico/testes-checklist.md`.

**Passo 1: commits pendentes (peça meu OK antes).** O teste de 26/11 passou. O código do Pacote E e o do Jev em modo sombra ainda estão sem commit: faça dois commits, um de cada. Há outras mudanças soltas no repositório (site, comercial, `CLAUDE.md`): não misture.

**Passo 2: desenhar a mudança de dor e cancelar, e me mostrar os textos antes de publicar.**
1. Tirar a oferta de encaixe (base, parte 11, e instrução I). Reclamação de dor vai direto para a Dra. Suzana. Propor 1 ou 2 perguntas para a Clara colher informação ("Desde quando?", "Tem inchaço ou febre?"), sem diagnóstico. A dentista precisa aprovar.
2. Separar "dói?" (pergunta sobre procedimento, respondida pela base) de "estou com dor / está doendo" (vai para a Dra.). "Dói pra engolir depois da extração?" é queixa. Listar as respostas de "dói?" por procedimento para a dentista escrever ou aprovar; não inventar conteúdo clínico.
3. Tirar o "melhore logo" automático (instrução H).
4. Cancelar com uma confirmação só (dia e hora). A Clara não oferece cancelar se o paciente não pediu.
5. Manter como está: dificuldade de respirar ou engolir manda para pronto-socorro ou 192; "Valeu!" conta como sim até eu decidir.
6. Avaliar, sem construir: a Clara procurar na agenda uma consulta que não foi ela que marcou.

**Passo 3: Jev.** Fica em modo sombra até 03/12, sem mudar o fluxo publicado. Proponha uma lista de regras (critérios em português e cortes) para "dói?" x dor e para o cancelar, e teste só na bancada (`tecnico/jev-bancada/`), com frases que não foram usadas para ajustar. Peça meu OK antes de chamar a API. Ver também: o Jev não opina no cancelar quando a última fala da Clara não tem "?".

Regras de sempre: pedir OK antes de mudar produção, não reiniciar o n8n, e os testes ao vivo ficam para a conversa de testes (me entregue o prompt de teste pronto).
