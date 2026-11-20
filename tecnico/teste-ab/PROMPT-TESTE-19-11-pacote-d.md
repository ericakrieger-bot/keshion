# Prompt de teste: Pacote D (ferramentas de teste, backup e restauração), 20/11/2026

Cole tudo abaixo da linha na conversa de testes, aberta na pasta `Documents\Claude Code\keshion`. Pode ser no Sonnet. **O Pacote D não muda a Clara** (nem o fluxo, nem as instruções): muda as ferramentas que testam e o backup. Por isso este prompt é curto e a Clara só é usada para provar que a ferramenta nova funciona do mesmo jeito.

---

Projeto Keshion. Quero verificar o Pacote D (D1 a D3 de `tecnico/n8n/codex-19-11/PLANO-CORRECOES-2.md`). Leia `CLAUDE.md` e esse plano. **Não mude nada no fluxo, nas instruções nem no servidor, e não reinicie o n8n:** só rode, confira e me traga o resultado.

## O que mudou

- **D3 (ferramentas de teste):** `paciente_simulado.py`, `teste_n8n.py` e `teste_isolamento.py` agora (a) param com "ERRO DE LEITURA" se o SSH ou o SQL falhar, em vez de contar como "Clara sem resposta"; (b) levam para o relatório a falha de qualquer perfil ou conversa; (c) marcam a rodada como **INVÁLIDA** (arquivo `-INVALIDA`, código de saída 2, sem gravar notas em `historico-notas.csv`) se faltar perfil, conversa sem nota ou caso; (d) passam a senha do banco pelo ambiente, nunca em argumento; (e) no fim apagam fichas, mensagens, saídas simuladas **e reservas de vaga**, esperam 75 s e apagam de novo (saídas atrasadas), e avisam se sobrou linha.
- **D1 (backup):** o script do servidor tem `trap` antes de tudo (inclusive `mkdir` e `flock`), só diz `OK` depois de gravar e reler o status, e falha de gravação do status derruba o backup. **Só vale no servidor depois do OK da Erica e da instalação** (confira `sha256sum /opt/keshion/backup-postgres.sh` contra o do Git).
- **D2 (restauração):** roteiro em `tecnico/servidor-n8n.md` corrigido (usuário inicial `restaurador`, `--entrypoint sh`, `trap` apagando o arquivo de segredos). Já foi ensaiado de ponta a ponta com dados fictícios; não repita nada com a chave real.

## Passos

1. **Testes locais, sem custo** (no PC): `python tecnico/teste-ab/testar_ferramentas_teste.py` (esperado: "TUDO CERTO", 24 conferências) e `bash tecnico/servidor/testar-backup-local.sh` (esperado: 52 certas, 0 erradas, leva uns 90 s).
2. **Uma rodada curta da ferramenta nova, com a Clara no ar:** `python tecnico/teste-ab/paciente_simulado.py 801 803` (2 perfis, num terminal da Erica, PC acordado). Esperado: termina com código 0, relatório sem a faixa "RODADA INVÁLIDA", notas gravadas, nenhuma linha dos telefones 801 e 803 sobrando nas quatro tabelas (`pacientes`, `mensagens_recebidas`, `saidas_teste`, `reservas_horario`) depois do fim (a ferramenta espera cerca de 75 s antes de conferir). Anotar hora de Curitiba e custo.
3. **56 mensagens fixas** com o `teste_n8n.py` novo (caminho do webhook na variável `WEBHOOK_CAMINHO` em vez de argumento, como em `tecnico/testes-checklist.md`): esperado "FIM: 56/56 casos completos" e nenhuma linha sobrando dos telefones 101 a 107.
4. **Só se a Erica já tiver dado OK e a instalação do backup novo estiver feita:** conferir pelo SSH (só leitura) que `/opt/keshion/backup-postgres.sh` é o do Git, que `bash -n` passa e que `STATUS-BACKUP.txt` da próxima rodada das 03h (ou do backup manual que a Erica autorizar) está `OK` com os dois arquivos do mesmo horário. Sem OK, não rode backup.
5. **Relatório:** tabela dos passos 1 a 4 (esperado, o que aconteceu, OK ou problema), notas dos 2 perfis, resultado das 56, hora de Curitiba, custo e problemas em linguagem simples. Atualize `tecnico/testes-checklist.md` e `tecnico/RETOMAR-AQUI.md`; commit e push só dos seus arquivos.
