# Prompt para o Codex: verificar as correções dos Pacotes A e B e fazer um teste geral (19/11/2026)

**Abra o Codex na pasta `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`** (não na pasta antiga do OneDrive, onde ele salvou os relatórios de 18/11). Antes de colar, confira que nenhuma outra conversa está rodando teste da Clara (duas rodadas ao mesmo tempo apagam as fichas uma da outra), que há saldo na conta da Anthropic e que o PC não vai dormir durante a rodada (rodadas longas já travaram quando o PC dormiu). Copie tudo abaixo da linha e cole no Codex.

---

Você fez em 18/11/2026 uma revisão independente da assistente de WhatsApp da Keshion (Clara) e do backup. Os relatórios estão em `tecnico/n8n/codex-18-11/` (resumo: `resumo-codex-tres-revisoes-2026-11-18.md`; plano de correções do Claude: `PLANO-CORRECOES.md`). Outra IA (Claude) corrigiu e publicou. Quero agora duas coisas: **(1) confirmar, com evidência, se cada achado seu foi mesmo corrigido; (2) um teste geral independente** da Clara. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: explique cada problema em linguagem simples, além do detalhe técnico.

Um teste por vez, nunca dois ao mesmo tempo. Não corrija nada no código nem em produção: só aponte.

## Regras de segurança (obrigatórias, a demo está no ar)

Leia e siga a seção "Regras de segurança" de `tecnico/n8n/PROMPT-CODEX-REVISAO.md` e as do prompt de 18/11 (`tecnico/n8n/PROMPT-CODEX-REVISAO-3-FEATURES-18-11.md`). Em resumo: só números com prefixo `554199900`; nada em produção sem me perguntar; nunca mostrar senha, token, chave privada do backup nem caminho do webhook; o Google Agenda é real (cancele o que marcar e confira que nada sobrou; existem eventos antigos que não são de teste, como o do Sergio e o do Henrique, final 810: aponte, não apague); não use os números 972584285541 e 972552994413; não force falha real de envio; no backup, não restaure nada sobre produção (só contêiner descartável, sem rede, e sem a chave privada real).

## O que mudou desde a sua revisão

**Pacote A (fluxo da Clara, publicado na demo em 18/11 às 17h36 de Curitiba, sem reiniciar o n8n; gerador `tecnico/n8n/gerar_fluxos.py`):**
- A1: só deixa de avisar a equipe quando a mensagem nova é confirmação pura (ok, obrigada, 👍, thanks, gracias). Informação nova gera aviso ou complemento (no máximo 1 a cada 15 min). Urgência (sangramento, inchaço, febre, dor forte, pus, desmaio) sempre gera aviso novo marcado URGENTE.
- A2: contador `recusas_agenda` na ficha. 1ª recusa por data não reconhecida: pede o dia e o mês. Da 2ª em diante: avisa que a equipe vai confirmar e a equipe recebe aviso com o motivo técnico.
- A3 e A4: aceita hoje/amanhã nos 3 idiomas; data e hora precisam estar juntas e ligadas na mesma mensagem; minutos, mês e ano têm de bater; segundos diferentes de zero são recusados.
- A5: só cancela se a última fala da Clara foi pergunta de confirmação e a paciente disse que sim; "não, quero manter" mantém a avaliação.
- A6: campo `idioma` e frases fixas em português, inglês e espanhol.
- A7: "I'll forward / let me check / voy a pasar" também viram aviso para a equipe.
- A8: trava de vaga de 5 min e limite de 30 s nas chamadas ao Google da marcação.

**Pacote B (backup e roteiros):** script `tecnico/servidor/backup-postgres.sh` novo instalado no servidor em 18/11 às 10h10 (erro tratado desde o início, status `EM ANDAMENTO` e `OK` só no fim, `flock`, retenção local por idade); `tecnico/servidor-n8n.md` (restauração com `ON_ERROR_STOP`, `pipefail`, `pg_isready`); `tecnico/n8n/CLINICA-NOVA.md` sem reinício do n8n. **Ainda não feitos de propósito:** alerta externo (Healthchecks.io, falta a Erica criar a conta), client_id próprio do Google para o rclone e as contas limitadas `clara_app` e `clinica_teste_app` (B7). Não conte esses três como "esquecidos"; conte como pendências e diga se bloqueiam o piloto de 01/12.

## O que o Claude testou (para você não repetir de olhos fechados, mas pode contestar)

