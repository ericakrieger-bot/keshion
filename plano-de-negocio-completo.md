# Plano de negócio completo: atendente de IA para clínicas odontológicas de alto padrão

> Versão 1, 20/10/2026. Complementa o plano para o sócio (`plano-de-negocio-socio.md`), que traz mercado, concorrentes, diferenciais e estrutura societária.
> Este documento detalha custos, ferramentas, como o produto é montado, cronograma e o passo a passo de operação.
> Preços de ferramentas de outubro de 2026, com dólar a cerca de R$ 5,60 e euro a cerca de R$ 6,20. Confira antes de contratar.

---

## 1. Resumo

| Item | Definição |
|---|---|
| Produto | Implantação e operação de atendente de IA no WhatsApp para clínicas odontológicas de alto padrão |
| Promessa | Recuperar os orçamentos que a clínica deixa esfriar e medir isso em reais |
| Cliente | Clínica independente, 2 cadeiras ou mais, anúncio no Instagram, tratamentos acima de R$ 5 mil |
| Preço | Implantação de R$ 3 a 12 mil + mensalidade de R$ 1,2 a 3,5 mil |
| Custo direto | R$ 180 a 590 por clínica por mês, conforme o caminho do número |
| Operação | 100% remota |
| Meta de 12 meses | 10 clínicas, cerca de R$ 18 a 20 mil de receita recorrente por mês |

## 2. Ferramentas

### 2.1 Do produto

| Ferramenta | Para quê | Custo |
|---|---|---|
| **Make** (plano Core) | Automação: roda os 6 cenários do atendimento | US$ 10,59/mês (cerca de R$ 60) + créditos por clínica |
| **Claude API** (Anthropic) | IA que escreve as respostas. Modelo rápido (Haiku) na maioria; modelo maior (Sonnet) em casos difíceis e resumos | Por uso, com limite mensal no console |
| **Transcrição de áudio** (OpenAI) | Converte áudio do paciente em texto | Centavos por minuto |
| **WhatsApp: Z-API** | Conexão com o WhatsApp sem API oficial. Só no número de demonstração | R$ 99,99/mês por número (R$ 89,99 a partir de 10) |
| **WhatsApp: API oficial da Meta** | Conexão autorizada para as clínicas, com número novo | R$ 0 + mensagens no cartão da clínica |
| **WhatsApp: parceiro de coexistência** (ex.: 360dialog) | API oficial no mesmo número que a clínica já usa | A partir de € 49/mês por número (cerca de R$ 300) |
| **Google Agenda e Planilhas** | Agenda da clínica, contatos e orçamentos | Grátis |
| **Chatwoot** | Painel onde a equipe da clínica vê as conversas. Entra a partir de 3 clínicas | Grátis em servidor próprio (R$ 40 a 80/mês para todas) ou US$ 19 por atendente na nuvem |

### 2.2 Da empresa

| Para quê | Ferramenta | Custo |
|---|---|---|
| Construção técnica | Claude Code | Assinatura já existente |
| Achar clínicas | Apify, Biblioteca de Anúncios da Meta, Google Maps | Apify por uso (centavos por coleta) |
| Reuniões | Google Meet + Cal.com ou Calendly | Grátis para começar |
| Notas de reunião | Granola | Conforme plano |
| Propostas e diagnósticos | Páginas publicadas, Gamma ou Lovable | Conforme plano |
| Contrato | gov.br, Autentique, Clicksign ou D4Sign | gov.br grátis |
| Cobrança recorrente | Asaas ou similar | Taxa por cobrança |
| Empresa | CNPJ no Simples Nacional (provavelmente ME) + contabilidade digital | R$ 100 a 300/mês |
| Senhas e acessos | Bitwarden | Grátis |
| Treinar secretárias | Loom | Grátis para começar |
| Organizar clientes | Notion ou Google Drive (sem dado de paciente) | Grátis |
| Relatório visual | Looker Studio ou página publicada | Grátis |
| Domínio e e-mail | Registro.br + e-mail profissional | Cerca de R$ 40/ano + e-mail |

## 3. Custos

