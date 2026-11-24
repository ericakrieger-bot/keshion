# Prompt para o Codex: construir o site da Keshion AI

> Cole tudo abaixo da linha na primeira mensagem do Codex, aberto na pasta `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`.
> Opcional: anexe um print de conversa de WhatsApp (celular, tema claro) como referência extra do visual. Sem print, a seção 5 já descreve tudo.
> Preparado em 24/11/2026 a partir de `site/copy-v4.html` e `site/DECISOES.md` (versões de 24/11). Revisado em 24/11/2026 pelo PM de Marketing: copy conferida frase por frase contra a copy-v4, caminhos conferidos, correções listadas no fim do arquivo.

---

Você vai construir o site da **Keshion AI** (keshion.com). O site precisa estar pronto para publicar até **26/11/2026**, porque o app do Google e a política de privacidade dependem dele.

Escreva sempre em português do Brasil, com acentos e frases curtas. Nunca use travessão (o traço longo) nem ponto de exclamação nos textos do site. A dona do projeto, Erica, não é programadora. Fale com ela em linguagem simples, só com o resultado e o que ela precisa decidir.

## 1. O que é a Keshion

A Keshion AI vende para **clínicas odontológicas** (somente odontologia, da rotina de consultório à estética dental; nenhuma outra área da saúde) o **Assistente Inteligente**, que atende o WhatsApp da clínica. Ele tira dúvidas, mostra os horários livres, marca a consulta na agenda, retoma orçamentos parados, confirma consultas e chama a equipe quando a conversa pede uma pessoa. Junto vem um app para a equipe organizar a rotina: conversas, agenda do dia, pacientes, orçamentos e painel de valores recuperados.

O público é o dentista dono de clínica. Ele não conhece vocabulário de vendas nem de tecnologia. O objetivo do site é um só: fazer ele **agendar o diagnóstico grátis** pelo WhatsApp.

## 2. Documentos que você pode e deve ler (todos nesta pasta)

Leia antes de escrever código, nesta ordem:

| Arquivo | Para quê |
|---|---|
| `site/copy-v4.html` | A copy oficial, 13 seções. **É a fonte de verdade do texto.** O texto completo também está na seção 9 deste prompt. As "Notas internas" no fim do arquivo não vão para o site. |
| `site/DECISOES.md` | Todas as decisões do site (preço, níveis, contato, demonstração, o que nunca pode aparecer). |
| `site/design-v1-visualizar.html` | **O design aprovado pela Erica.** Tem a abertura (hero) e a seção 2 prontas. Siga este visual em todo o site. O arquivo tem imagens em base64, então leia só o CSS e o HTML. |
| `site/design-v1.html` | A mesma coisa, sem base64 (mais fácil de ler). |
| `site/PROMPT-DESIGN.md` | Direção visual original (tom sóbrio, arcos, ícones Lucide). Atenção, três pontos estão velhos: fala em "Clara", em "estética de alto padrão" e em site inteiro em tema escuro. Hoje vale `DECISOES.md` e, no visual, o `design-v1-visualizar.html` (abertura clara; só as seções 6, 9 e 13 são escuras). |
| `branding/guia-de-marca.md` | Marca: logo, cores, contraste medido, fontes, tom de voz. |
| `branding/kit/LEIA-ME.md` | Como usar os arquivos oficiais do kit no site. |
| `branding/kit/digital/keshion.css` e `keshion-tokens.json` | Variáveis de cor e fontes. Não recrie a paleta à mão. |
| `branding/kit/logos/` | Logos oficiais em SVG. Use `keshion-ai-fundo-claro.svg` em fundo claro e `keshion-ai-fundo-escuro.svg` em fundo escuro. |
| `branding/kit/icones/` | `favicon.svg`, `favicon.ico`, `apple-touch-icon-180.png`. |
| `branding/kit/midias/compartilhamento-1200x630.png` | Imagem do Open Graph. |
| `branding/kit/fontes/` | Manrope e Inter variáveis, licença OFL (pode embutir no site). |
| `site/politica-de-privacidade.html` | Rascunho da política de privacidade, com campos a preencher. Use como base de `privacidade.html`. |
| `app-crm-painel/LEIA-PRIMEIRO.md`, `app-crm-painel/prototipo-crm-mobile.html`, `app-crm-painel/previa-painel.html` | O que o app mostra de verdade, para desenhar a tela do app coerente. |
| `site/COMPARATIVO-HOSPEDAGEM.md` | Por que Netlify (Free, com Netlify Forms). |

**Não edite** nenhum arquivo fora de `site/publicar/`. A copy é mantida em outra conversa. Se um texto atrapalhar o design, avise a Erica em vez de reescrever.

## 3. O que entregar (tudo em `site/publicar/`)

1. `index.html`: página única, responsiva, celular primeiro, com as 13 seções da copy na mesma ordem.
2. `privacidade.html`: política de privacidade simples, adequada à LGPD, baseada em `site/politica-de-privacidade.html`. Contato: contato@keshion.com. Dados coletados pelo formulário: nome, WhatsApp e nome da clínica. Razão social, CNPJ e endereço como `[a preencher]`, bem visíveis para não esquecer.
3. `obrigado.html`: página de agradecimento depois do formulário, com um botão que leva ao WhatsApp.
4. `comparar.html`: página só de pré-visualização (não vai para o menu do site). Mostra o **mesmo** `index.html` lado a lado em dois iframes: moldura de celular com 375 px de largura e moldura de computador com 1280 px (pode reduzir com `transform: scale` para caber na tela). Serve para a Erica comparar.
5. `img/`: imagens do site.
6. `netlify.toml` simples, se precisar (cabeçalhos de segurança e cache de fontes e imagens).
7. `img/LEIA-ME.md`: lista de cada imagem com arquivo, onde aparece, fonte e licença.

