# Diagnóstico de organização da Keshion (22/11/2026)

> Fase 1: só leitura. Nada foi movido, apagado ou editado (fora este arquivo).
> Base: varredura das pastas `keshion/`, `keshion-wt-copiloto/` e `keshion-wt-retomar/`, git local, e os arquivos `conflitos-e-duplicatas.md` (19/11) e `INVENTARIO-MATERIAIS.md` (22/11), que já existiam.
> Cada item tem uma sugestão. Nada acontece sem o seu OK.

## Resumo em 5 linhas

1. **O mais importante:** o agente PM ainda trabalha com a meta "piloto da Dra. Vivian em 01/12", que foi suspenso em 20/11. Por isso o daily das 9h pode estar contando dias para um marco que não existe mais.
2. Pelo menos **8 documentos ativos** ainda tratam o piloto da Vivian como se estivesse de pé (app, roadmap, quadro, site, histórico, RETOMAR-AQUI).
3. A pasta é pequena (cerca de 23 MB de conteúdo). O peso maior é técnico e se refaz sozinho: `node_modules` (410 MB) e `.next` (164 MB) do app.
4. Quase não há arquivos duplicados de verdade. O excesso está em **histórico de testes e revisões do Codex**: cerca de 45 arquivos de 16 a 20/11.
5. As duas pastas `keshion-wt-*` **não são cópias velhas**, ao contrário do que diz o inventário. São áreas de trabalho do git com alterações ainda não juntadas na `main`. Não apagar antes de resolver.

---

## 1. Arquivos duplicados

| Grupo | Onde | Sugestão |
|---|---|---|
| PDF do piloto v2 igual em 2 lugares | `comercial/piloto/keshion-piloto-clinicas-v2.pdf` e `comercial/sergio/materiais/02-piloto-keshion-para-clinicas.pdf` | Manter os dois **se** a pasta do Sérgio é o "pacote para enviar". Senão, deixar só um. Risco: atualizar um e esquecer o outro. |
| Ícones, favicon e fontes (8 arquivos) | `branding/kit/` e `app/web/` | **Manter.** O app precisa da própria cópia para funcionar. Não é bagunça. |
| Cache do Graphify (34 arquivos iguais) | `graphify-out/cache/` | Ignorar: é cache automático, fora do git. |
| Fotos do Graphify por dia | `graphify-out/2026-11-20/` e `2026-11-21/` | Podem ser apagadas. O grafo atual fica na raiz de `graphify-out/` e é refeito com `graphify update`. |

Quase duplicados por nome (versões):

| Arquivos | Qual vale | Sugestão |
|---|---|---|
| `site/copy-v2.html`, `copy-v3.html`, `proposta-estrutura-e-copy.html` | v3 (mais recente) | Mover v2 e a proposta antiga para `arquivo/`. |
| `site/design-v1.html` e `design-v1-visualizar.html` | Os dois (um é a página, o outro a forma de ver) | Manter. |
| `material-piloto.html` e `keshion-piloto-clinicas.pdf` (v1) | v2 | Já foram movidos para `arquivo/` hoje, mas **sem commit**. |

## 2. Informação duplicada dentro dos documentos

| Assunto | Repetido em | Fonte oficial sugerida |
|---|---|---|
| Pilha atual (n8n no Contabo, Haiku, Whapi, regra de testes) | `CLAUDE.md`, `tecnico/RETOMAR-AQUI.md`, `historico-e-estrategia.md` | `CLAUDE.md`. Os outros dois só apontam para ele. |
| Lembretes do orçamento (3, 10, 17 e 30 dias) | `app-crm-painel/LEIA-PRIMEIRO.md`, `site/DECISOES.md`, `tecnico/PROMPT-CONEXAO-CLARA-APP.md` | Um lugar só (sugiro `clientes/clinica-demo/base-clinica.md`). Os outros apontam para lá. |
| Decisões do app de 16/11 | `app-crm-painel/LEIA-PRIMEIRO.md` e `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md` | `LEIA-PRIMEIRO.md`. O resumo vai para `arquivo/`. |
| Roadmap | `roadmap/roadmap-etapas.html`, `roadmap/roadmap-visual.html`, `quadro/quadro.html` + `tarefas.json`, Notion (Marcos) | Definir **um**. Pela regra do PM, gestão fica no Notion. Os três HTML viram histórico. |
| Limpeza de dados de teste | `PROMPT-RETOMAR-TESTE-19-11.md` e `PROMPT-TESTE-18-11-pacote-a.md` | Um passo único em `tecnico/testes-checklist.md`. |
| Inventário e conflitos | `INVENTARIO-MATERIAIS.md`, `conflitos-e-duplicatas.md` e este diagnóstico | Depois da fase 2, juntar tudo em um só (ou arquivar os dois antigos). |

## 3. Informação desatualizada ou conflitante

