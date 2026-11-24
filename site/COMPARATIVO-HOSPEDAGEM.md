# Site Keshion: onde criar e hospedar (comparativo de 23/11/2026)

Só pesquisa. Nada foi publicado, nenhuma conta criada, nada gasto. Prazo: site no ar até 26/11/2026 (precisa de keshion.com, site no ar e página de política de privacidade para o app do Google, tarefa 21).

## Recomendação

**Netlify (plano grátis) com o site em HTML que o Claude já deixou pronto.** Motivos:
- A conta da Netlify já existe (criada em 18/11, e-mail da Keshion) e é onde o app vai ficar.
- Custa R$ 0 por mês. O único gasto é o domínio keshion.com (se ainda não estiver pago).
- O site é uma página só, então o plano grátis dá folga. Os formulários da Netlify são grátis e sem limite nos planos atuais.
- O Claude faz tudo: página, botão do WhatsApp, formulário e política de privacidade. A Erica só aprova e liga o domínio.
- Dá para publicar em 1 dia, sobra tempo para ajustes até 26/11.

Plano B se algo travar: Framer ou WordPress.com (mais fáceis de mexer sozinha, mas pagos e com a copy toda a refazer).

## Como funciona o lead (vale para a recomendação)

1. Visitante preenche nome, WhatsApp e clínica (formulário da página).
2. O dado vai para o n8n da Keshion (ou para o painel da Netlify, com aviso por e-mail).
3. A tela de obrigado leva ao WhatsApp da Keshion (link wa.me com mensagem pronta).
4. Botão "Agendar diagnóstico grátis" também abre direto o WhatsApp.

Aviso de consentimento (LGPD) junto ao botão do formulário, com link para a política.

## Tabela comparativa

Dólar usado: R$ 5,87 (fechamento de 18/11/2026, [Brasil 61](https://brasil61.com/n/dolar-fecha-em-alta-de-1-45-e-chega-a-r-5-87-bras2617492)). Cartão internacional pode ter IOF e variação do câmbio. "Não conferido" = não consegui ler a página oficial; valor vem de fonte secundária.

| Opção | Custo por mês | Custo por ano | Prós | Contras | Esforço da Erica | Cumpre 26/11 |
|---|---|---|---|---|---|---|
| **1. Netlify Free + HTML do Claude (recomendada)** | R$ 0 (Personal: US$ 9 = R$ 53) | R$ 0 (Personal: R$ 634) + domínio | Grátis, domínio próprio com SSL, formulários grátis, conta já criada, mesmo lugar do app | Se acabarem os 300 créditos o site pausa (uma página leve fica longe disso). Mudanças pedem o Claude ou GitHub | Baixo: aprovar, ligar o domínio (DNS) | Sim |
| **2. Sites do ChatGPT (ideia da Erica)** | Exige Plus: R$ 99,90 (Free e Go não têm) | R$ 1.199 | Gera e publica no próprio ChatGPT, sem tocar em código | Recurso em beta. Sem formulário de leads documentado. Domínio próprio só "onde disponível". Custo alto para uma página. Cria um segundo lugar para cuidar | Médio: refazer a copy lá e achar um jeito de captar lead | Arriscado |
| **3. Wix** | Não conferido: cerca de R$ 53 (anual) a R$ 100 (mensal) no plano Light | Cerca de R$ 635 a R$ 1.200 | Editor visual, formulários prontos, suporte em português | Cobra em dólar, plano grátis não aceita domínio próprio, teria de refazer o design | Médio a alto | Sim, com retrabalho |
| **4. Framer** | Basic US$ 10 = R$ 59 (preço da página mostrada com cobrança anual) | Cerca de R$ 705 | Visual bonito, domínio incluso, rápido de publicar | Pago, formulário e limites não aparecem na página de preço, copy a refazer | Médio | Sim, com retrabalho |
| **5. WordPress.com** | Personal US$ 4 no anual = R$ 23; US$ 9 no mensal = R$ 53 | Cerca de R$ 282 (anual) | Barato, conhecido, domínio grátis no 1º ano no plano anual | Menos controle do visual, o design v1 não encaixa direto, mais configuração | Médio a alto | Sim, apertado |
| **6. Cloudflare Pages ou GitHub Pages + Tally** | R$ 0 (Tally grátis) | R$ 0 + domínio | Grátis, rápido, domínio próprio | Precisa de Git e formulário externo (Tally grátis com redirecionamento). Cloudflare Pages: limites não conferidos. É igual à opção 1, só com mais peças | Médio | Sim |
| **7. Google Sites** | Site grátis; domínio próprio exige Workspace (preço não conferido) | Não conferido | Simples | Pouco controle de visual, formulário e política de privacidade limitados | Médio | Possível, não indicado |

Domínio keshion.com: o CLAUDE.md já trata keshion.com como da Keshion, então confirme se já está pago e onde fica o DNS. Se faltar comprar: .com custa em geral de US$ 12 a US$ 15 por ano, ou R$ 70 a R$ 90 ([registradores](https://www.hostinger.com/br/tld/dominio-com); a Cloudflare vende "a preço de custo", sem valor na página). O Registro.br só vende .br, não .com.

## Política de privacidade

- Em qualquer opção ela é uma página comum (`keshion.com/privacidade`), com link no rodapé e ao lado do formulário. O Google exige a página no mesmo domínio e acessível pela home.
- Na opção 1 o Claude escreve e publica a página junto com o site. Precisa de: razão social e CNPJ (a preencher no rodapé do site), e-mail de contato (contato@keshion.com), quais dados o site coleta (nome, WhatsApp, clínica), para quê e por quanto tempo, e quem recebe (n8n, Netlify). Para o app do Google, vale incluir também os dados do Google que o app usa.
- Recomendo uma revisão de advogado depois do lançamento. Não é bloqueio para 26/11.

## Fontes oficiais

- Netlify, [preços](https://www.netlify.com/pricing/) e [formulários grátis nos planos de créditos](https://www.netlify.com/changelog/2026-04-14-pricing-updates-april-2026/)
- ChatGPT, [Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites) e [preços](https://chatgpt.com/pricing); valor em reais: [Canaltech](https://canaltech.com.br/apps/chatgpt-plus-fica-mais-barato-no-brasil-com-nova-cobranca-em-real/) (R$ 99,90, cobrado pela loja de apps pode variar)
- Framer, [preços](https://www.framer.com/pricing)
- WordPress.com, [preços](https://wordpress.com/pricing/) (divisão mensal e anual deduzida, ver lacunas)
- Wix, [planos](https://www.wix.com/plans): página não carregou; valores de [guia de 2026](https://guiaferramentasdigitais.com.br/guias/wix-review-brasil-2026/)
- Tally, [preços](https://tally.so/pricing); [GitHub Pages](https://pages.github.com/); [Google Sites e domínio](https://support.google.com/sites/answer/9068867)

## Lacunas (não conferi na fonte oficial)

Preço do Wix em reais, limites do Cloudflare Pages, preço exato do .com, Registro.br, formulários do Framer e do WordPress Personal, preço do Google Workspace. Nenhuma muda a recomendação, porque a opção 1 depende só da Netlify (conferida).

## Para decidir (OK da Erica antes de qualquer ação)

1. Seguir com a opção 1 (Netlify Free)?
2. Publicar em keshion.com (apontando o DNS) ou em um endereço de teste da Netlify primeiro?
3. Os leads vão para o n8n ou ficam só no painel da Netlify com aviso por e-mail?
4. Dados para a política: razão social, CNPJ e endereço (ou o que for mostrar).