A pasta `site/publicar/` já tem uma base de outra sessão: `img/` (logos, favicon, imagem do Open Graph e 5 placeholders de foto `foto-*.svg`), `fontes/` (Manrope e Inter) e um rascunho de `css/site.css` (25 KB) e `js/site.js` (5 KB). **Esse rascunho de CSS e JS é antigo** (o `NOME_PRODUTO` dele está vazio, de antes da escolha do nome): trate como ponto de partida, confira tudo contra este prompt e reescreva o que divergir. Não há nenhum HTML ainda. Se o rascunho atrapalhar, pode apagar `css/site.css` e `js/site.js` e começar do zero; as imagens e fontes ficam.

Sem framework e sem etapa de build. HTML, CSS e um pouco de JavaScript puro. Precisa funcionar subindo a pasta direto no Netlify.

## 4. Design

- **Siga `site/design-v1-visualizar.html`.** Abertura em tema claro: foto de fundo com degradê branco-gelo à esquerda (texto) e foto livre à direita, arcos azul e verde translúcidos nos cantos, menu com logo, links ("Como funciona", "O app", "Perguntas") e botão pequeno, headline grande, dois celulares inclinados à direita (um com WhatsApp, outro com o app) e uma curva na transição para a seção seguinte.
- Seção 2 exatamente como no design: três cards ligados por uma linha tracejada, a frase da causa com barra azul à esquerda e o bloco "Quem quer marcar..." com a lista de três itens em caixas névoa.
- Para as seções 3 a 13, continue o mesmo vocabulário visual: rótulo pequeno em caixa alta acima de cada título, cards brancos com borda fina e cantos de 12 px, ícones Lucide com traço de 2 px dentro de quadrados névoa, muito espaço livre.
- Alterne fundos claros. As seções 1 (abertura), 6 (app), 9 (demonstração) e 13 (fechamento) têm peso visual. Na copy, 6, 9 e 13 estão marcadas como escuras (azul-noite `#0B1126`, cards marinho `#17233E`).
- Cores (do kit): azul-noite `#0B1126`, azul `#4388E8`, verde `#55C96A`, branco-gelo `#F7F8F4`, marinho `#17233E`, névoa `#E8EFF9`, azul intenso `#2459A6`, ardósia `#50596A`, prata `#CCD5E6`.
- Contraste: em fundo claro, botão e link em azul intenso `#2459A6`. **Nunca** texto verde nem texto azul `#4388E8` pequeno sobre fundo claro (veja a tabela de contraste no guia). Em fundo escuro, botão azul `#4388E8` com texto azul-noite.
- Fontes: Manrope 700 nos títulos, Inter 400 no texto, Inter 600 em botões e rótulos. Carregue os arquivos locais de `fontes/` (sem Google Fonts, melhor para a LGPD).
- **Logo:** sempre o arquivo SVG oficial. Nunca escreva "KESHION AI" no lugar do logo. Em texto corrido, escreva "Keshion AI".
- Seção 6 (app): mostre um celular com a tela do app (tema escuro, como o segundo celular do hero: "Agenda do dia", linhas com ícone verde, etiqueta "Precisa de você", barra de abas Conversas, Agenda, Pacientes). Inclua um bloco visual do **painel de valores recuperados** com as três categorias (recuperado, influenciado, veio sozinho e não conta) e o critério. Use barras ilustrativas **sem números inventados**.
- Seção 11 (custos): três cards lado a lado no computador e empilhados no celular, com um indicador de nível (1, 2 ou 3 traços preenchidos). Destaque visual leve no Completo, sem selo "mais vendido" nem urgência.
- Seção 12 (perguntas): acordeão com `<details>` e `<summary>`.
- Tom visual sóbrio e refinado. Nada de visual de infoproduto: sem selos, contadores, cronômetros, faixas piscando ou urgência artificial.

## 5. Mockup do WhatsApp: tem que parecer o app de verdade

Este é o elemento mais importante do site. A pessoa precisa bater o olho e reconhecer o WhatsApp. Siga a lista abaixo. **Se a Erica anexou um print de WhatsApp, use o print como referência extra de visual** (proporções, cores, espaçamentos, jeito das mensagens) e, se o print e a lista divergirem no visual, siga o print. O texto das mensagens vem sempre da seção 9, nunca do print.

Faça um componente reutilizável (HTML e CSS puros, sem imagem) dentro de uma moldura de celular, usado no hero e na seção 9:

