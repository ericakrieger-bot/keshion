# Conflitos e duplicatas nos documentos da Keshion

> Gerado em 19/11/2026 a partir do grafo do Graphify (56 arquivos .md e o código do app). Nenhum arquivo foi alterado.
> **Conferido** = li o trecho no arquivo de origem. **Do grafo** = apontado pela leitura automática, ainda não conferido no arquivo.
> Quando digo "vale", é o que o CLAUDE.md, o RETOMAR-AQUI, o guia de marca ou o código dizem hoje. Onde não há como saber, está marcado "decidir".

## 1. Corrigir primeiro (afetam o dia a dia)

| # | Problema | Situação | O que fazer |
|---|---|---|---|
| 1 | ✅ **RESOLVIDO em 19/11/2026.** **Filtro de número nos prompts de teste** | Os prompts `PROMPT-TESTE-18-11-avisos-idioma-hora.md` e `PROMPT-TESTE-18-11-data-em-ingles.md` usavam o prefixo largo `5541999%`. | Trocado para `554199900%` nos dois, igual ao `CLAUDE.md`. |
| 2 | ✅ **RESOLVIDO em 19/11/2026.** **Domínio** | Vale keshion.com. Corrigido em `servidor-n8n.md`, `MIGRACAO-N8N-LEIA-PRIMEIRO.md`, `PROMPT-CODEX-REVISAO.md`, `questionario-clinica.md` e em `quadro/tarefas.json` (o `plano-de-acao.md` foi regerado). `SESSAO` e `comparacao-make-n8n-vps` foram arquivados com o texto antigo. | Nada a fazer. O n8n só muda para `n8n.keshion.com` quando você pedir. |
| 3 | ✅ **FECHADO em 19/11/2026 (decisão da Erica).** **Trava de vaga de 5 min** | Risco mínimo de duas pessoas quererem a mesma vaga em 5 minutos. Saiu da lista de testes (`testes-checklist.md`) e o `LEIA-ME.md` do n8n agora diz 5 minutos. | Nada a fazer. |
| 4 | ✅ **ALINHADO em 19/11/2026.** **Copiloto** | Ele ainda não existe e está no roadmap. Os documentos de venda que o tratavam como pronto foram para `arquivo/`. | Ao vender, falar em "no roadmap". |
| 5 | ✅ **RESOLVIDO nos arquivos em 19/11/2026.** **Lembretes do orçamento: 3, 10, 17 e 30** | Corrigido em `quadro/tarefas.json` (e `plano-de-acao.md` regerado) e em `plano-estrategico-keshion.md`. Os planos antigos foram arquivados já corrigidos. **Falta:** a base da Clara no servidor ainda diz 15 dias e dias 2, 7 e 14. Os relatórios `roteiro-testes-codex.md` e `relatorio-codex-20261117.md` citam isso como foi achado e ficam como histórico. | Levar a base nova para o servidor, com o seu OK (mexe em produção). |

## 2. Decisões que só você pode tomar

| Tema | Os dois lados | Documentos |
|---|---|---|
| **Primeiro cliente pagante** | Até 18/12/2026 contra até 31/01/2027 (18/12 vira só uma conferência de atividade). | Plano de ação, plano do sócio e plano de negócio completo, contra `plano-estrategico-keshion.md` (10/11). Do grafo. |
| **Sociedade** | Erica fundadora única (investidores), Erica e Sérgio com vesting de 4 anos (sócio), sociedade pai e filha meio a meio com acordo de uma página (plano estratégico). | `plano-de-negocio-investidores.md`, `plano-de-negocio-socio.md`, `plano-estrategico-keshion.md`. Do grafo. Convém alinhar antes de mostrar qualquer plano a terceiros. |
| **Captar investimento** | O plano para investidores prevê captar R$ 300 a 500 mil depois de 3 clínicas. O plano estratégico recomenda seguir sem investidores até R$ 100 mil por mês. | Do grafo. |
| **Metas de crescimento** | 30 a 40 clínicas e R$ 70 a 100 mil em out/2028 (investidores e sócio) contra 40 clínicas e R$ 100 mil já em jun/2028 (plano estratégico). 10 clínicas em out/2027 contra set/2027. | Do grafo. O plano estratégico é o mais recente (10/11). |
| **Conexão oficial do WhatsApp** | Os planos de negócio mandam clínicas pagantes para a API oficial. O plano estratégico exige API oficial no 1º trimestre de 2027. O site e o piloto da Vivian ficam em conexão não oficial por ora. | `MATERIAL-COMPLETO.md`, `site/DECISOES.md`, `plano-estrategico-keshion.md`. Do grafo. |
| **Preços da oferta** | Piloto R$ 3.000 a 6.000 de implantação e R$ 1.200 a 2.500 por mês (MATERIAL-COMPLETO) contra fundador R$ 3.000 e R$ 1.500 por 12 meses, preço cheio R$ 6.000 e R$ 2.200 a 2.800 (plano estratégico e plano de ação). | Do grafo. Os valores de fundador batem entre plano de ação e plano estratégico. Falta decidir se o app entra na mensalidade (`site/DECISOES.md`). |
| **Mamãe Planejada** | **Conferido.** O histórico registra o pedido de não citar a Mamãe Planejada nos planos da Keshion, mas `plano-de-negocio-investidores.md` (linha 118) cita. | Tirar ou manter de forma consciente. |
| **Prazo de retorno e parcelamento da avaliação** | A base da demo diz "retornamos em instantes" e "12x" genérico. O prazo real e o parcelamento ainda não foram decididos. | `PLANO-CORRECOES.md` e `roteiro-testes-codex.md`. Do grafo. |
| **Decisão da voz (Ester x OpenAI)** | O bloco de resultado do roteiro está em branco. | `tecnico/teste-voz/roteiro-comparacao-ester-x-openai.md`. Conferido pelo grafo. |
| **Dono do alerta de backup** | Erica ou Sérgio, ainda pendente. | `PASSO-A-PASSO-ERICA-BACKUP.md`. Do grafo. |

