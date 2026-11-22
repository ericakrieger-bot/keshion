# Red team da estratégia atual da Keshion (22/11/2026)

> Feito com a skill `strategy-red-team`, seguindo as regras do agente `estrategia`. Rascunho para a Erica ler: nenhum documento, servidor, n8n ou Notion foi mexido.
> Fontes: `CLAUDE.md`, `plano-estrategico-keshion.md`, `comercial/piloto/estrutura-piloto-conhecidos.md`, `comercial/piloto/cliente-ideal-e-aprendizado.md` (seção 1), `comercial/estrategia-de-preco.md`, `comercial/sergio/conversa-piloto-dr-william.md`, `tecnico/RETOMAR-AQUI.md`, `conflitos-e-duplicatas.md`. O cronograma técnico de 23 a 29/11 (publicação única em 27/11, testes em 28 e 29/11) veio do pedido, não de um arquivo da pasta: está no Notion.

## O plano em uma linha

Três clínicas odontológicas do dia a dia, de conhecidos, entram aos poucos (fora do horário, depois copiloto, depois funções novas), sem custo por um período estendido; o preço só é testado na semana 4; e disso deve sair o primeiro pagante até 31/01/2027.

## As 7 suposições, da mais perigosa para a menos

### 1. "O primeiro pagante até 31/01/2027 vai aparecer"

- **Por que pode ser verdade:** um piloto que gosta vira fundador; o plano já tem a oferta de fundador pronta.
- **Risco se estiver errada:** hoje não existe caminho no papel para esse pagante. Os 3 pilotos ficam sem custo por um período estendido e sem data de fim. A prospecção fria só volta depois de 02/12, e a meta semanal do Sérgio está suspensa "até o fim dos pilotos", que agora não têm fim. Dezembro e janeiro são meses lentos (risco já listado no próprio plano). Resultado provável: 31/01 chega com 3 clínicas felizes e nenhuma pagando.
- **Teste mais barato (esta semana):** escrever no convite do 1º piloto uma frase com data: "sem custo até [data]; depois, preço de clínica piloto com desconto". Ver se o dentista aceita assim. Custa uma frase.
- **Critério de parada:** se até 15/12 nenhum dos pilotos aceitar uma data de fim do período sem custo, o primeiro pagante não sai deles e a prospecção precisa voltar logo em dezembro.
- **Recomendação:** definir já a data em que o período sem custo termina (sugestão: no máximo 31/01 ou 28/02) e decidir de onde vem o 1º pagante. Opção barata: indicações dos próprios pilotos e conhecidos de segunda linha a partir de 03/12, sem voltar à lista fria.

### 2. "O dentista consegue aprovar as respostas no copiloto sem o paciente esperar mais do que hoje"

- **Por que pode ser verdade:** dá segurança ao dentista, cada correção vira regra, e ele aprova pelo celular.
- **Risco se estiver errada:** a dor número 1 do cliente ideal é "mensagem sem resposta enquanto o dentista está com paciente na cadeira". O copiloto no horário de atendimento pede justamente a essa pessoa que aprove cada mensagem, "o tempo que for". Na clínica sem secretária, a semana 2 pode deixar o paciente esperando mais do que hoje, e a primeira impressão da Clara vira "mais uma coisa para eu fazer".
- **Teste mais barato:** na conversa de 60 min, perguntar quem responde o WhatsApp no horário e quanto tempo leva hoje. Depois, numa manhã da semana 0, mandar ao dentista 5 pedidos de aprovação de mentira, no número de teste, e medir em quanto tempo ele responde.
- **Critério de parada (estimativa, ajustar com ela):** se a aprovação demorar mais de 15 a 20 minutos na maioria das vezes, o copiloto no horário não serve para essa clínica.
- **Recomendação:** deixar combinado um plano B para o copiloto: quem aprova é a secretária, quando existe; ou, se ninguém aprovar em X minutos, a Clara manda só um "recebi, já te respondo" e espera. Isso é decisão de produto para o técnico, não para agora no fluxo.

