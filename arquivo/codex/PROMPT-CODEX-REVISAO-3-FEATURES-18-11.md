# Prompt para o Codex: revisão de 3 features em sequência (18/11/2026)

Abra o Codex na pasta `Documents\Claude Code\keshion` (repositório privado `ericakrieger-bot/keshion`). Antes de colar, confira que nenhuma outra conversa está rodando teste da Clara (duas rodadas ao mesmo tempo apagam as fichas uma da outra) e que há saldo na conta da Anthropic (sem saldo a Clara responde "Só um instante, vou verificar" a tudo e os testes não valem). Copie tudo abaixo da linha e cole no Codex.

---

Você vai fazer uma revisão independente de três features que outra IA (Claude) montou, publicou e testou na assistente de WhatsApp da Keshion. Quero uma segunda opinião honesta: o que ficou certo, o que ficou errado ou pela metade, o que é arriscado e o que não foi testado. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: explique cada problema em linguagem simples, além do detalhe técnico.

Faça as três partes **em ordem, uma de cada vez**, e rode **um teste por vez** (nunca dois ao mesmo tempo).

## Regras de segurança (obrigatórias, a demo está no ar)

Leia e siga a seção "Regras de segurança" de `tecnico/n8n/PROMPT-CODEX-REVISAO.md`. Em resumo:
- só números com prefixo `554199900`;
- nada em produção sem me perguntar (fluxos, config, .env, credenciais, Docker, Whapi, usuários do Postgres, backups);
- nunca mostrar senha, token, chave privada do backup ou caminho do webhook;
- o Google Agenda é real: cancele o que marcar e confira que nada sobrou (sabe-se de um evento de teste antigo: Henrique, 19/11 às 14h, telefone 554199900810; só aponte, não apague sem me perguntar);
- não use os números 972584285541 e 972552994413 e **não force uma falha de envio real**;
- no backup, não restaure nada sobre os bancos de produção: se testar restauração, use só um contêiner descartável, sem rede.

## Parte 1: correções de 17/11 (noite) e 18/11 (manhã)

Leia `tecnico/n8n/PROMPT-CODEX-CORRECOES-17-11-NOITE.md` **inteiro** e siga exatamente o que ele pede (o que mudou, o que conferir e a entrega). Pule só as instruções de "colar no Codex". O relatório desta parte vai em `tecnico/n8n/revisao-codex-correcoes-17-11-AAAA-MM-DD.md`.

## Parte 2: conferência de data e hora antes de marcar (18/11, tarde)

**O que mudou.** O fluxo confere, antes de criar ou mudar evento, se o dia e a hora apareceram na conversa. A função `temData` em `tecnico/n8n/gerar_fluxos.py` agora também reconhece datas em inglês e espanhol ("Nov 19", "November 19th", "19 Nov", "the 19th", "Thursday 19", "11/19", "19 de noviembre") e horas ("9am", "4 pm", "at 4", "a las 9"), sem aceitar 11:19, R$ 1.019 ou "Thursday 11am" como dia. Antes, uma paciente em inglês ouvia 10 vezes "Esse horário não está disponível" sem aviso para a equipe. Publicado só no atendimento da demo (a clínica de teste foi gerada, não publicada). Cópia do fluxo anterior no servidor em `/opt/keshion/backup-atendimento-antes-data-ingles.json`.

**O que o Claude testou.** `node tecnico/n8n/teste_validacao_data_hora.js` (61 casos, todos certos), sem custo. Teste ponta a ponta na conversa dele ainda não foi feito (prompt em `tecnico/teste-ab/PROMPT-TESTE-18-11-data-em-ingles.md`).

