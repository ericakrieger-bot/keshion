# Resumo da sessão de 19/10 a 01/11/2026 (Keshion IA)

> Leia este arquivo inteiro antes de continuar o projeto. Ele resume uma conversa longa: decisões, o que já existe, onde está cada coisa e o que falta. O contexto fixo do projeto fica em `negocio-ia-clinicas/CLAUDE.md`; o material de base em `negocio-ia-clinicas/MATERIAL-COMPLETO.md`.

## 1. Quem e o quê

- **Empresa:** Keshion IA (em inglês, Keshion AI). Razão social sugerida: Keshion Tecnologia Ltda. (o contador decide). Domínio: keshion.com.br (domínio e @keshion no Instagram confirmados como livres pela Erica; o INPI não foi consultado porque o site de busca não abre fora do Brasil, e a busca na web não achou marca igual).
- **Sócios:** Erica (produto, textos, montagem com o Claude) e Sérgio (vendas e relacionamento). Os dois moram em Israel e vendem para o Brasil (fuso: Brasil = Israel menos 5 h).
- **Serviço:** atendente de IA no WhatsApp para clínicas odontológicas de alto padrão, vendido como "recuperar orçamentos" (acompanhamento do orçamento formal, agenda, confirmações, retorno de pacientes antigos e relatório de valor recuperado).
- **Clínica piloto real:** Dra. Vivian (sobrenome Ramina). Prazo de implantação do piloto: 09/11/2026.
- **Clínica demo (fictícia), montada como se fosse cliente real:** Dra. Suzana. O Sérgio está criando os dados dela (respostas do questionário).
- **Nomes descartados:** Revive (lotado de clínicas), Cadence (marca registrada), Reaver ("saqueador"), Maane (lido como "Mané"), Kesher e Ezer (preteridos).

## 2. Decisões tomadas nesta sessão

| Tema | Decisão |
|---|---|
| IA | **Só OpenAI** no piloto: escreve as respostas, lê fotos e prints, transcreve áudio (gpt-4o-mini-transcribe). Escolha da Erica por simplicidade. Não reabrir sem ela pedir. Modelo de texto deixado como `gpt-5.4-mini` (confirmar o nome na página de preços da OpenAI). |
| Automação | **Make** no piloto (plano **Core** ativo desde 01/11/2026, conta da Erica, zona eu1). Migrar para **n8n em servidor próprio na Hostinger (KVM 2)** quando chegar a 3 clínicas ou o Make passar de cerca de US$ 50 por mês. n8n Cloud descartado. Comparação em `tecnico/comparacao-make-n8n-vps.md`. |
| Conta do Make | Continua a conta atual (não criar outra). Sugestão: trocar o e-mail de login para o da Keshion ou convidar o e-mail da Keshion e o do Sérgio para a organização; renomear "My Organization" para "Keshion". |
| Jev (TypeSafe AI) | Não usar agora: não gera texto, está em lista de espera, sem português declarado e sem informação de LGPD. Reavaliar depois só para a parte de decisões. |
| Agenda e CRM | **Entram já na primeira versão** (pedido da Erica). Google Agenda + Google Planilhas na conta Google da clínica. |
| Conta Google da clínica demo | **keshion.ai.2026@gmail.com** (grafia com "e", corrigido em 01/11/2026; serve só para a demo; o e-mail oficial da empresa será @keshion.com.br). |
| Autonomia da IA | A IA **responde sozinha** tudo o que está na base da clínica (dúvidas de tratamento, avaliação, endereço, agendar, confirmar, lembretes de orçamento). A equipe só é chamada para: pedido de pessoa, dor ou urgência, reclamação, desconto ou condição especial, pergunta fora da base. Sugestão aceita como opção: 1 semana inicial de segurança com aprovação antes do envio. |
| Linguagem do app | Sem termos de vendedor (nada de "funil", "lead", "etapa", "temperatura"). |
| Estilo visual do app | **Oliva** (creme e verde-oliva). A Erica viu Menta e Lavanda e decidiu manter Oliva. |
| Avisos para a equipe | Aviso imediato no grupo de WhatsApp da clínica a cada pendência; lembrete à recepção após 10 min sem resolução (horário comercial); aviso direto à doutora após 30 min; fora do horário, o paciente recebe o horário de retorno e o aviso sai na abertura. Tempos ajustáveis por clínica. |
| Resultados | Mostrar só o que dá para medir, com a regra de cada número. "Faltas evitadas" não é medível com certeza: mostrar taxa de faltas antes (informada pela clínica) x agora, rotulada como comparação. Remarcações feitas pela IA contam como horários reaproveitados. "Valor recuperado" = fechamentos marcados pela equipe em que o paciente chegou fora do horário, fechou depois de lembrete de orçamento da IA ou voltou por mensagem de retorno. |
| Pacientes antigos | Importação por planilha exportada do sistema da clínica (nome, telefone, último atendimento; recomendados: procedimento, profissional, nascimento). Reativação só com autorização escrita da clínica, no máximo 1 mensagem a cada 90 dias, opção "SAIR", envio em lotes pela API oficial (Z-API em volume = risco de bloqueio). Clínica é controladora, Keshion é operadora (LGPD). |
| Tom da mensagem de retorno | Assinada por uma pessoa da equipe, exemplo aprovado pela Erica: "Olá, Sônia, tudo bem? Aqui é a Erica, da clínica da Dra. Suzana. Vi que já faz um tempo da sua última visita e queria saber se você quer marcar sua revisão. Quer que eu veja os horários livres da doutora?" Se responder sim, a IA oferece horários e marca. Ajustar o tom final quando as respostas da clínica fictícia chegarem. |