- **Moldura de celular:** borda preta arredondada, recorte de câmera no topo e barra de status (hora, sinal, wi-fi, bateria).
- **Cabeçalho verde** (`#008069`, WhatsApp no tema claro): seta de voltar, foto redonda do contato, nome do contato, status embaixo do nome e ícones brancos de vídeo, telefone e menu de três pontos à direita.
- **Contato:** quem aparece é a **clínica**, porque a tela é o celular do paciente. Nome: "Clínica Sorriso". **Nunca** o nome da Keshion nem do produto. A foto do contato é um avatar neutro de clínica (por exemplo, um dente desenhado), nunca o logo da Keshion.
- **Status:** "online", que vira "digitando..." enquanto a clínica escreve.
- **Fundo bege** (`#EFEAE2`) com o padrão sutil de desenhos do WhatsApp (SVG em data URI, bem fraco).
- **Etiqueta de dia** centralizada (por exemplo "TERÇA-FEIRA" ou "HOJE"), fundo branco, sombra leve.
- **Balões:** mensagem enviada pelo paciente em verde claro (`#D9FDD3`) à direita; mensagem da clínica em branco à esquerda. Cantos de cerca de 8 px, sombra de 1 px e **rabinho** no primeiro balão de cada sequência (canto de cima do lado do rabinho reto).
- **Horário** pequeno e cinza (`#667781`) no canto de baixo à direita de cada balão. Nas mensagens do paciente, **tique duplo azul** (`#53BDEB`) ao lado do horário. As mensagens da clínica não têm tique.
- **Campo de digitar** embaixo: barra branca arredondada com ícone de emoji, texto "Mensagem", clipe e câmera, e o botão redondo verde (`#00A884`) com microfone.
- **Fonte e tamanhos como no app:** Segoe UI, Helvetica Neue ou Arial, texto em torno de 14 a 15 px, linha de 19 px, horário com cerca de 11 px.
- Use `em` nas medidas internas para o mesmo componente funcionar em dois tamanhos (menor no hero, maior na seção 9) e continuar legível no celular de 375 px.

### Animação das mensagens

- As mensagens aparecem **uma de cada vez, como numa conversa real**, quando o celular entra na tela.
- Antes de cada mensagem da clínica: três pontinhos de "digitando" num balão branco por cerca de 1 a 2 segundos (proporcional ao tamanho do texto) e o status do cabeçalho muda para "digitando...". Depois os pontinhos somem e a mensagem entra com fade e um leve deslize para cima.
- Mensagens do paciente entram depois de uma pausa curta, já com o tique duplo azul.
- Quando a conversa passa da altura da tela, as mensagens antigas sobem (como no app). Um degradê suave no topo esconde o corte.
- Na seção 9 há **quatro conversas**. Mostre-as com abas ou botões ("Limpeza", "Orçamento", "Confirmação", "Lentes"). Trocar de aba reinicia a animação daquela conversa. As abas funcionam com teclado (setas) e têm `aria-selected`.
- Ao lado do celular, mostre o título e o contexto da conversa ativa (por exemplo "Terça-feira, 21h07, clínica fechada").
- Sem JavaScript, todas as mensagens aparecem de uma vez. Com `prefers-reduced-motion`, também: sem digitando e sem animação.

### Texto das conversas

Use o texto exato da seção 9 da copy (mais abaixo). No hero, use uma versão curta da conversa 1 (quatro balões). Na tela do paciente, o que a copy marca como mensagem do paciente fica verde à direita e o que é da clínica fica branco à esquerda. Os horários dos balões seguem o contexto de cada conversa (21:07, 21:08...). **Nenhum valor de tratamento** aparece nas conversas e nenhum dado de paciente real.

## 6. Outras animações (todas leves)

- **Entrada suave ao rolar:** títulos, cards e fotos aparecem com fade e um deslize curto (20 px), em cascata dentro de cada grade (cerca de 90 ms entre um card e o outro). Use `IntersectionObserver`.
- **Microinterações:** botões sobem 2 px no hover, ganham sombra e a seta desliza para a direita; no clique, encolhem um pouco. Cards sobem 4 px no hover e o ícone gira de leve. Abas e perguntas mudam de cor com transição.
- **Celulares do hero** flutuam devagar (poucos pixels, ciclo de cerca de 7 segundos).
- **Painel de valores recuperados:** as barras crescem quando o bloco entra na tela.
- **Página de obrigado:** o sinal de "ok" se desenha.
- Sem biblioteca de animação. Só CSS e JavaScript puro.
- **Respeite `prefers-reduced-motion`:** com ele ligado, nada se mexe e todo o conteúdo aparece direto.
- Nunca esconda conteúdo sem JavaScript: só aplique o estado "escondido antes de animar" quando o JS estiver rodando (por exemplo, com uma classe `js` no `<html>`).

## 7. Fotos

A Erica quer fotos variadas: fachada ou ambiente de clínica odontológica, recepção, dentista atendendo, paciente sorrindo e celular com WhatsApp na mão.

- **Não baixe nenhuma foto.** Não use foto de fonte sem licença clara. As imagens `site/img/hero-a.jpg` e `hero-b.jpg` têm origem desconhecida: **não use**.
- Use os placeholders que já estão em `site/publicar/img/` (`foto-clinica.svg`, `foto-recepcao.svg`, `foto-dentista.svg`, `foto-paciente.svg`, `foto-celular.svg`), ou faça placeholders melhores no mesmo estilo.
- Distribuição sugerida: clínica no fundo do hero (variável CSS `--hero-foto`, como no design), recepção na seção 3, paciente na seção 5, celular com WhatsApp na seção 7, dentista na seção 10.
- Deixe a troca fácil: cada foto é um arquivo em `img/` com nome fixo. Para trocar, basta salvar a foto real com o mesmo nome e mudar a extensão em um lugar. Use `width`, `height`, `loading="lazy"` e `aspect-ratio`.
- **Alt text em português**, descrevendo a foto pretendida (por exemplo: "Recepção de uma clínica odontológica, com a atendente ao computador").
- Se quiser sugerir fotos de banco gratuito, **só liste** (nome, link, licença, tamanho) em `img/LEIA-ME.md` para a Erica aprovar. Não baixe.

