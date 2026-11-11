# Make x n8n x VPS (Hostinger e Contabo)

> Comparação feita em 29/10/2026 para a Keshion. Os preços vêm de fontes de terceiros de agosto a outubro de 2026, que nem sempre concordam entre si. Confirmar na página oficial de cada empresa antes de assinar.

## 1. Quanto cada um consome numa clínica

Conta de referência: uma clínica com cerca de 100 mensagens por dia, ou 3.000 por mês.

- **Make cobra por crédito.** Cada módulo que roda gasta pelo menos 1 crédito. Um atendimento passa por 8 a 12 módulos (receber, desviar áudio, transcrever, IA, gravar na planilha, mandar para aprovação, enviar). Isso dá cerca de 30 mil créditos por mês por clínica.
- **n8n Cloud cobra por execução.** Uma execução é o fluxo inteiro rodando uma vez, não importa quantos passos tenha. As mesmas 3.000 mensagens dão cerca de 3.000 execuções por mês.
- **n8n no servidor próprio (VPS)** não tem limite de execução. O limite é a capacidade do servidor, e um servidor de 8 GB aguenta várias clínicas.

## 2. Make x n8n

| Critério | Make | n8n Cloud | n8n no servidor próprio |
|---|---|---|---|
| Preço de entrada | Core: cerca de US$ 9 (anual) a US$ 10,59 (mensal) por 10 mil créditos | Starter: cerca de € 20 (anual) a € 24 (mensal) por 2.500 execuções | Só o servidor: cerca de US$ 5 a 15 por mês |
| Custo por clínica de 3.000 mensagens | Cerca de 30 mil créditos: pacote maior do Core, na faixa de US$ 30 a 40 por mês (confirmar a tabela de créditos) | Passa do Starter: Pro, cerca de € 50 a 60 por mês por 10 mil execuções | Quase zero a mais por clínica |
| Custo com 5 clínicas | Cerca de 150 mil créditos: US$ 150 ou mais por mês | 15 mil execuções: passa do Pro | O mesmo servidor, cerca de US$ 15 por mês |
| O que acontece quando acaba o limite | Dá para comprar mais créditos automaticamente | Os fluxos param até o mês virar | Não tem limite |
| Facilidade | A mais fácil. Montagem visual, muitos módulos prontos, já conectado ao Claude Code por MCP | Média. Mais técnico, mas com nós prontos de IA | A mais difícil. Vocês cuidam de atualizações, cópias de segurança e segurança |
| Projetos paralelos | Cenários ilimitados no Core. O plano Teams separa cada cliente em equipe própria | Pastas e projetos dentro da conta | Ilimitados, tudo no mesmo servidor |
| Copiar e adaptar uma automação | Clonar o cenário ou exportar como arquivo (blueprint) e importar em outra conta. Depois, trocar as conexões da clínica nova | Copiar e colar os nós ou exportar o fluxo em arquivo (JSON). Depois, trocar as credenciais | Igual ao n8n Cloud |
| Flexibilidade | Boa para quase tudo do projeto | Alta: aceita código, agentes de IA e fluxos longos | Alta, sem limite de tempo de execução |
| Regra de licença | Sem restrição para atender clientes | Sem restrição para atender clientes | Pode rodar fluxos para clínicas desde que a clínica nunca acesse o n8n |

**Leitura:** o Make é o mais rápido para colocar o piloto no ar, mas cobra por passo e encarece em ritmo constante a cada clínica nova. O n8n no servidor próprio é quase de graça por clínica, mas exige alguém cuidando do servidor (aqui, o Claude Code faz essa parte com vocês).

## 3. n8n pago (Cloud) x n8n no servidor próprio (VPS)

| Critério | n8n Cloud (pago) | n8n no VPS |
|---|---|---|
| Custo mensal | € 20 a 60 e sobe com o volume | US$ 5 a 15 fixo, para várias clínicas |
| Limite | Execuções por mês (2.500 no Starter, 10 mil no Pro) | Só a capacidade do servidor |
| Manutenção | A n8n cuida de atualização, cópia de segurança e disponibilidade | Por conta de vocês: atualizar, fazer cópias de segurança e proteger o acesso |
| Tempo para começar | Minutos | 1 a 2 horas na primeira vez (a Hostinger tem modelo pronto com n8n instalado) |
| Quando faz sentido | Quem quer n8n sem cuidar de servidor e tem pouco volume | Quem vai atender várias clínicas e quer custo fixo baixo |

