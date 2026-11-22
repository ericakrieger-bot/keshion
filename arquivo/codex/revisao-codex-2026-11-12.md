# Revisão independente da Clara no n8n

12 de novembro de 2026 · Keshion IA

## Resumo em cinco linhas

1. Eu ainda não liberaria a Clara para atender pacientes da Dra. Vivian em 01/12/2026.
2. A demonstração respondeu às perguntas básicas, agrupou mensagens próximas e executou operações reais na agenda de teste.
3. O webhook aceitou mensagens sem autenticação, inclusive uma mensagem que simulava a doutora assumindo o atendimento.
4. Reproduzi perda de mensagem em lote, resposta duplicada após reenvio e respostas fora de ordem em uma mesma conversa.
5. Para liberar o piloto, eu exigiria isolamento da clínica, agenda e encaminhamento humano confiáveis, proteção dos dados e recuperação do servidor testada.

## Como fiz a revisão

Li os documentos de migração e servidor, o gerador e o esquema do Postgres, a base e as instruções da demo, os quatro cenários exportados do Make e os materiais do A/B. Fiz a leitura do código sem executar o gerador ou importar fluxos. No VPS, confirmei por leitura os fluxos publicados e a configuração do prefixo. Em seguida, fiz POSTs em UTF-8 com números inéditos no prefixo autorizado e conferi as fichas, a caixa de saída simulada e as etapas registradas no n8n. As datas e horas da agenda abaixo usam o horário de Curitiba.

Nenhuma configuração, credencial, versão publicada ou código foi alterado. O único arquivo novo no projeto é este relatório. Nos testes em produção, as mensagens para paciente e equipe passaram pelo envio simulado. Criei uma única avaliação de teste pela conversa, na agenda demo, e cancelei pela mesma conversa. Nos registros, todas as 69 execuções associadas aos testes terminaram com `success`, inclusive as que apresentaram os defeitos abaixo. O acesso SSH usou o registro confiável da conta da Erica, com a verificação da identidade do servidor ativa.

## Testes e evidências

Os números abreviados na tabela são IDs de execução do n8n. “Saída” identifica a linha observada em `saidas_teste` antes da limpeza. Uma execução com `success` pode ter passado por um tratamento de erro ou encerrado cedo. Conferi também o que ocorreu nas etapas relevantes.