**O que quero que você confira.**
1. Rode `teste_validacao_data_hora.js` e tente quebrar a conferência com casos novos: formatos que deveriam passar e não passam, e formatos que passam e não deveriam (valores em reais, horas, CEP, telefone, ano, ordinais, "next Friday", "amanhã", "daqui a 3 dias").
2. A conferência pode liberar uma marcação em dia ou hora errados? Pode bloquear uma marcação certa (falso negativo) e deixar a paciente num ciclo sem aviso?
3. O que acontece na 2ª ou 3ª recusa seguida? Existe aviso para a equipe? (Proposta pendente: avisar a equipe na 2ª recusa e usar frases fixas no idioma da paciente. Diga se faz sentido e se é urgente.)
4. O fluxo publicado na demo é igual ao gerado pelo código atual (só leitura, sem importar)?
5. Rode 3 a 5 conversas de teste em inglês, espanhol e português (números `554199900...`, uma por vez), marque e cancele pela conversa, e confira a agenda no fim.

## Parte 3: backup fora do servidor (18/11)

**O que mudou.** Todo dia às 03h, `tecnico/servidor/backup-postgres.sh` (instalado em `/opt/keshion/`) faz dump dos bancos, criptografa com `age` (chave pública no servidor, chave privada só no PC da Erica e no cofre de senhas), envia ao Google Drive da conta da Keshion pelo `rclone` (escopo só dos arquivos que ele cria, pasta `keshion-backups/`, retenção de 30 dias) e guarda a configuração (`.env`, Compose, Caddyfile). Confere se o dump terminou inteiro e escreve o resultado em `/opt/keshion/backups/STATUS-BACKUP.txt`. Backup local dos últimos 7 dias continua. O passo a passo está em `tecnico/servidor-n8n.md`, seção Backup. A restauração foi testada de ponta a ponta numa cópia isolada.

**O que quero que você confira (só leitura no servidor).**
1. Script: falha silenciosa (`set -e`, `pipefail`, dump parcial, disco cheio, rclone fora do ar, token do Google expirado), permissões dos arquivos e da pasta, o que aparece em log, `ps` ou histórico.
2. Segredos: a chave privada do `age` está só onde diz? A chave pública no servidor é mesmo só pública? O `.env` enviado ao Drive está criptografado? O `rclone.conf` tem permissão restrita?
3. Cobertura: todos os bancos entram (`clara`, `clinica_teste`, `n8n`, papéis e usuários)? Entra o que o n8n precisa para abrir as credenciais (chave de criptografia do n8n)? O que ficaria de fora numa restauração de verdade?
4. Retenção e limpeza: a de 30 dias no Drive e a de 7 dias local funcionam e não apagam o que não devem?
5. Aviso de falha: hoje só fica no `STATUS-BACKUP.txt`. Quanto tempo uma falha pode passar sem ninguém ver? Diga o que recomenda antes do piloto de 01/12.
6. Conferir o `STATUS-BACKUP.txt` da última rodada e se o arquivo mais recente no Drive existe e tem tamanho coerente (sem baixar nem abrir conteúdo de pacientes).
7. O aviso do rclone sobre o `client_id` compartilhado do Google Drive (será desativado em 2026): qual o risco e a data provável da quebra?
8. Restauração: leia o passo a passo e diga se uma pessoa que não é você conseguiria seguir. Se quiser testar, só em contêiner descartável, sem rede e sem a chave privada real: se precisar dela, **pare e me peça**.

## Entrega

1. As partes 1, 2 e 3 geram um relatório cada. Parte 1: o arquivo descrito no outro prompt. Parte 2: `tecnico/n8n/revisao-codex-data-hora-AAAA-MM-DD.md`. Parte 3: `tecnico/n8n/revisao-codex-backup-AAAA-MM-DD.md`.
2. Em cada relatório: resumo em 5 linhas (o que ainda impede ligar a Dra. Vivian em 01/12/2026), tabela de testes (teste, como fez, resultado, evidência), problemas do mais grave ao mais leve (o que é, por que importa em linguagem simples, como corrigir) e confirmação de limpeza (linhas de teste apagadas nos dois bancos e nenhum evento de teste novo na agenda).
3. No fim, um resumo de uma página juntando os três, com a lista do que corrigir primeiro.

Não corrija nada no código nem em produção: só aponte. Eu decido depois o que aplicar.
