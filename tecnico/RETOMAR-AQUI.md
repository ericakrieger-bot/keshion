# Retomar aqui (Keshion · automações da Clara)

Atualizado em 17/11/2026 (noite). Ler só este arquivo para começar; abrir os outros só quando a tarefa pedir.

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

## Roadmap

**Urgente (esta semana)**
- **Google Agenda:** o app do Google está em modo Teste, e a autorização expira 7 dias depois de dada. A credencial foi atualizada em 17/11 às 05:16 e a agenda responde: se foi reconexão, vale até cerca de 24/11; se não, o prazo é perto de 19/11. Até publicar o app, reconectar no n8n quando expirar. Para publicar: domínio keshion.com (já registrado), página inicial e política de privacidade.
- **Achados do Codex nos testes (relatório `tecnico/teste-ab/relatorio-codex-20261117.md`, roteiro em `tecnico/roteiro-testes-codex.md`).** Nada disso foi aplicado; decidir antes do piloto:
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
2. **Backup fora do servidor (próxima feature).**
3. Base, instruções e voz da Dra. Vivian; nome da assistente escolhido por ela; conexão no número dela; preencher `clientes/dra-vivian/clinica.json` e seguir "Clínica nova" do LEIA-ME.
4. Decidir com ela o modo copiloto (aprovar antes de enviar na 1ª semana): ainda não existe.
5. Canal de alerta fora do WhatsApp (e-mail ou Telegram) para falhas.
6. Usuário de manutenção com sudo (no lugar do root).

**Depois do piloto**
Confirmações (48 h, véspera, 2 h antes), CRM em Google Planilhas, Sonnet nas mensagens clínicas, ordem de envio garantida entre respostas próximas, reservas de horário no banco, resumo do histórico longo, Postgres 17, Jev (classificador de intenção).

## Próxima feature: backup fora do servidor

Por que agora: com a Vivian, o banco passa a ter conversas de pacientes reais. Hoje o backup diário (03h, `pg_dumpall`, últimos 7) fica no próprio servidor (`/opt/keshion/backups/`): se o servidor ou o disco se perderem, o backup vai junto. Também não existe cópia do `/opt/keshion/.env` fora do servidor, e a restauração nunca foi testada. Detalhes do backup atual em `tecnico/servidor-n8n.md` (seção Backup).

O que entra:
1. Cópia diária, criptografada, para fora do servidor, com a chave de abrir guardada fora do servidor.
2. Cópia segura do `.env` do servidor (senhas dos bancos, chave de criptografia do n8n) fora dele.
3. Teste de restauração numa cópia (outro contêiner Postgres temporário), conferindo que os bancos `clara`, `clinica_teste` e `n8n` voltam inteiros e que o n8n abre as credenciais.
4. Aviso quando o backup falhar (até existir o canal de alerta, pelo menos um registro fácil de conferir).

O que decidir no começo: para onde vai a cópia (recomendação: Google Drive da conta da Keshion pelo rclone, sem custo; alternativa paga e simples: Backblaze B2), como criptografar (recomendação: `age`, com a chave privada só no PC da Erica e num cofre de senhas) e quanto guardar fora (recomendação: 30 dias). Gastar dinheiro ou criar conta: pedir OK antes.

Pronto quando: existe cópia fora do servidor de ontem, criptografada; a restauração foi testada de ponta a ponta numa cópia isolada, sem tocar na produção; `.env` guardado fora; `tecnico/servidor-n8n.md` atualizado com o passo a passo de restaurar. Depois, revisão no Codex.

## Regras de sempre

Português com acentos e sem travessão. Chaves só no `.env` (PC) ou em `/opt/keshion/.env` (servidor), nunca no chat nem no Git. Pedir OK antes de mudar produção, gastar dinheiro ou mexer em número de WhatsApp. Testar só com o prefixo `554199900`, um teste por vez. Commit e push dentro de `Documents\Claude Code\keshion`; memória `keshion-migracao-n8n` com cópia no segundo cérebro.
