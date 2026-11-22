# Revisão independente do backup fora do servidor

## Resumo em cinco linhas

1. O backup externo existe, está criptografado pelo desenho do script e teve seus arquivos e tamanhos confirmados no Drive sem download.
2. O último status é OK de 18/11 às 07h10 de Curitiba; a primeira execução automática da versão nova, às 03h de 19/11, ainda precisa ser conferida.
3. Eu ainda não liberaria o piloto de 01/12/2026 sem alerta independente: falha ou ausência de execução pode passar despercebida por tempo indefinido.
4. Falhas antes da instalação do tratamento de erro deixam um OK antigo; sete arquivos locais não garantem sete dias e a restauração documentada pode continuar após erro SQL.
5. Antes do piloto, recomendo client_id próprio, monitoramento de atualização do backup e roteiro de recuperação que outra pessoa consiga executar e conferir.

## Escopo e evidências

Parte iniciada depois do fechamento e da limpeza das partes 1 e 2. Li o script inteiro e a seção de backup e restauração de `tecnico/servidor-n8n.md`. No servidor, fiz somente leituras, comparação do script por SHA-256, validação de sintaxe com `bash -n`, teste de integridade gzip e listagem de metadados do Drive. Não executei backup, retenção, restauração ou alteração de produção.

Não baixei nem abri backups de pacientes. A chave privada não foi lida ou usada. Não fiz nova restauração: o teste anterior é um relato documentado, não uma prova independente desta revisão. As simulações adicionais rodaram no PC, em cópias locais com dados fictícios e substitutos de Docker, age e rclone, um cenário de cada vez. Elas testam o controle de erros do shell, não a criptografia real, a rede, a recuperação do banco ou a validade real de tokens.

Evidências: `parte3-servidor.json`, `parte3-cobertura.json`, `parte3-gzip.json` e `parte3-falhas-simuladas.json`, na pasta `evidencias-revisao-2026-11-18/`. Ferramentas criadas para esta revisão: `auditoria_backup_2026_11_18.py` e `testes_backup_local_2026_11_18.py`. As linhas de erro das simulações pertencem à cópia com substitutos, portanto não são os números de linha do script original.

## Tabela de testes