### 3.1 Antes do primeiro cliente (por mês)

| Item | Custo |
|---|---|
| Make Core | cerca de R$ 60 |
| Z-API (número de demonstração) | R$ 99,99 |
| Claude API (testes, com limite) | R$ 30 a 60 |
| Chip de demonstração (Vivo Lite com eSIM) | R$ 30 |
| Domínio | cerca de R$ 3,50 (R$ 40/ano) |
| **Subtotal sem empresa** | **cerca de R$ 225 a 255** |
| Empresa e contador (quando o primeiro cliente estiver perto de fechar) | R$ 100 a 300 |
| **Total com empresa** | **cerca de R$ 325 a 555** |

### 3.2 Investimento inicial (uma vez)

| Item | Custo |
|---|---|
| Créditos iniciais do Claude | cerca de US$ 5 a 10 |
| Abertura de CNPJ | R$ 0 a 1.000, conforme o contador |
| Contrato-base revisado por advogado, com anexo de LGPD | R$ 1.000 a 3.000 (estimativa) |
| Saldo de roaming para ativar o número | R$ 20 |
| **Total estimado** | **R$ 1.100 a 4.100** |

### 3.3 Custo por clínica (por mês)

**Caminho A (Z-API no número da clínica, só com aceite de risco por escrito)**

| Item | Cálculo | Custo |
|---|---|---|
| Z-API | 1 número por clínica | R$ 99,99 |
| Créditos do Make | cerca de 2.000 mensagens × 9 créditos + 2.000 das rotinas = 20 mil créditos | R$ 110 a 170 |
| Claude API | cerca de 2.000 respostas + casos difíceis e resumos | R$ 60 a 110 |
| Transcrição | cerca de 300 áudios curtos | cerca de R$ 5 |
| **Total** | | **R$ 280 a 390** |

| Caminho | Como fica para a clínica | Custo por clínica/mês |
|---|---|---|
| A. Z-API no número | Mesmo número; risco de bloqueio sem aviso | R$ 280 a 390 |
| B. API oficial, número novo (padrão) | Número só para o atendimento | R$ 180 a 290 + mensagens da Meta no cartão da clínica |
| C. API oficial no mesmo número | Mesmo número, via parceiro autorizado | R$ 480 a 590 + mensagens da Meta no cartão da clínica |

O custo do caminho C é repassado no preço. Para o cálculo de margem, usamos a média de R$ 435.

### 3.4 Custos fixos com operação rodando

| Item | Até 3 clínicas | 10 clínicas |
|---|---|---|
| Make Core (base) | R$ 60 | R$ 60 |
| Contador | R$ 200 | R$ 300 |
| Servidor do Chatwoot | R$ 0 | R$ 80 |
| Ferramentas de venda e gestão | R$ 100 | R$ 200 |
| Z-API da demonstração | R$ 100 | R$ 100 |
| **Total fixo** | **cerca de R$ 460** | **cerca de R$ 740** |

Comissão de SDR (a partir da 2ª clínica): [preencher percentual] sobre a implantação. Operadora de implantação no Brasil (a partir de cerca de 5 a 10 clínicas): [preencher salário ou valor por clínica].

## 4. Resultado projetado (cenário base)

Premissas: mensalidade média de R$ 1.800, implantação média de R$ 4.000, custo direto de R$ 435 por clínica, sem cancelamentos no período. Antes de impostos.

| Mês | Clínicas | Receita recorrente | Implantações no mês | Custo direto | Custo fixo | Resultado do mês |
|---|---|---|---|---|---|---|
| Dez/2026 | 1 | R$ 1.800 | R$ 4.000 | R$ 435 | R$ 460 | R$ 4.905 |
| Mar/2027 | 3 | R$ 5.400 | R$ 4.000 | R$ 1.305 | R$ 460 | R$ 7.635 |
| Jun/2027 | 5 | R$ 9.000 | R$ 4.000 | R$ 2.175 | R$ 600 | R$ 10.225 |
| Out/2027 | 10 | R$ 18.000 | R$ 8.000 | R$ 4.350 | R$ 740 | R$ 20.910 |

