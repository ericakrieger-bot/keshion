# Plano de correções, rodada 2 (depois da verificação do Codex de 19/11/2026)

Relatório do Codex nesta pasta: `revisao-codex-verificacao-2026-11-19.md` (cópia; o original ficou em `OneDrive\Documentos\ChatGPT\KESHION\tecnico\n8n`, porque o Codex foi aberto de novo na pasta antiga: da próxima vez, abrir em `Documents\Claude Code\keshion`). O Claude conferiu no `gerar_fluxos.py` os achados C1 a C4, C7 e D3 (a parte do código; ver notas): procedem.

Resultado dos testes do Codex: 5 perfis média 7,8; 22 perfis média 7,32 (17/11: 7,23; 18/11: 7,05); 56 de 56; 7 conversas próprias de marcar e cancelar (pt, en, es) todas OK; zero "SEM RESPOSTA". Ou seja: o dia a dia da Clara está bom. O que sobra são **proteções que falham quando a IA erra** e itens de segurança e operação.

Já aceitos pela Erica (não corrigir agora): vaga presa por uns 4 min depois de cancelar; cancelamento perguntado duas vezes em um caso.

## Pacote C: fluxo da Clara (`tecnico/n8n/gerar_fluxos.py`), antes do piloto

| # | Problema (simples) | Como corrigir |
|---|---|---|
| C1 | "Sim, esse é meu telefone" pode cancelar a avaliação se a IA escolher cancelar por engano; "isso é só uma dúvida, pode dizer o preço?" também conta como "sim" | Cancelar só se a última fala da assistente **fala de cancelar** (cancelar, cancel, cancelar + a avaliação) e pergunta; o "sim" da paciente tem de ser curto e afirmativo, e negativa, pergunta ou outro assunto vencem. |
| C2 | Horário negado ("não posso 24/11 às 11h", "não marque ainda") ainda passa na conferência quando a IA monta a marcação | Na `parNaConversa`, olhar a negativa da mensagem mais recente antes de aceitar o par data/hora, nos 3 idiomas. |
| C3 | Urgência escrita como pergunta ("estou sangrando, o que faço?") não gera o aviso garantido, porque o fluxo exige "sem ?" e só vale se a IA respondeu "responder" | Tirar a condição `!pend.includes('?')` (linha ~699) e valer para qualquer ação; tratar negação ("não estou com febre", "no tengo fiebre") para não avisar à toa. |
| C4 | Quando a equipe assume pelo celular, 2 mensagens da Clara que já estavam saindo chegaram 14 s e 45 s depois | Reler a pausa (`pausado_ate`) no subfluxo de envio imediatamente antes de cada mensagem para a paciente e descartar as pendentes; avisos para a equipe continuam. |
| C5 | O aviso de falha pode levar texto livre do erro (`error.message`) com dado de paciente | Usar só clínica, código fixo do erro e ID da execução. |
| C6 | Áudio WAV renomeado para .ogg não transcreve (voz normal do WhatsApp em Ogg funciona) | Só trocar a extensão para `.ogg` quando for oga, opus ou sem extensão; manter nome, extensão e MIME dos demais. |
| C7 | O gerador rejeita o campo `numeros_keshion` vazio, mas o roteiro de clínica nova manda deixar vazio | `_faltando` aceita vazio nesse campo (clínica real); `preparar_banco.py` continua recusando número preenchido fora da demo e do teste. Testar o cadastro da Vivian de ponta a ponta sem publicar. |
| C8 | Aviso repetido para o mesmo assunto (Fernanda: 3 avisos); promessa de "urgência" sem a marca URGENTE (Marta); Diego: isenção de multa e agendamento normal ficaram todos com a equipe | Deduplicar por assunto, não por palavras; separar a exceção (pessoa decide) do agendamento normal (Clara continua oferecendo horários). **Prioridade menor**: pode ser feito com acompanhamento no piloto. |

Depois: gerar, rodar os testes locais (61+32, 48 do Pacote A, os do Codex em `tecnico/n8n/testes-codex/`, mais casos novos de C1 a C3 e C7), commit e push, pedir OK para publicar na demo (import e publish, sem reiniciar o n8n), conferir publicado = gerado e entregar prompt de teste. Incluir também a clínica de teste, que está com o fluxo antigo.

## Pacote D: servidor, backup e ferramentas de teste

| # | Problema | Como corrigir |
|---|---|---|
| D1 | Backup: duas falhas ainda deixam o "OK" antigo (`mkdir`/`flock` antes dos traps; falha ao gravar o status sai com código zero) | Traps desde a primeira linha, `CONCLUIDO=1` só depois do status gravado, falha de gravação vira falha do backup. Instalar no servidor só com OK. |
| D2 | Roteiro de restauração: para num erro que ele mesmo cria (usuário inicial já existe); `sh -c` com a imagem do n8n tenta rodar `n8n sh`; arquivo com segredo sem limpeza em erro | Usar outro usuário inicial no destino ou tratar o conflito esperado, `--entrypoint sh`, `trap` de limpeza. Testar de ponta a ponta no contêiner descartável. |
| D3 | Simulador e `teste_n8n.py`: perdem a leitura sem avisar (foi o que invalidou a rodada de 19/11 das 08h20) e dão nota baixa à Clara; senha vai em argumento do processo | Parar com erro claro quando a consulta SQL/SSH falhar, propagar falha das threads, exigir a contagem completa, senha por ambiente. Limpar também as saídas atrasadas e as reservas no fim. |

## Dependem da Erica

1. **Google Agenda: publicar o app OAuth** (sair do "modo Teste"). Em modo Teste a autorização expira em 7 dias: a Clara perde a agenda no meio do piloto (aconteceu hoje, `invalid_grant`, e a Erica reconectou). Passo a passo guiado na conversa certa. **É o item de operação mais urgente.**
2. Conta do Healthchecks.io (alerta do backup fora do WhatsApp), cliente OAuth próprio do rclone, contas limitadas `clara_app` e `clinica_teste_app` (B7, janela e OK). Até o monitor existir: conferir todo dia o `STATUS-BACKUP.txt` (responsável e substituto).
3. Com a Dra. Vivian: prazo real de retorno da equipe (a base diz "retornamos em instantes"), se a avaliação pode ser parcelada, dados da clínica, base, credenciais e aceite.

## Pode esperar depois do piloto

Fila de envio com confirmação de entrega, idempotência e coordenação de vaga por calendário e intervalo, duas avaliações para a mesma pessoa, histórico de cada versão das instruções, manifesto de hashes do backup, cópia imutável do backup, vocabulário de urgência em espanhol, resposta sobre "memória" da Clara (dizer que não guarda quando o histórico guarda).