## 8. Regras técnicas

- **Botão principal "Agendar diagnóstico grátis"** (menu, hero, demonstração, fechamento e página de obrigado) abre o WhatsApp em nova aba:
  `https://wa.me/554137900181?text=Ol%C3%A1!%20Quero%20agendar%20o%20diagn%C3%B3stico%20gr%C3%A1tis%20da%20Keshion`
  com `target="_blank" rel="noopener"`.
- **Número do WhatsApp em um lugar só (pendente da Erica).** O número (41) 3790-0181 pode ser trocado antes de publicar (hoje ele roda a demonstração e a Erica ainda decide com a parte técnica). Marque todo link do WhatsApp com `data-wa`, deixe o link padrão acima no HTML (funciona sem JS) e crie no topo do JS duas constantes, `var WHATSAPP_NUMERO = "554137900181";` e `var WHATSAPP_TEXTO = "Olá! Quero agendar o diagnóstico grátis da Keshion";`, que reescrevem o `href` de todo `a[data-wa]` e o texto visível do número ("(41) 3790-0181") em todo elemento marcado com `data-wa-texto`. Esse número é só um contato para falar com a equipe: **nenhuma demonstração ao vivo** no site.
- **Sem cookies, sem analytics, sem pixel, sem script de terceiros.** Assim não precisa de aviso de cookies. Se algum dia entrar medição, a política de privacidade muda antes.
- **Cabeçalhos do Netlify (`netlify.toml`):** use `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` e `X-Frame-Options: SAMEORIGIN` (não `DENY`, senão o `comparar.html` não mostra o site nos iframes). Cache longo só para `/img/*`, `/fontes/*`, `/css/*` e `/js/*`.
- **Segundo botão do hero:** "Ver uma conversa de exemplo", que leva à seção 9 (`#demonstracao`).
- **Formulário de contato (segunda via)** no fechamento, com Netlify Forms:
  - `<form name="contato" method="POST" action="/obrigado.html" data-netlify="true" netlify-honeypot="bot-field">`
  - `<input type="hidden" name="form-name" value="contato">`
  - Campo honeypot `bot-field`, escondido visualmente.
  - Campos: nome, WhatsApp (`type="tel"`, `autocomplete="tel"`) e nome da clínica, todos com `<label>`.
  - Aviso LGPD logo acima do botão: "Usamos seus dados só para entrar em contato sobre o diagnóstico. Veja a [política de privacidade](privacidade.html)."
  - Botão: "Quero que me chamem" (ou parecido, sem exclamação).
- **Nome do produto em um lugar só:** o nome é "Assistente Inteligente" (escolha da Erica em 24/11). Marque os pontos com a classe `np` e uma constante no topo do JS, `var NOME_PRODUTO = "O Assistente Inteligente";`, como em `copy-v4.html`. O HTML já traz o mesmo texto como padrão, para funcionar sem JS.
- **Nomes dos níveis em um lugar só:** os nomes (Essencial, Avançado, Completo) ainda podem mudar, principalmente o do meio. Coloque os três nomes numa constante única no JS (por exemplo `NOMES_NIVEIS`), usada em todos os lugares onde aparecem (cards, texto do Completo "Tudo do avançado", perguntas), com o texto no HTML como valor padrão.
- **Preço:** só os valores que estão na copy-v4 (mensalidade e implantação dos três níveis). Nenhum outro valor em reais, nenhum valor de tratamento.
- **Nunca no site:** "API oficial", "sem bloqueio", depoimento, nome de clínica real, número ou estatística sem fonte, etiqueta "em construção", datas de entrega, "Clara", selo de "mais vendido".
- **Rodapé:** logo (versão fundo escuro), "Keshion · automações inteligentes", WhatsApp (41) 3790-0181, contato@keshion.com, keshion.com e link "Política de privacidade". Sem razão social, CNPJ e endereço no rodapé por enquanto (decisão da Erica). Ano atual.
- **SEO básico:** `lang="pt-BR"`, `<title>` (por exemplo "Keshion AI · Assistente inteligente no WhatsApp da clínica odontológica"), `meta description` com até 155 caracteres, `link rel="canonical"` para `https://keshion.com/`, Open Graph (`og:title`, `og:description`, `og:type`, `og:url`, `og:image` com URL absoluta `https://keshion.com/img/compartilhamento-1200x630.png`, `og:locale` pt_BR) e Twitter card. Favicon SVG, ICO e `apple-touch-icon`. `theme-color` `#0B1126`. `robots.txt` simples.
- `obrigado.html` e `comparar.html` com `noindex`. `privacidade.html` fica indexável.
- **`comparar.html` é só para a Erica olhar no computador dela.** Ele não vai para o ar: deixe no `netlify.toml` uma regra de redirecionamento (`/comparar.html` para `/`, status 404) ou, melhor, avise a Erica de que ele deve ficar fora da pasta enviada ao Netlify no dia de publicar.
- **Acessibilidade:** contraste conforme a tabela do guia de marca, foco visível em tudo (contorno de 3 px, azul intenso no claro e verde no escuro), link "Pular para o conteúdo", um único `h1`, títulos em ordem, `alt` em todas as imagens, ícones decorativos com `aria-hidden="true"`, mockups de WhatsApp com descrição acessível (por exemplo `role="img"` e `aria-label` resumindo a conversa, ou o texto legível pelo leitor de tela).
- **Desempenho:** sem bibliotecas externas, sem Google Fonts, imagens com `loading="lazy"` (menos a do hero), CSS e JS em arquivos próprios (`css/site.css`, `js/site.js`) usados pelas três páginas.
- Teste em 375 px, 768 px e 1280 px. Nada pode estourar a largura do celular (sem rolagem lateral).