| Teste | Como fiz | Resultado | Evidência |
|---|---|---|---|
| Primeiro contato, fila de 7 s e ficha | Enviei duas mensagens de texto com 1 s de intervalo | **OK** | Execuções 152 e 161. Um turno, os dois textos no histórico, ficha com Rosa e alinhadores, pendência vazia. |
| Reenvio imediato | Enviei o mesmo texto e ID duas vezes | **OK** | Execuções 153 e 157. Um turno de resposta. |
| Reenvio atrasado | Enviei A, depois B e, após as respostas, reenviei A com o ID original | **Falhou** | Execução 182. Três turnos no total. A saída 178 voltou a responder sobre clareamento. |
| Concorrência na mesma conversa | Enviei outra pergunta 8,7 s depois da primeira | **Falhou** | Execuções 177 e 180. Saídas 169, 173, 180 e 181. A resposta sobre cartão entrou antes da continuação da resposta anterior sobre preços. |
| Lote no mesmo POST | Enviei dois itens em `messages` | **Falhou** | Execução 172. Só o marcador do primeiro item entrou no histórico. |
| Áudio público válido | Enviei como `voice` dois áudios públicos, em FLAC e Ogg Vorbis e conferi o nó de transcrição | **OK** | Execuções 203 e 222. Transcrições “How old is the Brooklyn Bridge?” e “This is an example sound file in Ogg Vorbis format”. |
| Voz com URL real do Whapi | O caso anterior usou mídia pública | **Não deu para testar** | Falta uma amostra sintética entregue pelo CDN do Whapi, de preferência voz em português no formato usado pelo celular. |
| Áudio indisponível | Enviei URL pública inexistente | **OK** | Execução 188. Download 404 e ausência de arquivo binário. A saída 186 pediu que a pessoa escrevesse. |
| Foto | Enviei imagem pública de consultório no formato do Whapi | **OK** | Execução 204. Saída 210 descreveu a dentista, a cadeira e os equipamentos. |
| Documento | Enviei PDF simulado com nome de arquivo | **OK** | Execução 151. Saída 160 informou que verificaria, e a saída 176 registrou o aviso simulado. O conteúdo do PDF ficou fora do teste. |
| Figurinha, vídeo e localização | Enviei os três tipos em conversas distintas | **OK** | Execuções 154, 159 e 162. Resposta leve para a figurinha e pedido de contexto para vídeo/localização. |
| Grupo, status e retorno da API | Enviei evento de grupo, status sem mensagem e mensagem com `from_me=true` e `source=api` | **OK** | Execuções 149, 155 e 158. Nenhum efeito nos contatos de teste. |
| Pausa de 12 horas | Simulei fala da doutora pelo celular e enviei outra pergunta | **OK** | Execuções 170 e 171. Ficha pausada e fala do paciente guardada. O número ficou com apenas o turno anterior à pausa. |
| `#reiniciar` | Enviei o comando de um número de teste fora da lista autorizada | **OK**, para a restrição | Execução 205. Resposta comum, sem aviso de reinício. A autorização positiva ficou sem repetição porque envolve a lista de números reais. |
| Histórico longo | Passei de 11.000 caracteres em dois textos e fiz outra pergunta | **OK**, no cenário executado | Execuções 156 e 175. Limite de 11.000, marcador antigo saiu, ficha preservada e saída 167 informou o valor do clareamento. |
| Marcar e avisar a equipe | Dois números consultaram a mesma vaga, e o primeiro confirmou | **OK** | Execução 194. Evento criado para 19/11 às 14h. Saída 192 confirmou, e a 196 registrou o aviso à equipe. |
| Horário ocupado entre oferta e escolha | O segundo número aceitou a mesma vaga depois da marcação do primeiro | **OK** | Execução n8n 196 consultou a agenda já ocupada. Saídas 197, 198 e 200. A Clara avisou que estava ocupada, deu alternativas e deixou a ficha sem evento. |
| Horário ocupado entre checagem final e escrita | Exige intervir no intervalo entre a checagem e a escrita | **Não deu para testar** | O cenário anterior chegou à IA com a vaga já ocupada. A janela de concorrência e a rota fixa de horário ocupado precisam de simulação isolada. |
| Despedida | Deixei o primeiro número sem responder por cerca de um minuto após marcar | **OK** | Saída 199. “Te esperamos na quinta!” |
| Segunda avaliação | Pedi uma nova avaliação mantendo a primeira | **OK**, com texto ambíguo | Saídas 201 e 202. Mostrou a avaliação existente e não criou outra, mas perguntou se queria manter e marcar outra. |
| Remarcar | Perguntei se o novo horário estava livre no contexto de uma remarcação | **Falhou**, por antecipar a confirmação | Execução 202 e saídas 205 e 207. O mesmo evento foi movido para 24/11 às 11h antes de “Sim, pode remarcar”. |
| Cancelar | Pedi cancelamento e confirmei em outro turno | **OK** | Execução 217 e saídas 215 e 216. Pediu confirmação e limpou os campos. A saída 218 registrou o aviso à equipe. |
| Anthropic indisponível ou JSON ilegível | Revisei a rota de erro em código | **Não deu para testar** | Teste com serviços simulados descrito no problema 4. |
| Google Agenda indisponível | Revisei as rotas de erro em código | **Não deu para testar** | Teste com respostas simuladas descrito no problema 4. |
| Bateria histórica de 56 mensagens | Li o script, o comparador, o arquivo de resultados e o relatório | **Não repetido** | Artefato do Claude contém 56 respostas e nove avisos. A revisão independente usou casos direcionados. |
| Envio real pelo WhatsApp | Mantive a saída simulada e reservei a validação real para a Erica | **Não testado por mim** | A documentação de migração relata um envio de texto real confirmado pela Erica após a virada. |

