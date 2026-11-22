# Resumo da sessão: correções e testes da Sarah (Keshion)

Período: 09 e 10/11/2026
Projeto: Negócio de IA para Clínicas (Keshion), clínica demo da Dra. Suzana

## 1. O que você pediu

1. Comparar o seu prompt mestre de auditoria com o que já existe no projeto e dizer o que inserir, mudar ou remover, com o meu ponto de vista.
2. Aplicar as suas decisões na base, nas instruções e no Make.
3. Depois dos seus testes (aba "Testes - Erica"): verificar tudo e continuar as correções.
4. Eu mandar mensagens para a Sarah, avaliar as respostas e registrar na planilha, para você ver e comentar.
5. "Aplique agora": aplicar os 5 ajustes encontrados.

## 2. Decisões tomadas por você

- Manter o nome **Sarah** e os tratamentos da base.
- Identidade: "Sarah, assistente da clínica da Dra. Suzana" ou "da equipe da Dra. Suzana". Só usa a palavra "virtual" se perguntarem.
- Só **1 dentista**: sai o Dr. Rafael, a Dra. Camila e o serviço de implantes.
- **Remarcar e cancelar** fazem parte do fluxo.
- Sem mensagem de "não quero receber mais mensagens". Parar de retomar o contato é decidido pela conversa.
- O paciente precisa ter **histórico** (para follow-up e confirmação de consultas), então o CRM será conectado.
- Manter o tom atual da mensagem inicial e todos os diferenciais.
- A base manda: o prompt mestre estava atrasado em relação a ela.
- Lembrar do **#reiniciar** no piloto com a Dra. Vivian.
- Site e Instagram: verificar só quando for uma clínica real.

## 3. O que foi feito

### Documentos (pasta `negocio-ia-clinicas`)
- `clientes/clinica-demo/base-clinica.md`: reescrita, só Dra. Suzana. Sem implantes, protocolo, siso e canal. Pagamento por Pix, cartão de crédito e débito, transferência (5% à vista no Pix ou na transferência). Agenda de até 90 dias. Perguntas frequentes e seção 11 com perguntas que não precisam de pessoa (objeções, outras clínicas, outros pacientes e urgência).
- `clientes/clinica-demo/instrucoes-sarah.md`: novo. Regras de A a P e H2, mais as regras 1 a 15 de agendar, remarcar e cancelar. Saída em JSON.
- `tecnico/especificacao-sarah.md`: novo. Especificação completa e seção 8 com as correções aplicadas e o que falta.
- `clientes/clinica-demo/roteiro-teste-respostas.md`: versão 2, com 38 testes.
- `CLAUDE.md` do projeto: registradas as decisões e correções de 09/11.

### Make (equipe 3084523)
- **1A Entrada**, **1B Resposta**, **1C Fechamento** e **1D Envio** ajustados.
- Data store `_base` e `_instrucoes` atualizados com os textos novos.
- A Sarah responde em até 3 mensagens, junta mensagens rápidas (fila de 7 segundos, só a última responde), marca, bloqueia marcação em dobro, remarca (mesmo evento), cancela e limpa a ficha.
- Rotas de erro com mensagem de segurança: "Só um instante, vou verificar aqui e já te retorno."

### Planilha "Keshion · Teste da Sarah"
- Aba "Testes - Claude": testes e avaliações (linhas 1 a 64) e **reteste nas linhas 66 a 80**.
- Coluna "Observações da Erica" livre para você anotar.

## 4. Os 5 ajustes aplicados

1. **Oferta de avaliação repetida**: agora oferece, deixa a pessoa responder e só volta a oferecer quando faz sentido.
2. **Nome pedido várias vezes**: pede uma vez só.
3. **Chamar a equipe sem precisar** (achei caro, concorrente, outra paciente): ela responde sozinha.
   - Concorrente: "Prefiro não comentar o trabalho de outras clínicas, mas aqui a Dra. Suzana mostra tudo com calma na avaliação."
   - Outro paciente: "Por privacidade, só consigo passar informações sobre o seu próprio atendimento."
4. **Dor**: sempre deseja melhoras, sem repetir o problema.
5. **Urgência com a clínica aberta**: orienta pronto-socorro se houver dificuldade para respirar ou engolir e avisa que vai falar com a Dra. Suzana sobre um encaixe hoje.

Defeito novo achado no reteste e corrigido: ela copiava a expressão "com gentileza" das instruções. Troquei por frases de exemplo e incluí a regra de não copiar palavras das instruções.

## 5. Resultado do reteste

12 linhas: **9 Ok e 3 ajustes pequenos**.

Pontos pequenos que restam:
- A oferta de avaliação às vezes volta um pouco antes do previsto.
- Na pergunta do dente escuro, ela acrescentou "não fazemos canal" sem ninguém perguntar.
- A resposta sobre dor de dente ficou um pouco longa.

## 6. Problemas que aconteceram (e a lição)

- Um loop de espera em bash bateu no webhook do 1B e gerou cerca de 46 requisições vazias. O cenário ficou inválido. Corrigido apagando as requisições vazias e reativando.
- **Lição:** nunca chamar a URL de webhook para esperar. Usar espera em segundo plano.
- O Git Bash enviou os acentos em latin1. A Sarah entendeu do mesmo jeito.

## 7. O que ainda falta

- Proteção contra chamada sem telefone no 1B.
- Pausar a Sarah quando a equipe assume a conversa.
- CRM em Google Planilhas (histórico do paciente).
- Confirmações, lembretes e retomada de conversas (teste 38 do roteiro).
- Várias mensagens no mesmo aviso do WhatsApp.
- **Remover o #reiniciar antes do piloto com a Dra. Vivian.**
- Migração para o n8n (decidida como futura, por causa do custo de créditos do Make). Ainda não migrar.
- Atualizar a memória da pendência de correções, que já foi cumprida.

## 8. Próximo passo

Você anota as observações na coluna "Observações da Erica" da planilha (testes e reteste). Com as suas anotações, sigo a partir delas. Nenhuma outra correção será iniciada sem o seu pedido.
