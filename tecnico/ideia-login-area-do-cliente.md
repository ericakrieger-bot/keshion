# Ideia: login e área do cliente

> Anotado em 12/11/2026, a pedido da Erica. **Não fazer agora.** Abrir uma conversa nova sobre isto quando o 1º piloto com clínica conhecida já estiver rodando (a partir de 01/12/2026; o piloto da Dra. Vivian foi suspenso em 20/11).

## Ponto de partida

- A ficha de implantação (questionário da clínica) está em https://keshion-questionario-clinica.vercel.app, sem login. As respostas ficam salvas só no aparelho e navegador de quem preenche, e cada "Salvar" ou "Enviar" grava uma linha na planilha da Keshion pelo Make (cenário 8491037).
- Limite de hoje: quem troca de aparelho ou limpa o navegador perde o rascunho na página (a cópia continua na planilha). Todas as respostas caem numa planilha só.
- Quem responde a ficha já é cliente, na fase de implantação.

## O que a Erica quer avaliar

1. Login e senha para entrar na ficha, para continuar de qualquer aparelho.
2. Já criar uma **área do cliente** da Keshion, onde a clínica entra para preencher a ficha e, depois, ver outras coisas.

## Perguntas para a conversa

- O que mais entra na área do cliente além da ficha? Ex.: status da implantação, base da clínica para revisar e aprovar, relatório de resultados, aplicativo com o cadastro dos pacientes (protótipo em `app-crm-painel/`), contrato e termo de parceria.
- Tipo de login: link mágico por e-mail (sem senha), senha, ou entrar com Google.
- Onde guardar os dados: Supabase (banco e login prontos), Lovable Cloud, ou o servidor da Keshion junto com a migração para o n8n.
- Uma área por clínica, com o que é dela separado (LGPD: a clínica é dona dos dados).
- Custo mensal e o que cabe no plano gratuito de cada ferramenta (a Vercel gratuita é para uso não comercial).

## Arquivos ligados

- `arquivo/dra-vivian-suspenso-2026-11-20/questionario-web/index.html` (ficha atual)
- `app-crm-painel/LEIA-PRIMEIRO.md` (aplicativo e painel da clínica)
- `plano-estrategico-keshion.md`
