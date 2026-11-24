# Guia de marca Keshion AI

> Fonte de verdade da marca. Atualizado em 17/11/2026 com o Manual de Marca e o Kit de Marca oficiais.
> **Regra:** todo material da Keshion (site, app, redes sociais, propostas, contratos, apresentações, SOPs, questionários, documentos, e-mails, avatar do WhatsApp) segue este guia. Antes de gerar qualquer material visual, ler este arquivo.

## Onde estão os arquivos

| O quê | Onde |
|---|---|
| Manual de marca (PDF, 5 páginas) | `branding/kit/Keshion_AI_Manual_de_Marca.pdf` |
| Logos (SVG e PNG transparente, 4 versões + símbolo) | `branding/kit/logos/` |
| Ícones: app 1024/512/192, maskable, apple-touch, favicon, avatar do WhatsApp | `branding/kit/icones/` |
| Imagem de compartilhamento 1200x630 | `branding/kit/midias/` |
| CSS com fontes e variáveis, tokens JSON, manifest PWA | `branding/kit/digital/` |
| Fontes Manrope e Inter (variáveis) e licenças | `branding/kit/fontes/` |
| Instruções oficiais do kit | `branding/kit/LEIA-ME.md` |
| Comparativo antigo de paletas (arquivo morto, não usar) | `branding/historico/` |

## 1. Logo

- Wordmark em minúsculas: **keshion AI**, com o "o" substituído pelo símbolo de dois arcos (azul e verde). O "o" remete à conexão que inspira o nome.
- **Nunca digitar "KESHION AI" em caixa alta como se fosse o logo.** O logo é sempre o arquivo. Em texto corrido, escrever "Keshion AI".
- Versões:

