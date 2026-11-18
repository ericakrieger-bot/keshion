# Retomar aqui (Keshion · automações da Clara)

Atualizado em 18/11/2026 (tarde). Ler só este arquivo para começar; abrir os outros só quando a tarefa pedir.

## Onde estamos

A Clara (assistente de WhatsApp da clínica demo da Dra. Suzana) **roda no n8n próprio desde 12/11/2026**. O Make está desativado (1A a 1D só desligados, não apagados). **Desde 17/11, cada clínica tem banco, fluxos e credenciais próprios**, gerados a partir de um arquivo por clínica.

| Peça | Onde |
|---|---|
| Servidor | Contabo 169.58.41.107, `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`, tudo em `/opt/keshion` (n8n 2.47.5, Postgres 16.15, Caddy 2.11.9). Detalhes: `tecnico/servidor-n8n.md` |
| n8n | https://n8n.169-58-41-107.sslip.io · demo: `ClaraAtendimento` e `ClaraEnvio000001` · clínica fictícia de teste: `TesteAtendimento` e `TesteEnvio000001` |
| Clínicas | uma pasta por clínica em `clientes/<slug>/` com `clinica.json` (sem chaves), instruções e base. Modelo em `clientes/_modelo/`. Ficha da Dra. Vivian em `clientes/dra-vivian/clinica.json` (faltam os dados dela) |
| Fonte dos fluxos | `tecnico/n8n/gerar_fluxos.py <slug>` (fluxos) e `tecnico/n8n/preparar_banco.py <slug>` (banco). Saída em `tecnico/n8n/gerados/<slug>/`, fora do Git. Passo a passo, inclusive "Clínica nova", em `tecnico/n8n/LEIA-ME.md` |
| Caminhos dos webhooks | secretos, um por clínica, em `tecnico/n8n/segredos.local.json` (fora do Git) |
| Dados | Postgres, um banco por clínica (`clara` = demo, `clinica_teste` = teste), cada um com usuário próprio. Tabelas: `pacientes`, `config` (`_instrucoes`, `_base`, `modelo`, `aprovador`, `prefixo_teste`...), `mensagens_recebidas`, `saidas_teste` |
| Instruções e base | `clientes/<slug>/` (demo: `instrucoes-sarah.md` e `base-clinica.md`). Depois de mudar, rodar `preparar_banco.py <slug>` e aplicar o SQL no banco da clínica |
| Testes | lista em `tecnico/testes-checklist.md`; números com prefixo `554199900` nunca saem pelo WhatsApp. `teste_n8n.py` (56 mensagens, servidor), `paciente_simulado.py` (22 pacientes simulados, PC; aceita filtro: `python paciente_simulado.py 816 817`; grava `historico-notas.csv`), `teste_isolamento.py` (duas clínicas, servidor), todos em `tecnico/teste-ab/`. **Rodar um teste por vez:** duas rodadas ao mesmo tempo apagam as fichas uma da outra |

## O que já foi feito

