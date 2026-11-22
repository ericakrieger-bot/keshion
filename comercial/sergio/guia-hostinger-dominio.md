# Guia do Sérgio: proteger o domínio keshion.com e a conta da Hostinger

Para o Sérgio, 22/11/2026. Tarefa no Notion: "Proteger o domínio keshion.com e a conta da Hostinger" (prazo 24/11). Tempo: cerca de 30 minutos.

**Por que importa:** o keshion.com é o endereço do site, do e-mail contato@keshion.com e do app. Se o domínio vence sem querer ou alguém invade a conta, a gente perde o e-mail e o endereço de uma vez, e recuperar pode levar semanas.

> Os nomes dos menus da Hostinger mudam de vez em quando. Se algum não aparecer igual, procure pela palavra principal (por exemplo "Segurança" ou "Renovação") ou use o chat de ajuda da Hostinger. **Nunca mande senha ou código no WhatsApp nem no e-mail**: senhas ficam só no Bitwarden.

## 1. Proteger a conta (10 min)

1. Entrar em hpanel.hostinger.com com a conta onde o domínio está.
2. Ir em **Perfil** (canto superior direito) → **Segurança**.
3. Ligar a **verificação em duas etapas** (2FA) com um aplicativo autenticador (Google Authenticator, Microsoft Authenticator ou o próprio Bitwarden). Guardar os **códigos de recuperação** no Bitwarden.
4. Conferir que a senha da conta é forte e única (só usada aqui) e está guardada no Bitwarden.
5. Conferir o **e-mail de contato da conta**: tem de ser um e-mail que a gente lê sempre. É para lá que vão os avisos de vencimento.

## 2. Proteger o domínio (10 min)

1. No menu **Domínios**, abrir o **keshion.com**.
2. **Renovação automática:** ligada. Conferir a data de vencimento e se o cartão cadastrado ainda vale. Anotar a data no Notion (Finanças, linha da Hostinger: "Próxima cobrança").
3. **Bloqueio de transferência** (às vezes chamado "Transfer lock" ou "Bloqueio do domínio"): ligado. Impede que alguém leve o domínio para outra empresa.
4. **Proteção de privacidade** ("WHOIS privacy" ou "Proteção de privacidade"): ligada, para não expor nome, telefone e endereço na internet.
5. Conferir os **dados do titular**: nome e e-mail certos. Hoje o domínio está no CPF de um de vocês; quando houver CNPJ, transferir para a empresa.

## 3. E-mail que não cai no spam (10 min, pode ser junto com a Erica)

É a tarefa "Configurar o e-mail do keshion.com para não cair no spam" (prazo 24/11).

1. No hPanel, abrir **E-mails** → keshion.com e procurar **Configurações de DNS** ou **Autenticação**.
2. Conferir se aparecem como ativos os três registros: **SPF**, **DKIM** e **DMARC**. Muitas vezes a Hostinger cria SPF e DKIM sozinha; o DMARC às vezes precisa ser ligado.
3. Se algum estiver faltando, usar o botão de configurar automaticamente ou pedir pelo chat da Hostinger: "Quero SPF, DKIM e DMARC ativos para o domínio keshion.com".
4. Teste: mandar um e-mail de contato@keshion.com para um Gmail e ver se chega na caixa de entrada, não no spam.

## 4. Quando terminar

- Marcar a tarefa como Feita no Notion (ou avisar a Erica).
- Contar no grupo: "2FA ligado, renovação automática ligada, bloqueio ligado, vencimento em DD/MM". Sem senha, sem código.
