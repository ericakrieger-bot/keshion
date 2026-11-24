# Mapa do projeto Keshion

Atualizado em 24/11/2026. Substitui o `INVENTARIO-MATERIAIS.md`, o `conflitos-e-duplicatas.md` e o `DIAGNOSTICO-ORGANIZACAO-2026-11-22.md` (os três estão em `arquivo/organizacao/`).
Para que serve: saber onde está cada coisa, qual arquivo vale quando dois falam do mesmo assunto, e o que ainda está para decidir.

## 1. Fonte oficial de cada assunto

Quando dois documentos discordarem, vale o desta tabela.

| Assunto | Vale | Observação |
|---|---|---|
| O que é a Keshion, pilha atual, regras e padrões de trabalho | `CLAUDE.md` | Os outros documentos só apontam para ele |
| Estado técnico, pendências e próxima feature | `tecnico/RETOMAR-AQUI.md` | Começar sempre por ele numa conversa técnica |
| Plano de longo prazo e metas até 2030 | `plano-estrategico-keshion.md` | |
| Modelo de negócio em uma página | `startup-canvas-keshion.md` (visual: `estrategia/canvas-page/startup-canvas.html`) | |
| Pilotos com clínicas conhecidas | `comercial/piloto/estrutura-piloto-conhecidos.md` | Cliente ideal: `cliente-ideal-e-aprendizado.md`. Material para a clínica: `material-piloto-v2.html` e o PDF v2 |
| Preço e pacotes | `comercial/estrategia-de-preco.md` e `comercial/proposta-de-valor-planos.md` | Hipótese até os primeiros pagantes. Com as clínicas piloto (parceiras) não se fala de dinheiro (decisão de 22/11) |
| Pacote de materiais do Sérgio | `comercial/sergio/materiais/` (PDFs 01 a 05, gerados de `fontes/`) | O PDF 02 é cópia do PDF v2 do piloto: ao gerar um novo, copiar para os dois lugares |
| Marca | `branding/guia-de-marca.md` e `branding/kit/` | Também pela skill `keshion-marca` |
| App, CRM e painel | `app-crm-painel/LEIA-PRIMEIRO.md` (decisões de 16/11 em `RESUMO-HOSPEDAGEM-E-DECISOES-APP.md`) | `crm-agenda-painel.md` é o conceito de 01/11: onde ele discordar, vale o LEIA-PRIMEIRO |
| Código do app | `app/LEIA-ME.md` e `app/web/` | |
| Como a Clara está montada | `tecnico/n8n/LEIA-ME.md` | Clínica nova: `tecnico/n8n/CLINICA-NOVA.md` |
| Servidor, backup e restauração | `tecnico/servidor-n8n.md` | Passo a passo da Erica em `tecnico/servidor/` |
| Testes | `tecnico/testes-checklist.md` | Prompts em uso: `tecnico/teste-ab/PROMPT-TESTE-19-11-pacote-d.md` e `PROMPT-TESTE-20-11-pacote-c-rodada-completa.md` |
| Revisão do Codex | `tecnico/n8n/PROMPT-CODEX-REVISAO.md` | Última revisão e plano aberto: `tecnico/n8n/codex-19-11/` |
| Site | `site/DECISOES.md` e `site/copy-v4.html` | Design: `site/design-v1.html` |
| Pesquisa de mercado | `pesquisa/` (concorrentes, nichos, análise competitiva de 22/11, red team de 22/11, organização da operação dos pilotos de 22/11) | `guia-tecnico-e-mercado.html` é de 04/10, só referência |
| Histórico das decisões | `historico-e-estrategia.md` | Só para consultar o porquê de uma decisão |
| Roadmap, tarefas, decisões e daily | **Notion** (página KESHION AI), mantido pelo agente `project-manager` | Nada de roadmap em arquivo na pasta |
| Agentes (PM e especialistas) | `.claude/agents/` | |

## 2. Estrutura das pastas

| Pasta | O que tem |
|---|---|
| raiz | `CLAUDE.md`, este mapa, plano estratégico, canvas, histórico, guia técnico e de mercado |
| `tecnico/` | Só o que está em uso: RETOMAR-AQUI, n8n (gerador, banco, testes locais), servidor, testes e prompts de teste vigentes |
| `comercial/` | Piloto, preço, planos e materiais do Sérgio |
| `clientes/` | `_modelo`, `clinica-demo` (Dra. Suzana, fictícia) e `clinica-teste`. A próxima clínica piloto entra aqui |
| `app/`, `app-crm-painel/` | Código do app e decisões |
| `site/`, `branding/`, `pesquisa/`, `estrategia/` | Site, marca, mercado e canvas visual |
| `arquivo/` | Tudo o que saiu de uso, organizado por tema. Lista completa e como trazer de volta: `arquivo/LOG.md` |
| `graphify-out/` | Mapa de conhecimento gerado (fora do git). Refazer com `graphify update .` |