| Teste | Como fiz | Resultado | Evidência |
|---|---|---|---|
| Código instalado e fonte | SHA-256 com normalização de CRLF | OK | Script instalado igual à cópia local |
| Sintaxe | `bash -n` no servidor | OK | `sintaxe_bash_ok: true` |
| Última rodada registrada | Li somente STATUS | OK registrado | `OK 2026-11-18 07:10`, arquivo `postgres-2026-11-18_0707.sql.gz.age`, 68.234.517 bytes |
| Arquivo correspondente no Drive | `rclone lsjson`, só nomes, tamanhos e datas | OK como metadados | Banco 68.234.517 bytes; configuração 2.454 bytes; ambos com rótulo `2026-11-18_0707` |
| Tamanho coerente | Comparei metadados com dump local | OK como plausibilidade | Local 68.217.677 bytes; criptografado tem 16.840 bytes adicionais, compatível com encapsulamento; não prova conteúdo restaurável |
| Integridade do gzip local | `gzip -t` no mais recente, sem imprimir conteúdo | OK | `parte3-gzip.json` |
| Cron e fuso | Li somente o arquivo da tarefa e o relógio | OK configurado | `0 3 * * * root ...`; servidor UTC-3, Curitiba |
| Execução automática nova | Conferi status, horários e log | Ainda não demonstrada | Status de 07h10; log do cron vazio; primeira rodada da versão nova esperada em 19/11 às 03h de Curitiba, 08h de Israel |
| Permissões | Metadados de arquivos e pasta | OK no essencial | Backups 700; dumps, `.env`, `rclone.conf` e chave pública 600; script 700; todos root |
| Log | Tamanho e linhas operacionais, sem despejar erros arbitrários | Sem execução no log atual | `/var/log/keshion-backup.log` com zero bytes e modo 644 |
| Disco atual | `df -h` | OK neste momento | 96 GB totais, cerca de 90 GB livres, uso de 7% |
| Chave no arquivo do servidor | Verifiquei apenas formato do destinatário público, sem exibir valor | OK | Uma chave pública age; sem marcador privado nesse arquivo |
| Chave privada no PC e cofre | Somente existência dos arquivos conhecidos no PC; não acessei cofre | Parcial | Arquivos de chave privada, pública, rclone e cópia do `.env` existem; cofre e exclusividade de todas as cópias não comprovados |
| Configuração do rclone | Campos não secretos e permissões | OK para mínimo escopo; risco de aposentadoria | `scope=drive.file`, token presente, client_id e client_secret próprios ausentes |
| Chave de credenciais do n8n | Presença, nunca valor | OK por cobertura declarada | `N8N_ENCRYPTION_KEY` presente no `.env` e no processo do n8n; `.env` entra no tar criptografado |
| Bancos e papéis atuais | Somente catálogo de nomes e privilégios básicos | Cobertura correta pelo comando | `clara`, `clinica_teste`, `n8n`, `postgres`; papéis `clara`, `clinica_teste`, `keshion`, este último superusuário |
| Retenção local | Leitura do comando e listagem, sem apagar | Parcial em relação a “sete dias” | Sete arquivos, de 14 a 18/11, incluindo rodadas extras |
| Retenção do Drive | Leitura dos alvos e filtro, sem executar delete | Correta pelo desenho, ainda não observada após 30 dias | Dois arquivos novos; nenhum vencido para provar a limpeza real |
| Controle sem falha | Cópia local, todos os serviços simulados | OK | Código zero e novo status OK |
| Dump retorna erro | Docker simulado falha, gzip não mascara o erro | OK | Código 1, FALHA; arquivo `.parcial` não vira dump final |
| Dump incompleto com código zero | SQL fictício sem marcador final | OK | FALHA “dump incompleto” |
| Compactação falha | Simulei retorno de erro do gzip, sem encher disco real | OK para o erro simulado | FALHA; não prova que STATUS possa ser escrito num disco realmente cheio |
| age falha | Comando simulado retorna erro | OK | FALHA; nenhum OK novo |
| rclone indisponível ou token inválido | Comando simulado retorna erro | OK para retorno de erro | FALHA; não houve revogação nem falha real de rede ou token |
| Tamanho remoto diverge | Metadado remoto simulado diferente | OK | FALHA “tamanho no Drive diferente” |
| `.env` ausente | Cópia local sem arquivo | Falhou na atualização do status | Código 1, mas preserva `OK ANTIGO` |
| Pasta temporária falha | `mktemp` simulado falha | Falhou na atualização do status | Código 1, mas preserva `OK ANTIGO` |
| Restauração e abertura das seis credenciais | Li o roteiro e o relato anterior | Não repetido | Dependeria de chave privada; nenhuma restauração nesta revisão |

## Problemas, do mais grave ao mais leve

### 1. Alta: a falha pode ficar invisível, inclusive com o status antigo em OK

Em linguagem simples: se ninguém abrir o arquivo de status, ninguém fica sabendo. E, em alguns casos, ele continua exibindo sucesso de uma rodada antiga mesmo depois de a rodada nova falhar.

Detalhe técnico: `cd /opt/keshion`, leitura do `.env` e `TMP=$(mktemp -d)` acontecem antes do `trap ERR`. As simulações de `.env` ausente e de `mktemp` com erro confirmaram saída 1 sem atualizar o status. Se o cron não executar, o arquivo também não muda. Se o disco estiver totalmente cheio, o próprio `tee` que escreve FALHA pode não conseguir gravar. Não há serviço externo verificando a idade do último sucesso.

Quanto tempo pode passar: **sem limite definido**. Só conferir manualmente impõe um limite humano. Uma falha hoje pode ser descoberta apenas quando alguém precisar restaurar. Um backup diário também permite perder as alterações desde a última rodada boa, perto de 24 horas mesmo em operação normal, além do tempo necessário para reconstruir o sistema.

Como corrigir antes do piloto: tratamento de erro desde o início, status com início/fim e publicação atômica, indicação de execução em andamento e monitor fora do servidor. Alertar em falha, atraso e ausência de novo sucesso, inclusive quando o servidor inteiro não responde. Recomendo responsável e substituto, conferência até 04h de Curitiba e alerta se não houver rodada válida até esse horário, ajustando o limite ao tempo medido. O aviso deve sair fora do WhatsApp e sem conteúdo de pacientes. Não criei monitor nem alterei cron.