## 3. Documentos defasados (a decisão mudou, o texto antigo ficou)

**19/11/2026:** `MATERIAL-COMPLETO`, `SESSAO-2026-11-01-RESUMO`, `comparacao-make-n8n-vps` e os três `plano-de-negocio-*` foram para `arquivo/` com aviso no topo (movidos com `git mv`, ainda sem commit). Links em `historico-e-estrategia.md` e `LEIA-PRIMEIRO.md` atualizados. O `plano-de-acao.md` é gerado pelo `quadro/gerar.py`; os outros pontos da tabela ficam nele e nos documentos técnicos.

Valores que valem hoje, segundo o CLAUDE.md e os arquivos técnicos recentes.

| Tema | Vale hoje | Ainda aparece o antigo em |
|---|---|---|
| IA das respostas | Claude Haiku 5.5 desde 11/11 | `plano-de-acao.md` (tarefa 5: "OpenAI definida"), resumo de 01/11. |
| WhatsApp da demo | Whapi (desde 05/11, cerca de US$ 12 por mês) | `plano-de-acao.md` (tarefa 18), `MATERIAL-COMPLETO.md` (Z-API a R$ 99,99), planos de negócio. |
| Servidor do n8n | Contabo, instalado em 12/11 | Hostinger KVM 2 em `comparacao-make-n8n-vps.md`, no resumo de 01/11 e no plano estratégico (que ainda prevê n8n no 1º trimestre de 2027). |
| Migração para o n8n | Feita em 12/11 com 1 clínica (o gatilho era 3 clínicas) | Plano de negócio completo e `MATERIAL-COMPLETO.md` tratam o n8n como futuro. |
| Piloto da Dra. Vivian | 01/12/2026 | 09/11 em `plano-de-acao.md`, resumo de 01/11 e comparação Make x n8n. 20/11 no `plano-estrategico-keshion.md`. |
| CRM e painel | App Next.js com Netlify e Supabase (decisão de 16/11) | Planilha Google e Looker Studio em `plano-de-acao.md` (tarefa 26), `crm-agenda-painel.md` e `especificacao-sarah.md`. |
| Visual do app | Marca Keshion (17/11) | Estilo Oliva no resumo de 01/11. |
| Nomes das abas do app | Conversas, Painel, Reativar (17/11) | Pendências, Resultados e Retornos (16/11). |
| Regra de reais recuperados | Parado 7 dias ou mais, respondeu à assistente, aceitou em 30 dias (16/11) | `crm-agenda-painel.md` (regra de 01/11). |
| Retenção do backup local | Por idade, 7 dias | A revisão do Codex de 18/11 diz "sete arquivos". O `servidor-n8n.md` mostra que já foi corrigido. |
| Backup externo | O envio ao Drive pelo rclone existe (documentos de 18/11) | O relatório de 17/11 diz que a cópia externa segue sem confirmação. |
| SSH | Só por chave desde 12/11 à tarde | O achado 7 do Codex (12/11) diz root com senha. Já corrigido. |

## 4. Itens menores

- **Alerta de falha do WhatsApp** (`alerta-keshion.json`): o prompt de 17/11 diz que vai só para a Keshion, mas a revisão de 18/11 mostra que usa a mesma credencial Whapi da demo. Ainda depende do WhatsApp. Do grafo.
- **Frases do roteiro de voz** não batem com as regras da clínica: 40 minutos contra cerca de 60, sexta e 14h30 contra avaliação só às terças e quintas em horário cheio. Corrigir antes de gerar os áudios. Do grafo.
- **Notas dos testes** diferem entre rodadas (Bia 9 e 8, Fernanda 9 e 6, Emily 8 e 6). São rodadas com horários e roteiros diferentes, então não é erro, mas não compare sem olhar a data. A rodada de 17/11 aparece com 8 perfis num documento e 15 em outro. Do grafo.
- **"Antes: rodada de 12/11"** aparece nos três relatórios de tom com números diferentes. Na prática é uma cadeia: o "Depois" de um é o "Antes" do próximo. Só o rótulo engana. Do grafo.
- **`relatorio-voz.md`** trata do tom do texto da Clara, não da voz em áudio. O nome confunde com a comparação de voz.
- **Custo por clínica:** R$ 280 a 390 no `MATERIAL-COMPLETO.md` contra média de R$ 435 e faixa de R$ 180 a 590 no plano de negócio completo. Do grafo. Não deu para dizer qual é o certo.
- **Decisão de 09/11 de não migrar** e "desde 12/11 roda no n8n" estão no mesmo documento (`historico-e-estrategia.md`) sem marcar que a primeira ficou para trás.

