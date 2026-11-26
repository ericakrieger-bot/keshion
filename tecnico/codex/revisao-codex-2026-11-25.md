# Revisão independente da Clara, 25/11/2026

Concluída em 25/11 no fuso de Israel. Escopo e consultas referentes a 24/11/2026, horário de Curitiba. A pasta das evidências mantém a data 24/11.

## Resumo em cinco linhas

1. **Não recomendo conectar o número real da clínica piloto para atendimento autônomo com a versão examinada.**
2. Cancelamento, consentimento para marcar e proteção de urgência ainda têm falhas reproduzidas no código publicado.
3. Os 216 testes locais existentes passam; 11 dos 43 casos independentes mostram proteções insuficientes, inclusive nos nós publicados.
4. As correções de 24/11 estão publicadas; português obrigatório continua apenas no Git; o modo fora do horário não está nesta versão.
5. O banco está sem linhas de teste, mas há dois eventos de testes anteriores na agenda; a média 6,64 também não alcança o mínimo 7 definido pela Keshion.

## Método, escopo e versões

Revisão das mudanças recentes solicitadas, sem revisar a migração nem comparar cenários do Make. Fontes da aplicação em `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`. Entrega e instrumentos da auditoria na pasta deste chat, `C:\Users\Erica Krieger-Akerma\OneDrive\Documentos\ChatGPT\KESHION\tecnico\n8n`.

Li contexto, estado atual, documentação do n8n/servidor, gerador, esquema e preparador do banco, configuração/instruções/base da demo, modelo de clínica, checklist, registro dos erros da Erica, revisão/plano de 19/11, roteiro de publicação e ferramentas/resultados de teste. O próprio `RETOMAR-AQUI.md` tem cronogramas conflitantes: copiloto na semana 1 e também na semana 2. O gerador examinado não implementa aprovação humana nem atendimento restrito a fora do horário. A branch separada não foi certificada nesta revisão.

Consultas remotas somente de leitura, com transações `BEGIN READ ONLY` no banco. A chave pública SSH foi comparada com a impressão digital autorizada no pedido antes da autenticação. O primeiro acesso dentro do ambiente restrito falhou; o acesso de leitura com a chave autorizada funcionou. Não há mais pendência de confirmação SSH.

As conferências ocorreram aproximadamente entre **18h48 e 18h55 de Curitiba em 24/11**, equivalentes a **23h48 e 23h55 de Israel**. A clínica estava aberta pelo horário geral, mas doutora e secretária já estavam fora de seus respectivos expedientes. Os testes locais não dependem desse horário. Horários exatos constam nas evidências.

Não alterei aplicação, fluxos, instruções, banco, credenciais, Whapi ou Docker. Não reiniciei o n8n. Não mandei POST ao webhook, não chamei modelos de IA e não repeti rodadas de 56 mensagens ou 22 perfis. Não enviei mensagens para Erica, Sérgio ou outro número real. Apenas criei/atualizei relatório, executores e evidências da auditoria no workspace.

**Método dos testes:** executei os três scripts JavaScript originais com texto intacto, substituindo a leitura dos JSON por fluxos gerados em memória. Executei 43 casos independentes nos nós locais e nas cópias dos nós publicados, sempre em memória. Isso não executa o workflow n8n nem seus serviços. Q01 e Q02 modelam operações de texto da SQL, sem executar Postgres. Identificadores como C02 são casos locais, não IDs de execução n8n.

Evidências relativas a `evidencias-revisao-2026-11-24/`. Fontes/hashes atuais: `fontes-escopo-atual.json`. Método: `metodo-complemento.json`. Executor complementar: `concluir_revisao_2026_11_24.py`. Este relatório substitui a versão preliminar que deixava SSH pendente e incluía comparação fora do escopo.

### O que está no ar