1. Servidor seguro (firewall, fail2ban, SSH só por chave, versões fixas, backup diário local dos últimos 7).
2. Clara migrada do Make para o n8n: fila de 7 s, ficha, Google Agenda (marcar, remarcar, cancelar), até 3 mensagens com "digitando", avisos para a aprovadora, despedida 1 min depois de marcar, pausa de 12 h quando a doutora responde, áudio (.oga corrigido) e foto.
3. Revisão independente do Codex e correções: webhook secreto e só do canal da clínica, mídia só do Whapi, ids repetidos ignorados, avisos antes do paciente, falhas de agenda e IA viram "chamar uma pessoa", segunda tentativa quando a IA vem vazia. Pendências em `tecnico/n8n/plano-pos-revisao-codex.md`.
4. Tom: menos cara de robô (humanizer), espelha o jeito do paciente conforme a voz definida na base de cada clínica, pede nome completo e telefone para marcar, dor e remédio sempre chamam a Dra.
5. **Estrutura por clínica (17/11):** um banco e um par de fluxos por clínica; fuso, cidade, nome da assistente, calendário, duração da avaliação, canal e credenciais vêm do `clinica.json`. Demo reimportada pelo gerador novo (cópia dos fluxos antigos em `/opt/keshion/backups/fluxos-20261117/`). Bancos `clara`, `n8n` e `clinica_teste` fechados para outros usuários.
6. Resultados em 17/11: isolamento passou (mesmo telefone e mesmo id nas duas clínicas, cada uma só lembra do próprio paciente, canal de outra clínica ignorado); 56/56 no teste fixo sem falha técnica; pacientes simulados: 15 perfis com média 8,2 e, depois, 7 perfis de ciclo de vida (antigos, follow-up, cancelou); os antigos tiraram 5 a 6. Detalhes e correções pedidas pelo Codex em "Urgente".
7. **Decisões e correções antes da Vivian (17 e 18/11):** alerta de falha só para a Keshion e sem texto do paciente; `modo_teste` ausente vale como teste; `#reiniciar` só na demo; dois usuários por banco (demo ainda no dono); roteiro geral em `tecnico/n8n/CLINICA-NOVA.md`. Em 18/11: aviso de "complemento" quando o paciente traz assunto novo, lembrete de idioma no pedido para a IA, nada de "encaixe" com a clínica fechada, conferência de horário que entende hora em inglês e espanhol. Tudo publicado na demo e na clínica de teste. Teste do paciente simulado 7 vezes mais barato (paciente no Haiku).
8. **Backup fora do servidor (18/11):** todo dia às 03h, dump criptografado com `age` no Google Drive da keshion.ai.2026@gmail.com (`keshion-backups/`, 30 dias), junto com a configuração (`.env`, Compose, Caddyfile). Chave privada só no PC (`C:\Users\Erica Krieger-Akerma\.keshion-backup\`) e no cofre de senhas. Resultado em `/opt/keshion/backups/STATUS-BACKUP.txt`. Restauração testada de ponta a ponta numa cópia isolada (bancos inteiros, n8n abriu as 6 credenciais). Passo a passo em `tecnico/servidor-n8n.md`, seção Backup.

## Roadmap

**Urgente (esta semana)**
- **Pendente agora, nesta ordem:**
  1. Rodar `tecnico/teste-ab/PROMPT-TESTE-18-11-avisos-idioma-hora.md` na conversa de testes (pode ser Sonnet). Nada do que foi publicado em 18/11 foi testado ainda numa rodada válida.
  2. Revisão do Codex com `tecnico/n8n/PROMPT-CODEX-CORRECOES-17-11-NOITE.md` (cobre 17/11 noite e 18/11). Não rodar junto com o item 1.
  3. Conferir a agenda da demo: apagar eventos de teste que sobraram (havia Henrique, 19/11 às 14h).
  4. Com OK: passar a demo e a clínica de teste para o usuário `_app` do banco (passo a passo a pedir ao Codex).
- **Google Agenda:** o app do Google está em modo Teste, e a autorização expira 7 dias depois de dada. A credencial foi atualizada em 17/11 às 05:16 e a agenda responde: se foi reconexão, vale até cerca de 24/11; se não, o prazo é perto de 19/11. Até publicar o app, reconectar no n8n quando expirar. Para publicar: domínio keshion.com (já registrado), página inicial e política de privacidade.
- **Achados do Codex nos testes (relatório `tecnico/teste-ab/relatorio-codex-20261117.md`, roteiro em `tecnico/roteiro-testes-codex.md`).** **Itens 1 a 6 CORRIGIDOS em 17/11 (noite)**, publicados na demo e na clínica de teste (detalhes em `tecnico/n8n/LEIA-ME.md`, seção "correções da revisão do Codex"). **Falta validar:** a rodada dos 22 pacientes não terminou porque o saldo da conta da Anthropic acabou (erro "credit balance is too low"); sem saldo, a própria Clara responde "Só um instante, vou verificar" (confirmado na clínica de teste). Depois de recarregar: rodar `paciente_simulado.py` (uma rodada) e `teste_n8n.py`, conferir a agenda da demo à mão (sobrou 1 evento de teste: Henrique, 19/11 às 14h, telefone 554199900810; apagar no Google Agenda da demo). Enunciado original dos itens:
  1. **Agenda:** o fluxo só confere "horário livre" no Google e confia na IA para dia da semana, limite de 90 dias e aceite do paciente; duas pessoas pegando a mesma vaga ao mesmo tempo podem criar duas reservas (não reproduzido). Validar no próprio fluxo antes de criar ou mudar evento.
  2. **Avisos:** a Clara às vezes promete "vou passar para a Dra. Suzana" sem gerar aviso (Gustavo, 1ª rodada) e às vezes manda 3 ou 4 avisos iguais (Cláudio, Fernanda, Camila). Registrar o aviso quando ela disser que encaminhou e deduplicar por pessoa e assunto.
  3. **Ordem de envio:** uma pergunta de horário chegou depois da confirmação da marcação (já está no roadmap, "ordem de envio garantida").
  4. **Pacientes antigos (notas 5, 6 e 6):** não informa a faixa da limpeza (R$ 280 a R$ 350), diz "a Dra. tem o seu prontuário", não oferece marcar. A base e as instruções não têm regra para retorno e manutenção.
  5. **Idioma:** não existe regra; a 1ª resposta da Emily veio em português e o espanhol voltou em português.
  6. **Promessas sem base:** "faz tudo com anestesia", "ainda hoje", "logo entra em contato".
  7. **Follow-up do orçamento (dias 2, 7, 14), confirmações e reengajamento não existem.** Antes de construir: quem registra que o orçamento saiu e como a clínica registra cancelamento e pedido para sair da lista.
  - **Não são falhas da Clara (corrigido no script):** as notas 3 de Júlia, Henrique e Gustavo e os dois eventos que sobraram na agenda vieram de duas rodadas ao mesmo tempo (a limpeza de uma apagava as fichas da outra). Refeitas sozinhas, deram 9, 9 e 8. O script agora limpa só os números da própria rodada e o nome do relatório tem segundos. A média de referência correta é 8,2 (eu tinha dito 8,3).
  - A agenda da demo precisa ser conferida à mão depois de cada rodada: o script só vê o que a ficha lembra, e os dois eventos que sobraram não estavam na ficha.
- **Revisão do Codex da estrutura por clínica (feita em 17/11, `tecnico/n8n/revisao-codex-estrutura-por-clinica-2026-11-17.md`).** Conclusão dele: manter a arquitetura, mas ainda não ligar a Vivian.
  - **Corrigido em 17/11 (noite):** o gerador recusa ficha copiada (ids de fluxo, semente e caminho do webhook, canal, banco e credenciais iguais aos de outra clínica; compartilhamento só declarado em `compartilha_para_teste`, nunca o banco), ids fora do formato, nome ou cidade com aspas e fuso ou duração inválidos. `preparar_banco.py` trava se rodar no banco errado (testado: recusou o SQL da clínica de teste no banco da demo, sem escrever nada), usa delimitador seguro e só aceita chaves conhecidas. Modelo e ficha da Vivian sem números da Keshion herdados (`aviso_falha_envio` e `numeros_keshion` agora são PREENCHER). `teste_isolamento.py` confere exclusividade antes, limpa em `finally`, acusa erro de SQL, testa canal errado nos dois sentidos e usa marcadores exclusivos (passou de novo).
  - **Decidido com a Erica em 17/11 (noite):** (b) `#reiniciar` só na demo e na clínica de teste: feito (`numeros_keshion` vazio no modelo e na Vivian; `preparar_banco.py` recusa número nas outras). (c) a clínica de teste pode marcar na agenda da demo: fechado. (e) dois usuários por banco, dono `<banco>` só para instalar e `<banco>_app` para o n8n (lê e grava linhas, só lê a `config`, não apaga nem muda tabelas): feito no `preparar_banco.py` e testado num Postgres descartável. A demo e a clínica de teste ainda usam o dono: migrar com OK, junto com a próxima mexida no servidor. (f) roteiro geral de clínica nova em `tecnico/n8n/CLINICA-NOVA.md`.
  - **Feito em 17/11 (noite), com OK da Erica, publicado no envio da demo e da clínica de teste:** (a) o alerta de falha do WhatsApp vai só para a Keshion (`tecnico/n8n/alerta-keshion.json`), pelo canal do Whapi da Keshion e não pelo da clínica, sem o texto do paciente: só a clínica, o final do telefone e o erro. Ainda é WhatsApp: o canal fora dele continua no item 5 abaixo. (d) `modo_teste` ausente agora vale como teste, e o `preparar_banco.py` exige "1" ou "0". Teste de isolamento passou depois de publicar. O caminho do alerta não foi disparado de verdade, para não mandar mensagem real; a expressão foi conferida com dados de exemplo.

**Antes do piloto da Dra. Vivian (01/12/2026)**
1. ✅ Estrutura por clínica (17/11).
2. ✅ Backup fora do servidor (18/11). Falta: a Erica guardar a chave privada e o `.env` no cofre de senhas; revisão no Codex.
3. Base, instruções e voz da Dra. Vivian; nome da assistente escolhido por ela; conexão no número dela; preencher `clientes/dra-vivian/clinica.json` e seguir "Clínica nova" do LEIA-ME.
4. Decidir com ela o modo copiloto (aprovar antes de enviar na 1ª semana): ainda não existe.
5. Canal de alerta fora do WhatsApp (e-mail ou Telegram) para falhas.
6. Usuário de manutenção com sudo (no lugar do root).

**Depois do piloto**
Confirmações (48 h, véspera, 2 h antes), CRM em Google Planilhas, Sonnet nas mensagens clínicas, ordem de envio garantida entre respostas próximas, reservas de horário no banco, resumo do histórico longo, Postgres 17, Jev (classificador de intenção).

**Custo dos testes (18/11):** os US$ 10 de crédito foram gastos US$ 7,49 nos testes (Sonnet) e US$ 2,52 na Clara (Haiku, cerca de US$ 0,002 por resposta). `paciente_simulado.py` agora usa Haiku no paciente e Sonnet com esforço médio no juiz, e mostra o custo no fim: 5 pacientes custaram US$ 0,12 (antes eram cerca de US$ 0,80). Na rodada de 18/11 (22h37 em Curitiba, clínica fechada), Bia, Camila, Fernanda, Patrícia e Emily tiraram 8, 7, 6, 7 e 7, abaixo de 17/11. Os problemas apontados são da Clara: promete encaixe com a clínica fechada, diz que não sabe uma resposta que está na base, escreve "avalição", volta para o português com a Emily. **Investigado em 18/11:** o juiz novo dá as mesmas notas às conversas de 17/11 (8,0 contra 8,3), então não é o teste. Causas: (1) a deduplicação de avisos publicada em 17/11 (noite) engoliu avisos com assunto novo (Fernanda: parcelamento da avaliação; Camila: clareamento em outra clínica), porque palavras genéricas como "paciente", "clínica" e "fechada" fazem os motivos parecerem iguais; (2) a rodada foi à noite, e com a clínica fechada a Clara misturou a regra de clínica aberta (prometeu "encaixe"); (3) deslizes do Haiku: ofereceu horários em português para a Emily, não usou a resposta da base "Posso parcelar a avaliação?", escreveu "avalição". Propostas (aguardam OK, mexem na produção): aviso de "complemento" em vez de engolir quando a mensagem traz pergunta nova; lembrete de idioma no fim do pedido para a IA; "com a clínica fechada, nunca fale em encaixe" nas instruções; repetir a rodada em horário comercial de Curitiba. **Aplicado em 18/11 (manhã), com OK da Erica:** aviso de "complemento" (publicado), lembrete de idioma no pedido para a IA (publicado), "nunca fale em encaixe" com a clínica fechada (base da demo e da clínica de teste, aplicada no banco). Isolamento passou. A rodada de 5 pacientes depois disso **não vale**: outro teste (provavelmente o Codex) rodava ao mesmo tempo com os mesmos números, e o reinício do n8n às 06h17 (horário de Curitiba) derrubou execuções dele. Achado real dessa rodada: a validação de horário só reconhecia hora em português, e paciente em inglês não conseguia marcar ("9am"). **Corrigido e publicado em 18/11** (06h45 de Curitiba, sem reiniciar o n8n). Teste a fazer na conversa de testes: `tecnico/teste-ab/PROMPT-TESTE-18-11-avisos-idioma-hora.md`. As frases fixas do fluxo ("Esse horário não está disponível...") continuam só em português.

## Backup fora do servidor: feito em 18/11

Decidido com a Erica: Google Drive da keshion.ai.2026@gmail.com (rclone, escopo só dos arquivos que ele cria), `age` com chave privada só no PC e no cofre, 30 dias no Drive. Script `tecnico/servidor/backup-postgres.sh` (instalado em `/opt/keshion/`). Também passou a conferir que o dump terminou inteiro (antes, uma falha do `pg_dumpall` passava em silêncio).

Pendências desta feature:
- A Erica colar no cofre de senhas o conteúdo de `C:\Users\Erica Krieger-Akerma\.keshion-backup\chave-backup-keshion.txt` e de `env-servidor-20261118.txt`. Se o PC se perder sem isso, os backups do Drive não abrem.
- Conferir amanhã (19/11) o `STATUS-BACKUP.txt` da rodada das 03h, a primeira automática.
- O rclone avisa que o client_id compartilhado do Google Drive dele será desativado em 2026. Se o envio falhar, criar client_id próprio (depende de publicar o app do Google, como a Agenda).
- Aviso automático de falha: entra junto com o canal de alerta fora do WhatsApp (item 5).
- Revisão no Codex (`tecnico/n8n/PROMPT-CODEX-REVISAO.md`, feature "backup fora do servidor": script, permissões, restauração).

## Próxima feature (sugestão): canal de alerta fora do WhatsApp

A base e a voz da Vivian dependem dos dados dela. Enquanto isso, o canal de alerta (e-mail ou Telegram) cobre as falhas de envio da Clara e as do backup, que hoje só ficam registradas.

## Regras de sempre

Português com acentos e sem travessão. Chaves só no `.env` (PC) ou em `/opt/keshion/.env` (servidor), nunca no chat nem no Git. Pedir OK antes de mudar produção, gastar dinheiro ou mexer em número de WhatsApp. Testar só com o prefixo `554199900`, um teste por vez e só na conversa de testes da Erica (as outras conversas corrigem, publicam e entregam um prompt de teste). Publicar fluxo com import e publish, sem reiniciar o n8n. Commit e push dentro de `Documents\Claude Code\keshion`; memória `keshion-migracao-n8n` com cópia no segundo cérebro.