- Testes locais sem custo: `node tecnico/n8n/teste_validacao_data_hora.js` (61 + 32), `node tecnico/n8n/teste_pacote_a.js` (48) e seus dois scripts em `tecnico/n8n/codex-18-11/` (extras 27 de 33; os 6 restantes são formatos que não adivinhamos de propósito: "às nove" por extenso, "next Friday", "12/1").
- Ao vivo (18/11): casos 1 a 7 passaram (sangramento depois de recibo gera aviso URGENTE; "amanhã às 11h" marca; cancelar em inglês com "Yes"; "não, quero manter" mantém; espanhol; duas opções sem misturar; ver `tecnico/RETOMAR-AQUI.md` e `tecnico/testes-checklist.md`). 5 perfis: Bia 6, Camila 7, Fernanda 7, Patrícia 8, Emily 8.
- **A rodada de 22 perfis de 19/11 às 08h20 é inválida** (o teste perdeu a leitura das respostas por volta das 08h28; o n8n não teve erro). Não use essas notas.
- **Problemas já conhecidos e aceitos por mim (não precisa reportar de novo, só diga se discorda):** (a) depois de cancelar, a vaga fica presa por até uns 4 minutos pela trava de 5 min (a chance de outra paciente pedir exatamente aquele horário nesse tempo é muito baixa); (b) em um caso a paciente foi perguntada duas vezes se queria cancelar. Fora esses dois, quero tudo.

## Parte 1: o que você achou foi corrigido?

Para **cada item** do seu `resumo-codex-tres-revisoes-2026-11-18.md` e dos três relatórios, diga: corrigido, corrigido pela metade ou não corrigido, com a evidência (código lido, teste local, conversa de teste ou consulta no servidor) e se ainda impede ligar a Dra. Vivian em 01/12/2026. Confira em especial:
1. O fluxo publicado na demo é igual ao gerado pelo código atual (só leitura, sem importar), e o que existe na clínica de teste.
2. Reproduza os seus casos locais de 18/11 contra o código novo (`testes_locais_revisao_2026_11_18.js`, `testes_data_hora_extras_2026_11_18.js`) e tente quebrar de novo a conferência de data e hora, o aceite do cancelamento e a recusa repetida.
3. Backup: o `STATUS-BACKUP.txt` da primeira rodada automática do script novo (19/11, 03h de Curitiba): deve ter `OK`, nomes com segundos e dois arquivos coerentes no Drive (só nomes e tamanhos; não baixe nada). Releia o script, as simulações de falha que você fez antes e o roteiro de restauração (outra pessoa conseguiria seguir?). Diga se o backup sem alerta externo é aceitável até 01/12 ou o que fazer.

## Parte 2: teste geral independente da Clara

Use os mesmos scripts e roteiros que o Claude usa, para a comparação ser justa, e rode **de um terminal seu, em segundo plano e com o PC acordado**:
1. 5 perfis de agenda: `python tecnico/teste-ab/paciente_simulado.py 801 803 807 811 815`, depois os **22 perfis**: `python tecnico/teste-ab/paciente_simulado.py` (de preferência com a clínica aberta, depois das 8h de Curitiba). Compare com as notas anteriores (`tecnico/teste-ab/historico-notas.csv`; 17/11 e 18/11 manhã: 6 a 9, exceto Emily 2 antes da correção da data em inglês). Confira se há "SEM RESPOSTA" e, se houver, se a causa é a Clara ou o teste.
2. 56 mensagens fixas (`teste_n8n.py` no servidor, como em `tecnico/testes-checklist.md`): 56 de 56 sem falha técnica.
3. Os seus próprios casos, escritos por você, sem seguir o roteiro do Claude: pelo menos 3 conversas em português, 2 em inglês e 2 em espanhol com marcação e cancelamento; um relato de urgência depois de um aviso administrativo; pedido repetido de horário que a demo não tem; pedido de cancelar respondendo "não" e depois "sim"; mensagens em rajada; mídia (áudio, foto) se a ferramenta permitir sem envio real. Procure o que o Claude não pensou.
4. Limpeza: ao fim, apague as fichas, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` dos telefones de teste que usou, nos dois bancos (`clara` e `clinica_teste`), cancele o que marcou e confira a agenda do Google de hoje até 30 dias (a ficha só lembra uma avaliação; os scripts podem deixar eventos para trás).

## Entrega

1. Relatório em `tecnico/n8n/revisao-codex-verificacao-AAAA-MM-DD.md`: resumo em 5 linhas (o que ainda impede ligar a Dra. Vivian em 01/12/2026); tabela "achado de 18/11, situação, evidência"; tabela de testes (teste, como fez, resultado, evidência); problemas novos do mais grave ao mais leve (o que é, por que importa em linguagem simples, como corrigir); confirmação de limpeza (linhas apagadas nos dois bancos e nenhum evento de teste novo na agenda).
2. Uma página final com a lista do que corrigir primeiro e o que pode esperar até depois do piloto.
3. Se criar scripts ou evidências, ponha em `tecnico/n8n/evidencias-verificacao-AAAA-MM-DD/` sem segredos.