| Peça | Conferência e conclusão |
|---|---|
| Atendimento demo | Publicado `66526f94-0409-4a82-9583-2bd9ada999e7`. Nós e conexões coincidem com o gerador anterior a `be5ff46`. |
| Envio demo | Publicado `7e6e9566-d04d-474f-a677-220b2360a498`. Coincide com o gerador atual. |
| Correções de 24/11 | Reinício com limpeza ampliada, espera de 20 s, digitação de 4 a 50 s e espera estimada de envio até 180 s presentes no publicado. A cópia anterior das 07h19 está documentada; não restaurei nem testei reversão. |
| Português obrigatório | Git atual `8ac4f12` contém `be5ff46`. Publicado e instruções do banco continuam anteriores à mudança. |
| Base da demo | Igual à base local após normalizar CRLF/LF. Inclui retorno de alinhador de R$ 150 à parte. Diferença de hash bruto não significa divergência de conteúdo. |
| Clínica fictícia de teste | Dois fluxos ativos; versões salvas iguais às publicadas. Não certifiquei seu conteúdo como igual à última demo. |
| Execuções nas 24 h consultadas | 556 atendimentos e 412 envios com `success`; nenhum erro/crash ou execução pendente. Término técnico não comprova consentimento, qualidade ou entrega no celular. |

Evidências: `servidor-comparacao-fluxos.json`, `publicado-proveniencia.json`, `servidor-preflight-leitura.json`. Os 11 resultados negativos são os mesmos nos nós locais e publicados. A alteração de idioma não os resolve.

## Tabela de testes

Resultados novos locais estão separados dos testes anteriores de Claude/Erica. Sem novos atendimentos no servidor, não há novas execuções nem trechos novos de `saidas_teste` atribuíveis a esta revisão.

| Teste | Como fiz | Resultado | Evidência |
|---|---|---|---|
| Pacote A | Script original, nós atuais em memória | **ok**, 48/48 | `teste_pacote_a.js.resultado.json` |
| Pacote C | Script original, atendimento/envio em memória | **ok**, 75/75 | `teste_pacote_c.js.resultado.json` |
| Datas e horas | Script original sobre trecho do validador | **ok**, 61/61 e 32/32 | `teste_validacao_data_hora.js.resultado.json` |
| Cancelar com pergunta explícita e aceite curto | Nó completo, evento fictício | **ok**, libera cancelar | C01 em `casos-independentes.json` e `casos-independentes-publicado.json` |
| Cancelar após “é a avaliação de..., certo?” | Pedido anterior e “Sim, pode cancelar” | **falhou**, pergunta novamente | C02, `rota=responder` |
| “Sim” sobre telefone ou negativa de cancelar | IA simulada tentando cancelar | **ok**, bloqueia | C03 e C05 |
| Confirmação cita outra data | Ficha de 01/12, pergunta sobre 03/12 e “sim” | **falhou**, libera cancelar | C04, `rota=cancelar` |
| Sangramento com pergunta e dor forte | IA simulada como responder | **ok** no encaminhamento | U01/U04; texto ao paciente tem ressalva no item 1 |
| Dificuldade para respirar/engolir e falta de ar | IA simulada como responder | **falhou**, não força encaminhamento | U02/U03/U07 |
| Negação de febre e dúvida geral de gengiva | Nó com ação responder | **ok**, não força urgência | U05/U06; não mede a IA real |
| Escolha de data, negativas e escolha parcial | Validador completo | **ok** nos controles | A01 a A05 |
| Oferta antiga sem escolha atual | “Estou só vendo preços”, IA tenta marcar | **falhou**, valida | A06, `passo=ok` |
| Paciente escreve linha começando com “Clara:” | Data/hora fictícia após recusa | **falhou**, valida | A07, `passo=ok` |
| Vaga ocupada entre oferta e escolha | Google fictício ocupado no nó de reconsulta | **ok** no bloqueio | G01; sem disputa real de vaga |
| Google livre ou resposta inválida | `busy=[]` e lista ausente | **ok** no nó | G02/G03 |
| Google indisponível com oferta numérica | `agenda_ok=false`, “terça às 9h” | **ok**, rota sem agenda | G04 |
| Google indisponível com hora por extenso | “terça às nove da manhã” | **falhou**, mantém oferta | G05 |
| Google não devolve ID ao criar | Resultado vazio fictício | **ok**, não registra marcação | G06 |
| IA ilegível e preparação do aviso de falha | Leitor original e erro fictício | **ok** nos nós | I01/I02/I04; equipe primeiro e paciente com “Só um instante...” |
| Mensagem da IA em formato de objeto | `mensagem1={x:1}` | **falhou**, aceita `[object Object]` | I03 |
| Grupos, retorno da API, status e canal errado | Entradas fictícias no normalizador | **ok**, ignora | N01/N02/N09/N10 |
| Doutora pelo celular | Normalizador original | **ok** na classificação | N03; pausa SQL conferida por leitura, sem novo teste integrado |
| Documento, figurinha, vídeo e localização | Normalização de cada tipo | **ok** na entrada; resposta final **não deu para testar** | N04 a N07 |
| Áudio fora da lista de origens | URL fictícia externa | **ok**, não baixa como áudio | N08 |
| WAV/Ogg | Código multipart e testes de metadados | **ok** em metadados; transcrição real **não deu para testar** | C6 no Pacote C; não são arquivos sonoros reais |
| Prefixo protege lote e avisos | Montagem de lote fictício | **ok** nos casos exercitados | S01/S02; prefixo do banco confirmado `554199900` |
| Reenvio do mesmo ID | Revisão do `ON CONFLICT` | **não deu para testar** novamente integrado | Nó de fila; ressalvas no item 8 |
| Mensagem nova igual à processada | Modelo literal do `replace` SQL | **falhou**, remove também a nova | Q01 |
| Histórico acima de 11.000 caracteres | Modelo do corte pela direita | **falhou** em preservar fronteira de fala; sem exceção | Q02 |
| Mesmo telefone concorrente e mensagem durante envio | Revisão de consultas e ordem dos nós | **não deu para testar** com concorrência controlada | Item 4 |
| Reinício durante IA/agenda | Revisão da limpeza e condição de salvamento | **não deu para testar** integrado; proteção parcial | Item 4 |
| 56 mensagens de 24/11 | Resultado anterior, sem repetir | **ok** como 56 respostas; **falhou em comprovar ciclo de agenda** | `rodada-claude-24-11-leitura.json`: C2 sem evento nas 12 etapas |
| 22 perfis de 24/11 | Relatório/conversas anteriores | **falhou** no portão de média 7 | Média 6,64 em `paciente-simulado-20261124-214610.md` |
| Agenda e limpeza | GET de eventos e SELECT dos bancos | Banco **ok**; agenda **falhou** no critério zero sobra | `servidor-agenda-inventario.json`; lista no fim |
| Envio real pelo WhatsApp | Reservado à Erica | **não deu para testar**, conforme restrição | Nenhum envio real |