Fora da pasta: `Documents\Claude Code\keshion-wt-copiloto` é a área de trabalho do git da branch `feat/copiloto-e-fora-do-horario` (copiloto e modo "só fora do horário", em construção). Não apagar: quando a feature estiver pronta, juntar na `main` e remover pelo git (`git worktree remove`).

## 3. Decisões em aberto

Também registradas no Notion, em "Decisões a tomar".

| Tema | Os lados | Quem decide |
|---|---|---|
| Sociedade | Erica fundadora única, Erica e Sérgio com vesting de 4 anos, ou sociedade meio a meio com acordo de uma página (plano estratégico) | Erica e Sérgio, antes de mostrar qualquer plano a terceiros |
| Captar investimento | O plano estratégico recomenda seguir sem investidores até R$ 100 mil por mês. O debate de 19/10 (arquivado) discutia captar depois de 3 clínicas | Erica |
| Conexão oficial do WhatsApp | O plano estratégico pede a API oficial no 1º trimestre de 2027. Pilotos começam na conexão não oficial | Erica, antes do 1º pagante |
| Prazo de retorno e parcelamento da avaliação | A base da demo diz "retornamos em instantes" e "12x" genérico; o real de cada clínica sai do questionário | Cada clínica piloto |
| Voz em áudio (Ester x OpenAI) | O roteiro de comparação (`tecnico/teste-voz/`) está sem resultado. As frases do roteiro não batem com a demo (40 min x 60 min; sexta 14h30 x avaliação só terça e quinta): corrigir antes de gerar os áudios | Erica |
| Oferta de fundador final, app na mensalidade ou à parte, quem paga cada ferramenta até o CNPJ, e-mail profissional (a Erica vai ver o que a Hostinger oferece; alternativa: Google Workspace) | Detalhes e prazos no Notion | Erica e Sérgio |
| Custo por clínica | Estimativas antigas variavam de R$ 180 a 590 por mês, sem fonte confiável | Medir no 1º piloto |

**Decididas no Notion em 21/11 (valem sobre os arquivos):** lembretes de orçamento nos dias 3, 10, 17 e 30 vão para a base do servidor junto com a próxima publicação, testados com o paciente simulado (ainda não publicado); quem confere o backup é a Erica, com o Sérgio de substituto, e o executor das 14h confere todo dia até o alerta por e-mail existir; a migração para o usuário `_app` (B7) é depois do teste do Pacote C e antes da 1ª clínica piloto entrar no ar. Copiloto: decidido em 21 e 22/11 (ver `tecnico/RETOMAR-AQUI.md`).

**Resolvidas na organização de 22/11:** primeiro pagante até 31/01/2027 (era 18/12 em planos antigos); metas de crescimento seguem o plano estratégico (os planos de negócio de outubro foram apagados em 19/11); a Mamãe Planejada só aparecia em material de outubro, hoje arquivado; piloto da Dra. Vivian suspenso em 20/11.

**Mudou em 24/11:** a Dra. Vivian retomou o contato e tem reunião em 25/11 com ela e o Dr. Eduardo (sócio); o piloto dela voltou a ser possível. O Dr. William recusou o piloto, mas se ofereceu para ajudar na parte odontológica. Convidado: Dr. Victor. Em espera até a reunião da Vivian: Dra. Sibelly, Dra. Gabrielli e Dra. Helka. **Nome do pacote decidido:** "Assistente Inteligente" (a Clara continua sendo o nome da assistente); sem registro no INPI por enquanto. O Google Agenda precisa ser reconectado em 25/11 (a conexão vence por volta de 26/11) até o app do Google ser publicado.

## 4. Regras de organização

1. Arquivo novo de registro (teste, revisão, resumo) usa data no nome: `AAAA-MM-DD-descricao.md`. Arquivos-guia ficam em maiúsculas (`LEIA-ME`, `RETOMAR-AQUI`).
2. Quando algo sai de uso, vai para `arquivo/<tema>/` com `git mv` e uma linha no `arquivo/LOG.md`. Nada é apagado direto.
3. Uma regra mora em um lugar só (tabela da seção 1). Os outros documentos apontam para ela.
4. Resultado de teste e relatório do Codex vão para `arquivo/` assim que o RETOMAR-AQUI registrar a conclusão.
5. Gestão (roadmap, tarefas, decisões, status) fica no Notion, não em arquivo.
6. Ao fim de uma rodada de organização: atualizar este mapa, rodar `graphify update .` e fazer commit e push.