## 9. A copy completa (texto exato do site)

Use estes textos sem reescrever. Rótulo pequeno da seção entre colchetes.

### Seção 1 · Abertura [sem rótulo]

**Título (h1):** Foque nos seus pacientes. Deixe a IA cuidar do resto.

**Subtítulo:** O Assistente Inteligente atende o WhatsApp da clínica, tira as dúvidas dos pacientes, mostra os horários livres e marca a consulta na agenda. Quando a conversa pede uma pessoa, chama a equipe.
(O trecho "O Assistente Inteligente" é o nome do produto, com maiúsculas, dentro do `<span class="np">`. Nas outras seções, "assistente" continua minúsculo, como palavra comum.)

**Botões:** Agendar diagnóstico grátis (WhatsApp) · Ver uma conversa de exemplo (`#demonstracao`)

**Microtexto:** 30 minutos. Você sai com um retrato de como o WhatsApp da clínica atende hoje.

### Seção 2 · [Problema]

**Título:** O caminho entre a primeira mensagem e a consulta marcada

**Abertura:** Entre a primeira mensagem de um paciente e a consulta na agenda, a conversa costuma parar em três pontos.

Cards:
- **Fora do horário.** O paciente escreve à noite ou no fim de semana, quando está decidindo. A clínica responde no dia seguinte, e até lá ele pode já ter conversado com outra.
- **Durante o expediente.** Entre o balcão, o telefone e o paciente na cadeira, o WhatsApp espera a vez. Perguntas simples, como horário e endereço, ocupam o tempo da recepção.
- **Depois do orçamento.** O paciente recebeu o valor do tratamento e disse que ia pensar. Ninguém tem a tarefa de voltar a falar com ele, e a conversa simplesmente termina.

**Frase de destaque:** Esses pontos têm uma causa em comum: a mesma pessoa cuida de muita coisa ao mesmo tempo.

**Subtítulo:** Quem quer marcar costuma marcar com quem responde primeiro

**Texto:** Quem precisa de uma limpeza, de uma obturação, de lentes de contato dental ou está com um dente doendo escreve para a clínica e espera pouco. As perguntas se repetem o dia todo: quanto custa a limpeza, se tem horário no sábado, qual é o endereço. Uma resposta na hora, com o valor que a clínica definiu e um horário livre, faz o paciente marcar ali mesmo. Uma resposta só no dia seguinte faz ele procurar outra clínica ou deixar para depois.

Lista:
- **Rapidez e retorno.** Quem responde primeiro, e quem volta a falar depois, costuma ser lembrado.
- **Clareza.** Uma resposta que explica o caminho transmite mais segurança que um valor solto.
- **Próximo passo.** Uma sugestão de horário concreta tira a decisão do campo das ideias.

### Seção 3 · [Como funciona] (âncora `#como-funciona`)

**Título:** Como o assistente entra na rotina da clínica

1. **Diagnóstico.** Em 30 minutos, olhamos como as mensagens chegam hoje e em que ponto a conversa para.
2. **Configuração.** Montamos uma base completa da clínica: tratamentos, horários, regras e o jeito de falar. As informações vêm de um questionário completo e de reuniões com os dentistas (no nível Essencial, só do questionário). Conectamos a agenda, e você revisa tudo antes de ir ao ar.
3. **Início acompanhado.** No começo, a sua equipe acompanha de perto o que o assistente responde. Quando todos estiverem à vontade, ele passa a responder sozinho o que for rotina.
4. **Acompanhamento.** Toda semana, lemos as conversas e ajustamos o que precisar. O que o assistente não souber, ele passa para a sua equipe, e você acompanha tudo pelo app.

### Seção 4 · [O assistente no WhatsApp]

**Título:** O que o assistente faz no WhatsApp da clínica

**Abertura:** Ele atende o paciente com as informações que a clínica definiu e leva a conversa até a consulta marcada.

Cards:
- **Responde com a base da clínica.** Tratamentos, horários, endereço e formas de pagamento, do jeito que a clínica definiu.
- **Marca, remarca e cancela.** Mostra os horários livres da agenda real e grava a marcação. Só diz que marcou depois de gravar.
- **Entende áudio e foto.** Transcreve o áudio e lê a imagem que o paciente enviou.
- **Chama a equipe.** Passa a conversa com o contexto, para o paciente não repetir a história. Quando o dentista responde, o assistente pausa.
- **Retoma orçamentos parados.** Quem recebeu o valor do tratamento e não respondeu recebe uma mensagem de retorno, em intervalos combinados com a clínica e sem insistência.

**Fecho:** A recepção volta a cuidar de quem está na clínica, e nenhum orçamento depende da memória de alguém.

### Seção 5 · [Pacientes atuais]

**Título:** A clínica também cuida de quem já é paciente

**Abertura:** O assistente não serve só para quem chega pela primeira vez. Ele também acompanha quem já está na base da clínica.