## Problemas, do mais grave ao mais leve

### 1. Urgências importantes ainda dependem da interpretação da IA

**Em linguagem simples:** se a IA interpretar mal “não consigo engolir” ou “estou com dificuldade para respirar”, a proteção extra não chama a equipe sozinha. Não afirmo que a IA sempre errará; a barreira é que não cobre esse erro. Quando corrige uma resposta comum para encaminhamento, o código também pode manter um texto inadequado da IA.

**Evidência técnica:** `gerar_fluxos.py:300`, expressão `URGENCIA`, não contempla essas formulações. U02/U03/U07 ficam em responder, embora as instruções/base prevejam esses sinais. U01 vira humano, mas conserva “Resposta fictícia.”. A resposta fixa de urgência só substitui o texto quando a ação anterior não era responder.

**Como corrigir:** definir com a clínica sinais e respostas aprovadas, ampliar casos de relato/negação/contexto e produzir aviso e resposta coerentes quando a barreira intervier. Definir responsável e horário de monitoramento, especialmente fora do expediente. Esta é uma conclusão sobre cumprimento das regras existentes, sem criar protocolo clínico novo.

### 2. Cancelamento tem múltiplas causas de repetição e não vincula a confirmação ao evento

**Em linguagem simples:** a Clara tenta deduzir pelo texto se já confirmou o cancelamento. Isso pode gerar perguntas repetidas e, no sentido oposto, aceitar uma confirmação sobre outra avaliação.

**Causa confirmada:** `gerar_fluxos.py:722` exige `?` e `/cancel/` na última fala da assistente. A regra 10 ensina “A sua avaliação de..., certo?”, sem a palavra. C02 reproduz o bloqueio. Entretanto, isso **não explica sozinho Bia e Sandra**:

* **Bia:** as respostas seguintes contêm perguntas e “mas antes me responde...”. `curto` e `simSegundaVez` rejeitam qualquer `?` na mensagem inteira, além de palavras fora da lista. Não considero “antes de cancelar...” autorização inequívoca para apagar imediatamente; o erro é ignorar a dúvida e repetir sem saída.
* **Sandra:** a pergunta inicial já tem “cancelar”. Sua confirmação longa cita filha, nome, data e hora, ultrapassando a lista/tamanho. Depois, “não é minha, é da Laura” vira negativa global do cancelamento. O fluxo chega a dizer “continua marcada”, embora ela esteja corrigindo quem é a paciente.
* **Thiago:** começa com a pergunta sem “cancelar”; depois usa “Valeu!”, ausente de `SIM_OK`. A flexibilização só ocorre após duas perguntas explícitas e ainda depende de tamanho e pontuação.

