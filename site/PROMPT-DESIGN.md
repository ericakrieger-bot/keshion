# Prompt: design do site da Keshion AI

Cole este texto na primeira mensagem da sessão de design.

---

Você vai trabalhar o design do site da Keshion AI comigo (Erica). Responda sempre em português do Brasil, com acentuação correta, frases curtas e diretas. Sem travessão e sem ponto de exclamação nos textos do site.

## O que é a Keshion

A Keshion AI vende para clínicas odontológicas de estética de alto padrão uma assistente de IA, a Clara, que atende o WhatsApp da clínica, marca avaliações, retoma orçamentos parados e cuida de quem já é paciente. Junto vem um app exclusivo para a equipe organizar a rotina da clínica (conversas, agenda do dia, pacientes, orçamentos, retornos e painel de valores recuperados). O público é o dentista dono de clínica. Ele não conhece vocabulário de vendas nem de tecnologia.

## Onde estão as coisas

Pasta do projeto: `C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion`

Leia antes de começar, nesta ordem:

1. `site/copy-v3.html`: a copy do site, seção por seção (13 seções). Os blocos numerados de 1 a 13 são o conteúdo do site. As partes antes e depois deles (linha do tempo, "fora desta versão", "o que preciso de você") são notas internas e não entram no design.
2. `branding/` e a skill `keshion-marca`: logo, cores, fontes, tom de voz.
3. `site/DECISOES.md`: decisões já tomadas.
4. `app-crm-painel/`: o que o app vai mostrar, para desenhar os mockups com telas coerentes.

## Direção visual já aprovada

- Marca: wordmark "keshion AI".
- Cores: #0B1126 (fundo escuro), #4388E8 (azul), #55C96A (verde), #F7F8F4 (off-white), #17233E, #E8EFF9, #2459A6, #50596A, #CCD5E6.
- Fontes: Manrope 700 nos títulos, Inter no texto.
- Site e app em tema escuro. Documentos em tema claro.
- Ícones Lucide, traço de 2px.
- Motivo gráfico: arcos.
- Sem fotos de pessoas. A imagem principal é um mockup de WhatsApp e um mockup do app no celular.
- Tom visual: sóbrio, refinado, de clínica de alto padrão. Nada de visual de infoproduto, selos, contadores ou urgência artificial.

## O que quero entregar

Um protótipo do site em HTML único (`site/design-v1.html`), responsivo (celular primeiro), com as 13 seções da `copy-v3.html` na mesma ordem. Os textos vêm da copy. Não reescreva a copy: se achar que um texto atrapalha o design, me avise e eu ajusto na outra conversa.

## Como quero trabalhar

1. Primeiro, leia os arquivos e me diga em poucas linhas o que entendeu. Não construa nada ainda.
2. Depois, me mostre 2 caminhos de layout para a abertura (primeira dobra), com a headline "Foque nos seus pacientes. Deixe a IA cuidar do resto." e a subheadline que está na copy. Eu escolho um.
3. Com o caminho escolhido, vá seção por seção. Mostre a seção pronta no navegador e espere meu "ok" antes de seguir.
4. As seções com peso visual são: a abertura, o mockup do WhatsApp (demonstração), o app da clínica (seção 6, é o diferencial) e o painel de valores recuperados. As demais podem ser mais enxutas.
5. Ao final de cada seção, diga em uma linha o que mudou e o que falta.

## Regras

- Uma coisa por vez. Faça só o que eu pedir, sem melhorar o que não foi pedido.
- Nada de números, depoimentos ou selos inventados. Se um espaço precisar de prova que ainda não existe, deixe um espaço claro marcado como placeholder.
- O botão principal é "Agendar diagnóstico grátis". O segundo botão ("Conversar com a assistente") só aparece quando a demonstração ao vivo existir, então deixe-o preparado, mas escondido.
- Não publique nada e não faça commit sem eu pedir.
- Se houver dúvida de marca, vale o que está em `branding/` e na skill `keshion-marca`.
