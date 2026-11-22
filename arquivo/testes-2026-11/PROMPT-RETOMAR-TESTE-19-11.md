# Retomar o teste do Pacote A (19/11): passos 2 e 3

Situação ao pausar (madrugada de 19/11, hora do PC): os casos 1 a 7 e os 5 perfis (caso 8) do prompt `PROMPT-TESTE-18-11-pacote-a.md` já foram feitos pela conversa de testes `teste-pacote-a` (notas dos 5 perfis: Bia 6, Camila 7, Fernanda 7, Patrícia 8, Emily 8; em `paciente-simulado-20261118-234158.md`). A rodada de 22 perfis travou (processo parado, sem processador nem conexão, 1h50 de execução contra 34 min normais) e foi encerrada sem gerar resultado. Nada foi publicado nem mudado no fluxo.

Quando rodar: depois das 8h de Curitiba (13h no relógio de Israel), com a clínica aberta. Antes, deixe o PC sem suspender (Configurações, Sistema, Energia, Suspender: Nunca).

Cole na conversa de testes `teste-pacote-a` (ou numa nova na pasta do projeto):

---

Projeto Keshion. Retome o teste do Pacote A (`tecnico/teste-ab/PROMPT-TESTE-18-11-pacote-a.md`). Os casos 1 a 7 e o caso 8 (5 perfis) já foram feitos; falta o resto. Não mude nada no fluxo, nas instruções nem no servidor: só rode, confira e relate.

1. **Antes de tudo:** confirme que nenhum teste está rodando (`select telefone, atualizado from pacientes where telefone like '554199900%' and atualizado > now() - interval '10 minutes'` no banco `clara`; e nenhum `python.exe` do `paciente_simulado.py` aberto no PC). Anote a hora de Curitiba e se a clínica está aberta.
2. **Limpeza da rodada travada:** apague de `pacientes`, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` (banco `clara`) as linhas dos telefones de teste de 18/11 (finais 8xx dos 22 perfis, 961 a 967 e 101 a 107 se ainda existirem). Liste os eventos do Google Agenda da demo de hoje até 30 dias à frente e apague só os de teste (descrição com telefone `554199900...`); não apague o evento antigo do Henrique (final 810) sem perguntar à Erica. Confirme o que apagou e o que sobrou.
3. **Rodada de 22 perfis** (um teste por vez, em segundo plano, sem ficar consultando): `python tecnico/teste-ab/paciente_simulado.py`. Comparar com 18/11 manhã (notas de 6 a 9, Emily 2) e com os 5 perfis de ontem à noite. Trazer custo e hora de Curitiba.
4. **56 mensagens fixas** (`teste_n8n.py` no servidor, como em `tecnico/testes-checklist.md`): 56 de 56 sem falha técnica.
5. **Limpeza final** igual ao passo 2 e conferência da agenda.
6. **Relatório:** tabela dos casos 1 a 7 (esperado, o que aconteceu, OK ou problema, com as saídas que provam), notas dos 5 e dos 22 perfis comparadas às anteriores com custo e hora de Curitiba, resultado das 56 e da limpeza, e problemas novos do mais grave ao mais leve em linguagem simples. Atualize `tecnico/testes-checklist.md` e `tecnico/RETOMAR-AQUI.md`, commit e push só dos seus arquivos.

---

Depois do relatório: a conversa principal escreve o prompt de verificação para o Codex (abrir o Codex na pasta `Documents\Claude Code\keshion`) e segue para a conexão Clara e App (`tecnico/PROMPT-CONEXAO-CLARA-APP.md`).