## 5. Duplicatas

### 5.1 O mesmo assunto em vários planos
Estes arquivos repetem oferta, preços, projeções, concorrentes e diferenciais:
`MATERIAL-COMPLETO.md` (19/10, 53 KB), `plano-de-negocio-investidores.md` (19/10), `plano-de-negocio-completo.md` (20/10), `plano-de-negocio-socio.md` (20/10), `plano-de-acao.md` (29/10, 63 KB), `SESSAO-2026-11-01-RESUMO.md`, `plano-estrategico-keshion.md` (10/11) e `historico-e-estrategia.md`.

Repetições que o grafo achou:
- Oferta de fundador, R$ 3.000 e R$ 1.500 por 12 meses: `plano-de-acao.md` e `plano-estrategico-keshion.md` (valores iguais).
- Mapa de concorrentes: `MATERIAL-COMPLETO.md` e `plano-de-negocio-socio.md`.
- Projeção de 24 meses: `plano-de-negocio-investidores.md` e `plano-de-negocio-socio.md`.
- Cronograma e decisão de 18/12: `plano-de-negocio-completo.md` e `plano-de-acao.md`.
- Avisos à equipe (imediato, 10 min, 30 min): `LEIA-PRIMEIRO.md` e `SESSAO-2026-11-01-RESUMO.md`.
- Painel Looker: `crm-agenda-painel.md` e `plano-de-acao.md`.

**Sugestão (você decide):** manter como fonte `plano-estrategico-keshion.md`, `CLAUDE.md`, `tecnico/RETOMAR-AQUI.md` e `historico-e-estrategia.md`. Os outros cinco planos (`MATERIAL-COMPLETO`, `plano-de-acao`, os três `plano-de-negocio-*`) concentram quase todos os conflitos da seção 3. Poderiam ir para `arquivo/` com uma linha no topo dizendo que estão superados, antes de qualquer reuso para investidor ou sócio. Antes de mover o `plano-de-acao.md`, conferir se o `quadro/tarefas.json` ainda depende dele.

### 5.2 O mesmo texto em três lugares
- **Lembretes do orçamento (3, 10, 17, 30):** `LEIA-PRIMEIRO.md`, `site/DECISOES.md` e `tecnico/PROMPT-CONEXAO-CLARA-APP.md`. Estão iguais hoje, mas se um mudar os outros ficam errados. Ideal: um único lugar com a regra e os outros apontando para ele.
- **Pilha atual e padrões de trabalho:** `CLAUDE.md`, `RETOMAR-AQUI.md` e `historico-e-estrategia.md` dizem a mesma coisa (n8n no Contabo, Haiku, Whapi, testes só na conversa de testes).
- **Decisões do app de 16/11:** `LEIA-PRIMEIRO.md` e `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md`.
- **Limpeza de teste (fichas, mensagens, reservas, agenda):** `PROMPT-RETOMAR-TESTE-19-11.md` e `PROMPT-TESTE-18-11-pacote-a.md`. Poderia ser um passo único em `testes-checklist.md`.

### 5.3 Histórico das revisões do Codex
`PROMPT-CODEX-*`, `revisao-codex-*` e a pasta `codex-18-11/` somam cerca de 15 arquivos. Os achados e as correções estão ligados no grafo. Depois que as correções do `PLANO-CORRECOES.md` estiverem publicadas e testadas, dá para arquivar o conjunto.

## 6. O que este relatório não cobre

- Só os arquivos .md e o código do app. Ficaram de fora os HTML (inclusive `quadro.html`, `guia-tecnico-e-mercado.html`), as imagens, o PDF de paletas, os fluxos .json do n8n e os .sql.
- A pasta `2026-10-19-ia-clinicas-investidores/` e `apresentacoes/` ficaram fora do grafo de propósito. A primeira também cita a Mamãe Planejada.
- A leitura automática pode ter deixado passar números pequenos escondidos em parágrafos longos. Uma lista sem um item não prova que o item não existe.
- Os itens "Do grafo" são candidatos fortes, com trechos específicos citados pelos agentes, mas só os marcados "Conferido" eu abri no arquivo.

**19/11/2026 (limpeza da seção 5):** apagados `MATERIAL-COMPLETO`, os três `plano-de-negocio-*` e `plano-de-acao.md` (cópia gerada; o `gerar.py` não a cria mais, a fonte é `quadro/tarefas.json`). Seguem no histórico do git. `SESSAO-2026-11-01-RESUMO` e `comparacao-make-n8n-vps` ficaram em `arquivo/`, porque o `LEIA-PRIMEIRO` do app ainda aponta para o resumo (estado do Make e concorrentes). Os trechos acima que citam os arquivos apagados são só o registro da análise.
