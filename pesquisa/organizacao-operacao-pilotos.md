# Como organizar a operação dos pilotos (dezembro de 2026)

Pesquisa de 22/11/2026. Recomendação, nada instalado, nenhuma conta criada, nada mudado no Notion.

## A pergunta

Em dezembro a Erica vai cuidar de até 3 clínicas piloto (de 01 a 31/12, com recesso), trabalhando sozinha com os agentes do Claude Code. O Sérgio é sócio, mas não é técnico. Os pagantes começam em janeiro de 2027. Qual estrutura, fora do Claude Code e ligada a ele, segura essa operação sem virar mais uma frente?

## O que a operação de dezembro precisa, de verdade

1. **Uma lista por clínica:** em que semana do piloto ela está, o que liga agora e qual é o próximo passo (seções 3 e 6 da `comercial/piloto/estrutura-piloto-conhecidos.md`).
2. **Uma lista única de retorno da clínica:** cada 🔴 🟡 🟢 💡 do grupo de WhatsApp, com o que foi feito e quando. A estrutura do piloto já diz "tudo anotado numa lista única (Notion)", mas essa lista ainda não existe.
3. **Um jeito fácil de a Erica falar com os agentes** longe do computador (celular, à noite, no recesso).
4. **Algo que o Sérgio abra no celular** e entenda sem ajuda.

Com 3 clínicas, o problema não é volume, e sim **lugar demais e coisa desatualizada**. Toda ferramenta nova é mais um lugar para ficar desatualizado.

## Os caminhos

### A. O que já existe: Notion + daily visual (com 2 bases novas)

- **O que resolve:** o Notion já tem Tarefas, Marcos, Decisões, Funil, Vitórias e os Dailies, já é lido e atualizado pelo PM todo dia e já se conecta ao Claude. Falta só o que é do piloto: uma base **"Pilotos"** (uma linha por clínica: semana, o que está ligado, próximo passo, data da conversa semanal) e uma base **"Retorno do piloto"** (clínica, emoji, o que aconteceu, status, corrigido em). O daily visual com botões continua sendo a porta de entrada da Erica para decidir.
- **Custo:** zero a mais (Notion e Claude já pagos ou grátis).
- **Tempo para montar:** 1 a 2 horas, feito pelo PM com OK da Erica.
- **Risco:** baixo. O risco que existe já é conhecido: o Notion ficar desatualizado. A proposta de 20/11 (varredura completa todo dia) ataca isso.
- **Quanto depende da Erica:** baixo. Ela aprova a criação das bases; o PM e o executor das 14h preenchem. O Sérgio usa o app do Notion no celular, só para ler e marcar.

### B. CRM pronto com MCP (exemplo: Twenty)

- **O que resolve:** o Twenty é um CRM de código aberto com conexão nativa ao Claude Code (MCP, o "plugue" que deixa o Claude ler e escrever nele). Bom para funil de vendas com muitas clínicas, etapas e histórico de contato.
- **Custo:** cerca de US$ 9 por usuário por mês na nuvem (conferir no site antes de qualquer decisão), ou grátis se instalado num servidor próprio, que alguém precisa manter.
- **Tempo para montar:** 1 a 2 dias, mais levar o Funil do Notion para lá.
- **Risco:** médio. Em dezembro não há prospecção (ela volta em 07/01/2027), então o CRM ficaria quase vazio. Vira um segundo lugar para tarefas e clínicas, com o Notion do lado. Instalar no servidor da Clara está fora de questão: é onde ficam os dados das clínicas.
- **Quanto depende da Erica:** médio. Criar conta, migrar, ensinar o Sérgio, decidir o que mora onde.
- **Quando faz sentido:** em janeiro, se o Funil passar de 15 a 20 clínicas em conversa ao mesmo tempo e o Notion começar a atrapalhar. Até lá, não.

### C. Reinstalar o Hermes

- **O que é:** o Hermes Agent (da Nous Research) é um agente de código aberto que roda num servidor e conversa pelo Telegram, WhatsApp, Slack ou e-mail, com memória própria e conexão a MCP. Rodava no servidor da Contabo e foi apagado na reinstalação de novembro (`tecnico/MIGRACAO-N8N-LEIA-PRIMEIRO.md`).
- **O que resolve:** conversar com um agente pelo celular, a qualquer hora, mesmo com o computador desligado.
- **O que ele não resolve:** o Hermes é **outro agente**, não os agentes do Claude Code. Ele não enxerga a pasta do projeto, o PM, os especialistas nem as regras do `CLAUDE.md`, a menos que alguém monte tudo de novo nele. Seriam dois cérebros para manter em dia.
- **Custo:** o programa é grátis, mas precisa de uma chave de IA paga por uso e de um servidor. No servidor da Clara **não recomendo**: um agente com acesso ao terminal no mesmo lugar dos dados das clínicas é risco de segurança e de LGPD. Um servidor separado custa poucos euros por mês.
- **Tempo para montar:** 1 a 3 dias, com instalação, chave, bot do Telegram e testes.
- **Risco:** alto para dezembro. Mexe em servidor, cria contas, gasta dinheiro e abre uma frente técnica nova bem no mês dos pilotos.
- **Quanto depende da Erica:** alto. Ela teria de acompanhar a instalação, guardar as chaves e manter o agente.