## Problemas encontrados, em ordem de gravidade

### 1. Crítico · Qualquer pessoa com o endereço do webhook pode se passar por paciente ou doutora

**Em linguagem simples.** Quem souber o endereço pode fingir que recebeu ou enviou uma mensagem pelo WhatsApp. No meu teste, um POST direto marcou a ficha como pausada, exatamente como aconteceria se a doutora tivesse assumido. Com um número real, esse acesso pode gerar mensagens pagas, interromper atendimento e induzir marcação ou cancelamento. O endereço está em documentos, no gerador e nos artefatos. Trate-o como já compartilhado.

**No código.** `gerar_fluxos.py:173-208` confia em `from`, `chat_id`, `from_me` e `source` do corpo. Não valida autenticidade, canal ou origem, e converte a entrada em dígitos em vez de exigir um identificador de conversa válido. A lista de números do `#reiniciar` depende dessa mesma identidade. Em `260-270`, uma URL do corpo também vira um GET pelo VPS, abrindo possibilidade de acesso a serviços internos por meio do servidor, conforme as proteções de rede. O contêiner não tinha configuração explícita de proteção SSRF. Testei apenas com URLs públicas.

**Correção técnica.** Autenticar antes de processar. Usar assinatura verificada se a integração de produção oferecer esse recurso, ou um cabeçalho secreto dedicado e rotacionável após comprovar suporte no Whapi. Validar formato, canal e evento, limitar taxa e tamanho, e separar o endereço público de entrada do painel administrativo. Para mídia, aceitar apenas hosts e protocolos esperados, verificar redirecionamentos, DNS e IPs privados, limitar tamanho e tempo e ativar proteção de saída em rede e no n8n. [Webhook do n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/) · [Cabeçalhos no teste de webhook do Whapi](https://whapi.readme.io/reference/webhooktest) · [Proteção SSRF do n8n](https://docs.n8n.io/hosting/securing/ssrf-protection/)

### 2. Alto · Mensagens podem sumir, reaparecer ou sair na ordem errada

**Em linguagem simples.** Duas mensagens dentro de um único pacote fizeram a Clara esquecer a segunda. Um reenvio antigo ganhou uma nova resposta. Quando duas respostas ficaram prontas perto uma da outra, a resposta sobre cartão entrou entre a apresentação e a resposta sobre preços. Isso pode misturar instruções de atendimento e confirmações da agenda.

**No código.** `179` lê apenas `messages[0]`. Em `300-319`, o UPSERT com parâmetros é um acerto para acumular mensagens na mesma linha, mas `ultimo_id` é uma memória de um único ID. O teste após 7 s não reserva a conversa. Em `504-517`, um resultado antigo salva a ficha sem checar a versão e `replace(pendente, lote_anterior, '')` apaga todas as ocorrências iguais, inclusive texto legítimo repetido. `253-256` também limpa pendências sem reconciliar com execuções em curso. As mídias entram na fila só após o processamento e podem chegar à IA em ordem diferente da de recebimento. `107-110,145-167,518-519` separam as partes dentro de um envio, mas não ordenam envios de duas execuções para a mesma conversa.

**Correção técnica.** Persistir todos os eventos válidos na entrada, com chave única por clínica, canal e ID do provedor. Acusar recebimento após persistir. Consumir mensagens por IDs e por ordem de chegada, com um processador por conversa, lote reservado e versão conferida antes de agir. Fazer a pausa humana invalidar trabalho e envios pendentes. Registrar saídas em fila persistente junto com a atualização da ficha e enviá-las na ordem da conversa, com tentativa controlada e reconciliação. Testar também o reenvio após reinício, eventos de voz repetidos e intervenção humana durante a geração.

### 3. Alto · A IA escolhe ações de agenda com pouca validação e pode concorrer por uma vaga

**Em linguagem simples.** Conferir se há vaga duas vezes ajuda, mas duas pessoas podem receber a última vaga se confirmarem ao mesmo tempo. A Clara também pode interpretar errado um horário ou uma frase ambígua e agir sem uma confirmação comprovável. Se o Google marcar e a ficha falhar logo depois, a clínica fica com uma marcação que a Clara não consegue localizar.

**No código.** `391-430` usa um retrato da ficha e separa `freeBusy` de POST ou PATCH, sem reserva atômica. `408-416` valida data legível e ocupação, sem impor horário da clínica, feriados, duração configurável, limite de 90 dias ou vaga realmente oferecida. Remarcar e cancelar exigem somente ID de evento, inclusive passado, sem verificar confirmação explícita ou a versão atual. `avaliacao_inicio` é texto e a decisão de futuro usa `new Date` (`schema-clara.sql`, `gerar_fluxos.py:394`), enquanto a IA recebe `avaliacao_texto` sem filtro de futuro (`344`). Edição manual na agenda ou `#reiniciar` (`240-248`) pode deixar a ficha e o calendário divergentes. Em `452-484`, ausência de `j.error` é tomada como êxito, inclusive em criação sem ID.

**Correção técnica.** Calcular vagas e exceções em código com agenda explícita por clínica e horários tipados. Persistir oferta, confirmação, reserva e operação com identificadores, proteger o intervalo de concorrência no Postgres e reler o Google imediatamente antes da escrita. Reservas locais controlam a concorrência entre execuções da Clara. Alterações manuais no Google exigem reconciliação. Usar `timestamptz`, conferir a resposta de cada API, criar com ID estável e confirmar ao paciente após persistência e validação do resultado. Definir tratamento para eventos antigos, alterados fora do fluxo ou sem vínculo. [Consulta de ocupação do Google Agenda](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query)

### 4. Alto · Falhas de agenda e encaminhamentos humanos dependem demais da IA e do mesmo WhatsApp

**Em linguagem simples.** Se o Google cair, a Clara pode oferecer um horário porque a proibição é uma instrução escrita. Se o WhatsApp cair, o aviso da própria falha também pode sumir pelo mesmo canal. Uma pessoa pode ouvir “já te retorno” sem ninguém ter recebido um chamado.

**No código.** `320-357` só inclui um texto de indisponibilidade no pedido à IA. Considera `busy` válido se for um array e não checa `calendars.primary.errors`. A segunda checagem já impede a escrita quando não recebe um array, mas a oferta e a transferência continuam dependentes do modelo. `358-389` aceita uma primeira mensagem convertível em texto, sem validar o esquema, e a rota de falha envia aviso sem resolver a pendência no banco. `395-400` trata ação desconhecida como resposta normal. `149-165` tenta avisar por Whapi quando o próprio Whapi falha, e o aviso ignora o erro. `458-460` abre o aviso sem criar um estado de atendimento humano. O pai pode aparecer como `success` enquanto o subfluxo continua ou a entrega falha.

**Correção técnica.** Gerar a resposta segura e encaminhar o pedido de agenda quando a disponibilidade for indeterminada. Validar tipos, ações e campos obrigatórios da IA. Guardar a pendência e o aviso com estado, responsável e prazo de retorno, sem reprocessar o texto automaticamente em cada mensagem nova. Monitorar separadamente falhas de API, falhas do subfluxo, aceitação pelo provedor e entrega. Usar um canal operacional independente para indisponibilidade do WhatsApp. Antes do piloto, testar no ambiente isolado Anthropic com timeout, 429, 500, JSON truncado e JSON bem formado com ação inválida. Para Agenda, simular timeout, 401, 403, resposta HTTP 200 com erro por calendário e falha no POST, PATCH e DELETE. Conferir texto ao paciente, aviso, ficha e ausência de falso sucesso.

### 5. Alto · Dados da clínica e do paciente ficam espalhados e a demo não está isolada do piloto por desenho

**Em linguagem simples.** Conversas, fotos, sintomas, comprovantes, telefones e tratamentos podem aparecer em vários lugares. Copiar o fluxo da demo sem trocar todas as referências pode mandar dados ou avisos para a pessoa errada e marcar na agenda errada.

**No código.** A chave primária em `schema-clara.sql` é só o telefone. `gerar_fluxos.py:8-20,119-154,320-351,419-430` fixa IDs de credenciais, agenda `primary`, marca Clara, Curitiba, fuso, destinatário de falha, duração e IDs de fluxos. `371-386,439-491` pode colocar a mensagem original e dados pessoais em avisos. O título e a descrição da agenda também incluem tratamento, nome ou telefone. Os testes confirmaram que o banco de execuções guarda dados suficientes para recuperar o conteúdo de cada etapa. O contexto completo passa para a Anthropic, e áudio e foto passam pela OpenAI.

**Correção técnica.** Usar instância ou banco e credenciais próprios do piloto, ou isolamento por clínica e canal em toda a cadeia, inclusive consultas, agenda, envios, backups e permissões. Parametrizar nome, regras, dias, duração, agenda, fuso e responsável. Mapear quais dados cada serviço precisa, reduzir o que vai para IA e avisos, preferir dados mínimos no calendário, restringir acesso a execuções e definir prazo de retenção e exclusão. Testar com o mesmo telefone fictício em dois canais e comprovar fichas, calendários e avisos independentes. Rever as instruções da Vivian para que a Clara nunca faça promessa de retorno, diagnóstico, recomendação de tratamento ou urgência além do protocolo aprovado pela dentista. [Retenção de dados de execução no n8n](https://docs.n8n.io/hosting/scaling/execution-data/)

### 6. Alto · A integração da agenda pode expirar antes de 01/12 e o domínio envolve mais que trocar DNS

**Em linguagem simples.** O Google pode parar de renovar a autorização da agenda antes do piloto. Trocar o endereço da Clara também pode parar a entrada de mensagens ou dificultar a reconexão com o Google.

**No código e na documentação.** O guia de migração registra OAuth externo em modo de teste. Nesse modo, o Google documenta expiração em sete dias para escopos de Agenda. O servidor usa domínio provisório e a documentação aponta `WEBHOOK_URL`. O n8n documenta a migração para `N8N_WEBHOOK_URL` a partir da versão 2.35. O host também aparece no script A/B e no log emitido pelo gerador.

**Correção técnica.** Antes do piloto, estabilizar a autorização em uma conta e agenda dedicadas, verificar renovação real e detectar perda de acesso. Na mudança de domínio, validar DNS, TLS, Caddy, URLs públicas do n8n, callback OAuth cadastrado no Google e webhook configurado no Whapi. Planejar sobreposição controlada ou reversão, e testar o percurso completo com o prefixo. Separar a virada do domínio da entrada da Vivian para facilitar o diagnóstico. [Expiração do OAuth do Google](https://developers.google.com/identity/protocols/oauth2/) · [Configuração de webhook atrás de proxy no n8n](https://docs.n8n.io/hosting/configuration/configuration-examples/webhook-url/)

### 7. Alto · Backup no mesmo VPS e acesso administrativo com privilégio total

**Em linguagem simples.** Se o VPS ou o disco forem perdidos, as cópias locais podem sumir junto. Uma credencial de root comprometida dá controle sobre o sistema inteiro. Encontrei um arquivo de backup local de 12/11. A restauração e a existência de cópia externa ficaram sem verificação.

**Divergência confirmada no servidor.** O guia diz que o root entra só por chave. Para a origem da conexão usada na revisão, a configuração efetiva informou `PermitRootLogin yes`, `PasswordAuthentication yes` e `AuthenticationMethods any`. A conta root apresentou status `P` para a senha. Verifiquei a configuração em leitura e não tentei autenticar com senha. Eu trataria essa divergência antes do piloto.

**Correção técnica.** Guardar cópias cifradas fora do VPS, com alerta de falha, retenção e teste de restauração isolado. Proteger também o Compose, configurações e a chave de criptografia do n8n, em armazenamento separado com acesso restrito. Documentar como restaurar banco, volumes, credenciais e DNS, e em quanto tempo. Usar conta nominal de manutenção com sudo e acesso restrito, testar recuperação via console e então desabilitar senha no SSH e retirar login direto de root. Conferir com `sshd -T -C` para as origens relevantes e validar acesso por chave com a nova conta. Conferir regras efetivas de rede, 2FA do painel e acesso restrito ao editor. O n8n e o banco separados por credenciais e sem portas públicas documentadas, HTTPS via Caddy e atualizações de segurança são escolhas que eu manteria. [Opções do servidor OpenSSH](https://man.openbsd.org/sshd_config)

### 8. Médio · O modo de teste protege o WhatsApp e ainda usa a agenda real

**Em linguagem simples.** O prefixo barrou os envios ao WhatsApp nos casos observados. Ele continua deixando a Clara alterar a agenda demo. O desvio de teste também depende de a configuração existir e de o lote incluir o paciente de teste. Se alguém copiar o fluxo e esquecer um desses vínculos, uma simulação pode virar uma mensagem real.

**No código.** `119-146` usa prefixo vazio e modo desligado como valores padrão para configuração ausente, e infere o teste pelos destinos do lote. Uma nova rota com aviso sozinho para a equipe poderia perder esse isolamento. As operações de agenda em `404-430` acontecem antes do desvio de envio.

**Correção técnica.** Determinar o modo de teste pela origem e pelo número da conversa na entrada, propagá-lo como dado explícito em todos os subfluxos e recusar envio quando a configuração necessária estiver ausente. Usar agenda e credenciais descartáveis em testes automatizados. Desativar ou restringir o reinício na clínica real. Uma opção de reversão para o Make precisa considerar que ele usa outra ficha e pode ficar sem os vínculos de eventos criados desde a virada.

### 9. Médio · O corte do histórico funciona no tamanho, mas prejudica a despedida e pode cortar informação ao meio

**Em linguagem simples.** A Clara continuou conversando depois de alcançar 11.000 caracteres. Esse limite pode partir a fala anterior ao meio. Ele também engana a regra da despedida. A conversa pode continuar com exatamente 11.000 caracteres depois de uma resposta nova, e o sistema achar que ninguém respondeu.

**No código.** `215-218,253-257,504-515` cortam pelo fim do texto. `212-214` não limita a primeira fala da doutora ao inserir uma ficha. `525` compara comprimento e pendência vazia, sem conferir ID da última entrada, versão da conversa, pausa ou vínculo da despedida com a avaliação atual. O Make 1C já usava comprimento. O teto fixo aplicado depois de acrescentar a fala da Clara torna a igualdade particularmente fácil no n8n. O campo `pendente` também não tem teto de tamanho e vai para a IA.

**Correção técnica.** Preservar turnos completos com limite em tokens ou caracteres, guardar fatos persistentes separados e resumir a conversa antiga quando necessário. Vincular a despedida ao ID da marcação e à versão da conversa no momento da confirmação. Antes do envio, conferir ausência de nova mensagem ou resposta humana e se a avaliação continua no mesmo estado.

### 10. Médio · Postgres 16 funciona agora, mas a estratégia de atualização é frágil

**Em linguagem simples.** O Postgres 16.15 e o n8n 2.47.5 serviram aos testes. Encontrei registros do n8n que mencionam Postgres 17 e suporte ou recomendação. O risco é descobrir o efeito de uma atualização junto com pacientes usando o serviço.

**Correção técnica.** Confirmar o texto exato do aviso do n8n e o suporte da versão instalada. Fixar versões de imagem em vez de atualizar com a etiqueta flutuante `stable`. Ensaiar migração do Postgres em cópia restaurada, com teste da Clara e plano de retorno. Uma troca de versão principal exige um procedimento de migração dos dados. A documentação do servidor registra a preferência do n8n pelo Postgres 17. [Instalação Docker Compose do n8n](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/)

## Diferenças Make x n8n e decisões com as quais discordo

- **Preservaria** consultas SQL parametrizadas, descarte de grupo/status/API logo na entrada, proteção contra telefone vazio, fallback de áudio e gravação do resultado da Agenda antes de compor o histórico. O descarte de mensagens da API já existia como filtro no Make 1A. No n8n elas ainda chegam ao webhook, mas a execução termina na normalização e não chama IA.
- **Não trataria a migração como equivalência completa.** O Make 1B relia a ficha depois da IA, no módulo 43. O n8n decide a ação com a leitura anterior à IA. A releitura antiga tampouco garantia atomicidade, mas a ausência dela amplia o intervalo com dados desatualizados. Deduplicar só o último ID, operar só o primeiro item do lote, apagar pendentes por texto e checar a despedida por tamanho são problemas herdados que mereciam correção na migração.
- **Discordo de colocar o aviso humano atrás da sequência de mensagens do paciente.** O Make 1B começava a rota humano pelo aviso, no módulo 13, e depois pedia a resposta ao 1D. O n8n põe paciente antes da equipe no mesmo lote e espera entre as partes. Um encaminhamento de urgência ou uma falha da IA pode esperar a simulação de digitação. A equipe precisa receber o chamado imediatamente, com uma fila de envio própria que preserve o isolamento de teste.
- **Discordo de tratar “56 de 56” como prova de entrega ou liberação.** O arquivo histórico contém 56 respostas, zero timeouts e nove avisos, incluindo ações de agenda. `teste_n8n.py:71-91` mede a conversa salva na ficha. `comparar_n8n.py:7-31` coloca os textos lado a lado com a ação do A/B, sem validar automaticamente a ação real ou os critérios de segurança. O A/B usava outra data e agenda fictícia. O teste foi uma boa verificação de tom e regressão básica. Em `teste_n8n.py:96-103`, há exclusão e `TRUNCATE saidas_teste` antes da verificação do prefixo. Por isso usei casos direcionados e deixei a bateria completa sem nova execução.
- **Discordo de prometer aprovação humana no piloto com os fluxos atuais.** O briefing da migração lista a rota de aprovação como trabalho futuro. Os quatro cenários exportados do Make e os dois fluxos n8n revisados não implementam o ciclo de rascunho, autorização e envio. Se a primeira semana depender dessa aprovação, o ciclo precisa existir e ser testado. Também falta confirmar com a Vivian quem recebe avisos e como ela assume uma conversa.
- **Discordo de usar a base de demonstração como configuração suficiente para a Vivian.** A base promete lembretes e confirmações automáticos e cita envio de orçamento em PDF, que estes dois fluxos não executam. A base ainda traz marca, endereço, preços, agenda e equipe fictícios. Validar as promessas, as rotas humanas e as regras clínicas com o roteiro da Vivian antes de conectar o número dela.

## Limpeza verificada

- **Banco da Clara.** Excluí 19 fichas e 73 saídas simuladas desta revisão. As 73 saídas incluem quatro avisos simulados da equipe, removidos pelos IDs individuais e pelo número fictício contido no texto. Conferi zero fichas e zero saídas restantes no escopo desta rodada. Mantive os registros históricos do n8n para auditoria.
- **Google Agenda.** Foi criado um único evento. Começou em 19/11 às 14h, foi movido para 24/11 às 11h com o mesmo ID e foi cancelado pela conversa. As execuções 194, 202 e 217 registraram criação, alteração e cancelamento sem erro. Uma nova consulta real do Google, execução 221, mostrou as duas vagas livres. As fichas desta rodada estavam sem vínculo ativo antes da exclusão. **Nenhum evento desta revisão ficou na agenda.** [Operação de exclusão do Google Agenda](https://developers.google.com/workspace/calendar/api/v3/reference/events/delete)
- **WhatsApp.** Conferi os subfluxos de envio das execuções associadas aos testes. Nenhum passou pelo nó de envio real ou pelo nó de aviso real de falha. Os dois números pessoais ficaram fora dos POSTs.