Cards:
- **Confirmação da consulta.** Pergunta ao paciente se ele vem, 48 horas antes, na véspera e algumas horas antes. Se ele pedir para remarcar, o assistente oferece novos horários na hora.
- **A ficha de cada pessoa.** Cada conversa fica ligada ao cadastro do paciente, com histórico, orçamentos e próximos passos.

**Fecho:** Menos faltas na agenda, sem que alguém precise lembrar de ligar.

### Seção 6 · [O app da clínica] (âncora `#app`, fundo escuro)

**Título:** Um app exclusivo para organizar a rotina da clínica

**Abertura:** A Keshion tem um app próprio, que você instala no celular. Nele, a equipe acompanha o que o assistente está fazendo e organiza o dia a dia da clínica: conversas, agenda, pacientes e orçamentos no mesmo lugar.

Cards:
- **Conversas.** As mensagens que pedem uma pessoa ficam no topo, na área "Precisa de você". Você assume a conversa, devolve para o assistente e ensina a resposta certa para a próxima vez.
- **Agenda do dia.** Quem vem hoje, quem confirmou, quem faltou. Um toque marca "compareceu" ou "faltou".
- **Pacientes.** A ficha de cada pessoa com o histórico da conversa, para a equipe não perguntar duas vezes.
- **Orçamentos.** Registre o orçamento, gere o PDF e envie pelo WhatsApp. Os lembretes de retorno seguem o intervalo combinado com a clínica.
- **Painel de valores recuperados.** Quanto voltou para a clínica depois que o assistente entrou, com o critério à vista.

**Caixa de destaque:** **O critério do painel.** Conta como recuperado o paciente que estava parado há 7 dias ou mais, respondeu ao assistente e fechou o tratamento em até 30 dias. O que o assistente apenas influenciou aparece separado, e o que veio sozinho não entra. A clínica confirma ou contesta cada caso.

**Fecho:** O app organiza o atendimento e o relacionamento com o paciente. Prontuário, nota fiscal e financeiro continuam no sistema que você já usa.

### Seção 7 · [Controle]

**Título:** Você acompanha o que o assistente responde, e pode assumir quando quiser

**Texto:** No começo, a sua equipe acompanha as respostas de perto e corrige o que for preciso. Quando todos estiverem seguros, o assistente passa a responder sozinho o que é rotina. O que for delicado continua indo para uma pessoa, e você pode assumir qualquer conversa pelo app.

### Seção 8 · [Limites]

**Título:** O que o assistente não faz

**Ele não**
- Dá diagnóstico nem indica medicação.
- Trata dor forte, inchaço ou urgência: encaminha direto para o dentista.
- Informa preço, horário ou promoção que a clínica não tenha definido.

**Ele sempre**
- Só confirma uma marcação depois de gravá-la na agenda.
- Evita marcar dois pacientes no mesmo horário.
- Diz que é um assistente virtual, se o paciente perguntar.

### Seção 9 · [Demonstração] (âncora `#demonstracao`, fundo escuro)

**Título:** Quatro conversas de exemplo

**Abertura:** Na Clínica Sorriso Exemplo, uma clínica odontológica fictícia. Os nomes e os horários são inventados para ilustrar.

Legenda: **P** = paciente (balão verde, à direita, com tique duplo azul). **C** = clínica (balão branco, à esquerda).

**Conversa 1 · Quanto custa a limpeza · terça-feira, 21h07, clínica fechada**
- P: Boa noite. Queria marcar uma limpeza. Vocês atendem sábado?
- C: Boa noite. Atendemos aos sábados, das 8h às 12h. Para a limpeza, tenho sábado às 9h ou às 10h30. Qual fica melhor?
- P: 9h.
- C: Combinado. Para deixar marcado, me passa o seu nome completo?
- P: Mariana Souza. Ah, e um dente está doendo um pouco quando tomo gelado.
- C: Anotado, Mariana. Sua limpeza ficou marcada para sábado, às 9h. Sobre o dente, vou avisar o Dr. Paulo agora, para ele olhar isso com você.

**Conversa 2 · Orçamento que esfriou · lembrete do 10º dia, quinta-feira, 10h15**
- C: Bom dia, Carlos. Aqui é o assistente da Clínica Sorriso Exemplo. Há alguns dias o Dr. Paulo passou o orçamento do seu tratamento de canal. Ficou alguma dúvida que eu possa ajudar a esclarecer?
- P: Bom dia. Fiquei em dúvida se dá para dividir o valor.
- C: As formas de pagamento são definidas pela clínica, e prefiro que o Dr. Paulo confirme as condições com você. Vou pedir para ele te responder ainda hoje. Se preferir, já te mostro os horários livres desta semana.
- P: Pode mostrar.
- C: Tenho sexta, às 14h, ou segunda, às 9h30. Qual fica melhor?

**Conversa 3 · Confirmação de consulta · véspera, 17h00**
- C: Boa tarde, Roberto. Lembrando da sua consulta amanhã, às 8h30, na Clínica Sorriso Exemplo. Você consegue vir?
- P: Amanhã eu não consigo, surgiu uma reunião.
- C: Sem problema. Posso remarcar para quinta, às 8h30, ou sexta, às 16h. Qual prefere?
- P: Quinta, 8h30.
- C: Pronto, sua consulta ficou para quinta, às 8h30. Até lá.

