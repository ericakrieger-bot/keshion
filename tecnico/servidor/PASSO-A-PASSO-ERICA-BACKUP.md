# Backup: o que a Erica precisa fazer (B2 e B5)

Feito em 18/11/2026. Nenhum dos dois passos mexe na Clara nem reinicia o n8n. Senha, chave e links secretos **nunca vão no chat**: ficam no Bitwarden e no arquivo `.env` do PC (`Documents\Claude Code\keshion\.env`).

Telas do Google e do Healthchecks mudam de vez em quando. Se uma tela for diferente, tire um print e mande: a Claude te guia pela tela que aparecer.

---

## B2. Alerta por e-mail quando o backup falha ou não acontece (Healthchecks.io)

**Para que serve (em simples):** hoje, se o backup falhar ou nem rodar (servidor desligado, cron parado), ninguém fica sabendo até alguém abrir o arquivo de status. O Healthchecks.io é um "porteiro" fora do servidor: o backup avisa "comecei", "terminei bem" ou "falhei". Se até as 04h de Curitiba não chegar um "terminei bem", ele manda um e-mail para você. Vale também quando o servidor inteiro cai, porque o porteiro está fora dele.

**Custo e privacidade:** o plano gratuito basta (um único aviso por dia). Só precisa de e-mail. O aviso leva apenas a etapa e o código do erro, nunca dados de paciente.

**Precisa do seu OK para criar a conta.** Quando você disser sim, a conta pode ser criada por você (recomendado, com o e-mail e a senha ficando só com você e no Bitwarden) ou pela Claude na tela com você olhando.

Passos:

1. Entrar em healthchecks.io e criar a conta com o e-mail que você quer receber os alertas (sugestão: um que você olhe todo dia). Guardar a senha no Bitwarden.
2. Criar um "check" chamado **Backup Keshion**:
   - Schedule: **Cron expression** `0 3 * * *`, fuso **America/Sao_Paulo**.
   - Grace Time: **1 hour** (assim o alerta chega até as 04h).
3. Em Integrations, conferir que o **Email** da sua conta está ligado para esse check.
4. Copiar o **ping URL** do check (endereço secreto, começa com `https://hc-ping.com/`). Quem tiver esse endereço consegue mandar "estou vivo" falso, então trate como senha.
5. Abrir o `.env` do PC (`Documents\Claude Code\keshion\.env`) e acrescentar uma linha, sem aspas:
   `HC_BACKUP_URL=<o endereço copiado>`
   Guardar também no Bitwarden. **Não mandar o endereço no chat.**
6. Avisar a Claude. Com o seu OK, ela copia essa linha para `/opt/keshion/.env` no servidor (sem mostrar o valor), instala o script novo e confere na tela do Healthchecks que o check ficou verde depois do próximo backup (ou de um backup manual, que também só roda com o seu OK).
7. Teste do alerta (opcional, recomendado uma vez): no Healthchecks, o botão **Pause** e depois esperar passar do horário mostra que o e-mail chega; ou usar o botão de teste da integração de e-mail.

**Dono e substituto (decidido em 21/11, no Notion):** a Erica recebe o alerta e o Sérgio é o substituto. Até o alerta existir, o executor das 14h confere o backup todo dia e avisa no daily.

**Resposta ao e-mail de alerta:** abrir o status no servidor (`cat /opt/keshion/backups/STATUS-BACKUP.txt`, ou pedir à Claude). `FALHA` mostra a etapa; sem alteração desde ontem significa que o cron ou o servidor não rodou.

---

## B5. Cliente do Google próprio para o backup (antes de 01/12/2026)

**Para que serve (em simples):** o programa que envia o backup ao Google Drive (rclone) usa uma "identidade" emprestada, compartilhada com milhares de pessoas, que o Google vai desligar em 2026 (sem data confirmada). Quando desligar, o envio para de funcionar. A solução é criar uma identidade só da Keshion, em 15 minutos, e reconectar. Não custa nada.

**Cuidados importantes:**

- O app novo precisa estar **publicado** ("In production"), não em "Testing": em modo Teste o Google desfaz a autorização em 7 dias e o backup quebra sem aviso.
- O acesso fica limitado a `drive.file`: o app só enxerga arquivos que ele mesmo criou. Por isso, **os backups antigos (feitos pela identidade antiga) provavelmente não ficam visíveis para o app novo**. Isso é esperado; a Claude confere e, se for o caso, baixa uma cópia dos antigos para o PC antes da troca. Os 30 dias de retenção do Drive só apagam o que o app novo criou: os antigos ficam até alguém apagar à mão (pasta `keshion-backups/` do Drive).
- Fazer a troca num dia sem pressa e **depois** de confirmar o backup de 19/11.

Passos (conta **keshion.ai.2026@gmail.com**; fazer no navegador onde você já está logada nela):

1. Abrir console.cloud.google.com e aceitar os termos, se pedir.
2. No topo, **Select a project > New Project**. Nome: `keshion-backup`. Criar e selecionar.
3. Menu **APIs & Services > Library**, procurar **Google Drive API** e clicar **Enable**.
4. Menu **Google Auth Platform** (ou **APIs & Services > OAuth consent screen**) e **Get started**:
   - Nome do app: `Keshion Backup`. E-mail de suporte: o da conta.
   - Público: **External**.
   - E-mail de contato: o da conta. Aceitar a política e **Create**.
5. Em **Data Access** (Scopes), **Add or remove scopes** e marcar só `.../auth/drive.file` ("See, edit, create and delete only the specific Google Drive files you use with this app"). Salvar.
6. Em **Audience** (ou **Publishing status**), clicar **Publish app / In production** e confirmar. Esse escopo não é "sensível": não pede análise do Google nem logotipo. O status precisa aparecer como **In production**.
7. Em **Clients** (ou **Credentials > Create credentials > OAuth client ID**): tipo **Desktop app**, nome `rclone-keshion`. Anotar o **Client ID** e o **Client secret** (o secret aparece uma vez; se perder, cria outro). Guardar os dois no Bitwarden e no `.env` do PC como `RCLONE_GDRIVE_CLIENT_ID=` e `RCLONE_GDRIVE_CLIENT_SECRET=`. **Não mandar no chat.**
8. Avisar a Claude. Ela faz no PC (e a Erica só clica "Allow" na janela do Google que abrir):
   - `rclone config` criando um remoto novo `gdrive2` com esse Client ID e Secret, escopo `drive.file`;
   - conferir `rclone lsl gdrive2:keshion-backups/postgres` para ver se as cópias antigas aparecem;
   - se não aparecerem, baixar as antigas com o remoto antigo para uma pasta do PC;
   - gerar o `rclone.conf` novo (remoto de nome `gdrive`, como o script espera) e, **com o seu OK**, copiá-lo para `/opt/keshion/rclone.conf` no servidor (cópia do arquivo antigo guardada ao lado) e rodar um backup manual (também só com o seu OK) para conferir `OK` e os dois arquivos novos no Drive.
9. Conferir no dia seguinte (03h) que a rodada automática deu `OK` pelo novo acesso.

**Se algo der errado:** voltar o `rclone.conf` antigo (a cópia fica no servidor e no PC); o backup volta a funcionar enquanto o Google não desligar o antigo.