Nos meses de implantação, os pilotos de fundador podem ter preço menor. A partir de cerca de 5 clínicas, entra o custo de uma operadora de implantação, que reduz o resultado mas libera horas dos sócios para vender. [preencher com números reais a cada mês]

## 5. Como o produto funciona

### 5.1 Caminho de uma mensagem

Paciente → WhatsApp → conexão (Z-API ou API oficial) → **Make** (lê a regra da clínica, o histórico e a agenda) → **Claude** (escreve a resposta no tom da clínica) → saída:

- **Fora do horário:** responde sozinho, agenda a avaliação e registra o contato na planilha.
- **No horário (copiloto):** manda o rascunho para a secretária no grupo interno; ela confere e envia.
- **Caso delicado** (dor, reclamação, pergunta clínica, paciente pedindo pessoa): avisa a equipe e não responde sozinho.

### 5.2 Os 6 cenários de automação

| Cenário | Quando roda | O que faz |
|---|---|---|
| 1. Atendimento | A cada mensagem | Ignora grupos e mensagens da equipe, transcreve áudio, busca histórico, pede a resposta ao Claude e decide entre responder, mandar rascunho ou chamar uma pessoa |
| 2. Agenda | Quando o paciente aceita horário | Consulta horários livres e marca no Google Agenda |
| 3. Confirmações | Todo fim de tarde | Confirma as avaliações do dia seguinte e remarca quem não pode |
| 4. Acompanhamento do orçamento | Toda manhã | Procura orçamentos em aberto e manda a mensagem do dia certo (1, 3, 7, 15, 30) |
| 5. Relatório | Toda semana e todo mês | Conta contatos, avaliações, faltas evitadas e orçamentos recuperados em reais |
| 6. Alarme | Quando algo falha | Avisa a equipe no WhatsApp |

**Primeira versão sem servidor:** histórico no Make, contatos e orçamentos numa planilha do Google, agenda no Google Agenda.

**Versão de escala:** um conjunto único de cenários que lê a configuração de cada clínica (corrigiu uma vez, vale para todas), Chatwoot como painel e, quando o volume justificar, migração para n8n + Postgres + Metabase num servidor próprio (2 vCPU e 8 GB, R$ 33 a 80/mês).

### 5.3 O que cada clínica recebe na implantação

| Peça | Conteúdo |
|---|---|
| Base da clínica | Endereço, horários, profissionais, tratamentos, política de preço autorizada, avaliação, formas de pagamento, diferenciais reais, perguntas frequentes |
| Manual de voz | Tom, tratamento do paciente, palavras que usa e proibidas, como responder "quanto custa" e "vou pensar", 10 a 20 respostas modelo aprovadas |
| Regras que a IA nunca quebra | Sem orientação clínica, sem preço não autorizado, sem promessa de resultado, avisa que é atendimento automático quando perguntada |
| Quando chamar uma pessoa | Dor, urgência, reclamação, pergunta clínica, pedido de pessoa, negociação fora da política |
| Jornada do orçamento | Mensagens dos dias 1, 3, 7, 15 e 30, escritas por tipo de tratamento e aprovadas |
| Relatório mensal | Contatos, tempo de resposta, avaliações, comparecimento, faltas evitadas, orçamentos acompanhados e fechados, reais recuperados |

## 6. Estrutura da empresa

### 6.1 Áreas e responsáveis

| Área | O que inclui | Responsável |
|---|---|---|
| Produto e tecnologia | Cenários, IA, integrações, manutenção, alarmes | A definir |
| Texto e qualidade | Base da clínica, manual de voz, jornada do orçamento, revisão semanal | A definir |
| Vendas | Prospecção, cliente oculto, diagnóstico, reunião, proposta, contrato | A definir |
| Implantação | Levantamento, conexão do número, treino da secretária, 2 semanas de copiloto | A definir |
| Relacionamento | Gerente de conta, reunião mensal, relatório, pedido de indicação | A definir |
| Administrativo | Empresa, cobrança, notas, contratos, LGPD | A definir + contador |

### 6.2 Quem a empresa nunca substitui