**Leitura:** para a Keshion, o n8n Cloud fica no pior dos dois mundos: mais caro que o Make no começo e com limite de execução que trava os fluxos. Se for para o n8n, o caminho é o servidor próprio.

## 4. Hostinger x Contabo (servidor para o n8n)

| Critério | Hostinger KVM 2 | Contabo Cloud VPS 10 |
|---|---|---|
| Preço | Cerca de US$ 7 a 9 por mês na promoção (contrato de 24 a 48 meses). Na renovação, cerca de US$ 15 | Cerca de € 4,40 por mês. Na renovação, cerca de € 5,50 |
| Configuração | 2 vCPUs, 8 GB de memória, 100 GB de disco NVMe, 8 TB de tráfego | Mais processador e disco pelo mesmo preço (confirmar a configuração atual na página) |
| Taxa de instalação | Não tem | Fontes recentes dizem que foi retirada em 2026. Confirmar no checkout |
| n8n pronto | Sim: modelo com n8n já instalado em um clique | Não: instalação manual (ou com o Claude Code guiando) |
| Painel e facilidade (UX) | Painel simples, em português, com assistente de IA | Painel antigo e mais técnico |
| Suporte | Chat 24 horas em português | Mais lento, por e-mail e em inglês |
| Pagamento | Em reais, com Pix e cartão brasileiro (Hostinger Brasil) | Em euro, só com cartão internacional ou PayPal |
| Domínio grátis | As fontes divergem: algumas ofertas de VPS incluem domínio grátis no 1º ano, outras não. Para vocês não importa, porque o keshion.com.br vai no registro.br | Não tem |
| Estabilidade | Boa e constante | Conhecida por desempenho que varia (servidores mais cheios) |

**Leitura:** a Contabo é mais barata por recurso, mas a Hostinger é bem mais fácil para quem não é programador: n8n em um clique, painel em português, suporte em português e pagamento em reais. A diferença de preço fica em cerca de US$ 5 a 10 por mês.

## 5. Recomendação

1. **Agora, até o piloto de 09/11: ficar no Make (plano Core).** O plano já está desenhado para ele, a conta já está conectada ao Claude Code e o prazo é curto. Não é hora de trocar de ferramenta.
2. **Gatilho para migrar:** quando chegar a 3 clínicas ou quando a conta do Make passar de cerca de US$ 50 por mês, o que vier primeiro.
3. **Para onde migrar:** n8n no servidor próprio, na **Hostinger (KVM 2, com o modelo do n8n)**. O n8n Cloud não compensa para este projeto. A Contabo só vale se vocês ficarem confortáveis com uma operação mais técnica.
4. **Para facilitar a migração depois:** desde já, manter a base da clínica, o manual de voz e os textos das IAs em arquivos separados (não escritos dentro dos cenários do Make). Assim, migrar é refazer os fluxos, não reescrever o conteúdo.

## Fontes

- Make: [Jetadmin](https://www.jetadmin.io/blog/make-pricing/), [Latenode](https://latenode.com/pt-br/blog/precos-do-make-com-em-2026-planos-creditos-e-quanto-custa-executar-um-fluxo), [Costbench](https://www.costbench.com/software/ai-automation/make/)
- n8n: [Jetadmin](https://www.jetadmin.io/blog/n8n-pricing/), [Sliplane](https://sliplane.io/blog/n8n-pricing), [Automation Atlas](https://automationatlas.io/answers/n8n-pricing-self-hosted-vs-cloud-2026/)
- Hostinger: [Hora de Codar](https://horadecodar.com.br/custo-n8n-vps-hostinger/), [RamNode](https://www.ramnode.com/ramnode-hostinger), [página de VPS da Hostinger](https://www.hostinger.com/vps-hosting.md)
- Contabo: [PricingSaaS (aumento de junho/2026)](https://pricingsaas.com/companies/contabo.main/diffs/2026W25), [OneDollarVPS](https://onedollarvps.com/pricing/contabo-pricing), [Toolradar](https://toolradar.com/tools/contabo/pricing)
