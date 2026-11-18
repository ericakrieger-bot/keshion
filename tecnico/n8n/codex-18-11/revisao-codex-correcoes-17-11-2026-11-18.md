# Revisão independente das correções de 17 e 18/11/2026

## Resumo em cinco linhas

1. Eu manteria a estrutura por clínica, mas ainda não ligaria o atendimento da Dra. Vivian em 01/12/2026.
2. A demo publicada coincide com o gerador atual; base e instruções também coincidem após normalizar quebras de linha.
3. Uma informação nova curta sobre sangramento ficou sem aviso, mesmo com promessa de encaminhamento, em teste ao vivo.
4. Aceite de cancelamento, exclusividade de vaga e ordem de envio ganharam proteções, mas continuam incompletos.
5. Faltam ativar contas limitadas do banco, alerta fora do WhatsApp, cadastro e aceite da Vivian e concluir a validação operacional.

## Escopo e método

Leitura integral dos dois prompts obrigatórios; leitura dos arquivos indicados no roteiro, das duas revisões anteriores e dos commits `110f4d1`, `877df8d`, `d27a0f4` e `e58104a`. Fonte lida em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`; entregas e ferramentas desta auditoria ficam na pasta KESHION aberta no Codex. Não apliquei correções nem publiquei fluxos. A geração para comparação foi feita em memória, sem sobrescrever os JSONs originais.

Consultas remotas exclusivamente de leitura, exceto mensagens sintéticas autorizadas e remoção dos próprios registros de teste. Nenhum teste de envio real, de número pessoal ou de falha real do Whapi. Preflight: prefixo `554199900` nos dois bancos, nenhuma ficha de teste atualizada nos dez minutos anteriores, nenhuma execução ativa e nenhum dos três scripts conhecidos de teste em processo. Isso é uma fotografia inicial, não uma trava global contra outra pessoa iniciar uma rodada depois.

As conversas desta parte usaram finais 951, 952 e 953. Evidências estão em `evidencias-revisao-2026-11-18/`. O horário do primeiro caso foi 08h57 em Curitiba, clínica aberta. Os valores de execução e de saída são os do servidor. Uma reprodução local injeta saídas fictícias da IA para avaliar a barreira independente; ela não demonstra a frequência com que a IA cometeria aquele erro.

## Tabela de testes

| Teste | Como fiz | Resultado | Evidência |
|---|---|---|---|
| Segurança antes da rodada | Prefixo, atividade recente, processos e execuções | OK | `parte1-preflight.json` |
| Publicação e geração | Comparei nós e ligações; ignorei somente UUID aleatório de condição; verifiquei versão ativa igual à versão atual | OK na demo | `parte1-comparacao-fluxos.json`: zero nós diferentes nos dois fluxos da demo e no Envio de teste |
| Diferença da clínica de teste | Mesma comparação | Diferença esperada | Só `Validar o pedido de agenda` difere, por publicação da tarde exclusiva da demo |
| Conteúdo realmente aplicado | Comparei `_base` e `_instrucoes` com os arquivos, normalizando quebras de linha | OK | `parte1-metadados.json` |
| Paciente antigo, limpeza e recibo | Conversa ao vivo no final 951 | Parcial | Saídas 3756 a 3759: faixa de R$ 280 a R$ 350 e aviso administrativo; promessa de retorno “em breve” |
| Informação nova curta depois de um aviso | Mesmo perfil: “Agora comecei a sangrar muito” | Falhou | Saídas 3760 e 3761 para paciente; nenhum aviso novo à equipe; `conversa-554199900951-clara.json` |
| Mesmo defeito sem custo de IA | Executei o JavaScript do nó de resultado com último aviso recente e mensagem curta | Falhou | `parte1-testes-locais.json`: `aviso_humano` vazio e só um destinatário, o paciente |
| Idioma e anestesia | Conversa em inglês, final 952 | OK neste caso | Saídas 3762 a 3764: inglês, anestesia quando necessária e sem garantia de ausência de dor |
| Cancelamento sem aceite | Nó de decisão local, IA fictícia retorna `cancelar`, paciente diz que quer manter | Falhou como barreira independente | `parte1-testes-locais.json`: rota `cancelar` mesmo para “Não, quero manter” |
| Promessa de encaminhamento em três idiomas | Nó local com ação `responder` e promessa de encaminhar | Parcial | Português vira `humano`; inglês e espanhol permanecem `responder` |
| Privilégios entre bancos | `has_database_privilege`, sem tentativa de escrita | OK para a fronteira consultada | `clara` e `clinica_teste` conectam apenas ao próprio banco entre os três consultados |
| Usuários de aplicação | Consultei `pg_roles` | Ainda não implantado | Não existem `clara_app` e `clinica_teste_app`; donos não são superusuários |
| Compatibilidade com `_app` | Leitura das operações dos nós e dos GRANTs | OK por inspeção | Atendimento usa SELECT/INSERT/UPDATE/DELETE; config somente SELECT; sequências recebem USAGE e SELECT; ALTER está no instalador, não no atendimento |
| Alerta de falha | Leitura da ligação de erro e da expressão; sem provocar erro real | Parcial | Saída de erro do envio ligada ao alerta; erro livre truncado em 120 caracteres continua no texto |
| Trava de vaga e espera | Leitura do SQL e dos tempos HTTP | Parcial | Chave por início, mesmo telefone pode reutilizar; expira em 2 min; esperas HTTP de até 120 s por chamada; próxima resposta espera no máximo 60 s |
| Repetição de isolamento e limpeza | Evidência adicionada ao encerrar a parte | Ver complemento ao fim | Conversas do final 953 nos dois bancos |
| Queda real de WhatsApp, corrida simultânea e pausa durante resposta | Não provoquei falha real; não rodei testes concorrentes | Não testado ao vivo | Restrições da tarefa; risco avaliado por código |

## Problemas, do mais grave ao mais leve

### 1. Alta: informação nova relevante pode ficar sem aviso para a equipe

Em linguagem simples: a Clara diz que avisou, mas uma pessoa da clínica pode não ficar sabendo que o problema mudou. Depois de um aviso administrativo de recibo, a mensagem “Agora comecei a sangrar muito” recebeu promessa de encaminhamento e orientação ao paciente, sem aviso novo.

Detalhe técnico: em `RESULTADO_JS`, caso `humano`, a primeira condição sai do bloco quando o último aviso tem menos de 15 minutos, a mensagem tem menos de 60 caracteres e não contém `?`. Ela não verifica se o assunto mudou. Essa saída acontece antes da comparação de motivos e antes do complemento novo de 18/11. Uma declaração urgente normalmente não contém interrogação. O mesmo critério inadequado aparece no ramo de motivos semelhantes, até 90 minutos.

Como corrigir: suprimir apenas confirmações simples efetivamente equivalentes a “ok”; informação nova e agravamento devem gerar aviso. Separar urgência de semelhança de palavras. Usar chave de assunto e estado do encaminhamento, com teste de recibo seguido de relato novo. Prioridade antes do piloto.

### 2. Alta: o cancelamento ainda depende do entendimento correto da IA

Em linguagem simples: a proteção verifica se a assistente falou algo parecido com confirmação, mas não verifica se a pessoa aceitou. Uma interpretação errada da IA ainda pode apagar a avaliação.

Detalhe técnico: a expressão `/certo\s*\?|cancel/i` procura “certo?” ou qualquer ocorrência de `cancel` na última fala da assistente. Não exige estado de confirmação pendente nem aceite na mensagem nova. Em reprodução local, uma ação fictícia `cancelar` passou mesmo com “Não, quero manter” ou uma pergunta de preço depois de “certo?”. O trecho em inglês “can be canceled” também satisfaz `cancel`, sem necessariamente ser uma pergunta de confirmação.

Como corrigir: manter confirmação pendente com identificador do evento, proposta e prazo; aceitar cancelamento apenas com resposta afirmativa àquela proposta e tratar negativas explicitamente. Nunca usar apenas texto livre da própria IA como autorização. Não cancelei evento real para reproduzir esse erro.

### 3. Alta: a trava reduz a disputa, mas não garante uma única marcação

Em linguagem simples: melhorou a chance de duas pessoas não pegarem a mesma vaga, mas ainda há situações em que a proteção pode abrir cedo demais ou não ser compartilhada.

Detalhe técnico: o INSERT com conflito é uma boa proteção atômica para dois telefones diferentes, no mesmo banco e mesmo instante inicial. Porém, o mesmo telefone pode obter a trava de novo; não há identificação única da tentativa ou idempotência no POST ao Google. A trava vence em dois minutos, enquanto consulta e criação usam chamadas de até 120 segundos cada. Uma criação lenta pode completar depois de outra tentativa assumir a trava. A demo e a clínica de teste compartilham calendário, mas têm tabelas de reserva distintas. Horários sobrepostos com inícios diferentes também não colidem na chave. O último ponto pesa mais para clínicas com duração ou grade diferente da demo.

Como corrigir: uma tentativa persistente por paciente e operação, exclusividade pelo calendário e intervalo, renovação da trava enquanto a operação estiver em curso e criação idempotente com reconciliação no Google. Testar a concorrência apenas em ambiente isolado. A tarefa proíbe testes simultâneos nesta rodada, por isso não houve reprodução ao vivo.

### 4. Alta: o alerta continua dependendo do WhatsApp e pode carregar dados no erro

Está certo usar credencial separada da Keshion para falha de uma clínica e remover explicitamente o corpo da mensagem original e o telefone completo. A ligação à saída de erro está correta.

Em linguagem simples: se o próprio canal da Keshion estiver indisponível, o aviso pode não chegar. E cortar um erro em 120 caracteres não garante que o começo dele não contenha informação de paciente.

Detalhe técnico: a demo e o alerta usam a mesma credencial Whapi. Para falha geral desse canal, repetir por ele não oferece independência. O alerta usa `continueRegularOutput`, de modo que sua própria falha segue adiante sem nova escalada independente. O campo `$json.error.message` entra quase diretamente no texto. O vazamento por esse campo é uma possibilidade de código, não um vazamento real observado do Whapi nesta rodada. Além disso, quando falha o envio de um aviso à equipe, o “final do paciente” é na verdade o final do destinatário da equipe.

Como corrigir: usar alerta fora do WhatsApp com código de erro permitido, clínica e ID de execução; remover texto arbitrário, telefone e corpo de requisições do erro. Registrar falha de entrega de aviso de forma persistente. Ensaiar com respostas simuladas e destino controlado, sem falha real em produção.

### 5. Média: encaminhamento e idioma estão corrigidos só em parte

Está certo lembrar o idioma no fim do pedido à IA e colocar as regras R, S e T. O teste novo em inglês passou. Mas a defesa que transforma promessa em aviso reconhece essencialmente português. Uma resposta “I'll forward...” ou “Voy a pasar...” com ação `responder` não é corrigida para `humano` na reprodução local. Frases fixas de erro e confirmação continuam em português. A oferta com `9am` também escapa do reconhecedor de ofertas de horário usado quando a agenda não responde, se a ação for apenas `responder`.

Como corrigir: representar intenção de encaminhamento e idioma em dados estruturados, com validação de consistência, e localizar todas as mensagens fixas. Não depender somente de uma lista de frases em português.

### 6. Média: a ordem de envio é uma estimativa, não uma confirmação

Em linguagem simples: a conversa seguinte espera um tempo calculado, sem confirmar que a anterior terminou. Se o envio demorar mais que o previsto, as falas ainda podem chegar fora da ordem.

Detalhe técnico: `envio_ate` é calculado antes do subfluxo de envio, chamado com `waitForSubWorkflow: False`. A espera lê uma única estimativa e limita a 60 s, embora o próprio cálculo aceite até 120 s e três mensagens possam superar 60 s. Demora de rede, erro ou mensagens já em processamento não são refletidos nesse estado. Nenhuma nova verificação da pausa da doutora ocorre imediatamente antes de cada envio.

Como corrigir: fila persistente por conversa com confirmação de conclusão do envio, versão do turno e rechecagem da pausa antes de sair cada mensagem. Garantir prazo máximo com transferência explícita à equipe.

### 7. Média: roteiro de clínica nova ainda pode interromper a demo e expor senha em argumentos

Em linguagem simples: o roteiro ficou bem mais completo, mas ainda manda reiniciar o serviço que atende todas as clínicas. Isso contradiz a regra mais recente de publicar sem reiniciar. Também faltam instruções concretas para voltar à versão anterior.

Detalhe técnico: seção 5 de `CLINICA-NOVA.md` termina com `docker compose restart n8n`. Os comandos de criação de papel colocam a senha na string de `psql -c`; a conexão como dono passa senha em argumento de `sh -c`. Mesmo sem imprimir no terminal, argumentos podem ser vistos por processos com permissão. O passo 1 pede gerar SQL antes de cadastrar todos os campos que esse gerador exige. Backup do novo banco só é lembrado depois da virada, e falta verificar restauração antes dela. O “modo copiloto” aparece como escolha, mas não existe implementação descrita que permita ativá-lo.

Como corrigir: remover reinício do roteiro, ordenar os pré-requisitos, passar segredos por canal protegido em vez de argumentos, incluir cópia da versão anterior e reversão por importação/publicação autorizada, checagem do backup e aceite antes da virada. Copiloto precisa existir ou ser retirado da escolha operacional.

### 8. Média: contas limitadas ainda não foram aplicadas e validação de cadastro é incompleta

Os GRANTs concedem as operações que os nós precisam e protegem a config contra escrita direta do usuário de aplicação. As contas ainda não existem, conforme confirmado. O gerador valida o formato do fuso, não a existência de um fuso IANA; permite antecedência mínima negativa e não valida integralmente o calendário de datas. O histórico de instruções/base ainda guarda só a primeira substituição de cada dia.

Como corrigir: aplicar a separação de contas com autorização e teste controlado; validar valores com bibliotecas de calendário/fuso; versionar cada publicação. Ver roteiro de migração abaixo.

### 9. Baixa a média: a base continua ambígua em algumas promessas

O atendimento novo evitou a promessa de anestesia universal, o que é uma melhora real. Contudo, o pedido administrativo ainda recebeu “em breve”. A base promete “retornamos em instantes” em urgência com clínica aberta, o que pode não corresponder à capacidade real da recepção. A FAQ “Posso parcelar a avaliação?” responde apenas preço e abatimento; não resolve a pergunta sobre parcelamento, enquanto a parte de pagamento fala genericamente em 12 vezes. A regra S pede não prometer prazo e traz “já te retorno” como exemplo.

Como corrigir: a clínica deve aprovar o prazo real de resposta e a regra exata de parcelamento da avaliação; reescrever exemplos para não induzir garantia de retorno. O filtro determinístico não consegue consertar uma promessa que a própria base autoriza.

## Destino dos achados anteriores

“Resolvido” abaixo pode ser limitado a código ou a um caso testado. Não equivale à aprovação de todo o atendimento.

| Achado do relatório de testes de 17/11 | Situação | Motivo |
|---|---|---|
| 1.1 e 2.1: foto e mídia real | Parcial | Fora desta rodada; foto válida do Whapi e seis mídias continuam sem nova prova pelo celular |
| 1.2 e 1.3: comparação e 22 perfis | Parcial | Não repeti 56/22; CSV de 18/11 mantém casos abaixo de 17/11 e Emily com 2 antes da correção da tarde |
| 1.4: limpeza e sobras | Parcial | Ver confirmação desta rodada; isso não regulariza eventos antigos |
| 1.5, 4.6 e 5.2: validação e concorrência | Parcial | Regras independentes existem; aceite e reserva ainda têm lacunas |
| 3.1.1 a 3.1.3: pacientes antigos, recibo e limpeza | Parcial | Regra S e teste novo informaram a faixa; ainda há promessa de prazo e relatos anteriores não foram todos repetidos |
| 3.1.4 a 3.1.6: identidade, prontuário e placa | Parcial | Regras preservadas, sem repetição dos três casos ao vivo |
| 3.2.1 a 3.2.3: orçamento, pagamento e emoji | Parcial | Sem mudança funcional demonstrada nesses casos; não repetidos |
| 3.2.4, 3.3.3 e follow-up | Não resolvido como recurso | Não existem acompanhamento ou estado de cancelamento para essa finalidade; base agora declara a ausência |
| 3.3.1 e 3.3.2: voltar e ordem da confirmação | Parcial | Consulta de agenda e estimativa de espera existem; não há garantia de término real do envio |
| 3.4.1 e 3.4.2: desistência e exceção de falta | Parcial | Não repetidos nesta parte; não há prova nova de resolução completa |
| 3.4.3: cancelamento em menos de 24 h | Parcial | Instrução acrescentada, execução específica não repetida nesta parte |
| 3.4.4: duas avaliações para a mesma pessoa | Não resolvido | Ficha continua guardando apenas um identificador de avaliação |
| 3.4.5: confirmar cancelamento | Parcial | Há barreira textual, mas reprodução local demonstrou aceite insuficiente |
| 4.1: rajadas e ficha coerente | Parcial | Deduplicação mantida, estimativa de ordem acrescentada; sem nova prova de corrida |
| 4.2 e 4.8: dor e remédio | Parcial | Resposta ao paciente e encaminhamento são orientados; aviso de agravamento pode sumir, confirmado ao vivo |
| 4.3: idioma | Parcial | Inglês novo passou; frases fixas e defesa de encaminhamento continuam sem tradução completa |
| 4.4, 4.9 e 4.11 a 4.13: privacidade, injeção e tom | Parcial | Sem repetição integral; nenhuma conclusão nova de cura desses casos |
| 4.5, 4.7 e 4.10: aviso ausente ou repetido | Não resolvido integralmente | Complemento existe, mas informação nova curta continua suprimida; excesso de complementos também consta no histórico de 18/11 |
| 5.1, 2.3 e 2.4: contingências de IA e Google | Parcial | Sem falha real induzida; idioma e detecção de oferta têm lacunas |
| 5.3, 2.2 e 2.5: rajada, duplicação, pausa e concorrência | Parcial | Recursos mantidos; corrida e intervenção durante envio não reproduzidas |
| 5.4 e 2.6: entrada e segurança | Parcial | Restrições de canal e mídia mantidas; sem nova bateria de mídia ou rota antiga |
| 5.5, 2.9 e 2.10: carga e custo | Parcial | Resultados históricos não foram reexecutados; nenhuma carga paralela nesta revisão |
| 5.6 e 2.11: backup e recuperação | Avaliado na parte 3 | Não assumir que a existência de cópia prova recuperação completa |
| 5.7 e 2.7: isolamento | Ver complemento de execução | Repetição com mesmo telefone e ID, sequencial |
| 2.8: renovação do Google | Parcial | Consulta atual funcionou; publicação do app e renovação duradoura não demonstradas |
| 2.12 e 2.13: aceite e avisos da Vivian | Não resolvido | Cadastro incompleto e nenhum ensaio autorizado com a clínica real |
| 6: rotina semanal | Pendente | Piloto ainda não começou |

| Achado da revisão de estrutura de 17/11 | Situação | Motivo |
|---|---|---|
| 1. Colisão ao copiar clínica | Resolvido no código para os campos checados | Validação cruzada de IDs, caminhos, canal, banco e credenciais; ainda conferir inventário de produção antes de importar |
| 2. Destino herdado e reinício | Parcial | Modelo e Vivian sem números herdados; reinício restrito; alerta novo ainda usa erro livre e o mesmo canal da demo |
| 3. Teste podia virar envio real | Resolvido para ausência de modo | SQL de Envio assume teste quando ausente ou diferente de `0`; Atendimento não lê outro `modo_teste`; calendário continua real por decisão expressa |
| 4. SQL na clínica errada | Parcial | Trava `current_database()` e transação adicionadas; atualização por JSON desatualizado e histórico diário continuam possíveis |
| 5. Teste de isolamento apagava rastros | Parcial | Erros SQL e finally melhoraram; script ainda limpa número fixo depois de apenas checar uso recente e não consulta Google |
| 6. Texto vira código inválido | Parcial | Campos perigosos e delimitador SQL tratados; validações de fuso e valores ainda incompletas |
| 7. Base da demo em clínica real | Pendente operacional | Modelo existe, mas Vivian continua sem base/instruções e credenciais próprias |

## Migração para `_app`, somente roteiro, não executado

1. Com autorização, escolher janela e registrar IDs, versão ativa e vínculo das duas credenciais Postgres atuais. Confirmar backup recuperável e deixar reversão pronta.
2. Criar `clara_app` e `clinica_teste_app` com senhas distintas, sem superusuário, criação de banco, criação de papel ou herança indevida. Guardar senhas somente no local aprovado, sem argumentos visíveis.
3. Como dono de cada banco, aplicar os GRANTs revisados: CONNECT no próprio banco, USAGE no schema, SELECT/INSERT/UPDATE/DELETE nas tabelas operacionais, SELECT em config e USAGE/SELECT nas sequências. Conferir ausência de CREATE no schema e de privilégios herdados indevidos.
4. Validar as negativas de estrutura e de alteração da config primeiro em contêiner descartável sem rede. Não executar `DROP`, `TRUNCATE` ou alteração de config na produção para provar negativa.
5. Cadastrar novas credenciais Postgres no n8n sem apagar as anteriores; associá-las aos dois fluxos de cada clínica. Conferir banco, host e usuário. Publicar somente as versões autorizadas, sem reiniciar n8n.
6. Testar uma conversa sintética de cada vez, aviso simulado, gravação de ficha e saídas, marcação/cancelamento se autorizado no plano; conferir erros de permissão e agenda.
7. Se falhar, voltar à versão e credencial anterior autorizadas, sem restaurar banco por cima da produção. Não excluir o dono: permanece para manutenção. Documentar versão final e incluir segredos atualizados na proteção de backup.

## Discordâncias e pontos positivos

Concordo com bancos separados, validação independente de agenda, proteção padrão do modo de teste, retirada das promessas de lembretes inexistentes e restrição de reinício fora da demo. Também concordo com testar o alerta por simulação em vez de provocar falha real.

Discordo de chamar a proteção de agenda de confirmação completa de escolha: procurar data e hora na conversa não representa aceite. Discordo de tratar mensagem curta sem `?` como simples confirmação. Discordo de considerar WhatsApp um canal independente quando a própria demo e seu alerta usam a mesma credencial. O relato de que concorrência entre rodadas causou falhas antigas é plausível, mas não basta para descartar todos os defeitos do sistema sem reproduzir os casos isoladamente e conferir o Google.

## Limpeza e complemento de execução

Isolamento concluído com o mesmo telefone `554199900953` e os mesmos dois IDs nas duas clínicas. A demo lembrou Ana/GIRASSOL e a clínica de teste lembrou Bruno/CATAVENTO, sem cruzar os dados. Saídas da demo 3765 a 3770; teste 25 a 30. Foi uma adaptação sequencial do roteiro, para cumprir a exigência de um teste por vez e evitar a limpeza abrangente do script original. A rejeição de canal errado nos dois sentidos não foi repetida ao vivo nesta parte.

Limpeza confirmada após o término das mensagens: finais 951, 952 e 953 com zero linhas em `pacientes`, `mensagens_recebidas`, `saidas_teste` e `reservas_horario`, nos dois bancos. Saídas simuladas para a equipe associadas a esses telefones também foram removidas. Nenhum evento foi criado por esta parte. Consulta direta e paginada até o fim do intervalo de 18/11/2026 a 20/02/2027 não encontrou evento com esses telefones nas descrições. Evidência: `limpeza-554199900951.json`.

O evento antigo informado pela Erica, Henrique em 19/11 às 14h, final 810, não foi apagado. A busca por telefone de teste nas descrições não o localizou; isso não prova que ele inexiste, porque a descrição pode estar ausente ou diferente. Não declarei limpeza das rodadas antigas. Nenhum registro preexistente foi removido deliberadamente. Registros de execução do n8n permanecem sujeitos à retenção normal; não foram apagados nesta revisão.