- A clínica aprova todo texto que vai para paciente.
- A clínica é dona dos dados e da conta do WhatsApp; nós recebemos acesso de administrador, nunca a senha.
- Nenhum cenário que fala com paciente é ligado sem aprovação escrita da clínica.

### 6.3 Regras de segurança

- Chaves e senhas só no gerenciador de senhas e nas conexões das próprias ferramentas.
- Nenhum dado de paciente em pasta da empresa; só dados de teste.
- Contrato com a clínica como operadora de dados, informando que as mensagens passam pela conexão de WhatsApp (Brasil), pelo Make (Europa) e pela Anthropic (Estados Unidos).
- A clínica de demonstração é sempre apresentada como demonstração.

## 7. Cronograma

| Fase | Período | Objetivo | Entregável |
|---|---|---|---|
| 0. Contas e chaves | Semana 1 (out/2026) | Ter as ferramentas prontas | Número de demonstração ativo, chave do Claude no Make, Make no plano Core |
| 1. Demonstração | Semanas 2 e 3 | Uma clínica de demonstração respondendo no tom de alto padrão | Base e manual de voz da demonstração, cenários 1 a 6, 30 testes aprovados |
| 2. Venda | Semanas 3 a 8, em paralelo | Fechar as primeiras clínicas | 100 clínicas listadas, 50 conversas, 10 ofertas de piloto, 1 a 2 contratos |
| 3. Primeira clínica | 4 a 5 semanas por clínica | Implantar e provar resultado | Clínica em copiloto, relatório de 30 dias com reais recuperados |
| Decisão | 18/12/2026 | Seguir ou parar | Com 1 clínica pagante ou mais, seguimos |
| 4. Padronizar | Jan a mar/2027 | Chegar a 3 clínicas e documentar tudo | Implantação gravada, checklist por clínica, primeiros cases |
| 5. Escalar | Abr/2027 em diante | 10 a 20 clínicas | Conjunto único de cenários, Chatwoot, API oficial em todas, primeira contratação |

## 8. Passo a passo

### 8.1 Montar a demonstração

1. Criar a conta no console da Anthropic, comprar o mínimo de créditos, colocar limite mensal (ex.: US$ 10) e criar a chave `atendente-demo`.
2. Guardar a chave nas conexões do Make. Nunca mandar por chat.
3. Conseguir o número de demonstração (Vivo Lite com eSIM ou outro número só para isso) e ativar o WhatsApp Business nele, com verificação em duas etapas.
4. Escrever a base da clínica de demonstração e o manual de voz do alto padrão.
5. Montar no Make os cenários 1 (Atendimento) e 2 (Agenda) e testar com conversas simuladas.
6. Conectar o número na Z-API (só nesse momento, porque o teste grátis dura 2 dias).
7. Rodar o roteiro de 30 testes em 6 blocos: entrada, agenda, objeções, casos delicados, orçamento e limites.
8. Corrigir pelos registros de execução do Make e ajustar o texto.
9. Montar os cenários 3 a 6 e as mensagens da jornada do orçamento.
10. Aprovar a demonstração final: um dono manda mensagem e vê a resposta em segundos.

### 8.2 Achar e abordar clínicas

1. Listar clínicas que anunciam lentes, alinhadores e implantes agora (Biblioteca de Anúncios da Meta), com Instagram ativo e boa nota no Google Maps. Começar por capitais e cidades médias ricas.
2. Fazer cliente oculto: mandar mensagem como paciente interessado em tratamento caro, em horários variados, e anotar tempo de resposta, o que respondeu, se ofereceu avaliação e se voltou a procurar em 1, 3 e 7 dias. Nunca marcar avaliação que não será cumprida.
3. Transformar o resultado numa página de diagnóstico com prints, tempos e o que a clínica deixou escapar.
4. Enviar ao dono pelo Instagram, WhatsApp ou e-mail, com convite para 30 minutos por vídeo.

### 8.3 Reunião de 30 minutos