| Arquivo | Usar sobre |
|---|---|
| `keshion-ai-fundo-escuro` | Azul-noite (#0B1126) e marinho (#17233E): site, app, apresentação |
| `keshion-ai-fundo-claro` | Branco, branco-gelo, névoa: PDF, contrato, proposta, documento |
| `keshion-ai-monocromatico-escuro` | Fundo névoa ou claro, impressão em uma cor |
| `keshion-ai-monocromatico-claro` | Fundo marinho ou escuro, quando não pode ter cor |
| `simbolo.svg` | Áreas pequenas, ícones, avatar |

- **Tamanho mínimo:** logo completo com 160 px de largura. Abaixo disso, usar só o símbolo.
- **Margem de respiro:** pelo menos ¼ da altura do "o" ao redor.
- Não esticar, não girar, não trocar as cores do símbolo, não aplicar sombra nem contorno. (Bom senso: o manual não lista proibições. Se a Erica definir outras, registrar aqui.)

## 2. Cores

| Nome | Hex | Uso |
|---|---|---|
| Azul-noite | `#0B1126` | Fundo escuro principal, texto sobre claro |
| Azul | `#4388E8` | Ação principal em interface escura, acentos |
| Verde | `#55C96A` | Símbolo e destaques sobre fundo escuro. Reservar o verde vivo para isso |
| Branco-gelo | `#F7F8F4` | Fundo claro principal, texto sobre escuro |
| Marinho | `#17233E` | Cards e superfícies no tema escuro |
| Névoa | `#E8EFF9` | Cards e superfícies no tema claro, caixas de destaque |
| Azul intenso | `#2459A6` | Ação principal em interface clara, títulos de seção em documento |
| Ardósia | `#50596A` | Texto secundário no tema claro |
| Prata | `#CCD5E6` | Texto secundário no tema escuro (token do kit) |

### Temas (valem para site, app e qualquer interface)

| | Claro | Escuro |
|---|---|---|
| Fundo | #F7F8F4 | #0B1126 |
| Superfície | #E8EFF9 | #17233E |
| Texto | #0B1126 | #F7F8F4 |
| Texto secundário | #50596A | #CCD5E6 |
| Ação (botão) | #2459A6 | #4388E8 |
| Texto do botão | #F7F8F4 | #0B1126 |
| Foco | #2459A6 | #55C96A |

### Contraste medido (WCAG)

| Combinação | Razão | Pode? |
|---|---|---|
| Azul-noite sobre branco-gelo | 17,5 | Sim, qualquer tamanho |
| Ardósia sobre branco-gelo | 6,6 | Sim |
| Azul intenso sobre branco-gelo | 6,4 | Sim (links, botões, títulos) |
| Azul sobre branco-gelo | 3,3 | **Não para texto pequeno.** Só elementos grandes e ícones |
| Verde sobre branco-gelo | 2,0 | **Não.** Nunca como texto ou ícone essencial em fundo claro |
| Azul sobre azul-noite | 5,3 | Sim |
| Verde sobre azul-noite | 8,9 | Sim |
| Prata sobre azul-noite | 12,7 | Sim |

## 3. Tipografia

- **Manrope 700** nos títulos. **Inter 400** no texto corrido. **Inter 600** em botões e rótulos.
- Hierarquia digital: título principal Manrope 700 de 44 a 56 px; títulos de seção Manrope 700 de 28 a 36 px; texto Inter 400 de 16 px; botões e rótulos Inter 600 de 14 a 16 px.
- Rótulos pequenos de seção: Inter 600, caixa alta, com espaçamento entre letras (padrão visto no manual: "IDENTIDADE VISUAL", "01 / LOGO").
- Fontes variáveis em `branding/kit/fontes/` (licença OFL, uso livre, inclusive embutir). No Word/PowerPoint a fonte só aparece se estiver instalada no computador: preferir PDF.
- Na web: carregar `branding/kit/digital/keshion.css` e usar `data-keshion-theme="dark"` no elemento escuro.

## 4. Tom de voz

- **Direto, acolhedor e profissional.**
- Descrever o que a automação faz na prática, sem promessa vaga.
- Exemplos do manual: botão "Ver demonstração"; status "Consulta confirmada".
- Português do Brasil com acentos, sem travessão (regra do projeto).

## 5. Aplicações por canal

| Canal | Tema | Regras |
|---|---|---|
| Site | Escuro (azul-noite) como padrão, claro para conteúdo longo | Logo SVG no cabeçalho; `favicon.svg`/`favicon.ico`; `apple-touch-icon-180.png`; `compartilhamento-1200x630.png` em `og:image` com URL pública absoluta |
| App / CRM / painel | Claro e escuro (seguir o tema do sistema) | Ícone `app-icon-1024.png`; PWA com `site.webmanifest` (theme/background #0B1126) |
| WhatsApp | Avatar `avatar-whatsapp-1080.png` | Símbolo centralizado com margem para o recorte circular |
| Apresentação comercial | Escuro na capa e nos slides de impacto | Logo fundo escuro na capa; Manrope nos títulos |
| **PDF e documento impresso ou assinado** (contrato, proposta, questionário, SOP, manual, relatório) | **Sempre claro. Nunca fundo escuro** (pedido da Erica, 12/11/2026) | Fundo branco ou branco-gelo; texto azul-noite; títulos em azul intenso; logo "fundo claro" no cabeçalho; caixas de destaque em névoa com borda fina; verde só em detalhes pequenos |
| Redes sociais | Escuro ou claro | Seguir a seção 7 (ícones Lucide, arcos, mockup de WhatsApp, sem foto de pessoa). Modelos ainda não existem |
| Materiais da clínica para o paciente | Marca da clínica, não a da Keshion | Keshion aparece no máximo como "feito por Keshion AI" |

## 6. Estilo de interface (visto nos exemplos do manual)

- Cantos arredondados (cerca de 8 a 12 px), cards com borda fina, muito espaço livre.
- Linha divisória fina sob o cabeçalho; rótulo pequeno em caixa alta à direita.
- Botão com cantos arredondados, texto em Inter 600.

## Tokens de referência

Usar direto `branding/kit/digital/keshion.css` (variáveis `--keshion-*`) e `keshion-tokens.json`. Não recriar paleta à mão.

## Dados de contato e frase de marca (17/11/2026)

- **Domínio:** keshion.com (não usar .com.br). **E-mail:** contato@keshion.com. App: app.keshion.com.
- **Frase de marca (aprovada em 17/11/2026):** "Keshion · automações inteligentes" (ideia da Erica, escrita em minúsculas depois do nome). O descritor do manual, "Agentes de IA para atendimento no WhatsApp", fica como subtítulo do produto atual.
- **Assinatura de e-mail:** modelo em `branding/modelos/assinatura-email.html` (sem nome por enquanto: logo, frase, e-mail e site).

## Nome do produto (decidido pela Erica em 24/11/2026)

- **Assistente Inteligente** é o nome do produto: o atendente de IA no WhatsApp da clínica, mais o app. Em frase corrente, "o assistente inteligente da Keshion".
- **Clara** deixa de ser nome público. Pode seguir como nome interno da demo e dos fluxos técnicos, mas não aparece em site, redes, propostas nem materiais da clínica.
- **Keshion AI** continua sendo a marca (sempre pelo logo, nunca digitada no lugar dele). No site, o nome do produto fica em um ponto único de troca (`NOME_PRODUTO` em `site/copy-v4.html`).
- O paciente da clínica vê o nome da clínica no WhatsApp, não o nome do produto.

## Os SVGs do kit são os arquivos editáveis

Os logos e ícones em `kit/logos` e `kit/icones` são vetoriais (SVG): abrem e editam no Figma, Canva, Illustrator ou Inkscape. As letras do logo já são curvas, então não precisam de fonte. Não existe arquivo-fonte original nem logo vertical: para os dois, usar o símbolo isolado ou pedir ao designer.

## 7. Direção visual: fotos, ícones e ilustração (APROVADA pela Erica em 17/11/2026)

Detalhes e exemplos: `branding/direcao-visual.html` (abrir no navegador) e `branding/direcao-visual.md`.

**Ícones**
- Traço de 2 px, pontas e cantos arredondados. Biblioteca única: **Lucide** (licença ISC). Não misturar com outra biblioteca na mesma tela.
- Cor: azul-noite no traço, com um detalhe em azul (fundo claro) ou em verde (fundo escuro). Nunca verde sobre fundo claro.
- Tamanho: 24 px na interface; 48 a 64 px em seções de site.

**Elementos gráficos e ilustração**
- Motivo da marca: os dois arcos do símbolo, grandes, cortados pela borda, em azul e verde com baixa opacidade (cerca de 25 a 30%) sobre azul-noite. Usar em capas e em fundos de seção do site.
- Formas: círculos, arcos e cantos arredondados de 8 a 12 px. Sem degradês fortes, sem sombras pesadas.
- Para explicar o serviço: diagrama simples de três passos (mensagem chega, assistente responde, consulta confirmada) com ícones de traço e setas finas.

**Fotos**
- **Padrão: sem foto de pessoa.** A imagem principal é a conversa de WhatsApp em um celular (mockup), com mensagens de teste. Vale para o primeiro site e para materiais de venda.
- Quando precisar de foto: cenas de clínica sem rosto (mãos com o celular, recepção desfocada, agenda aberta), luz natural e suave, tons neutros. Sobre fundo escuro, aplicar camada de azul-noite (duotone).
- Pessoas reais só depois de ter clientes e com autorização escrita de uso de imagem. Sem foto de banco de "pessoa sorrindo para a câmera".

**Evitar sempre**
- Robôs, cérebros digitais, luzes de neon, rede de pontos azuis.
- Foto de paciente real ou print de conversa real (LGPD): só dados de teste.
- Misturar estilos de ícone ou de ilustração.
- Verde vivo como texto em fundo claro.

## O que ainda não existe

Dados oficiais da empresa (CNPJ, razão social, endereço), nome e telefone para a assinatura, modelos de redes sociais, apresentação, proposta, contrato e SOP, logo vertical.