### 3. "A Clara já atende bem o paciente antigo"

- **Por que pode ser verdade:** ela reconhece quem já conversou, marca, remarca e cancela sem horário em dobro.
- **Risco se estiver errada:** nos testes, os perfis de paciente antigo tiraram 5 a 6 de 10 (não informou a faixa da limpeza, disse "a doutora tem o seu prontuário", não ofereceu marcar). Com o público novo, retorno, limpeza e manutenção são a maior parte do WhatsApp. Não achei nos arquivos que essa regra já tenha sido corrigida. O dentista conhecido vai testar justamente isso na semana 0.
- **Teste mais barato:** colocar a regra de paciente antigo no pacote de 27/11 e rodar, na conversa de testes, só os 7 perfis de ciclo de vida (o teste com Haiku no paciente é barato).
- **Critério de parada:** média abaixo de 7 nos perfis de paciente antigo: não liga no número real da clínica.
- **Recomendação:** tratar a regra de paciente antigo como item obrigatório do dia 1, no mesmo nível do "só fora do horário".

### 4. "O cronograma técnico de 23 a 29/11 cabe"

- **Por que pode ser verdade:** uma publicação só reduz risco de derrubar conversas, e deixa 2 dias para testar.
- **Risco se estiver errada:** não há folga. Se o teste de 28/11 achar um erro grave, não sobra dia para corrigir e testar de novo. Além disso: (a) a autorização do Google Agenda vale só até cerca de 26/11, antes da publicação; (b) ainda faltam rodadas válidas pendentes (22 perfis e 56 mensagens dos Pacotes A e C) e revisões do Codex; (c) os testes rodam um por vez, só numa conversa. Ponto que alivia: o combinado é o 1º piloto **combinado** até 30/11, não **no ar**. Pela própria estimativa de implantação (5 a 7 dias do passo 1 ao 11), o número real da clínica só conecta por volta de 01 a 06/12. O "só fora do horário" precisa estar pronto nesse dia, não em 27/11.
- **Teste mais barato:** hoje, listar o que entra no pacote de 27/11 e marcar o que o piloto precisa no dia em que o número conectar. O resto sai do pacote.
- **Critério de parada:** se até 29/11 o "só fora do horário" e a regra de paciente antigo não passarem no teste, a conexão do número real espera, e o dentista segue testando no número de teste (isso não atrasa o "combinado").
- **Recomendação:** pacote de 27/11 enxuto (fora do horário e paciente antigo); copiloto numa segunda janela, em torno de 03 a 05/12; reconectar ou publicar o Google Agenda antes de 26/11.

### 5. "A clínica do dia a dia tem volume e dor suficientes, e paga o preço da tabela"

- **Por que pode ser verdade:** a Erica acredita que esse dentista é muito mais comum; a dor (mensagem à noite, falta, quem não volta) é real e repetida.
- **Risco se estiver errada:** (a) na semana 1, só fora do horário, uma clínica pequena pode receber poucas mensagens à noite e no fim de semana, e a semana ensina quase nada; (b) a tabela de preço foi pensada com cara de alto valor (Essencial a R$ 590, fundador a R$ 1.500), e esse dentista compara com a Secretária IA da Simples Dental, cerca de R$ 180 (pesquisa de 11/10/2026), e com a IA grátis da Meta.
- **Teste mais barato:** na conversa de 60 min, pedir ao dentista para contar no celular quantas mensagens chegaram nos últimos 7 dias e quantas fora do horário. É o "antes" que o piloto já prevê, só que pedido logo.
- **Critério de parada (estimativa):** menos de 5 conversas novas fora do horário por semana: a semana 1 vira uma etapa curta, e o copiloto entra antes. Na semana 4, se o "bom negócio" do dentista (pergunta 2 de Van Westendorp) ficar abaixo de R$ 590, o Essencial precisa ser revisto antes dos fundadores.
- **Recomendação:** manter o preço como hipótese, mas anotar o volume real desde a semana 0, para cada piloto.

