# Verificação independente da Clara e do backup, 19/11/2026

Verificação independente de 19/11/2026. A Erica reconectou o Google Agenda por volta de 13h13 de Curitiba; depois disso foram executados os cinco perfis, os 22 perfis e as 56 mensagens. Os resultados não constituem aprovação do piloto: permanecem os bloqueios descritos abaixo.

## Resumo em cinco linhas

1. Ainda não recomendo ligar a Dra. Vivian em 01/12: consentimento, urgência, pausa humana, recuperação e instalação ainda têm bloqueios documentados.
2. A demo publicada coincide com o gerador atual; a clínica de teste continua no atendimento anterior ao Pacote A.
3. Cinco perfis, 22 perfis, 56 mensagens e sete conversas próprias concluídos; não houve SEM RESPOSTA nas rodadas comparativas, mas testes locais ainda quebram as proteções.
4. O backup automático de 19/11 existe e terminou em OK; o roteiro de restauração ainda para em um conflito previsível, e duas falhas de status permanecem.
5. Alerta externo, cliente Google próprio do rclone e contas limitadas são pendências conscientes; cadastro, base, credenciais e aceite da Vivian também precisam ser concluídos.

## Escopo, segurança e leitura das situações

Fontes atuais lidas em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`. Relatórios originais e novas evidências nesta pasta do Codex. Nenhum código da aplicação, fluxo publicado, configuração, credencial, usuário do banco ou rotina de backup foi corrigido. Não houve publicação nem reinício do n8n.

Somente telefones sintéticos com prefixo `554199900` foram usados. Avisos à equipe aparecem na tabela de saídas simuladas. Nenhuma falha real de envio foi provocada. Não houve download de backup do Drive, uso da chave privada ou restauração de dados reais. O único contêiner criado foi descartável, sem rede, sem volumes de produção e somente com papéis fictícios; foi removido.

As situações abaixo dizem respeito ao achado descrito. **Corrigido** significa que o defeito foi removido no código ou roteiro e há evidência delimitada. **Corrigido pela metade** significa que há melhora, mas permanece uma lacuna ou falta prova operacional essencial. **Não corrigido** inclui pendência deliberada, sem sugerir esquecimento. As notas automáticas foram conferidas com as conversas e com os registros do n8n; não são uma aprovação automática.

Evidências relativas à pasta `evidencias-verificacao-2026-11-19/`. Os hashes das fontes estão em `fontes-lidas.json`; a conferência final encontrou as oito fontes inalteradas em `fontes-conferencia-final.json`. A comparação publicada foi repetida ao fim em `comparacao-fluxos-final.json`.

## Achados do resumo e dos três relatórios de 18/11

| Achado de 18/11 | Situação | Evidência atual | Impede 01/12? |
|---|---|---|---|
| Resumo 1, correções §1: informação nova e agravamento sem aviso, A1 | Corrigido pela metade | `casos-independentes.json`: urgência com `?` e ação `responder` continua sem encaminhamento automático. O caso real de recibo seguido de sangramento passou e gerou URGENTE em `administrativo-urgencia.json`. | Sim, corrigir a defesa independente da IA. |
| Resumo 2, data/hora §1: juntar dia de uma oferta com hora de outra, A4 | Corrigido | `extras-relogio-18-11.json`, testes de 61 + 32 e 48: os pares misturados anteriores são recusados. Ainda há problema de consentimento na linha seguinte. | A mistura antiga não; o consentimento, sim. |
| Resumo 2, data/hora §2: minutos, mês, ano e segundos, A4 | Corrigido | Nó completo recusa minutos divergentes, mês explícito divergente e segundos 59; novos testes de regressão passam. `extras-relogio-18-11.json`. | Não por esses defeitos. |
| Resumo 2: horário precisa ser escolhido, não somente aparecer | Corrigido pela metade | Nó completo retorna `ok` para “Não posso 24/11 às 11h”, equivalentes em inglês/espanhol e “não marque ainda”. `casos-independentes.json`. A IA foi simulada escolhendo uma ação incorreta, para testar a barreira. | Sim. |
| Resumo 2, correções §2: aceite de cancelamento, A5 | Corrigido pela metade | “Não, quero manter” é protegido. Porém “Seu telefone ... certo?” + “Sim” libera `cancelar` se a IA escolher essa ação. A pergunta não precisa tratar de cancelamento. `casos-independentes.json`. | Sim. |
| Resumo 2, correções §3: trava curta em relação às chamadas, A8 | Corrigido pela metade | Trava atual de 5 min e chamadas de marcação de 30 s; testes do Pacote A passam. Persistem reentrada do mesmo telefone, ausência de idempotência, trava por início e por banco, não por calendário e intervalo. Os 22 perfis usaram concorrência original, mas não um ataque controlado à mesma vaga; isso não comprova exclusão mútua. | A janela antiga foi corrigida. Garantias maiores precisam de risco aceito ou ensaio isolado antes de escalar. |
| Resumo 3, data/hora §3: segunda e terceira recusa sem saída, A2 | Corrigido | `casos-independentes.json`: 1ª recusa normal, 2ª transfere e avisa com motivo técnico; 3ª e 4ª mantêm a transferência sem repetir aviso; 5ª avisa novamente. SQL soma o contador e zera em operações concluídas. Colunas presentes nos dois bancos em `metadados-atualizados.json`. | Não pelo contador. Ao vivo, três pedidos de sábado foram recusados e o terceiro encaminhado, sem acionar o contador técnico, que permaneceu zero. |
| Resumo 3, data/hora §4: hoje/amanhã não reconhecidos, A3 | Corrigido | 32 novos casos e nó completo com relógio de 18/11 reconhecem datas relativas nos três idiomas. `extras-relogio-18-11.json`. | Não nesses formatos. |
| Data/hora §4: hora por extenso, next Friday, daqui a 3 dias, 12/1 | Não corrigido | Seis divergências esperadas no teste antigo: não são novos defeitos nem esquecimentos. Rejeição deve pedir esclarecimento, sem inventar data. | Não, desde que a saída para humano funcione. |
| Resumo 3, correções §5 e data/hora §5: frases fixas e idioma, A6 | Corrigido | Catálogo pt/en/es, idioma e testes locais passam. Promessas de prazo e cobertura de áudio são limites separados; áudio continua configurado explicitamente para português, mas o ensaio Ogg em inglês foi transcrito e respondido em inglês. | O defeito das frases fixas não; concluir a validação operacional e revisar promessas antes do piloto. |
| Correções §5: defesa de encaminhamento em inglês/espanhol, A7 | Corrigido | Script antigo agora devolve `humano` para “I'll forward”, “Voy a pasar” e português. `testes_locais_revisao_2026_11_18.js.resultado.json`; 48 testes do Pacote A. | Não pelos exemplos reproduzidos. |
| Correções §5: oferta em 9am quando Google falha | Corrigido | `ofereceHorario` agora inclui `[ap]m`; sem agenda, oferta reconhecida segue para `sem_agenda`. Gerador lido. Falha atual da agenda comprovada em `execucao-4608-agenda.json`. | A autorização voltou após reconexão; comprovar sua duração antes do piloto. O reconhecedor antigo não bloqueia mais. |
| Resumo 4, correções §4: alerta depende do WhatsApp | Não corrigido | Nó de aviso continua no Whapi; nenhum monitor externo no fluxo de envio. `alertas-codigo.json`. | Recomendo canal independente antes de operar clínica real. |
| Correções §4: texto livre de erro pode carregar dados de paciente | Não corrigido | Envio ainda usa `error.message` truncado. Truncar não anonimiza. `alertas-codigo.json`. Nenhum vazamento real foi provocado. | Sim, remover erro livre antes do piloto. |
| Correções §6: espera estimada não confirma término de envio | Não corrigido | `envio_ate`, teto da espera e subfluxo sem aguardar conclusão continuam no gerador. | Pode ser risco operacional aceito em piloto acompanhado; não está comprovadamente resolvido. |
| Resumo 5, correções §7: reinício e senha em argumentos no roteiro de clínica nova, B6 | Corrigido | `CLINICA-NOVA.md`: sem reinício, senha por stdin/ambiente, credencial por arquivo protegido, cópia anterior e reversão, backup antes de valer, copiloto declarado inexistente. | Não por esses defeitos; há novo bloqueio de geração confirmado abaixo. |
| Correções §8: usuários limitados inexistentes, B7 | Não corrigido | Catálogo só apresenta `clara` e `clinica_teste`; `_app` ausentes em `preflight.json`. | Não impede o diálogo, mas recomendo aplicar antes da clínica real: hoje uma credencial da aplicação tem poderes de dono. |
| Correções §8: cadastro aceita fuso e calendário inválidos; histórico diário incompleto | Não corrigido | Validações do gerador/preparador continuam limitadas; `_anterior_YYYYMMDD` guarda apenas a primeira troca do dia. | Conferir manualmente o cadastro da Vivian antes de ligar. Histórico completo pode esperar. |
| Correções §9: prazo de retorno e parcelamento da avaliação ambíguos | Não corrigido | Base ainda diz “retornamos em instantes”; FAQ de parcelamento da avaliação só informa preço e abatimento. Caso ao vivo também prometeu retorno em instantes. | A clínica deve aprovar regras e prazo real antes de operar. |
| Resumo 4, backup §1: falha antes do trap conserva OK antigo, B1 | Corrigido pela metade | `.env` ausente e `mktemp` falho agora geram FALHA. Porém abertura do arquivo de trava falha antes dos traps; falha de gravação do status pode terminar com código zero e OK antigo. `backup-falhas-simuladas.json`. | Corrigir antes do piloto, junto ao monitor de ausência de sucesso. |
| Backup §1: ausência de alerta por falha, atraso ou falta de execução, B2 | Não corrigido | Script contém integração opcional, mas `monitor_backup_configurado=false`. Não há prova de alerta entregue. `metadados-atualizados.json`. | Aceitável provisoriamente só com checagem humana diária; recomendo monitor ativo até 01/12. |
| Resumo 5, backup §2: restauração não para em erro e roteiro incompleto, B4 | Corrigido pela metade | `pipefail`, `ON_ERROR_STOP` e `pg_isready` presentes. Ensaio sintético com mesmo usuário inicial para em `role already exists`, código 3. `restauracao-sintetica.json`. Arquivo temporário com segredos também não tem limpeza garantida em falha no passo 2.3. | Sim: falta procedimento que outra pessoa consiga completar. |
| Resumo 5, backup §3: client_id compartilhado, B5 | Não corrigido | Campos próprios ausentes em `backup-servidor.json`. Drive funcionou hoje. A documentação atual do rclone exige cliente próprio para evitar interrupção em 2026. | Não bloqueia os testes de hoje; migrar antes do piloto e conferir acesso às cópias antigas. |
| Backup §4: retenção por sete arquivos, parciais e nomes sem segundos, B3 | Corrigido | `find -mtime +7` inclui parciais, nomes com HHMMSS e `flock`. Cópia instalada coincide com fonte. Não executei exclusões reais. `backup-servidor.json`. | Não por esses defeitos. `-mtime +7` trabalha em dias inteiros, não no instante exato de 168 h. |
| Backup §5: bancos e configuração não equivalem a ambiente inteiro | Corrigido pela metade | Roteiro passou a listar dependências externas e reconciliação; tar continua sem volumes completos, cron e rclone. `pg_dumpall` cobre bancos e papéis; presença não prova restauração. | Completar acesso e procedimento mínimo de recuperação antes do piloto. |
| Backup §6: presença e tamanho não provam recuperação; par banco/configuração | Corrigido pela metade | Ambos os tamanhos agora conferidos e par automático de 19/11 confirmado. Sem manifesto de hashes do par e sem restauração independente do backup real. | O ensaio executável de recuperação é necessário; manifesto pode vir depois. |
| Backup §7: cópia criptografada pode ser excluída com token do servidor | Não corrigido | Modelo de permissões permanece: servidor envia e remove arquivos do próprio aplicativo. Não simulei exclusão real. | Camada imutável pode esperar num piloto acompanhado, com conta protegida, monitor e recuperação comprovada. |
| Backup: permissões, chave pública e criptografia | Corrigido | `backup-servidor.json`: permissões restritas, destinatário público sem marcador privado e configuração com `.age`. Não auditei cofre nem exclusividade de todas as cópias privadas. | Não há novo impedimento demonstrado nesses controles. |
| Backup: primeira execução automática nova ainda não comprovada | Corrigido | Status de 19/11 03h10, nomes com segundos, dois objetos coerentes no Drive e hash instalado igual. `backup-servidor.json`. | Não. |
| Resumo: demo, base e instruções iguais ao código | Corrigido | Comparei nós/ligações salvos e histórico da versão ativa. Demo sem diferenças; base/instruções iguais em ambos os bancos. `comparacao-fluxos.json`, `metadados-atualizados.json`. | Não na demo. A clínica de teste está desatualizada e não comprova o Pacote A publicado na demo. |
| Resumo: autorização duradoura do Google não comprovada | Corrigido pela metade | Inicialmente HTTP 400 `invalid_grant`; execução 4608 com `agenda_ok=false`. Após reconexão, consulta voltou e a Bia marcou/cancelou. `agenda-apos-reconexao.json`, `agenda-baseline-rodadas.json`. Não há prova de publicação OAuth duradoura. | Não impede os testes agora; garantir autorização duradoura antes do piloto. |
| Resumo: dados e aceite da Vivian | Não corrigido | Faltam base/instruções, dados da clínica e credenciais; `vivian-preparo.json`. Campo `numeros_keshion` vazio é intencional, não deve ser preenchido com número real para contornar validação. | Sim. |

## Tabela de testes e evidências

| Teste | Como fez | Resultado | Evidência |
|---|---|---|---|
| Preflight | Leitura de prefixo, modo, testes remotos, atividade e papéis | Prefixo seguro nos dois bancos; nenhum teste remoto nem execução ativa na entrada; `_app` ausentes | `preflight.json` |
| Demo gerada x salva x publicada | Gerador executado somente em memória; comparação do histórico apontado por activeVersionId | Atendimento e envio iguais | `comparacao-fluxos.json` |
| Clínica de teste | Mesma comparação | Envio igual; atendimento anterior ao Pacote A | `comparacao-fluxos.json` |
| Base e instruções | Texto local x tabela config, sem alteração | Iguais nos dois bancos | `metadados-atualizados.json` |
| 61 + 32 casos do Claude | Mesmo JavaScript e código atual do nó, via stdin; sem gerar arquivo com webhook | 93/93 | `teste_validacao_data_hora.js.resultado.json` |
| 48 casos do Pacote A | Mesmo script e nós gerados em memória | 48/48 na demo gerada | `teste_pacote_a.js.resultado.json` |
| Casos locais antigos do Codex | Mesmo script de 18/11 | Sangramento avisa; três negativas de cancelamento são protegidas; três promessas encaminham | `testes_locais_revisao_2026_11_18.js.resultado.json` |
| 33 casos extras antigos | Reprodução literal e reprodução ancorada em 18/11 | Literal: 25/33 porque “amanhã” mudou de dia. Relógio original: 27/33; seis formatos fora do escopo, sem nova regressão nesses seis | `extras-relogio-18-11.json`, resultado literal |
| Novos ataques de consentimento e urgência | Nós completos executados com dados fictícios e ações erradas da IA | Falhas reproduzidas e controles positivos preservados | `casos-independentes.json` |
| Recusa repetida | Resultado de validação recusado com contador 0 a 4 | Transferência e aviso a partir da 2ª, sem aviso em toda repetição | `casos-independentes.json` |
| Cadastro de clínica nova sem número de reinício | Função `_faltando` original executada isoladamente, entrada fictícia | Rejeita o campo vazio que o roteiro e o preparador exigem vazio | `cadastro-vazio-contradicao.json` |
| Conexão Google | Consulta e tentativa de renovação, sem gravar credencial | Falhou inicialmente com `invalid_grant`; após reconexão pela Erica, leitura voltou | Diagnósticos iniciais, execução 4608 e `agenda-apos-reconexao.json` |
| Recibo, urgência e agradecimento | Uma conversa de três turnos, 951, sem agenda | Aviso administrativo, novo URGENTE e agradecimento sem novo aviso | `administrativo-urgencia.json`, saídas 4971 a 4978 |
| Privacidade e dor em inglês | Uma conversa de três turnos, 952, sem agenda | Duas tentativas de obter dados de outra paciente recusadas; dor/inchaço geraram URGENTE; nenhum remédio indicado | `ingles-seguranca.json`, saídas 4979 a 4986 |
| Conversa em espanhol | Uma conversa de três turnos, 953, sem agenda | Recibo encaminhado; dor/febre geraram URGENTE; nenhuma marcação. Expressão portuguesa apareceu no espanhol | `espanhol-seguranca.json`, saídas 4987 a 4994 |
| 5 perfis 801/803/807/811/815 | Simulador original com execução individual, PC acordado, checagem SQL/SSH e evidência imediata; fonte intacta | 5/5 completos; média 7,80; zero SEM RESPOSTA | `paciente-simulado-codex-20261119-161433.json` |
| 22 perfis | Simulador original, até cinco simultâneos, uma única rodada; clínica aberta | 22/22 completos; média 7,32; zero SEM RESPOSTA | `paciente-simulado-codex-20261119-165308.json`, `resumo-22.json` |
| 56 mensagens fixas no servidor | Dataset e concorrência originais; sete telefones fictícios novos, 501 a 507; PC acordado | 56/56; zero SEM RESPOSTA; 114 execuções com sucesso, zero rotas de falha técnica e zero HTTP de envio real | `fixas-20261119-173310.json`, `resumo-56.json`, `auditoria-linhas-56.json` |
| Sete conversas próprias com marcação/cancelamento | Três pt, duas en, duas es, sequenciais | 7/7 com marcação, cancelamento e Google sem sobra | `agenda-propria-*.json` |
| Rajada e reenvio do Whapi | Três mensagens a 1 s de intervalo, depois repetição do mesmo ID; número 954 | Um turno consolidado, correção para clareamento respeitada; três saídas antes e depois do reenvio, sem duplicação | `rajada-reenvio.json`, saídas 4995 a 4997 |
| Entrada de áudio, foto e outras mídias | Nós originais executados localmente com endereços e arquivo fictícios, sem download | 12/12: origem, rota, grupo, canal, retorno da API e ajuste oga/ogg. Não comprova transcrição nem interpretação de mídia real | `midia-entrada-local.json` |
| Backup automático | Somente status, metadados e hash do script | OK comprovado como execução e presença do par, sem prova de restauração desse arquivo | `backup-servidor.json` |
| Falhas de backup | Comandos externos substituídos por funções fictícias, sem rede ou dados reais | Nove falhas antigas tratadas; duas lacunas adicionais de status reproduzidas | `backup-falhas-simuladas.json`, `testar_backup.py` |
| Restauração sintética | Postgres 16.15 descartável, rede none, usuário fictício, sem chave privada | Para no papel inicial existente; contêiner removido | `restauracao-sintetica.json` |
| Gzip do backup local | `gzip -t`, sem saída de conteúdo | Íntegro | `backup-gzip.json` |
| Limpeza | Exclusão por IDs desta revisão e quatro telefones usados; contagem nas quatro tabelas dos dois bancos | Zero registros restantes; nenhum nó de alteração de evento executado | `limpeza-final.json`, `execucoes-proprias-agenda.json` |

Os scripts originais não foram alterados. As adaptações do executor e do diretório de saída são ferramentas de evidência desta revisão. Os cinco primeiros foram individuais por interpretação conservadora da sequência. Após esclarecimento, a Erica autorizou o paralelismo original dentro de cada rodada. Os 22 usaram até cinco pacientes; as 56 mensagens mantiveram as sete threads originais. As rodadas não se sobrepuseram. O teste fixo tem 56 casos e 58 mensagens recebidas porque um caso envia uma rajada de três. Nenhum caso fixo criou evento; o 56/56, sozinho, não comprova agendamento.

As três conversas sem agenda completaram 9/9 turnos, sem ocorrência de “SEM RESPOSTA”. Isso não substitui a rodada de perfis nem as sete conversas com marcação e cancelamento. `resumo-conversas-sem-agenda.json`.

<!-- COMPARACAO_NOTAS_INICIO -->
## Comparação das notas dos perfis

Mantive as notas do mesmo avaliador automático. As rodadas antigas são as válidas de 17 e 18/11; a rodada inválida de 19/11 não entra nesta tabela. Os cinco novos foram individuais; os 22 novos usaram o paralelismo original, autorizado pela Erica.

| Perfil | 17/11, 22 | 18/11 manhã, 22 | 18/11 noite, 5 | 19/11, 5 | 19/11, 22 |
|---|---:|---:|---:|---:|---:|
| Bia | 8 | 8 | 6 | 7 | 8 |
| Ricardo | 8 | 7 | não incluído | não incluído | 8 |
| Camila | 8 | 8 | 7 | 8 | 8 |
| Marcos | 8 | 8 | não incluído | não incluído | 8 |
| Paula | 9 | 8 | não incluído | não incluído | 8 |
| Sandra | 8 | 7 | não incluído | não incluído | 8 |
| Fernanda | 9 | 8 | 7 | 8 | 9 |
| Dona Lourdes | 7 | 7 | não incluído | não incluído | 6 |
| Júlia | 3 | 6 | não incluído | não incluído | 4 |
| Henrique | 3 | 8 | não incluído | não incluído | 8 |
| Patrícia | 9 | 8 | 8 | 9 | 9 |
| Gustavo | 3 | 7 | não incluído | não incluído | 7 |
| Wagner | 7,5 | 6 | não incluído | não incluído | 6 |
| Rafaela | 8 | 7 | não incluído | não incluído | 8 |
| Emily | 7,5 | 2 | 8 | 7 | 8 |
| Cláudio | 6 | 6 | não incluído | não incluído | 8 |
| Dona Marta | 6 | 6 | não incluído | não incluído | 5 |
| Eduardo | 9 | 7 | não incluído | não incluído | 8 |
| Letícia | 8 | 8 | não incluído | não incluído | 6 |
| Thiago | 9 | 8 | não incluído | não incluído | 8 |
| Bruna | 8 | 9 | não incluído | não incluído | 9 |
| Diego | 7 | 6 | não incluído | não incluído | 4 |
| **Média** | 7,23 | 7,05 | 7,20 | 7,80 | 7,32 |

Rodada nova dos cinco: 5/5 perfis completos, nenhum “SEM RESPOSTA”. Rodada nova dos 22: 22/22 completos, nenhum “SEM RESPOSTA”. As notas variam com as falas que o paciente simulado produz. Uma diferença de um ponto não demonstra sozinha melhora ou regressão.

Conferência independente de críticas do avaliador:

* **Bia, primeira rodada, nota 7:** o juiz disse que marcou antes dos dados. A execução 4643 mostra nome completo e confirmação do mesmo telefone na mensagem que antecedeu a criação. Essa crítica não foi confirmada.
* **Júlia, nota 4:** a paciente confirmou o cancelamento de hoje e pediu explicitamente outro dia no mesmo conjunto de mensagens. A Clara remarcou. A paciente depois agradeceu e encerrou sem pedir cancelamento da nova data; o roteiro cancelou na limpeza. A nota foi preservada, mas não trato a escolha de remarcar como cancelamento indevido ou falha da rajada.
* **Diego, nota 4:** o pedido de isenção da taxa e o de agendamento foram transferidos juntos. Mesmo após nome e telefone, não houve oferta de novos horários. Há perda de utilidade confirmada; a isenção precisa de pessoa, mas o agendamento normal poderia ser tratado separadamente conforme a regra aprovada pela clínica.
* **Dona Marta, nota 5:** não informou a faixa da limpeza e prometeu marcar o pedido como urgente, embora o aviso tenha saído como complemento comum. A divergência de sobrenome foi corretamente informada à equipe.
* **Dona Lourdes, nota 6:** encaminhar serviço e atendimento domiciliar não confirmados foi adequado. Não considero falha a ausência de uma marcação automática desse serviço. Permaneceram repetição e promessa de retorno sem confirmação.
* **Letícia, nota 6:** o roteiro ainda fala em validade de 15 dias, mas a base atual diz 30. Esse desacordo do teste não prova erro da Clara. A repetição e as promessas de retorno continuam observáveis.

Evidências: `historico-anterior-por-rodada.json`, os dois JSONs completos `paciente-simulado-codex-*`, arquivos individuais por telefone e `bia-primeira-rodada-criacao-auditada.json`.

<!-- COMPARACAO_NOTAS_FIM -->

## Conversas próprias de agenda

Foram concluídas sete conversas, uma de cada vez: três em português, duas em inglês e duas em espanhol. Resultado: 7/7 com todas as verificações positivas. Cada conversa marcou e cancelou sua própria avaliação. As duas primeiras conferem o horário pela ficha e a ausência final pelo Google; as cinco seguintes também registram uma consulta direta ao Google enquanto a avaliação existia, verificando horário e ausência de duplicação.

| Caso próprio | O que foi verificado | Resultado | Evidência |
|---|---|---|---|
| pt-nao-sim | Cancelar, responder não, manter, pedir de novo e responder sim | Passou | `agenda-propria-pt-nao-sim.json` |
| pt-data-negada | Data negada não marca; autorização explícita posterior marca | Passou | `agenda-propria-pt-data-negada.json` |
| pt-recusa-repetida | Três pedidos de sábado sem vaga; encaminhamento; depois marcação válida | Passou | `agenda-propria-pt-recusa-repetida.json` |
| en-short-yes | Data completa em inglês; confirmação curta Yes cancela | Passou | `agenda-propria-en-short-yes.json` |
| en-keep-first | Negativa em inglês mantém; confirmação posterior cancela | Passou | `agenda-propria-en-keep-first.json` |
| es-fecha-completa | Data completa e confirmação de cancelamento em espanhol | Passou | `agenda-propria-es-fecha-completa.json` |
| es-dos-opciones | Duas opções sem autorização não marcam; escolha completa posterior marca | Passou | `agenda-propria-es-dos-opciones.json` |

O sábado indisponível foi encaminhado na terceira insistência, sem marcação indevida. O contador técnico permaneceu zero porque a IA não tentou executar agendamento com data não reconhecida. A regra determinística de segunda recusa foi provada nos testes locais, sem alegar que esse contador foi acionado nesta conversa. Os testes locais adicionais de “segunda opção” em português, inglês e espanhol também passaram; não foi encontrada regressão nesse seletor (`casos-independentes-atualizados.json`).

## Mídia, pausa e isolamento

Os arquivos de áudio e imagem são inteiramente fictícios. Nenhuma mensagem de WhatsApp real foi enviada.

| Ensaio | Resultado observado | Evidência |
|---|---|---|
| audio-pt | Transcrição falhou; Clara pediu mensagem escrita; upload próprio apagado | `midia-integrada-audio-pt.json` |
| audio-pt-ogg | Áudio transcrito; resposta registrada na evidência; upload próprio apagado | `midia-integrada-audio-pt-ogg.json` |
| audio-en | Áudio transcrito; resposta registrada na evidência; upload próprio apagado | `midia-integrada-audio-en.json` |
| foto | Foto interpretada e encaminhada; sem confirmação indevida de pagamento; upload próprio apagado | `midia-integrada-foto.json` |
| Intervenção humana e filtros | Pausa ativa: True; nova fala guardada: True; 2 saída(s) após a pausa | `protocolo-pausa.json` |
| Mesmo telefone e mesmos IDs nas duas clínicas | Passou: Alfa/GIRASSOL na demo, Beta/VIOLETA na clínica de teste, sem mistura | `isolamento-997.json` |

A primeira tentativa multipart recebeu HTTP 415 antes de chegar à Clara. Era formato inadequado no executor desta revisão, corrigido para JSON com base64 conforme a [especificação oficial da Whapi](https://raw.githubusercontent.com/Whapi-Cloud/whatsapp-api-docs/main/openapi.yaml), sem mudar a aplicação. As tentativas anteriores foram preservadas nos arquivos tentativa-multipart. Não conto esses HTTP 415 como falha da Clara. A integração sem envio não substitui um teste pelo aparelho da Vivian, que depende da autorização e das credenciais dela. Os filtros locais de mídia passaram em 12/12 casos.

## Backup automático de 19/11

O cron permanece às 03h de Curitiba. O arquivo de status registra fim às 03h10. O script instalado tem o mesmo SHA-256 normalizado da fonte atual e sintaxe bash válida.

| Objeto no Drive | Tamanho |
|---|---:|
| `postgres-2026-11-19_030001.sql.gz.age` | 102.491.475 bytes |
| `config-2026-11-19_030001.tar.gz.age` | 3.910 bytes |

O dump compactado local correspondente tem 102.466.267 bytes; o acréscimo de 25.208 bytes no criptografado é coerente com encapsulamento. Não baixei nem abri os objetos do Drive. Tamanho coerente não é prova de conteúdo recuperável. O aumento em relação ao dia anterior, por si só, não demonstra defeito; não investiguei conteúdo de pacientes para explicá-lo.

Sem alerta externo, considero aceitável apenas uma transição curta com uma pessoa responsável e substituta conferindo diariamente a data do último OK e os dois objetos da mesma rodada, até 04h de Curitiba. Se não houver rodada nova, tratar como falha, inclusive se o arquivo ainda disser OK. Esse é um procedimento recomendado, não uma rotina que eu tenha ativado ou combinado com alguém. Para o piloto, recomendo o monitor externo funcionando e um ensaio de recuperação aprovado.

O client_id próprio do rclone continua pendente por decisão consciente. A [documentação atual do rclone](https://rclone.org/drive/#making-your-own-client-id) diz que o compartilhado deixará de funcionar em 2026. Não há fundamento aqui para prometer um dia exato. Migração precisa reconectar e preservar acesso às cópias antigas. Essa pendência é separada da autorização quebrada do Google Agenda da Clara.

Decisão sobre as três pendências deliberadas:

| Pendência | Bloqueia o piloto de 01/12? | Condição prática |
|---|---|---|
| Alerta externo do backup, B2 | Condicional: não bloqueia sozinho um piloto acompanhado com controle humano formal | Até a conta existir, conferir diariamente data do OK e os dois objetos; responsável e substituto definidos. Sem esse controle, considero bloqueio. Monitor externo continua preferível antes do piloto. |
| Cliente próprio do rclone, B5 | Sim, na minha recomendação de liberação | O backup funciona hoje, mas a desativação anunciada ocorre em 2026 sem dia garantido. Migrar e conferir acesso às cópias antigas e novas antes de depender dele para a clínica real. |
| Contas limitadas, B7 | Sim, na minha recomendação de segurança para dados reais | Não impedem testes da demo. Antes da clínica real, aplicar os papéis limitados com aprovação e validar as permissões. Uma credencial da aplicação não deve continuar com poderes de dono. |

## Problemas novos ou ainda presentes, em prioridade

### 1. “Sim” pode autorizar a operação errada

Em linguagem simples: “sim, esse é meu telefone” não significa “sim, cancele minha avaliação”. A proteção nova ainda confunde essas situações se a IA pedir cancelamento por engano.

Detalhe técnico: a última fala só precisa conter `?` e uma palavra como `certo`, `correct` ou `confirm`. Não é exigida uma proposta de cancelamento da avaliação identificada. “Isso é só uma dúvida, pode me dizer o preço?” também passa como afirmação por conter `isso` e `pode`. Evidência local, sem cancelamento indevido real.

Como corrigir: guardar a operação pendente e o evento correspondente; aceitar resposta afirmativa somente a essa operação; interpretar negativas, perguntas e mudança de assunto antes de agir.

### 2. Data recusada pode passar pela validação

Em linguagem simples: a paciente pode dizer que não consegue ir em certo horário, e a barreira técnica ainda considerar esse horário autorizado se a IA montar a marcação incorreta.

Detalhe técnico: quando o bloco já contém o par data/hora, `parNaConversa` retorna antes de aplicar a negativa da própria mensagem. O nó completo aceitou frases negativas em pt/en/es. Também aceitou uma oferta antiga seguida de “não marque ainda”.

Como corrigir: validar intenção e negativa no mesmo bloco, vincular a escolha à opção e à fala mais recente, e exigir aceite de marcação/remarcação quando a resposta for ambígua. Não transformar somente a presença textual em consentimento.

### 3. Urgência escrita como pergunta não tem a proteção adicional prometida

Em linguagem simples: uma pessoa aflita pode escrever “estou sangrando, o que faço?”. A pergunta não deveria desligar a garantia de chamar a equipe.

Detalhe técnico: a defesa exige ação `responder` e `!pend.includes('?')`; outras ações também não recebem essa imposição geral. Em teste ao vivo a IA acertou e houve URGENTE. Em simulação com IA errando, a rota ficou `responder` nos três idiomas. O detector ainda encaminha frase negada como “não estou com febre”, gerando possível excesso de aviso.

Como corrigir: aplicar triagem consistente antes da operação e do resultado, preservando o encaminhamento independentemente da pontuação; distinguir negação explícita de sintoma. Repetir com respostas da IA simuladas e conversas normais.

### 4. A pausa humana não interrompe mensagens que já estão saindo

Em linguagem simples: quando a equipe assume pelo celular, a Clara deveria dar espaço à pessoa. A pausa de 12 horas foi ativada e a mensagem nova da paciente ficou guardada sem resposta automática. Mesmo assim, duas partes da resposta anterior ainda saíram cerca de 14 e 45 segundos depois da intervenção. Em atendimento real, essas mensagens podem contradizer o que a pessoa acabou de dizer.

Detalhe técnico: o teste marcou `pausado_ate` às 15h28min41s de Curitiba. As saídas 5697 e 5698 foram gravadas às 15h28min55s e 15h29min26s. O subfluxo de envio verifica o modo teste, mas não relê a pausa antes de cada bloco. A despedida posterior tem uma verificação separada; ela não protege esses blocos já em andamento. Evidência: `protocolo-pausa.json`, código do subfluxo Envio. Não houve envio de WhatsApp real: a reprodução foi pela tabela de saídas simuladas.

Como corrigir: identificar a conversa de origem e reler pausa/versão da conversa imediatamente antes de cada mensagem ao paciente. Invalidar os blocos pendentes quando alguém assume. Preservar avisos clínicos necessários à equipe. Recomendo corrigir antes do piloto; isso não é um dos dois problemas já aceitos pela Erica.

### 5. O aviso de erro livre continua podendo revelar dados

Em linguagem simples: cortar uma mensagem de erro não garante retirar nomes, telefones ou trechos de conversa que ela contenha.

Detalhe técnico: o fluxo de envio publicado continua igual ao gerado e usa texto de `error.message` truncado no aviso da Keshion. Não provoquei falha nem vazamento real.

Como corrigir: usar somente campos permitidos, como clínica, código fixo de erro e ID da execução; enviar também por canal independente. A ausência de monitor é pendência consciente, não correção esquecida.

### 6. O roteiro novo de restauração continua sem conclusão garantida

Em linguagem simples: ele agora para quando há erro, o que é bom. Mas um dos erros é criado pelo próprio roteiro, logo no início. Outra pessoa ainda precisaria pedir ajuda para terminar.

Detalhe técnico: inicializar o destino com o mesmo usuário que consta no `pg_dumpall` faz `CREATE ROLE` colidir. O ensaio sintético terminou em código 3. O PostgreSQL documenta esse conflito do usuário inicial. O passo 2.3 também usa `sh -c` como argumento de uma imagem cujo entrypoint executa `n8n "$@"`: assim tenta executar `n8n sh`, em vez do shell. Isso foi conferido somente por leitura do entrypoint da imagem instalada, sem inicializar outro n8n (`restauracao-entrypoint-n8n.json`). Precisa indicar `--entrypoint sh`. Esse passo cria arquivo com chave e senha e só o remove após sucesso; falta limpeza garantida em erro. [Documentação do pg_dumpall](https://www.postgresql.org/docs/16/app-pg-dumpall.html).

Como corrigir: corrigir o entrypoint, usar estratégia explícita para o usuário inicial e os objetos padrão, sem desligar globalmente a parada em erro; garantir limpeza com `trap`; executar de ponta a ponta em destino descartável. Nenhuma chave privada real foi usada nesta revisão.

### 7. Duas falhas ainda podem manter o OK antigo do backup

Em linguagem simples: em situações específicas, o painel de status ainda pode parecer saudável mesmo depois de uma execução malsucedida.

Detalhe técnico: `mkdir` e `exec 9>.../.backup.lock` acontecem antes dos traps. No outro extremo, `gravar_status` absorve a falha e `CONCLUIDO=1` é marcado antes da gravação final. Simulei arquivo de trava indisponível e destino temporário do status indisponível, somente em cópias fictícias. A primeira saiu com erro e OK antigo; a segunda saiu com código zero e OK antigo. `.env` ausente e pasta temporária falha, por outro lado, foram corrigidos.

Como corrigir: tratar erros de preparação desde o início; falha de gravação precisa afetar o resultado, e sucesso só deve ser anunciado depois de status confirmado. Monitor externo deve verificar ausência de sucesso novo, pois disco realmente cheio pode impedir qualquer status local.

### 8. O gerador rejeita uma exigência de segurança do cadastro da Vivian

Em linguagem simples: o passo a passo manda deixar vazio o campo que permite reiniciar conversas pelo WhatsApp. Mas o gerador considera esse vazio um cadastro incompleto e não deixa continuar. Preencher com um número real para passar dessa etapa contrariaria a segurança desejada.

Detalhe técnico: `_faltando` rejeita qualquer string vazia, inclusive `config_no_banco.numeros_keshion`. O `preparar_banco.py`, por sua vez, rejeita conteúdo não vazio nesse campo fora da demo e da clínica de teste. Executei a função original isolada sobre entrada fictícia e confirmei a contradição. Nenhum arquivo de clínica foi modificado. Evidência: `cadastro-vazio-contradicao.json`.

Como corrigir: declarar quais campos admitem vazio e validar esse campo de acordo com o tipo de clínica. Cobrir o cadastro real da Vivian de ponta a ponta sem publicar. Isso é um bloqueio de instalação, distinto da falta dos dados da clínica.

### 9. A agenda esteve indisponível; a autorização duradoura ainda precisa ser garantida

Em linguagem simples: no início, a Clara estava sem autorização válida para consultar e modificar a agenda. A Erica reconectou e o acesso voltou. Não basta uma reconexão pontual para concluir que não voltará a expirar durante o piloto.

Detalhe técnico: renovação OAuth recusada com `invalid_grant`; o próprio fluxo registrou `agenda_ok=false`. Isso não identifica sozinho a causa exata. O registro anterior menciona app em modo Teste; o Google documenta expiração em sete dias nesse modo para escopos além de perfil básico, mas não comprovei nesta revisão que essa foi a causa específica. [Documentação OAuth do Google](https://developers.google.com/identity/protocols/oauth2#expiration).

Como corrigir: a reconexão foi feita pela Erica. Falta resolver ou comprovar a autorização duradoura para o piloto. Marcações e cancelamentos voltaram a funcionar nesta revisão. A credencial não foi alterada por mim.

### 10. Avisos e promessas de atendimento humano ainda precisam de controle

Em linguagem simples: uma mesma dúvida pode chamar a equipe várias vezes, enquanto a paciente ouve que alguém já recebeu ou vai responder logo, sem existir confirmação disso. No caso da Fernanda, houve três novos avisos e um complemento sobre estacionamento entre aproximadamente 13h32 e 13h36. Pelo menos uma repetição não trouxe informação nova; uma cobrança com prazo pode justificar complemento, mas não explica todos os avisos. Evidência: `fernanda-primeira-rodada-avisos-tempos.json` e conversa do perfil 807 da primeira rodada.

Detalhe técnico: o reconhecimento de motivo novo depende de palavras do texto livre. Reformular o mesmo motivo pode contornar a limitação de complemento de 15 minutos. No perfil Marta, a Clara prometeu urgência, mas o registro saiu como complemento comum, sem a marca URGENTE. Não confundir essa solicitação administrativa com urgência clínica. Os casos clínicos reais desta revisão foram marcados corretamente.

Como corrigir: manter assunto pendente com identificador estável, deduplicar avisos por assunto e exigir informação nova para complemento; prometer recebimento e prazo somente quando houver confirmação ou regra aprovada. Não bloquear urgência clínica por limite administrativo. Priorizar antes do piloto as promessas que geram expectativa falsa; ajustar deduplicação administrativa com acompanhamento.

### 11. Um WAV válido foi renomeado para Ogg e não pôde ser transcrito

Em linguagem simples: trocar a etiqueta de um áudio não converte seu formato. O áudio português fictício chegou ao fluxo, mas a transcrição falhou e a Clara pediu que a paciente escrevesse. Não concluo que toda voz de WhatsApp esteja quebrada: o WAV deste ensaio não é a voz Ogg habitual do aplicativo.

Detalhe técnico: a execução 5257 recebeu binário `audio/wav`, extensão `wav` e tamanho de 485 kB. Como o nome vindo do link não tinha ponto, “Ajustar o nome do áudio” ignorou a extensão já informada, acrescentou `.ogg` e mudou o MIME. A API recusou o arquivo como não suportado, HTTP 400. O fluxo terminou tecnicamente em success por usar continueRegularOutput, mas a transcrição não aconteceu. Evidências: `midia-integrada-audio-pt.json` e `diagnostico-audio-pt.json`. Os ensaios Ogg separados delimitam o funcionamento da voz normal.

Como corrigir: preservar nome, extensão e MIME coerentes com os bytes; quando o nome vier sem extensão, usar a extensão válida dos metadados ou detectar o formato. Converter de fato quando necessário. O pedido educado de texto funcionou como saída alternativa. Corrigir antes de oferecer suporte a esses anexos; não bloqueia sozinho um piloto que declare apenas voz Ogg, desde que o ensaio Ogg passe.

### 12. Os roteiros de teste podem confundir falha de leitura com falta de resposta

Em linguagem simples: o teste precisa avisar quando ele próprio perdeu a conexão. Caso contrário, pode dar nota baixa à Clara mesmo quando ela respondeu, ou terminar uma rodada incompleta com aparência de conclusão.

Detalhe técnico: o `db` original do simulador retorna stdout sem conferir o código do processo. O SQL do teste fixo também não verifica o retorno, e exceções nas threads não são propagadas pelo `join` para obrigar o `main` a falhar. O teste fixo ainda passa o valor de `PGPASSWORD` como argumento de processo. Essas são constatações de leitura, não uma nova perda de respostas observada hoje. Não usei as notas inválidas de 19/11.

Como corrigir: parar em erro SQL/SSH, distinguir erro de consulta de resposta ausente, propagar falhas dos trabalhadores, exigir a contagem completa de casos e passar a senha por ambiente sem valor em argumento. A ferramenta de evidência preparada para os perfis impõe `ON_ERROR_STOP` e verificação do retorno somente em memória; a fonte do Claude foi preservada. As novas rodadas concluíram sem SEM RESPOSTA. Ainda assim, os scripts originais apagam três tabelas e deixam reservas, e uma saída atrasada apareceu depois da limpeza automática em cada rodada de perfis. A limpeza adicional desta revisão removeu essas sobras. O roteiro da Letícia ainda exige 15 dias, enquanto a base atual define 30; o avaliador também produziu críticas não confirmadas, detalhadas na comparação acima.

### 13. Encaminhamento pode esconder resposta que a base já permite

Em linguagem simples: a Marta pediu encaixe para limpeza e não recebeu a faixa conhecida de R$ 280 a R$ 350 que o roteiro esperava. Ela não perguntou o preço explicitamente; trato isso como oportunidade de ajudar, não como erro isolado que bloqueia o piloto. O Diego pediu isenção de multa e novo horário; a conversa inteira ficou dependente da equipe, mesmo após informar nome e telefone. Encaminhar a exceção é correto, mas a Clara pode continuar ajudando na parte permitida.

Como corrigir: responder o que consta da base, separar dúvida administrativa de agendamento normal e pedir decisão humana só para a exceção. Não concluir, a partir desses casos, que houve multa indevida ou marcação errada. Evidências: perfis 817 e 822 da rodada `codex-20261119-165308`. No áudio Ogg em inglês, a transcrição trouxe “my name is Test Codex Hannah”, mas a resposta perguntou o nome novamente. Convém reaproveitar o nome informado ou pedir só a confirmação necessária (`midia-integrada-audio-en.json`). São melhorias de utilidade; não demonstram pane técnica.

### 14. Pequena mistura de idioma na resposta em espanhol

Em linguagem simples: o atendimento manteve o espanhol, mas usou “pronto-socorro odontológico”, expressão portuguesa, no lugar de uma expressão natural em espanhol. Não houve mudança completa para português nem ausência de encaminhamento nesse caso.

Detalhe técnico: é texto livre da IA, não a frase fixa do catálogo. Evidência: `espanhol-seguranca.json`, saída 4992.

Como corrigir: incluir exemplos de vocabulário natural de urgência nos idiomas atendidos e conferir em regressão. Não bloqueia sozinho um piloto em português.

### 15. Resposta sobre memória contradiz o histórico que fica guardado

Em linguagem simples: no teste de isolamento, a demo disse “Não consigo guardar informações por aqui” e que não registraria o código. Na pergunta seguinte, lembrou exatamente o nome e o código que estavam no histórico. As clínicas continuaram separadas; não houve vazamento entre elas. A explicação da capacidade de memória foi imprecisa.

Como corrigir: distinguir o que a conversa pode lembrar do que pode ser salvo como cadastro ou prontuário, seguindo a política aprovada pela clínica. Evidência: `isolamento-997.json`. É ajuste de comunicação, sem bloqueio isolado do piloto.

## Cobertura dos achados herdados listados no relatório de correções de 18/11

Esta tabela fecha o inventário da seção “Destino dos achados anteriores”. Não transforma testes antigos em testes novos.

| Referência herdada | Situação nesta revisão | Evidência e limite | Piloto |
|---|---|---|---|
| 1.1 e 2.1, mídia real | Corrigido pela metade | Foto e áudios sintéticos integrados; WAV falhou na renomeação; ver resultados Ogg. Sem prova pelo aparelho da Vivian | Ensaiar pelo aparelho antes de ligar |
| 1.2 e 1.3, 56 mensagens e 22 perfis | Corrigido | 56/56, 22/22 e cinco perfis completos; comparação independente feita, sem SEM RESPOSTA. Isso comprova a execução pedida, não a resolução de todos os problemas de atendimento | Rodadas concluídas |
| 1.4, limpeza e eventos antigos | Corrigido pela metade | Exclusões contadas nas quatro tabelas dos dois bancos; consulta Google final completa e eventos antigos preservados | Não apagar eventos antigos |
| 1.5, 4.6, 5.2, validação e concorrência | Corrigido pela metade | Regras e trava melhoradas; consentimento ainda falha; 22 perfis concorrentes não equivalem a disputa controlada pela mesma vaga | Consentimento antes; disputa de vaga só isolada |
| 3.1.1 a 3.1.3, antigos, recibo e limpeza | Corrigido pela metade | Perfis antigos repetidos; recibo encaminhado ao vivo; prazo ainda prometido e faixa da limpeza não oferecida no caso Marta | Aprovar regra da clínica |
| 3.1.4 a 3.1.6, identidade, prontuário e placa | Corrigido pela metade | Rodada completa executada; preservados os limites de serviço e de acesso ao cadastro observados nas conversas | Conferir regras e exceções com a Vivian |
| 3.2.1 a 3.2.3, orçamento, pagamento e emoji | Corrigido pela metade | Rodada completa e 56 mensagens executadas; ver conversas dos perfis e limites do juiz na comparação | Revalidar |
| 3.2.4, 3.3.3, follow-up | Não corrigido | Nenhum mecanismo de acompanhamento novo demonstrado | Pode esperar se não for oferecido |
| 3.3.1 e 3.3.2, retomada e ordem | Corrigido pela metade | Agenda voltou e marcou/cancelou; envio segue estimado | Agenda antes; fila robusta depois |
| 3.4.1 e 3.4.2, desistência e exceção de falta | Corrigido pela metade | Perfis correspondentes executados na rodada completa; encaminhamentos e utilidade avaliados na comparação | Revalidar |
| 3.4.3, cancelamento em menos de 24 h | Corrigido pela metade | Instrução existe; sem prova operacional nova | Revalidar |
| 3.4.4, duas avaliações por pessoa | Não corrigido | Ficha guarda um evento | Pode esperar se a operação limitar a uma |
| 3.4.5, confirmação de cancelamento | Corrigido pela metade | Novos contraexemplos locais | Corrigir antes |
| 4.1, rajada e ficha | Corrigido pela metade | Rajada real desta revisão e reenvio passaram; duas saídas após intervenção humana reproduzidas em protocolo-pausa.json | Corrigir pausa antes; demais garantias de fila podem esperar |
| 4.2 e 4.8, dor e remédio | Corrigido pela metade | Urgência pt ao vivo passou; defesa com pergunta ainda falha | Corrigir a defesa |
| 4.3, idioma | Corrigido pela metade | Catálogo passa; inglês e espanhol escritos com marcação/cancelamento passaram; áudio tem limites separados | Revalidar |
| 4.4, 4.9, 4.11 a 4.13, privacidade, injeção e tom | Corrigido pela metade | Duas tentativas de obter dados de terceira pessoa recusadas em inglês; demais não integralmente repetidas | Revalidar |
| 4.5, 4.7, 4.10, avisos ausentes/repetidos | Corrigido pela metade | Recibo, URGENTE e agradecimento funcionaram; defesa e limitação de complemento têm limites | Defesa antes |
| 5.1, 2.3, 2.4, falhas IA/Google | Corrigido pela metade | Falha real já existente do Google observada; sem falha provocada de IA/envio | Resolver Google e ensaiar falhas só isoladas |
| 5.3, 2.2, 2.5, duplicação e pausa | Corrigido pela metade | Reenvio do mesmo ID passou; pausa ativou, mas duas saídas pendentes continuaram | Corrigir a pausa antes |
| 5.4 e 2.6, entrada e segurança | Corrigido pela metade | 12 locais passaram; foto lida; WAV chegou mas transcrição falhou; resultados Ogg registrados | Revalidar pelo aparelho da clínica |
| 5.5, 2.9, 2.10, carga e custo | Corrigido pela metade | 22 perfis no paralelismo original concluídos; capacidade máxima e custo por paciente não foram medidos | Não prometer capacidade não medida |
| 5.6 e 2.11, recuperação | Corrigido pela metade | Par novo confirmado; roteiro falha em ensaio sintético | Corrigir roteiro antes |
| 5.7 e 2.7, isolamento | Corrigido | Permissões de conexão separadas e conversa com mesmo telefone e mesmos IDs passaram entre demo e clínica de teste, em isolamento-997.json | Repetir com Vivian quando o cadastro estiver pronto |
| 2.8, renovação Google | Corrigido pela metade | Acesso reconectado e operações funcionaram; duração OAuth não comprovada | Garantir duração antes |
| 2.12 e 2.13, aceite e avisos Vivian | Não corrigido | Cadastro incompleto; nenhum envio real autorizado | Bloqueia |
| 6, rotina semanal | Não corrigido | Piloto futuro | Definir responsável antes |
| Estrutura 1, colisão ao copiar clínica | Corrigido pela metade | Validações cruzadas permanecem; cadastro real precisa passar inteiro | Conferir antes |
| Estrutura 2, destino herdado e reinício | Corrigido pela metade | Roteiro sem reinício; erro livre e canal único persistem | Resolver alerta |
| Estrutura 3, teste virar envio real | Corrigido | Fluxo de envio conserva comportamento seguro; prefixo confirmado | Preservar no cadastro |
| Estrutura 4, SQL em clínica errada | Corrigido pela metade | `current_database()` e transação mantidos; JSON e histórico podem ficar desatualizados | Conferir versão e banco antes de aplicar |
| Estrutura 5, isolamento apagava rastros | Corrigido pela metade | Roteiro destrutivo original de isolamento não foi usado; testes de perfis tiveram evidência preservada antes da limpeza | Corrigir ferramenta de teste |
| Estrutura 6, texto vira código inválido | Corrigido pela metade | Delimitadores preservados; validação completa ainda insuficiente | Validar cadastro real |
| Estrutura 7, base da demo em clínica real | Não corrigido | Vivian sem base/instruções próprias | Bloqueia |

## Limpeza final confirmada

As quatro tabelas foram conferidas nos dois bancos: `pacientes`, `mensagens_recebidas`, `saidas_teste` e `reservas_horario`. A tabela abaixo conta linhas apagadas por etapa, incluindo a limpeza automática dos perfis, reconstruída pelos INSERTs bem-sucedidos das execuções, e a limpeza adicional por CTE com RETURNING. Reutilizar um telefone em outra etapa cria outra ficha; as somas são de linhas, não de pessoas únicas.

| Etapa e banco | Fichas | Mensagens recebidas | Saídas simuladas | Reservas |
|---|---:|---:|---:|---:|
| Primeira etapa, clara | 4 | 12 | 27 | 0 |
| Cinco perfis, clara | 5 | 51 | 112 | 2 |
| 22 perfis, clara | 22 | 189 | 388 | 5 |
| 56 casos, clara | 7 | 58 | 117 | 0 |
| Conversas próprias, clara | 7 | 31 | 81 | 7 |
| Conversas próprias, clinica_teste | 0 | 0 | 0 | 0 |
| Mídia, pausa e isolamento, clara | 6 | 7 | 20 | 0 |
| Mídia, pausa e isolamento, clinica_teste | 1 | 2 | 4 | 0 |
| **Total clara** | 51 | 348 | 745 | 14 |
| **Total clinica_teste** | 1 | 2 | 4 | 0 |

O primeiro conjunto, as duas rodadas de perfis e os 56 casos não criaram linhas na clínica de teste. Todos os telefones usados foram novamente consultados, inclusive saídas para a equipe que mencionam esses telefones, e terminaram com zero linhas nas quatro tabelas dos dois bancos. Evidências: `limpeza-final.json`, `limpeza-cinco.json`, `limpeza-22.json`, `limpeza-56.json`, `limpeza-proprias.json`, `limpeza-extras.json` e `conferencia-final-bancos.json`. As auditorias de linhas das rodadas estão preservadas.

A consulta completa do Google cobre 19/11/2026 até o fim de 19/12, em Curitiba, e foi ampliada até fevereiro para procurar sobras dos roteiros. Não há evento de teste novo. O único evento encontrado no inventário inicial e final foi o antigo do Sergio, de 19/11 às 9h, preservado pelo mesmo ID. O evento antigo do Henrique não apareceu nesse intervalo; não foi apagado. Evidências: `agenda-baseline-rodadas.json`, `agenda-final-30-dias.json` e `agenda-final-ampla.json`.

Não foram apagadas execuções do n8n, backups, dados de outros telefones, configurações ou usuários. O contêiner sintético foi removido. Nenhum backup real foi baixado ou restaurado e nenhuma chave privada de backup foi usada. As alterações locais limitam-se ao relatório, scripts e evidências desta revisão. A auditoria final das execuções de agenda própria, mídia, pausa e isolamento confirmou que nenhum nó HTTP de envio real do Whapi foi executado, inclusive no fluxo da clínica de teste (`auditoria-final-envio.json`). Uploads e exclusões dos arquivos fictícios usaram apenas o serviço de mídia, sem envio de mensagem.

## Página final: ordem de correção e o que pode esperar

**Antes de liberar o piloto de 01/12/2026:**

1. Vincular confirmação de cancelamento à operação e ao evento; rejeitar marcação em horário negado ou ainda não autorizado.
2. Garantir urgência mesmo com pergunta e mesmo se a IA escolher outra ação; interromper os blocos pendentes quando a equipe assumir a conversa.
3. Garantir autorização duradoura do Google Agenda, já reconectado pela Erica. Os cinco perfis, 22 perfis, 56 mensagens e sete conversas próprias concluíram; a limpeza também está comprovada.
4. Retirar texto livre dos alertas de erro, ativar canal externo e conferir que o aviso chega sem WhatsApp/servidor disponíveis. Não provocar falha real de envio na demo para isso.
5. Tornar o roteiro de restauração executável por outra pessoa, resolver conflito inicial e garantir limpeza de segredos em falha. Corrigir também os dois casos residuais de status do backup.
6. Migrar o cliente Google do rclone, verificar cópias antigas e novas, e aplicar as contas limitadas com autorização em janela apropriada. São pendências conscientes.
7. Resolver a contradição do campo de reinício no gerador e completar dados, base, credenciais, destinatário dos avisos e aceite da Vivian. Definir prazo real de resposta humana, parcelamento da avaliação, responsável e substituto pelo acompanhamento.

**Pode esperar depois do piloto, com os limites declarados e operação acompanhada:** fila de envio com confirmação completa além da correção obrigatória da pausa humana, idempotência e coordenação por calendário/intervalo mais abrangentes, duas avaliações na mesma ficha, histórico de cada versão, manifesto de hashes do par e camada adicional de retenção imutável. Esses itens continuam abertos, não viraram correções comprovadas.

Os dois problemas já aceitos, vaga presa por alguns minutos após cancelar e pergunta de cancelamento repetida em um caso, não são reapresentados como novos bloqueios. Não há evidência nova aqui que mude a avaliação de baixo impacto deles.