## 3. O que já está montado no Make (equipe "My Team", id 3084523, organização 9215132)

| Item | Id | Situação |
|---|---|---|
| Cenário `Keshion · 1A Entrada (WhatsApp)` | 8302405 | Criado, **inativo**. Recebe da Z-API, ignora grupos e mensagens da equipe, separa áudio (baixa e transcreve com OpenAI), foto (OpenAI descreve e lê texto, sem diagnóstico) e texto, e envia para o 1B. |
| Cenário `Keshion · 1B Resposta (IA e modo copiloto)` | 8302452 | Criado, **inativo**. Lê a base da clínica e o histórico no data store, pede a resposta à OpenAI (chat completions em JSON com os campos `resposta`, `acao` e `motivo`), salva a conversa e decide: responder, rascunho para o aprovador, chamar uma pessoa. **Precisa ser ajustado** à decisão de autonomia (responder sozinho no que está na base) e ao CRM. |
| Webhook 1A (vai no campo "Ao receber" da Z-API) | 4016951 | https://hook.eu1.make.com/1mi58p7lag4dr5hlsogrpnaxst78bcjq |
| Webhook 1B (chamado pelo 1A) | 4016952 | https://hook.eu1.make.com/3q8vf1mz9ln224024ott5y71uaq62el8 |
| Data store `Keshion · Conversas e base da clínica` | 240983 | Registro `_base` reservado para a base da clínica (ainda "PREENCHER"). Uma chave por telefone para o histórico. |
| Estruturas de dados | 673054 (Conversa), 673056 (Pedido para a OpenAI), 673057 (Resposta da IA) | |
| Pedido de credenciais OpenAI + Z-API | | https://eu1.make.com/3084523/credentials-requests/inbox?requestId=470b3229-7caa-420b-8e26-8696efda7120 (pendente) |
| Pedido de credenciais Google Agenda + Planilhas (conta demo) | | https://eu1.make.com/3084523/credentials-requests/inbox?requestId=6bc4843d-a573-46b7-846f-0f917b1ce775 (a Erica ia conectar) |
| Plugin `make-skills` (oficial do Make) | | Instalado no escopo do usuário (versão 0.2.0). As 7 skills carregam; a conexão própria do plugin (mcp.make.com) deu erro, mas a conexão do Make já existente funciona. |

Para rodar o Claude Code no PowerShell (não está no PATH): `& "$env:APPDATA\Claude\claude-code\<versão>\<hash>\claude.exe"` (o caminho muda quando o app atualiza).

## 4. Próximos passos da automação (ordem sugerida)

1. **Confirmar as conexões** no Make: OpenAI (chave colada no link, nunca no chat), Z-API (instância do número de demonstração, que é tarefa do Sérgio), Google da clínica demo.
2. **Receber do Sérgio as respostas da clínica fictícia** (questionário) e transformar na base da clínica (registro `_base` do data store e cópia em `clientes/clinica-demo/`). Formato da base: fatos curtos e regras explícitas, 1.500 a 3.000 palavras, 11 partes (identidade, endereço e horários, equipe, tratamentos com regra de preço, avaliação, pagamento, agenda, perguntas frequentes, objeções, tom de voz, quando chamar uma pessoa).
3. **Criar a planilha do CRM** na conta demo a partir de `app-crm-painel/modelo-crm-keshion.xlsx` (abas Contatos, Mensagens, Agenda, Configuração, Pacientes antigos).
4. **Ajustar o 1B:** responder sozinho no que está na base; gravar contato e mensagem na planilha; identificar situação, tratamento, interesse em agendar, horário escolhido e confirmação; abrir pendência para a equipe nos casos da tabela de autonomia.
5. **Cenários novos:** Agenda (oferecer 3 horários livres e marcar), Confirmações (véspera e 2 h antes), Lembretes de orçamento (dias 1, 3, 7, 15 e 30), Avisos para a equipe (grupo de WhatsApp com lembrete em 10 e 30 min), Retornos (pacientes antigos), Resumo do dia para a doutora, Alarme de falha.
6. **Número do aprovador / grupo da equipe:** a Erica ainda não informou. No módulo "Ajustes" do 1B, o campo está como `PREENCHER_NUMERO_DE_QUEM_APROVA`.
7. **Testar** com texto, áudio e foto no número de demonstração; depois ativar os cenários.
8. **App do CRM:** escolher entre AppSheet e Glide (ainda não comparados) e montar sobre a planilha seguindo o protótipo.