### 3.1 Piloto da Dra. Vivian (suspenso em 20/11) ainda tratado como ativo 🔴

| Arquivo | O que diz hoje | Sugestão |
|---|---|---|
| `.claude/agents/project-manager.md` (linhas 8 e 68) | "meta atual: piloto da Dra. Vivian em 01/12/2026" | Trocar pela meta do `estrategia.md`: 1º piloto com clínica conhecida até 30/11, 2º e 3º até 15/12, pagante até 31/01/2027. **Mais urgente**, porque alimenta o daily. |
| `.claude/agents/vendas.md` (linha 21) | "Piloto: `clientes/dra-vivian/`" | Apontar para `comercial/piloto/`. |
| `app-crm-painel/LEIA-PRIMEIRO.md` (linhas 11 e 123) e `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md` | Piloto real com a Vivian a partir de 01/12 | Atualizar para os pilotos com clínicas conhecidas. |
| `tecnico/RETOMAR-AQUI.md` (atualizado em 18/11) | "Antes do piloto da Dra. Vivian (01/12/2026)" e a lista de pendências dela | Atualizar a data e a lista. É o ponto de partida técnico de toda conversa. |
| `historico-e-estrategia.md` (linha 52) | "Início previsto: 01/12/2026" | Acrescentar "suspenso em 20/11". |
| `plano-estrategico-keshion.md` (linhas 63 e 91) | "já rodando na Dra. Vivian" e "case com números da Dra. Vivian" | Trocar por "1º piloto". |
| `roadmap/*.html`, `quadro/*` | Contagem para 01/12 e marco "até 09/11" | Arquivar (ver seção 2) ou atualizar. |
| `site/copy-v3.html` (linha 85) | "Até 01/12 (piloto): base, voz e conexão da Dra. Vivian" | Corrigir antes de publicar o site. |
| `clientes/dra-vivian/` (6 arquivos) | Material do piloto | Mover para `arquivo/dra-vivian-suspenso-2026-11-20/`, se o piloto não volta. Se pode voltar, deixar como está, com um LEIA-ME de uma linha dizendo "suspenso". |

### 3.2 Outros pontos desatualizados

| Tema | Situação | Sugestão |
|---|---|---|
| `CLAUDE.md`: "Estado técnico (17/11/2026)" | Data velha no título | Atualizar quando o RETOMAR-AQUI for atualizado. |
| `INVENTARIO-MATERIAIS.md`, observação 1 | Chama as pastas `wt-*` de "cópias antigas" | Corrigir (ver seção 4.1). |
| `conflitos-e-duplicatas.md` | Metade resolvida. Cita arquivos que já foram apagados. | Ainda abertos: base da Clara no servidor com 15 dias e dias 2, 7 e 14 (precisa do seu OK, porque mexe em produção), voz Ester x OpenAI, dono do alerta de backup, Mamãe Planejada. Levar os abertos para o Notion (Decisões) e arquivar o arquivo. |
| `historico-e-estrategia.md` | A decisão de 09/11 de não migrar e o "roda no n8n desde 12/11" aparecem juntos | Marcar a de 09/11 como superada. |
| `tecnico/make-cenarios/` e `tecnico/plano-make-zapi.html` | Make desativado | Mover para `arquivo/make/`. |
| `tecnico/especificacao-sarah.md` | Usa o nome antigo (Sarah, agora Clara) e a planilha Google como CRM | Marcar no topo como histórico, ou arquivar. |
| `resumo-sessao-sarah-2026-11-09.md` (raiz) | Resumo de sessão antigo solto na raiz | `arquivo/`. |
| `apresentacoes/plano-completo` e `plano-socio` (.pdf e .pptx, 20/10) | Feitos a partir dos planos de negócio que já foram apagados por estarem desatualizados | `arquivo/`, com aviso para não enviar a ninguém. |
| `2026-10-19-ia-clinicas-investidores/` | Debate de 19/10 sobre captar investimento. Cita a Mamãe Planejada. | `arquivo/`. |

## 4. Excesso

### 4.1 Trabalho que não está na `main` (resolver antes de apagar qualquer coisa) 🟡

| Onde | O que tem | Sugestão |
|---|---|---|
| `keshion-wt-copiloto/` (branch `feat/copiloto-e-fora-do-horario`) | 6 arquivos de código alterados sem commit e o `PLANO-COPILOTO.md`, que só existe ali | É trabalho em andamento do copiloto. Fazer commit na branch e seguir com ela. **Não apagar.** |
| `keshion-wt-retomar/` (branch `fix/cancelar-pergunta-duas-vezes`) | 1 commit da correção do "cancelar", com 5 testes, fora da `main` | Revisar e juntar na `main` (com OK), depois remover a área de trabalho pelo git. |
| Branch `fix/retomar-pendente-agora` (sem pasta) | 2 commits: prompt do Pacote C e RETOMAR-AQUI de 20/11 | Conferir se já entrou na `main` por outro caminho. Se sim, apagar a branch. Se não, juntar. |
| `keshion/` (main) | 10 arquivos alterados e 7 novos sem commit (material do piloto, Sérgio, pesquisa) | Fazer commit antes da fase 2, para ter um ponto de volta. |