Essas sequências estão nas conversas dos perfis de 24/11. C04 demonstra outro risco: ficha de 01/12, pergunta sobre 03/12 e “sim” liberam a rota que apaga o ID da ficha. Não fiz exclusão real.

**Correção segura proposta, sem implementar:** persistir operação pendente com tipo cancelar, clínica, telefone, paciente/beneficiário, ID do evento, início, versão da ficha, validade e ID da pergunta enviada. Gerar a confirmação pelo fluxo com esses dados. Executar somente após aceite inequívoco referente à operação atual, sem retirada de consentimento, revalidando versão e pausa. Consumir a autorização uma vez e identificar a operação para impedir repetição.

Nome/data/beneficiário divergentes, pergunta sobre telefone, “não cancela ainda”, “antes...” e dúvida sobre qual avaliação devem levar a esclarecimento ou pessoa, preservando o evento. Não tratar qualquer “não” como recusa global. Responder às dúvidas sem perder a pendência; após repetição sem resolução, encaminhar à equipe com contexto. Retirar apenas `/cancel/`, aceitar qualquer “sim” ou aumentar o limite de palavras recriaria o risco de cancelar sem confirmação.

**Testes da futura correção:** aceite simples; pergunta sem cancelar; confirmação com nome/data; responsável pela filha; evento errado; negativa; adiamento; dúvida antes de cancelar; outro assunto; confirmação vencida; intervenção humana; mudança de evento; mesmo aceite reenviado. Verificar o ID realmente afetado, não só a frase final.

### 3. Oferta antiga pode ser confundida com escolha do paciente

**Em linguagem simples:** mostrar um horário não significa que a pessoa o escolheu. A proteção permite marcar após “estou só vendo preços” se a IA tentar a ação errada. Uma linha do paciente começando com “Clara:” também pode ser interpretada como fala da clínica.

**Evidência:** A06/A07 retornam `passo=ok` no validador completo. Em `gerar_fluxos.py:939`, `ehAssistente` infere autoria pelo início do texto. Em `parNaConversa`, uma oferta pode bastar sem escolha positiva atual. As negativas explícitas corrigidas no Pacote C funcionam nos casos exercitados, mas não resolvem consentimento ausente.

**Como corrigir:** autoria estruturada; opções oferecidas com identificação/validade; escolha positiva ligada a uma opção vigente. Texto do paciente não pode mudar sua autoria. Nome, telefone e disponibilidade continuam necessários, mas não substituem a escolha.

### 4. Esperas de 20 s e 180 s não garantem exclusividade nem invalidam todo trabalho antigo

**Em linguagem simples:** juntar mensagens rápidas funciona, mas outro processamento pode começar enquanto o primeiro consulta IA/agenda. Uma resposta antiga pode gravar dados ou alterar avaliação depois de mensagem nova, reinício ou intervenção humana.

**Evidência:** `ultimo_id` é conferido ao ler a ficha, antes das chamadas externas. O salvamento em `gerar_fluxos.py:1169` exige só `ultimo_id IS NOT NULL`, não igualdade com a versão processada. `envio_ate` só nasce depois das chamadas e estima a duração. O subfluxo usa `waitForSubWorkflow=False`.

O reinício limpa os campos esperados, aceita as variações documentadas e impede o salvamento normal enquanto `ultimo_id` ficar nulo. Mas uma mensagem nova preenche esse campo e pode permitir salvamento velho. O ramo de registrar falha nem tem essa condição. Lote já entregue ao envio não carrega versão de reinício; ação Google anterior não é desfeita ao limpar a ficha.

A pausa é relida antes de cada mensagem, boa melhoria do C4. Ainda há janela depois da leitura, inclusive durante o HTTP com digitação. Não se deve prometer recolher mensagem já aceita pelo provedor. Também falta revalidar pausa antes de criar/mudar/cancelar no Google.

**Como corrigir:** processamento exclusivo por clínica/telefone, com versão e posse temporária; conferir versão/pausa antes de efeitos externos e ao salvar; identificar também lotes de envio. Registrar resultado real do envio, em vez de somente estimar duração. Ensaiar intercalamentos em ambiente isolado.