### 2. Alta: o roteiro de restauração pode parecer bem-sucedido com erros no meio

Em linguagem simples: copiar e colar os comandos não garante uma recuperação completa. Alguns erros podem passar e a pessoa precisa saber interpretar o que aconteceu.

Detalhe técnico: os comandos de restauração usam `psql -q -o /dev/null`, sem `-v ON_ERROR_STOP=1`, e não ativam `pipefail` nas cadeias locais e remotas de descriptografia, descompactação e restauração. O destino descartável é iniciado sem espera explícita por `pg_isready`. A conferência de tabelas, dados e credenciais está no relato, mas faltam os comandos e os critérios de aprovação. A documentação do PostgreSQL explica o comportamento de `ON_ERROR_STOP` e os códigos de saída de scripts. [psql 16](https://www.postgresql.org/docs/16/app-psql.html)

Há ainda comandos abreviados com `...`, variáveis `RC` e `AGE` sem instrução para localizar os executáveis e uma exportação de credenciais descriptografadas apenas acompanhada de “não imprimir o resultado”. Esse último comando precisa ter destino protegido ou captura em memória explícita; o operador não deve improvisar, pois a saída pode conter segredos. O roteiro manda remover o Postgres temporário, mas não fornece criação e limpeza completas do n8n temporário.

Como corrigir: roteiro completo e validado por uma segunda pessoa, versão exata das imagens, espera por saúde, `pipefail`, parada em erro SQL e tratamento explícito de conflitos esperados de papéis/bancos iniciais. Definir verificações de contagem, papéis, permissões, fluxos e capacidade de abrir credenciais, sem mostrar valores. Limpeza de todos os contêineres e volumes descartáveis com nomes próprios. Um técnico consegue usar o texto atual como orientação, mas eu não o considero um procedimento autossuficiente para a Erica ou outro operador sem conhecimento prévio. Não testei restauração sobre produção nem em outro destino.

### 3. Alta: esperar o client_id compartilhado quebrar é uma decisão frágil

O servidor usa o client_id compartilhado, confirmado pelos campos próprios ausentes. As fontes oficiais continuam avisando de aposentadoria em 2026, sem dia confirmado. O anúncio prevê aviso antes da desativação, mas não permite contar 90 dias a partir da postagem de julho; em setembro o autor ainda relatava indefinição. **Não há base para prometer uma data provável exata.** A previsão pública é 2026 e o acesso funcionou nesta leitura. Recomendo client_id próprio antes de 01/12, com autorização da Erica, sem aguardar o primeiro backup perdido. [Anúncio oficial e atualizações](https://forum.rclone.org/t/google-drive-and-google-photos-users-action-required/54005/), [orientação do rclone](https://rclone.org/drive/#making-your-own-client-id)

Ao migrar, manter `drive.file`, reconectar a autorização e conferir a visibilidade das cópias anteriores e o destino dos arquivos novos. Como a permissão é por aplicativo e arquivo, **há risco de o aplicativo novo não enxergar automaticamente os arquivos criados pelo antigo**. Esta é uma inferência do modelo de permissão, não um teste realizado na conta: a transição precisa de plano de acesso às cópias antigas. [Escopos oficiais do Google Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)

Não deixar o novo app externo em modo Teste: para escopos além de perfil básico, a documentação do Google informa expiração do refresh token em sete dias. Não basta trocar o identificador sem reconectar. [Expiração OAuth do Google](https://developers.google.com/identity/protocols/oauth2#expiration)

### 4. Média: a retenção local guarda sete arquivos, não sete dias

Em linguagem simples: fazer vários backups manuais no mesmo dia pode empurrar para fora os backups de dias anteriores. Hoje os sete arquivos cobrem 14 a 18/11, apenas cinco datas.

Detalhe técnico: `ls -1t ... | tail -n +8 | xargs -r rm -f` conserva as sete versões mais recentes por modificação. A limpeza acontece depois do dump íntegro, mas antes de comprovar envio externo. Falhas de dump deixam `.parcial`, que a limpeza não abrange. Não há bloqueio contra duas execuções e o nome só distingue o minuto: duas rodadas no mesmo minuto podem disputar o mesmo `.parcial` e arquivo final.

Como corrigir: definir a política como dias ou versões, manter ao menos uma cópia por dia da janela prometida, controlar espaço e parciais e usar bloqueio exclusivo, com identificador de execução único. Não removi backups, parciais nem alterei a retenção.

No Drive, o filtro de 30 dias está dirigido apenas a `keshion-backups/postgres/` e `config/`. Isso limita bem o alcance, mas não há filtro por nome: essas pastas devem ser exclusivas. `--min-age 30d` seleciona arquivos suficientemente antigos, e `delete` respeita filtros; não há `purge`. A idade é a do arquivo, não uma interpretação da data no nome. A exclusão real após 30 dias ainda não foi observada, pois só há o par novo. [Filtros de idade](https://rclone.org/filtering/#min-age-dont-transfer-any-file-younger-than-this), [rclone delete](https://rclone.org/commands/rclone_delete/)

O Google Drive usa lixeira por padrão no rclone, então “retirar da pasta após 30 dias” não significa necessariamente destruição permanente imediata. A política deve distinguir retenção operacional e eliminação definitiva, sem trocar isso automaticamente nesta revisão. [Exclusão no backend Drive](https://rclone.org/drive/#deleting-files)

### 5. Média: a recuperação inclui os bancos, mas não todo o ambiente e serviços externos

O uso de `pg_dumpall` como superusuário é adequado para incluir todos os bancos atuais, papéis e outros objetos globais; não é uma lista fixa que esqueceria um banco novo. A chave de criptografia do n8n está no `.env`, incluído no tar criptografado. Isso resolve uma dependência essencial das credenciais. O comando realiza dumps por banco; não é um único retrato simultâneo de todas as bases e do Google. [Cobertura do pg_dumpall](https://www.postgresql.org/docs/16/app-pg-dumpall.html)

| Elemento | Cobertura atual | O que falta na recuperação real |
|---|---|---|
| `clara`, `clinica_teste`, `n8n`, `postgres`, tabelas e dados | Incluídos por `pg_dumpall`, conforme comando | Prova independente da cópia específica por restauração não realizada |
| Papéis, donos e privilégios | Incluídos no dump global | Resolver conflitos iniciais e validar permissões após restaurar |
| Fluxos e credenciais do n8n | Banco n8n, com chave no `.env` criptografado | Conferir abertura sem exportar segredos e versão exata do aplicativo |
| Compose, Caddyfile e script de backup | Tar enviado ao age antes do Drive | Manifesto e verificação explícita do par de arquivos da mesma rodada |
| Chave pública age, rclone.conf e cron | Fora do tar atual | Repor a partir de fonte segura ou refazer autorização; instruções completas e acesso ao Drive |
| Volumes `n8n_data`, Caddy e arquivos externos ao Postgres | Não copiados integralmente por este script | Nós instalados, arquivos de armazenamento/binários que existirem e estado local podem precisar de recuperação própria |
| Google Agenda e Whapi | Não são restaurados pelo dump PostgreSQL | Reconciliar eventos e mensagens posteriores ao horário do backup; autorizações revogadas não voltam só com SQL |
| SSH, firewall, fail2ban, DNS e contas do provedor | Não copiados neste tar | Recriar acesso e segurança, conferir domínio/IP e certificados |
| Código e arquivos locais de implantação | Dependem de outra cópia/Git e dos fluxos no banco | Ter acesso ao repositório e aos segredos locais necessários; não considerar o tar uma cópia completa do projeto |

Como corrigir: inventário de recuperação com responsáveis, dependências e referências seguras. Validar os arquivos efetivamente usados de cada volume antes de decidir o que deve entrar em backup; não afirmei que todos os dados binários estão cobertos. Manter rotina de reconciliação com a agenda, porque voltar o banco a ontem não desfaz mudanças de hoje no Google.

### 6. Média: a conferência atual comprova existência e tamanho, não recuperação completa

Os tamanhos são coerentes e o gzip local passou. O script verifica conclusão do dump, retorno das ferramentas e tamanho explícito do arquivo de banco no Drive. Isso é substancialmente melhor do que apenas enviar algo e presumir sucesso. O upload da configuração depende do sucesso do próprio rclone; não recebe a mesma checagem extra explícita de tamanho nem manifesto de conjunto.

Em linguagem simples: ver uma caixa fechada no depósito não prova que tudo dentro poderá ser usado na emergência. Sem abrir nada nesta revisão, não posso confirmar que a chave guardada corresponde àquela cópia ou que os bancos voltarão integralmente.

Como corrigir: manifesto por rodada com arquivos, tamanhos e hashes do material criptografado, verificação do par banco/configuração, confirmação de sucesso somente no fim e restauração periódica isolada. O teste documentado de 18/11 é um bom precedente; falta uma prova independente repetível e critérios claros para outro operador. A primeira execução automática nova precisa ser acompanhada em 19/11.

### 7. Média: criptografia protege o conteúdo, mas não torna a cópia imune a exclusão

O escopo `drive.file` evita acesso geral ao Drive e foi confirmado. Porém, o token no servidor permite administrar os arquivos desse aplicativo, incluindo exclusão. Portanto, comprometer o servidor pode permitir apagar cópias externas, mesmo sem saber descriptografá-las. A lixeira e a conta proprietária podem oferecer caminhos adicionais, mas não equivalem a uma cópia imutável comprovada.

Como corrigir: avaliar uma camada independente de retenção protegida ou cópia adicional, com acesso de recuperação separado, e documentar resposta a exclusão. Para o piloto, ao menos alertas fora do servidor, proteção da conta Google e teste de recuperação de cópia antiga devem ter responsáveis definidos.

## Segredos, arquivos, logs e limites da verificação

Está correto: `umask 077`, pasta local 700, dumps 600, configuração do rclone 600 e chave pública no servidor. O `.env` não é enviado solto: passa por `tar | age`; o arquivo remoto termina em `.age`. O dump local continua sem criptografia adicional, mas dentro de pasta restrita; contém dados sensíveis e pode incluir material de autenticação dos papéis do Postgres, por isso as permissões são importantes.

O script não ativa `set -x`, não põe senha ou token literalmente nos argumentos e não imprime o `.env`. O age usa o caminho da chave pública; o rclone usa o caminho da configuração. A execução pelo cron não escreve por si só em histórico interativo. O log atual está vazio e modo 644; recomendo restringi-lo e definir rotação, embora não tenha encontrado vazamento nele. Erros futuros de ferramentas podem acrescentar detalhes de operação; não considerar truncar texto uma proteção suficiente.

Confirmei que o arquivo de chave do servidor contém somente destinatário público e que o arquivo privado conhecido existe no PC, sem lê-lo. **Não posso certificar que nunca houve outra cópia privada em algum lugar do servidor, em históricos ou em outro computador, nem conferir o conteúdo do cofre sem acessá-lo.** Não fiz varredura de todos os arquivos e históricos potencialmente secretos. A declaração “somente PC e cofre” continua parcialmente baseada no registro da Erica. Isso é limite da evidência, não descoberta de chave privada indevida.

## Antes de 01/12/2026

1. Implantar, com autorização, alerta fora do servidor e do WhatsApp para falha, atraso e ausência de backup novo, com responsável e substituto.
2. Migrar para client_id próprio, publicar a configuração OAuth adequada, reconectar e verificar acesso às cópias antigas e envio das novas.
3. Corrigir o tratamento de falha desde a preparação, travar execução simultânea e definir retenção como dias ou versões.
4. Completar o roteiro de restauração e executá-lo por outro operador num ambiente descartável sem rede, com autorização para usar a chave privada, sem produção como destino.
5. Confirmar em 19/11 a primeira rodada automática, os dois arquivos no Drive e o status novo. Não programei lembrete nem alterei tarefa automática nesta revisão.

## Confirmação de limpeza

Esta parte não criou linha de paciente, evento ou contêiner no servidor. Os finais 951 a 957 foram apagados e conferidos nas partes anteriores nos dois bancos; seus eventos foram cancelados pela conversa e a consulta final da parte 2 não encontrou sobras. O evento antigo de Henrique não foi alterado. As simulações desta parte usaram apenas arquivos fictícios locais; nenhum backup de produção foi apagado, substituído, restaurado ou baixado. Não houve uso de chave privada.

Conferência adicional no encerramento das três partes, somente leitura: novamente zero linhas dos sete números nas quatro tabelas de cada banco e nenhum evento ativo encontrado com esses telefones nas descrições. Evidência: `limpeza-final-tres-partes.json`.