## 5. Protótipo do app (CRM para celular) e painel

- **Protótipo navegável, versão 3:** https://claude.ai/artifact/5VeB6X6CdH4xaNmsg7a7Sr (arquivo `app-crm-painel/prototipo-crm-mobile.html`). A Erica aprovou o visual Oliva ("ficou ótimo") e disse que ainda tem alterações a fazer depois.
- **Abas:** Pendências (só o que precisa de pessoa: responder agora, decidir desconto, "responder e ensinar a IA", avaliações de hoje e amanhã, resumo do que a IA resolveu), Conversas (caixa de entrada com selos e "Assumir conversa" / "Devolver para a IA"), Pacientes (CRM com novos contatos e já pacientes, situações em linguagem de recepção, ficha editável com tratamento, sessões, valor, pagamento, anotações da equipe e histórico; anotação clínica fica no prontuário da clínica, não aqui), Retornos (pacientes antigos, mensagem assinada pela equipe), Resultados (medido pelo sistema x depende da equipe marcar).
- **Situações do paciente:** Novo contato, Em conversa, Avaliação marcada, Avaliou aguardando orçamento, Orçamento em aberto, Em tratamento, Tratamento concluído, Não fechou (pede o motivo).
- **Prévia antiga do painel (dados fictícios):** https://claude.ai/artifact/PTMcbDMS6ZhU4CibshYiGS (`app-crm-painel/previa-painel.html`). O painel real será no Looker Studio lendo a mesma planilha; a aba Resultados do app resume.
- **Desenho técnico do CRM, agenda e painel:** `app-crm-painel/crm-agenda-painel.md` (inclui regras de UX para o app real e a estrutura de dados).

## 6. Concorrentes analisados nesta sessão

| | Preço | Destaques | O que não têm |
|---|---|---|---|
| AtendeJá (atendeja.ia.br) | R$ 447 a 897/mês (fundador R$ 347 a 697), setup R$ 497, fidelidade 3 meses (12 no fundador) | Mesmo número, Google Agenda, confirmação 24 h e 2 h, reativação 30/60/90 dias, "pacientes quentes", "receita resgatada", sinal por Pix | Orçamento formal, cálculo explicado, aprovação antes do envio, prova social |
| Secretária Odonto (secretariaodonto.com.br) | R$ 297 a 997/mês + setup não informado, "sem fidelidade", teste de 7 dias | Multiagenda, áudio de ida e volta, ligações (plano alto), PDFs, comandos do gestor pelo WhatsApp, painel de conversas | Orçamento formal, valor recuperado, prova social real |
| Secretária IA (usesecretariaia.com) | Essencial R$ 397,90/mês (trimestral), Profissional sob consulta, 3 dias grátis, 7 dias de garantia | Médico e odonto, "anti-alucinação", tom customizado, CRM nativo e dashboard (sem telas), integrações (Clinicorp, Dental Office, Feegow, Kommo), diz ter 300 consultórios | Orçamento formal, aprovação, reativação, importação de base, LGPD detalhada |

Espaço livre confirmado para a Keshion IA: acompanhamento do orçamento formal, valor recuperado com regra explícita, autonomia com limites claros e avisos com escalonamento, tom de alto padrão por clínica, prova real (o caso da Dra. Vivian).

## 7. Outros entregáveis desta sessão (para achar depois)

- Plano de negócio para o sócio: `plano-de-negocio-socio.md` e completo: `plano-de-negocio-completo.md`; apresentações em `apresentacoes/` (PDF e PPTX).
- Quadro de tarefas compartilhado: https://claude.ai/artifact/3yH8An411hpGMSRTwmujsC (fonte `quadro/tarefas.json` → `quadro/gerar.py` gera `plano-de-acao.md` e `quadro/quadro.html`; edições feitas no quadro ficam no banco do artifact, coleção `tarefas`, e status na coleção `status`). Tarefas já marcadas como feitas: reunião de alinhamento, nome da empresa, decisão da IA (OpenAI). Domínio em andamento com o Sérgio.
- Questionário da clínica (modelo, endereçado à Dra. Suzana): `clientes/clinica-demo/Questionario-Keshion-Dra-Suzana.docx` e `.md` (74 perguntas, 15 seções). Para a Dra. Vivian, trocar o nome antes de enviar.
- Modelo da planilha do CRM: `app-crm-painel/modelo-crm-keshion.xlsx`.

## 8. Ideia futura da Erica

Criar um "segundo cérebro" com todos os projetos profissionais e pessoais (no GitHub ou em outra plataforma). Este resumo já está no formato de nota autossuficiente para entrar nele.