A reserva por início bloqueia parte das disputas entre telefones distintos, mas permite reentrada do mesmo telefone e não coordena intervalos sobrepostos nem calendário compartilhado entre bancos. Timeout após criação pode deixar evento sem ficha. Persistir identidade da operação e reconciliar antes de repetir. O Google recomenda ID próprio do evento para reduzir duplicação nesse caso: [criação de eventos](https://developers.google.com/workspace/calendar/api/guides/create-events).

### 5. Testes de aceitação deixam passar objetivos não cumpridos e limpeza incompleta

**Em linguagem simples:** “respondeu 56 vezes” não significa “marcou, remarcou e cancelou”. Na C2 de 24/11, as 12 etapas ficam sem evento. O roteiro não fornece sobrenome/telefone quando pedidos; portanto não comprova essas operações.

**Evidência:** `rodada-claude-24-11-leitura.json`. `teste_n8n.py` valida contagem e erros de ferramenta, não estado esperado da agenda. Até “SEM RESPOSTA” é contado no fim sem, por si só, tornar `valida=false`. A resposta é lida da ficha, salva antes da entrega pelo envio.

O simulador dos 22 perfis tenta cancelar pela conversa, o que é bom, mas verifica o ponteiro da ficha, não inventário Google. A limpeza final apaga esse ponteiro mesmo se o cancelamento não resolveu. O teste de 56 não faz cancelamento automático de evento. Os roteiros reutilizam telefones fixos e limpam antes, exigindo coordenação para não apagar evidência de outra rodada. Os eventos encontrados mostram por que banco vazio não comprova agenda limpa; não atribuo sua origem a uma execução específica sem rastreá-la.

**Como corrigir:** roteiros coerentes com dados obrigatórios; separar validade técnica de aprovação funcional; verificar ID/início no Google após marcar/remarcar e ausência após cancelar; reprovar ausência de resposta e objetivo descumprido; preservar inventário antes de apagar fichas. Telefones exclusivos por rodada e conferência direta de eventos no fim.

O avaliador também tem critérios antigos: `paciente_simulado.py` ainda pede validade de orçamento de 15 dias em alguns perfis, enquanto a base diz 30. Parte das críticas é preferência textual, não violação comprovada. Não descartaria a queda para 6,64, pois há falhas objetivas, mas alinharia critérios antes de atribuir toda diferença à qualidade da Clara. Nota não substitui segurança.

### 6. Falha do Google bloqueia algumas ofertas, mas outras passam

**Em linguagem simples:** sem agenda, “9h” é bloqueado, mas “nove da manhã” pode chegar ao paciente. Quando a vaga acaba de ser ocupada, o fluxo informa isso e pergunta se a pessoa quer outras opções; não calcula automaticamente novos horários.

**Evidência:** `ofereceHorario` em `gerar_fluxos.py:747`; G04 bloqueia e G05 passa. A reconsulta está ligada antes de criar/mudar e G01 segue para ocupado. `Resultado · ocupado` usa `F.ocupado` e `F.outras`, sem gerar alternativas. A exigência de oferecer outros está, portanto, parcialmente atendida.

**Como corrigir:** opções disponíveis estruturadas, permitindo oferta só a partir de consulta válida. No erro Google, resposta fixa e encaminhamento sem oferta. Se ocupado, recalcular alternativas ou encaminhar a verificação, sem afirmar disponibilidade não consultada. Não provoquei indisponibilidade real.

### 7. A fila pode perder mensagem nova e o histórico corta o meio de uma fala

**Em linguagem simples:** se a pessoa escreve “Oi” e repete enquanto a resposta é preparada, a limpeza pode remover os dois. Histórico longo pode perder quem disse o quê e uma decisão importante.

**Evidência:** `replace(pendente, pend_bruto, '')`, linhas 697/1154, remove todas as ocorrências. Q01 modela `Oi\nOi` virando só quebra de linha. `right(...,11000)` com `ltrim` não preserva mensagens, demonstrado em Q02. O modelo não gera exceção, mas não garante sentido. O corte de conversa também não limita pendências acumuladas.

**Como corrigir:** uma linha por mensagem, com ID e consumo apenas dos IDs processados; histórico por turnos completos e resumo controlado; limites de entrada/pendências. Estado de operações deve ficar fora do texto cortável. Não afirmo que toda conversa longa quebra.

### 8. Endereço secreto não autentica o webhook; mídia é deduplicada tarde

**Em linguagem simples:** quem descobrir o endereço pode copiar canal/telefone, fingir mensagem da doutora e causar custo ou pausa. O filtro de canal evita alguns erros, mas não prova o remetente.

**Evidência:** webhook sem autenticação, resposta imediata `onReceived`; normalizador confia em `channel_id`, `from_me`, `source`. Transcrição/foto ocorrem antes de inserir em `mensagens_recebidas`, então reenvio de mídia pode repetir chamadas pagas mesmo sem nova resposta. Ramo da doutora e reinício não passam pela mesma deduplicação. Sem ID, o identificador depende do momento e muda a cada reenvio.

**Como corrigir:** autenticação verificável compatível com o provedor, controle de taxa/tamanho, entrada persistida antes de confirmar recebimento; deduplicação antes das chamadas pagas e nos demais ramos. Validar origem/destino final de downloads e limitar tamanho/redirecionamentos. Lista Wasabi/Whapi é útil, mas não identifica dono do objeto nem valida sozinha todo redirecionamento. Não fiz tentativa de abuso.

### 9. Falta validar os tipos da resposta da IA

**Em linguagem simples:** resultado malformado pode virar mensagem estranha para o paciente, em vez de aviso de falha.

**Evidência:** I03 retorna `ok=true` com `[object Object]`. O leitor converte campos usando `String(...)`, aceitando tipo inadequado. Segunda tentativa e aviso existem, e funcionam nos nós locais para JSON ilegível. Isso não comprova HTTP/timeout e entrega dos avisos integrados.

**Como corrigir:** validar esquema, tipos, tamanhos e coerência entre ação/campos. Rejeitar objetos/arrays nos textos. Usar código de erro controlado no aviso: C5 retirou `error.message` do alerta de falha do WhatsApp, mas a falha da IA ainda incorpora até 300 caracteres do erro recebido. Não constatei vazamento real.

### 10. Dados de pacientes existem além da ficha

**Em linguagem simples:** cortar/apagar a conversa da ficha não apaga cópias nos registros de execução e backups.

**Evidência:** retenção configurada de 336 h e sem desativação explícita do salvamento de sucesso; o gerador também permite salvar execuções manuais. A documentação descreve salvamento de sucesso por padrão e limpeza periódica: [variáveis de execuções n8n](https://github.com/n8n-io/n8n-docs/blob/main/docs/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions.md). Histórico, saídas, execuções e backups têm retenções diferentes. Criptografia das credenciais não significa proteção equivalente de todo texto do paciente.

**Como corrigir:** definir finalidade, acesso e retenção por cópia; reduzir registros e texto sensível; evitar histórico bruto em aviso sem necessidade; definir exclusão e recuperação de backup. Aplicar usuário limitado `_app`. Não extraí dados de pacientes reais nem fiz auditoria jurídica.

### 11. Caso 8, Diego e Dona Lourdes precisam de regras mais precisas

**Caso 8, clareamento/gengiva:** concordo em rever excesso de encaminhamento quando é apenas dúvida geral. O código já deixa essa pergunta em responder no teste local. A decisão real de humano vem da IA e de instruções potencialmente conflitantes: H encaminha sangramento; regra 2 permite explicação geral. Esclarecer a diferença com exemplo aprovado pela clínica, sem diagnóstico. Não bloquear encaminhamento de relatos reais.

**Diego:** concordo com o resultado ruim, mas oferecer horário diretamente não era a regra vigente nesse cenário. Ele relata avaliação perdida, a ficha está sem evento, e a regra 9 manda usar humano; isenção de multa também exige pessoa. Separar a decisão da multa do próximo agendamento, com caminho explícito para nova avaliação após falta, sem presumir evento inexistente. A ficha sem telefone apesar de “já anotei” é outra inconsistência: o contrato de saída pede esse campo só em agendar/remarcar. Alinhar captura de dados, regra e expectativa do teste.

**Dona Lourdes:** a Clara deveria dizer que não faz implante, pois a base é explícita. **A base não diz expressamente que não faz dentadura.** Não é seguro exigir uma negativa inventada; cadastrar prótese removível/dentadura. Após 17h a clínica fica aberta até 19h, mas a doutora atende até 17h e secretária até 18h. “Clínica aberta” não garante retorno da doutora. A regra J induz o erro usando horário geral. Definir prazo por responsável e assunto, sem prometer “em breve” sem cobertura. Essas conclusões vêm das regras e conversas, não só das notas da outra IA.

### 12. Preparação operacional do piloto permanece incompleta

**Em linguagem simples:** há boas proteções na instalação, mas falta comprovar agenda correta, cobertura humana e recuperação para a primeira clínica.

**Confirmado:** n8n 2.47.5, Postgres 16.15 e Caddy 2.11.9 em execução; Postgres saudável; sem portas publicadas do n8n/Postgres; firewall, fail2ban, cron e atualizações automáticas ativos; SSH sem senha/teclado interativo; `.env` e rclone com permissão 600. Acesso segue como root por chave.

Backup instalado tem o mesmo hash da fonte local e sintaxe válida. Status registra `OK` às 03h05 de 24/11 para banco e configuração no Drive. Isso resolve a dúvida documental de D1 ainda não instalado, mas **não é restauração atual nem listagem do Drive**. Não rodei backup/rclone. Alerta externo desligado; rclone sem cliente OAuth próprio configurado. A documentação registra restauração sintética e mantém pendente ensaio com arquivo/chave reais. Evidência: `servidor-infra-backup.json`.

Credenciais usam os donos `clara` e `clinica_teste`; não encontrei papéis `clara_app`/`clinica_teste_app`. A separação do roteiro ainda não está aplicada nesses bancos. Recomendo usuário limitado antes de clínica real e usuário de manutenção com sudo no lugar de root; root por chave, sozinho, não demonstra comprometimento.

A agenda respondeu ao GET, com renovação normal de token apenas em memória. Não reconectei nem alterei credencial. Isso não garante funcionamento em dezembro: segue o risco de vencimento perto de 26/11. O Google documenta sete dias para autorização de app externo em teste com esses escopos. [Expiração OAuth](https://developers.google.com/identity/protocols/oauth2#expiration). Não consultei o painel para certificar a publicação do app.

Postgres 16 não exige troca emergencial por esse aviso: a política oficial atual inclui 16 por compatibilidade e recomenda 17/18. [Versões PostgreSQL no n8n](https://github.com/n8n-io/n8n-docs/blob/main/docs/deploy/host-n8n/configure-n8n/choose-n8ns-database.md). Planejar atualização com backup e ensaio. Não certifiquei vulnerabilidades de todas as dependências.

**Antes do piloto:** OAuth duradouro, monitor independente com responsável/substituto, restauração isolada, usuário limitado, configuração/aceite da clínica e teste do modo fora do horário. Agenda em caderno ou sistema odontológico exige sincronização confiável ou Clara só coleta preferência e equipe confirma. Google paralelo vazio não representa vagas reais. O gerador atual é centrado no Google, sem modo explícito para esses cenários.

Modelo de clínica traz dias, horários, feriados e recesso da demo. Revisá-los com a clínica. Validações impedem colisões importantes, mas fuso é verificado por formato, não existência; calendário/acesso e coerência base/regras não são certificados. Duração é configurável, enquanto a instrução da demo fala em 60 minutos.

## O que está certo

Pacote C melhora a proteção contra “sim” sobre telefone, horário explicitamente negado, urgência com pergunta e intervenção humana no lote. Os testes existentes exercitam essas melhorias em nós locais. O alerta de falha do WhatsApp ficou mais restrito, e o nome WAV preserva formato declarado em vez de apenas trocar para Ogg.

Separação por clínica, SQL parametrizada, IDs persistidos, reconsulta de vaga antes de marcar/mudar, limites Google, exigência de nome/telefone e ID devolvido são boas decisões. A proteção de teste considera o lote inteiro, inclusive avisos. Publicação/reversão evitam reinício. Versões fixas, portas internas e backup externo criptografado formam uma base operacional razoável.

## O que os testes locais comprovam e o que falta

`teste_pacote_a.js` executa decisão/resultado e verifica trechos de SQL/timeout. Não executa banco, concorrência, Google ou entrega. Alguns nomes ainda dizem inglês/espanhol, embora a expectativa já tenha sido alterada para português. Atualizar os nomes evita conclusão equivocada.

`teste_pacote_c.js` cobre frases específicas de cancelamento/negativa/urgência e metadados de áudio. C4/C5 conferem consulta e ligações, não pausa real durante HTTP. C6 não verifica bytes nem converte formato. As confirmações positivas usam principalmente a pergunta com cancelar, deixando fora a pergunta natural da regra 10 e responsável pela filha.

`teste_validacao_data_hora.js` extrai só o reconhecedor. Seus 93 casos não exercitam grade, antecedência, nome/telefone, reserva, Google ou consentimento. Podem usar data passada porque a parte que a rejeitaria está fora do recorte. É válido para reconhecimento, mas não são 93 marcações válidas.

Faltam integrados: WAV/Ogg Whapi; falhas HTTP/timeout IA/Google; concorrência controlada; reinício/pausa durante efeito externo; reenvio de mídia; histórico grande preservando decisões; resposta final a documento/figurinha/vídeo/localização. Envio real permanece com Erica.

## Como testar falhas sem mudar produção

Cópia isolada de banco/fluxos, sem credenciais reais nem acesso a WhatsApp/agenda real. Serviços substituídos por simuladores e saídas em coletor local. Somente telefones `554199900...`. Criar esse ambiente é próxima atividade, não algo feito/publicado nesta revisão.

Simular IA com 429/500, timeout, JSON truncado, só pensamento, tipos errados e falha nas tentativas. Exigir espera ao paciente e aviso à equipe. Simular Google indisponível, lista ausente, vaga ocupada após oferta, criação efetuada com resposta perdida e DELETE falho. Verificar ausência de confirmação falsa e operação repetida. Incluir falha ao salvar após efeito externo e erro de envio/alerta.

Segurar primeira resposta da IA, receber nova mensagem e intervenção humana, depois liberar a primeira: não pode alterar agenda nem sobrescrever estado novo. Repetir com reinício seguido de nova mensagem. Disputar vaga entre dois telefones, repetir operação do mesmo telefone e testar intervalos sobrepostos.

## Decisões de que discordo

1. **Só média 7 como portão.** Manter o mínimo de qualidade, junto de critérios obrigatórios para consentimento, urgência, pausa, agenda e recuperação. Média pode esconder falha grave.
2. **Adiar garantias de operação sem ensaio específico.** Parte foi deixada para depois no plano de 19/11, mas os casos afetam o primeiro piloto, não só escala futura.
3. **Corrigir cancelamento apenas com mais expressões.** A repetição inicial e Bia/Sandra têm causas diferentes. Estado pendente ligado ao evento é verificável.
4. **Tratar espera estimada ou success como prova de entrega.** Ficha/execução não comprovam mensagem recebida.
5. **Depender do WhatsApp para alertar sobre falha do WhatsApp.** Monitor independente é necessário; monitor de backup não mede saúde do atendimento.
6. **Avaliar por fatos ausentes ou antigos.** Dentadura não está negada expressamente e critérios ainda usam orçamento de 15 dias. O avaliador precisa acompanhar a fonte aprovada.

## Limpeza e eventos encontrados

**Não criei linhas de teste nem eventos nesta revisão. Não havia linhas próprias para apagar.** A leitura mostrou zero pacientes, saídas, mensagens recebidas e reservas `554199900%` nos bancos clara e clinica_teste. Nenhum evento foi apagado por mim.

**Não confirmo agenda limpa.** A consulta paginada de 12/11/2026 até o início de 25/02/2027 retornou nove eventos e identificou estas sobras pelo prefixo:

| Telefone fictício | Horário de Curitiba | ID do evento | Situação |
|---|---|---|---|
| `554199900801` | 26/11/2026, 11h às 12h | `qt60qgvcncab425nf980bvlth8` | Confirmado; criado em 24/11 às 12h41 |
| `554199900805` | 01/12/2026, 11h às 12h | `o66vl5lkmga5c1mha0psiep2a0` | Confirmado; criado em 24/11 às 12h41 |

Há ainda **dois eventos com marcador textual teste/Codex, sem prefixo identificável**, para classificar antes de excluir. Não os declaro sobras minhas nem exponho possíveis dados reais. A consulta é limitada ao intervalo e marcadores; não certifica todo o calendário de todas as épocas.

Os dois eventos com prefixo já existiam e não têm ficha correspondente. Não reconstruí conversa nem tentei cancelá-los: seria escrita sobre itens de outra rodada, fora da autorização de limpar apenas o que eu criasse. Evidência: `servidor-agenda-inventario.json`.

**Liberação proposta:** rever itens 1 a 4, comprovar ciclo real de agenda e limpeza, alinhar base/avaliador e prazos da equipe, concluir OAuth/monitoramento e testar fora do horário na clínica escolhida. Aprovação humana efetiva pode reduzir exposição no piloto, mas depende de implementação/validação; não está certificada aqui.