**Conversa 4 · Lentes de contato dental · domingo, 20h40**
- P: Oi, vi no Instagram de vocês as lentes de contato nos dentes. Quanto custa?
- C: Oi, tudo bem? O valor das lentes depende de uma avaliação com o dentista, porque cada caso é diferente. Por isso não passo um número por aqui. Posso marcar a sua avaliação? Tenho segunda, às 18h, ou terça, às 10h.
- P: Terça às 10h.
- C: Marcado para terça, às 10h. Me passa o seu nome completo para eu registrar?

**Nota abaixo:** Conversas ilustrativas, sem dados de pacientes reais. No app, a limpeza marcada aparece na Agenda do dia, o aviso sobre o dente chega para a equipe e a conversa inteira fica disponível para leitura.

**Botão:** Agendar diagnóstico grátis

(No cabeçalho do mockup, o contato aparece como "Clínica Sorriso". No texto das mensagens, mantenha "Clínica Sorriso Exemplo" como está na copy.)

### Seção 10 · [Para quem é]

**Título:** Para a clínica odontológica, do consultório pequeno à clínica movimentada

**Texto:** Pensado para clínicas odontológicas em que o WhatsApp é respondido pelo próprio dentista ou pela secretária que também cuida da recepção. Chegam muitas mensagens todo dia, quase sempre com as mesmas perguntas, e boa parte dos pacientes volta a cada seis meses. Por isso cada mensagem sem resposta e cada falta deixam um buraco na agenda.

Cards:
- **Rotina da clínica.** Limpeza, obturação, extração, canal e manutenção de aparelho.
- **Tratamentos de maior valor.** Lentes de contato dental, clareamento, implante e alinhadores, em que cada conversa sem resposta custa um tratamento inteiro.
- **Cada clínica com a sua base.** Os tratamentos, os horários e o jeito de falar são os da sua clínica, seja qual for a sua especialidade.

### Seção 11 · [Custos]

**Título:** Você escolhe o nível que cabe na sua clínica

**Abertura:** A mensalidade tem três níveis. Cada nível soma mais cuidado com a agenda e mais acompanhamento do resultado.

- **Essencial** · **R$ 349 por mês** · Implantação: R$ 490
  Para o consultório pequeno que quer começar. O assistente responde fora do horário, com uma base pronta de odontologia ajustada por um questionário, marca na agenda e avisa o dentista nos casos de urgência. Tem limite de conversas por mês e suporte por WhatsApp em horário comercial.
- **Avançado** · **R$ 590 por mês** · Implantação: R$ 1.500
  Para o dentista que atende sozinho e quer o jeito da sua clínica. A base é montada com você, com os tratamentos, os preços que podem ser ditos e o jeito de falar, e você aprova por escrito antes de ir ao ar. Atende fora do horário, marca, remarca e cancela, e envia um relatório simples todo mês.
- **Completo** · **R$ 1.290 por mês** · Implantação: R$ 3.000
  Para a clínica com secretária ou muitas mensagens. Tudo do avançado, e o assistente atende o dia todo, com a equipe aprovando as respostas com um toque quando quiser. Confirma e lembra as consultas e traz uma reunião mensal de resultado. Já vem com o app da clínica no celular, o painel de valores recuperados e prioridade no suporte.

**Fecho:** A implantação é paga uma única vez e cobre a base completa da clínica, a configuração, os testes e o treinamento da equipe. Os custos de conexão do WhatsApp, quando houver, são explicados no diagnóstico, antes de você contratar. O acompanhamento de orçamentos, a orientação de pós-operatório e o pedido de avaliação no Google podem ser somados como módulos opcionais.

(Os nomes dos níveis vêm da constante única `NOMES_NIVEIS`. Se a copy-v4 mudar antes de você terminar, os valores e nomes de lá valem mais que os daqui.)

### Seção 12 · [Perguntas] (âncora `#perguntas`)

**Título:** O que os donos de clínica perguntam antes de contratar

- **Preciso trocar de sistema?** Não. O assistente trabalha com a agenda digital da clínica (hoje, o Google Agenda), e no diagnóstico conferimos o seu caso. O app cuida das conversas, da agenda do dia, dos pacientes e dos orçamentos, e o prontuário e o financeiro continuam onde estão.
- **Ele substitui a recepção?** Não. Assume o que se repete e passa para a equipe o que precisa de uma pessoa.
- **O paciente vai perceber que é uma IA?** Se perguntar, o assistente diz que é virtual. As respostas são escritas no jeito da sua clínica.
- **E se o paciente perguntar o preço?** Ele só informa o que a clínica definiu. Orçamento de tratamento continua com o dentista.
- **Como o app funciona no dia a dia?** Você instala no celular, como um aplicativo comum, e abre quando quiser ver as conversas, a agenda do dia ou os orçamentos.
- **Como vocês calculam os reais recuperados?** Só entra o paciente que estava parado há 7 dias ou mais, respondeu ao assistente e fechou em até 30 dias. A clínica confirma ou contesta cada caso.
- **Quanto custa?** A mensalidade é de R$ 349, R$ 590 ou R$ 1.290, conforme o nível. A implantação é paga uma vez: R$ 490, R$ 1.500 ou R$ 3.000, conforme o nível.
- **Quanto tempo leva para entrar no ar?** Depende da agenda e da conexão do WhatsApp. No diagnóstico damos o prazo da sua clínica.
- **E os dados dos pacientes?** A clínica é a responsável pelos dados e a Keshion os trata conforme a LGPD. Os detalhes ficam no contrato.
- **Posso parar quando quiser?** As condições de cancelamento ficam claras antes de você contratar.