### 6. "O que os conhecidos disserem vale como sinal de mercado"

- **Por que pode ser verdade:** quem conhece fala com franqueza e aceita crítica; é o melhor jeito de achar erros rápido.
- **Risco se estiver errada:** conhecido tende a elogiar e a dizer que pagaria, para não decepcionar. "Quanto pagaria" é opinião, não compra. Com 3 clínicas, as respostas não são estatística (o próprio documento de preço avisa).
- **Teste mais barato:** na semana 4, em vez de só perguntar, oferecer de verdade o mês 2 pago (o experimento 1 do documento de preço) e ver se aceita.
- **Critério de parada:** se nenhum dos pilotos aceitar pagar algo quando a oferta for real, a opinião deles sobre preço não serve para a tabela.
- **Recomendação:** usar os conhecidos para achar erro e entender a rotina (ótimo uso) e validar preço com quem não é conhecido.

### 7. "A Erica dá conta de 3 pilotos e da construção ao mesmo tempo"

- **Por que pode ser verdade:** a estrutura por clínica já existe, e os pilotos 2 e 3 reaproveitam a base do 1º.
- **Risco se estiver errada:** os pilotos 2 e 3 entram na semana 2 do 1º, a mesma semana em que o copiloto estreia e em que a confirmação de consulta (prevista até 15/12) precisa ser construída. Na semana 1, a Keshion lê todas as conversas todo dia. Tudo cai em cima da Erica no mesmo período, junto com o Whapi, pago até 12/12.
- **Teste mais barato:** anotar as horas da semana 0 do piloto 1 (o plano já pede horas por clínica).
- **Critério de parada:** mais de 3 horas por clínica por semana (o alerta do próprio plano): os pilotos 2 e 3 esperam.
- **Recomendação:** o prazo de 15/12 para os pilotos 2 e 3 vale para **combinar**; ligar o número deles só quando o copiloto do piloto 1 estiver estável.

## O que está bem pensado

- **Começar com conhecidos:** acerta o problema do plano de 10/11 ("produto semanas à frente da venda"). Erro aparece rápido e com franqueza.
- **Entrar aos poucos:** fora do horário primeiro é o jeito de menor risco de errar com paciente real. Boa decisão.
- **"Só paga o que está no ar":** protege a confiança e tira a objeção "ainda não está pronto".
- **Protocolo de retorno:** grupo com emojis, 4 perguntas fixas e 🔴 corrigido no mesmo dia é simples e funciona para dentista ocupado.
- **Preço como hipótese:** honesto. O documento de preço já admite que 3 respostas não são estatística.

## O que não consegui avaliar

- O cronograma do Notion: usei só o que veio no pedido (27, 28 e 29/11).
- Se o 1º piloto já está garantido: a conversa com o Dr. William ainda é rascunho.
- Quantas horas por dia a Erica tem de verdade nesta fase.
- O volume real de mensagens de uma clínica do dia a dia: ainda não há nenhum dado.

## As 3 ações mais importantes desta semana

1. **Colocar data no período sem custo.** No convite do 1º piloto (e no roteiro do Sérgio para o Dr. William), escrever até quando é sem custo e o que acontece depois. Junto, decidir de onde vem o 1º pagante até 31/01 (sugestão: indicações dos pilotos e conhecidos de segunda linha a partir de 03/12).
2. **Enxugar o pacote técnico de 27/11.** Só o que o dia da conexão precisa: "só fora do horário" e a regra de paciente antigo. Copiloto em uma segunda janela. Antes de 26/11, reconectar ou publicar o Google Agenda.
3. **Fazer 3 perguntas na conversa de 60 min do 1º piloto:** quem responde o WhatsApp no horário e em quanto tempo consegue aprovar uma resposta; quantas mensagens chegaram nos últimos 7 dias e quantas fora do horário; e se ele aceita a data de fim do período sem custo. As respostas decidem o copiloto, a semana 1 e o pagante.