### 4.2 Histórico técnico acumulado (16 a 20/11)

| Grupo | Quantidade | Sugestão |
|---|---|---|
| Conversas de paciente simulado (`tecnico/teste-ab/paciente-simulado-*.md` e `.json`) | 13 .md (cerca de 800 KB) e os .json | Mover para `arquivo/testes-2026-11/`. Manter só a última rodada aprovada de cada pacote. |
| Relatórios de teste (`tecnico/teste-ab/relatorio-*.md`) | 5 | Manter o mais recente de cada tema. Os outros vão para o arquivo. |
| Prompts de teste já rodados (`PROMPT-TESTE-*`, `PROMPT-RETOMAR-*`) | 7 | Arquivar os pacotes A a D já aprovados (confirmar no `testes-checklist.md`). |
| Revisões e prompts do Codex (`tecnico/n8n/revisao-codex-*`, `PROMPT-CODEX-*`, `codex-18-11/`, `codex-19-11/`, `plano-pos-revisao-codex.md`) | Cerca de 15 | Manter `PROMPT-CODEX-REVISAO.md` (é o modelo em uso) e o `PLANO-CORRECOES-2.md` enquanto houver correção aberta. O resto vai para `arquivo/codex/`. |
| Logs de teste (`tecnico/teste-ab/*.log`) | 5 (11 a 18/11) | Apagar ou arquivar. |
| `tecnico/teste-ab/__pycache__/` | 3 | Lixo automático do Python, já fora do git. Pode apagar. |

### 4.3 Soltos

- `pesquisa/codex-prompt-keshion-competitor-market-research - Shortcut.lnk`: atalho do Windows que caiu na pasta. Apagar.
- `app/web/node_modules` (410 MB) e `app/web/.next` (164 MB): são refeitos com `npm install` e `npm run build`. Só apagar se precisar de espaço. Não ajudam nem atrapalham a organização.
- `.claude/data/healthcare/`: cache de plugin, fora do git. Deixar.
- Não há pastas vazias.

## 5. Proposta de estrutura

A estrutura atual já é boa. A mudança é **separar o ativo do histórico**:

```
keshion/
├── CLAUDE.md, plano-estrategico-keshion.md, startup-canvas-keshion.md, historico-e-estrategia.md
├── tecnico/        só o que está em uso: RETOMAR-AQUI, LEIA-ME, CLINICA-NOVA, servidor, testes-checklist,
│                   gerador, scripts de teste e o prompt de revisão do Codex
├── comercial/      piloto (v2), preço, planos, sergio/
├── clientes/       _modelo, clinica-demo, clinica-teste (e a próxima clínica piloto)
├── app/, app-crm-painel/, site/ (só a versão atual), branding/, pesquisa/
└── arquivo/
    ├── 2026-10-estrategia-antiga/   (apresentações, debate de investidores, resumos de sessão)
    ├── dra-vivian-suspenso-2026-11-20/
    ├── make/
    ├── codex/
    ├── testes-2026-11/
    └── site-versoes-antigas/
```

**Padrão de nomes:** os arquivos novos de registro usam `AAAA-MM-DD-descricao.md` (hoje há 4 formatos de data misturados: `2026-11-18`, `20261118`, `18-11` e `19-11`). Os arquivos-guia ficam em maiúsculas como já estão (`LEIA-ME`, `RETOMAR-AQUI`).

## 6. Fora deste diagnóstico

- Notion e GitHub (issues): quem cuida deles é o PM, no daily. O item 3.1 vale para o Notion também: conferir se o marco "piloto da Vivian" ainda está como "📍 Estamos aqui".
- O servidor (base da Clara em produção): só lido pelos documentos, sem acesso.
- Os PDFs, PPTX e HTML não foram lidos por dentro, só pelos nomes e datas (com exceção do `copy-v3.html` e do roadmap, onde a busca por "Vivian" achou trechos).

## Ordem sugerida para a fase 2

1. Commit do que está pendente na `main` (ponto de volta).
2. Corrigir a meta no `project-manager.md` e no `vendas.md` (2 linhas, impacto imediato no daily).
3. Resolver as branches do retomar e do copiloto.
4. Atualizar os 8 documentos da seção 3.1.
5. Mover para `arquivo/` o que está nas seções 3.2 e 4.2 (com `git mv`, para nada se perder), registrando tudo em `arquivo/LOG.md`.
6. Juntar inventário, conflitos e este diagnóstico em um só.