1. Mostrar o diagnóstico (5 min).
2. Perguntar os números: contatos por mês, quem responde e em quanto tempo, avaliações e faltas, valor médio de orçamento, orçamentos em aberto, verba de anúncio (10 min).
3. Calcular o prejuízo junto, com a calculadora (contatos perdidos + orçamentos que esfriam).
4. Demonstração ao vivo: o dono manda mensagem para o número de demonstração (5 min).
5. Proposta: implantação, mensalidade, garantia, preço de fundador (10 min).

### 8.4 Fechar

1. Proposta em página.
2. Contrato-base com: escopo, prazo de implantação, mensalidade e reajuste, garantia de 30 dias e meta de 60 dias, quem paga as mensagens da Meta, responsabilidade pelas informações da base, proteção de dados, propriedade dos dados (da clínica), cancelamento e devolução de acessos.
3. Assinatura eletrônica.
4. Cobrança recorrente por Pix, boleto ou cartão.

### 8.5 Implantar (4 a 5 semanas)

1. Chamada de levantamento gravada com dono e secretária, com o questionário completo.
2. Acompanhar por tela compartilhada o dono conectando o número (verificação na Meta ou QR code).
3. Copiar os cenários para a clínica, ligar na agenda dela, carregar base e manual de voz.
4. Treinar a secretária por vídeo (30 minutos) e deixar vídeos curtos gravados.
5. Duas semanas em modo copiloto, revisando os rascunhos todo dia.
6. Liberar a resposta automática fora do horário, com aprovação do dono.
7. Entregar o relatório de 30 dias com reais recuperados.

### 8.6 Reter e crescer

1. Relatório mensal com reais recuperados.
2. Reunião mensal de 30 minutos com o dono.
3. Pedir indicação depois do primeiro relatório bom.
4. Transformar resultados em cases, com autorização.
5. Subir o preço para novos clientes depois de 3 cases.
6. Usar o próprio atendente como vitrine no WhatsApp comercial da empresa.

## 9. Rotina semanal com clientes rodando

| Quando | O quê | Tempo |
|---|---|---|
| Todo dia | Alarmes e conversas marcadas para pessoa | 15 min |
| Segunda | Prospecção: 5 clientes ocultos e 5 diagnósticos enviados | 2 h |
| Terça e quarta | Reuniões de venda e de implantação | 3 a 4 h |
| Quinta | Revisão das conversas de cada clínica | 20 a 30 min por clínica |
| Sexta | Relatórios, melhorias e conteúdo para o Instagram da empresa | 2 h |
| Uma vez por mês | Reunião com o dono de cada clínica | 30 min por clínica |

Com 10 clínicas: cerca de 10 a 15 horas por semana de operação, além das horas de venda.

## 10. Indicadores

| Indicador | Meta inicial |
|---|---|
| Conversas com clínicas por semana | [preencher] |
| Pilotos oferecidos por mês | 10 |
| Taxa de fechamento | [medir] |
| Tempo médio de primeira resposta na clínica | Menos de 1 minuto |
| Comparecimento às avaliações | [medir antes e depois] |
| Reais recuperados por clínica/mês | Acima de 10 vezes a mensalidade |
| Cancelamento mensal | Perto de zero |
| Horas de operação por clínica/semana | [medir nas 4 primeiras semanas] |

## 11. Riscos operacionais

| Risco | Como evitar |
|---|---|
| Bloqueio do número | Só responder quem escreveu, nada de disparo em massa; Z-API só na demonstração; caminho B ou C nas clínicas |
| Dado de saúde | Contrato de operadora, mínimo necessário, nada de prontuário, apagar histórico antigo |
| Créditos do Make estourando | Alarme de consumo e revisão mensal por clínica |
| Gasto da IA | Limite mensal no console, modelo rápido na maioria das respostas |
| Erro de informação | Só preço autorizado, nada de orientação clínica, chamar pessoa na dúvida |
| Dependência de uma pessoa | Base, manual de voz e checklist documentados por clínica |
| Regras do CFO | Só preço autorizado por escrito; harmonização apenas como extra |

---
Base: `negocio-ia-clinicas/MATERIAL-COMPLETO.md` (19/10/2026) e `negocio-ia-clinicas/tecnico/plano-make-zapi.html`.