### D. Falar com os agentes pelo próprio Claude, no celular

- **O que resolve:** o mesmo item 3 do Hermes, sem servidor. O app do Claude no celular já conversa com as sessões do Claude Code abertas no computador (controle remoto), e existe um canal oficial do Claude Code para o Telegram (ainda em fase de teste da Anthropic). A Erica falaria **com o próprio PM**, que já conhece o projeto.
- **Custo:** zero a mais.
- **Tempo para montar:** 15 a 30 minutos.
- **Risco:** baixo. Limite: o computador precisa estar ligado com o app aberto, o mesmo limite que o daily das 9h e o executor das 14h já têm hoje. O canal do Telegram ainda é recurso em teste: usar só se o controle remoto pelo app não bastar.
- **Quanto depende da Erica:** baixo. Uma configuração, uma vez.

### E. O app próprio (`app-crm-painel/`)

- **O que é:** o app da **clínica** (Conversas, Agenda do dia, Pacientes), não um painel interno da Keshion.
- **Por que não serve para isto:** usar o app para organizar a Keshion tiraria tempo das telas de dezembro, que precisam estar prontas para a semana 3 do piloto 1. Ele entra na operação do jeito certo: as clínicas usam o app, e o que aparecer nele vira linha na base "Retorno do piloto".
- **Custo, tempo, risco:** alto custo de oportunidade. Não recomendo.

## Comparação

| Caminho | Resolve | Custo | Montar | Risco | Depende da Erica |
|---|---|---|---|---|---|
| A. Notion + daily visual + 2 bases | Lista por clínica, retorno, Sérgio no celular | Zero | 1 a 2 h | Baixo | Baixo |
| B. CRM pronto (Twenty) | Funil grande de vendas | Cerca de US$ 9 por usuário/mês | 1 a 2 dias | Médio | Médio |
| C. Hermes | Agente no celular sem PC ligado | Chave de IA + servidor | 1 a 3 dias | Alto | Alto |
| D. Claude no celular | Falar com o PM de qualquer lugar | Zero | 15 a 30 min | Baixo | Baixo |
| E. App próprio | Não é para isto | Tempo do técnico | Semanas | Alto | Alto |

## Recomendação

**Para dezembro: A + D.** Nada de ferramenta nova.

1. **Notion continua sendo o único lugar da gestão**, com 2 bases novas: "Pilotos" e "Retorno do piloto". O PM cria com o OK da Erica e passa a ler as duas no daily.
2. **O daily visual continua sendo a porta da Erica**: ela decide pelos botões, o executor das 14h aplica.
3. **Para falar com os agentes fora do computador:** controle remoto do app do Claude no celular, ligado na conversa fixa do PM.
4. **O Sérgio:** app do Notion no celular (só ler e marcar) e o grupo de WhatsApp de cada piloto.
5. **Hermes e CRM: rever em 05/01/2027**, antes da prospecção voltar. Hermes só se o computador desligado virar problema real em dezembro, e sempre num servidor separado do da Clara. CRM só se o Funil passar de 15 a 20 clínicas em conversa.

**Por quê:** com 3 clínicas, o que falta é disciplina num lugar só, não ferramenta. Cada lugar novo dobra o trabalho de manter as coisas em dia, e a Erica já sente isso hoje.

## Decisões para a Erica

1. Criar no Notion as bases "Pilotos" e "Retorno do piloto"? (recomendação: sim, até 28/11, antes do piloto 1 entrar no ar)
2. Ligar o controle remoto do app do Claude na conversa do PM? (recomendação: sim)
3. Deixar Hermes e CRM para 05/01/2027? (recomendação: sim)

## Fontes

- Hermes Agent, documentação oficial: https://hermes-agent.nousresearch.com/docs
- Twenty, preço: https://twenty.com/pricing e MCP: https://docs.twenty.com/user-guide/ai/capabilities/mcp.md
- Claude Code Channels (Telegram e Discord): https://code.claude.com/docs/en/channels
