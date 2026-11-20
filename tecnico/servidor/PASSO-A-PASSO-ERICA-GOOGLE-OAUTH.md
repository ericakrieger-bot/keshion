# Google Agenda da Clara: tirar o app do "modo Teste" (passo a passo para a Erica)

Preparado em 20/11/2026. **É o item de operação mais urgente antes do piloto de 01/12.** Nada aqui mexe nas mensagens da Clara nem reinicia o n8n. Leva uns 15 minutos.

## Para que serve (em simples)

A Clara consulta e marca avaliações no Google Agenda da clínica demo por uma "ligação" que você autoriza uma vez. Hoje o app do Google que faz essa ligação está em **modo Teste**, e o Google desfaz a autorização **depois de 7 dias**. Foi o que aconteceu em 19/11 (erro `invalid_grant`): a agenda parou e você precisou reconectar. A autorização de agora vale só até cerca de **26/11**. Se isso acontecer no meio do piloto, a Clara deixa de ver e de marcar horários.

A solução é **publicar o app** (mudar de "Testing" para "In production"). Não custa nada. Depois você reconecta **uma última vez** no n8n.

## O que você vai ver de diferente

- Como o app pede acesso à agenda (um acesso que o Google chama de "sensível"), ele **não será verificado** pelo Google. Isso é normal para uso interno. Na tela de autorização vai aparecer "O Google não verificou este app": clique em **Avançado** e depois em **Acessar Keshion (não seguro)** (o texto exato pode mudar). É a sua própria conta autorizando o seu próprio app.
- Esse aviso só aparece nessa hora da autorização. A Clara e as pacientes nunca veem.

## Antes de começar

- Use o navegador onde você já está logada na conta **keshion.ai.2026@gmail.com** (a conta Google da demo).
- Tenha o n8n aberto em outra aba: `https://n8n.169-58-41-107.sslip.io`.
- **Não mande no chat** nenhum Client ID, Client Secret, código ou link de autorização. Se precisar mostrar uma tela, tire um print **cobrindo esses campos**.
- As telas do Google mudam de nome de vez em quando. Se alguma for diferente, tire um print e mande: a Claude te guia pela tela que aparecer.

## Parte 1: achar o app certo no Google

1. No n8n, abra **Credentials** (Credenciais) e clique na credencial do **Google Calendar** da demo. Anote **só os 6 primeiros caracteres** do Client ID (ele termina em `.apps.googleusercontent.com`). Não copie o Client Secret.
2. Abra **console.cloud.google.com** (conta keshion.ai.2026). No topo, clique no seletor de projeto e escolha o projeto onde criamos o acesso ao Google Agenda.
3. Menu **APIs e serviços > Credenciais**. Confira que existe um "ID do cliente OAuth" cujo começo é igual ao que você anotou. Se achar, é o projeto certo. Se não achar, tente outro projeto da lista (ou me chame).

## Parte 2: publicar o app

1. No mesmo projeto, abra **Google Auth Platform** (ou **APIs e serviços > Tela de permissão OAuth**).
2. Vá em **Público-alvo** (em inglês, **Audience**). Em "Status da publicação" deve estar **Teste** (Testing).
3. Clique em **Publicar app** (**Publish app**) e confirme. O tipo de usuário continua **Externo**.
4. Confira que o status virou **Em produção** (**In production**). Se aparecer uma mensagem pedindo "verificação", **não precisa fazer agora**: o app já funciona sem ela para a sua conta (limite de 100 usuários, e só a sua conta usa).
5. Em **Acesso a dados** (Data access), confira que o único acesso da agenda é o do Google Calendar que já está lá. **Não adicione nem tire nada.**

## Parte 3: reconectar uma última vez no n8n

A autorização antiga foi dada no modo Teste e continua com prazo de 7 dias. Uma autorização nova, dada **depois** de publicar, não expira mais assim.

1. No n8n, abra a credencial do **Google Calendar** da demo e clique em **Sign in with Google** (Entrar com o Google).
2. Escolha a conta **keshion.ai.2026@gmail.com**. Se aparecer "O Google não verificou este app", clique em **Avançado > Acessar Keshion** e depois **Permitir** (marque o acesso à agenda).
3. Volte ao n8n: a credencial deve mostrar **Conectado** (verde). Salve.
4. A clínica de teste usa a **mesma credencial**, então ela também volta sozinha.

## Parte 4: conferir

1. Avise a Claude que terminou. Ela confere pelo n8n que a agenda responde (consulta de horários) **sem reiniciar o n8n** e sem mandar mensagem a ninguém.
2. Se der erro `invalid_grant` de novo em menos de uma semana, o app não ficou "Em produção": volte à Parte 2, passo 3.
3. Daqui a **8 a 10 dias** (por volta de 29/11 a 01/12), peça à Claude para conferir de novo. Se a agenda ainda responder, está resolvido de vez.

## Se algo der errado

- A Clara continua atendendo. Só a agenda fica sem resposta, e ela avisa a equipe e não marca nada (o fluxo trata a falha da agenda).
- Voltar atrás: não precisa. Se a nova autorização falhar, repita a Parte 3 (a credencial antiga continua valendo até o prazo dela).
- Nunca apague o "ID do cliente OAuth" no Google nem a credencial no n8n: perde-se a ligação e é preciso refazer tudo.

## Depois

Quando estiver feito, atualizar o `tecnico/RETOMAR-AQUI.md` (linha "Google Agenda") e, no piloto da Dra. Vivian, repetir o mesmo processo no Google dela se ela usar outra conta Google (fica em outra conversa).