### Seção 13 · Fechamento (âncora `#diagnostico`, fundo escuro)

**Título:** Em 30 minutos, mostramos onde o WhatsApp da sua clínica para de responder

**Texto:** Você leva o retrato do atendimento atual, contrate ou não. Chame a gente no WhatsApp e escolha o melhor horário.

**Botão:** Agendar diagnóstico grátis

**Microtexto:** WhatsApp (41) 3790-0181 · contato@keshion.com

Ao lado (ou abaixo no celular): o formulário de contato da seção 8 deste prompt, com o título "Prefere que a gente chame você?" e o texto "Deixe seu nome e WhatsApp. Respondemos em horário comercial."

### Rodapé

Logo · Keshion · automações inteligentes · WhatsApp (41) 3790-0181 · contato@keshion.com · keshion.com · Política de privacidade

### Página de obrigado (`obrigado.html`)

- Título: "Recebemos seu contato"
- Texto: "Em breve alguém da equipe da Keshion chama você no WhatsApp para combinar o diagnóstico. Se preferir adiantar, fale com a gente agora."
- Botão: Agendar diagnóstico grátis (mesmo link do WhatsApp) · link "Voltar ao site"

## 10. O que você não pode fazer

- Publicar no Netlify, criar conta, mexer no DNS (o domínio keshion.com fica no Hostinger), gastar dinheiro ou baixar arquivos.
- Fazer commit ou push.
- Editar arquivos fora de `site/publicar/`, inclusive a copy.
- Inventar números, depoimentos, selos, clínicas ou dados de pacientes.
- Usar a palavra "Clara" ou o nome da Keshion dentro do mockup de WhatsApp.

## 11. Como trabalhar e quando está pronto

1. Leia os documentos da seção 2 e escreva em até 5 linhas o que entendeu e qualquer conflito que encontrou entre os arquivos. **Só pare e espere resposta se o conflito impedir de construir** (o prazo é curto); do contrário, siga em frente e deixe o conflito no relatório final. Se este prompt e `site/copy-v4.html` ou `site/DECISOES.md` divergirem, vale o arquivo e você avisa.
2. Construa `index.html` primeiro (com CSS e JS), depois `obrigado.html`, `privacidade.html`, `comparar.html`, `netlify.toml`, `robots.txt` e `img/LEIA-ME.md`.
3. Abra `comparar.html` num navegador e confira o celular (375 px) e o computador (1280 px). Tire um print de cada um para a Erica.
4. Confira, uma por uma: nenhum travessão, nenhuma exclamação no texto do site, nenhum "API oficial", nenhum valor em reais além dos da seção 11 e da pergunta "Quanto custa?", nenhum nome de clínica real, todas as imagens com `alt`, todos os links do WhatsApp com a mensagem pronta, o formulário com `data-netlify`, honeypot e aviso LGPD, e as animações desligadas com `prefers-reduced-motion`.

**Pronto quando:** os 4 arquivos abrem sem erro no console, o mockup do WhatsApp parece o app de verdade e anima as mensagens chegando, `comparar.html` mostra celular e computador, e você entrega à Erica, em linguagem simples:
- os dois prints;
- a lista do que falta (fotos reais, dados da empresa na política de privacidade, nomes finais dos níveis);
- a lista das imagens com fonte e licença.

## 12. Pendências da Erica antes de publicar (não são suas, só não esqueça de listar)

1. **Número do botão de WhatsApp:** (41) 3790-0181 hoje roda a demonstração. A parte técnica precisa impedir a resposta automática nele, ou a Erica troca o número (por isso a constante `WHATSAPP_NUMERO`).
2. **CNPJ, razão social e endereço:** a Erica passa quando tiver. Entram na política de privacidade (`[a preencher]` hoje) e, se ela decidir, no rodapé.
3. **Política de privacidade:** precisa de revisão jurídica e dos campos preenchidos antes de ir ao ar.
4. **Fotos reais:** a Erica aprova a lista de `img/LEIA-ME.md` antes de qualquer download.
5. **Nomes dos níveis:** Essencial, Avançado e Completo saem agora; a Erica pode mudar depois (constante `NOMES_NIVEIS`).
6. **Publicar no Netlify e apontar o domínio keshion.com (Hostinger):** só com OK da Erica no chat.

## 13. O que mudou nesta revisão (24/11/2026)

- Foco corrigido para somente odontologia (antes o texto da seção 1 dizia "todas as áreas").
- O print de WhatsApp virou opcional (não existe um print escolhido); a seção 5 basta sozinha.
- O rascunho de CSS e JS em `site/publicar/` foi marcado como antigo (o nome do produto dele está vazio).
- Número do WhatsApp em constante única (`WHATSAPP_NUMERO`), por causa da pendência técnica do número.
- `X-Frame-Options` do Netlify em `SAMEORIGIN`, para o `comparar.html` funcionar; `comparar.html` fora do ar.
- Sem cookies, analytics ou pixel (sem aviso de cookies).
- Passo 1 não trava mais esperando resposta, por causa do prazo de 26/11.
- Aviso de que o `PROMPT-DESIGN.md` também está velho no tema escuro do site inteiro.
- Copy da seção 9 conferida frase por frase contra `site/copy-v4.html` (24/11): sem diferença.
