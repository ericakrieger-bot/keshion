# Resumo para retomar a conversa do app (16/11/2026)

> Copie o bloco abaixo e cole no chat que trata do aplicativo.

```
Resumo das decisões sobre o app da Keshion (conversa de 16/11/2026, no chat do Notion):

PÚBLICO E ESCOPO
- Público do app v1: dentista solo ou clínica com 2 ou 3 dentistas, geralmente sem software odontológico e às vezes sem secretária (caso da Dra. Vivian, piloto a partir de 01/12/2026).
- Dezembro: Pendências, Conversas (assumir e devolver para a IA), Agenda do dia (Google Agenda) com botões compareceu e faltou, Pacientes (ficha simples).
- Janeiro: Orçamentos com PDF na marca da clínica e envio pelo WhatsApp (botão "Quero fazer"; situações enviado, visto, aceito, recusado com motivo), Resultados (reais recuperados), Retornos.
- Fora do v1: prontuário, nota fiscal, financeiro completo, integrações com software (só se cliente pedir).
- Formato do orçamento da Dra. Vivian: definido na reunião de levantamento com ela.

TECNOLOGIA E HOSPEDAGEM
- Um único app web (Next.js) que abre no navegador do computador e instala no celular como aplicativo (PWA).
- Telas: Netlify, plano grátis (permite uso comercial; 300 créditos por mês; se os créditos acabam, o site pausa, não cobra; cada publicação gasta créditos, então publicar em lotes).
- Login, banco e arquivos: Supabase, plano grátis (500 MB de banco, 1 GB de arquivos, 50 mil usuários ativos, 2 projetos; pausa depois de 7 dias sem uso; sem backup diário).
- Criar o projeto do Supabase na região São Paulo (não dá para mudar depois). Projetos novos exigem permissões (grants) explícitas no Postgres para a API.
- Backup diário próprio do Supabase para o servidor Contabo (via n8n ou pg_dump), já que o grátis não tem.
- Cada clínica vê só os próprios dados (regras de acesso por linha no Postgres, RLS).
- Em aberto: o banco "clara" do n8n vai para o Supabase (um banco só) ou o app lê do Contabo.
- Domínio da empresa: keshion.com (Hostinger). App em app.keshion.com quando estiver pronto.

QUANDO PAGAR
- Piloto e 3 primeiros clientes cabem no grátis.
- Supabase Pro (US$ 25/mês, cerca de R$ 140): no primeiro cliente pagante, ou banco acima de 400 MB, ou se quisermos backup e suporte deles.
- Netlify Personal (US$ 9/mês, cerca de R$ 50): quando os créditos passarem de 80% no mês (app pausado com clínica usando é inaceitável).
- Com cerca de 10 clínicas: Netlify Pro (US$ 20) + Supabase Pro (US$ 25), perto de R$ 250/mês no total, para todas as clínicas.

RELATÓRIO DE REAIS RECUPERADOS (regras de atribuição)
- Lógica de link de afiliado: conta para a assistente quando o paciente volta pela mensagem dela dentro de uma janela.
- "Recuperado pela assistente": orçamento ou conversa parada há 7 dias ou mais, sem contato da equipe nesse período; paciente respondeu à mensagem da assistente; aceite ou comparecimento em até 30 dias. Entra no total.
- "Influenciado": assistente tocou, mas a equipe também conversou antes do aceite. Linha separada, fora do total.
- "Orgânico": sem toque da assistente. Não conta.
- Provas por linha: datas e horas, link da conversa, valor confirmado pela clínica. A clínica pode contestar antes de fechar o mês.
- Comparação: taxa de fechamento dos últimos 20 orçamentos (levantada na implantação) contra a atual.

PRÓXIMO PASSO PEDIDO
- Calculadora de perdas e ROI (parecida com a de um concorrente, a Secretária IA): perguntas de escopo feitas no chat do Notion; levar as respostas da Erica para cá.

Arquivos no repositório: plano-produto-diferenciais.md, app-crm-painel/RESUMO-HOSPEDAGEM-E-DECISOES-APP.md
```
