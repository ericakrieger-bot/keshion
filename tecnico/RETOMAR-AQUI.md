# Retomar aqui (Keshion · automações da Clara)

Atualizado em 17/11/2026. Ler só este arquivo para começar; abrir os outros só quando a tarefa pedir.

## Onde estamos

A Clara (assistente de WhatsApp da clínica demo da Dra. Suzana) **roda no n8n próprio desde 12/11/2026**. O Make está desativado (1A a 1D só desligados, não apagados).

| Peça | Onde |
|---|---|
| Servidor | Contabo 169.58.41.107, `ssh -i ~/.ssh/keshion_vps root@169.58.41.107`, tudo em `/opt/keshion` (n8n 2.47.5, Postgres 16.15, Caddy 2.11.9). Detalhes: `tecnico/servidor-n8n.md` |
| n8n | https://n8n.169-58-41-107.sslip.io · fluxos `ClaraAtendimento` e `ClaraEnvio000001` |
| Fonte dos fluxos | `tecnico/n8n/gerar_fluxos.py` (mudar aqui, gerar, importar e publicar pelo CLI do n8n; passo a passo em `tecnico/n8n/LEIA-ME.md`) |
| Caminho do webhook | secreto, em `tecnico/n8n/segredos.local.json` (fora do Git) |
| Dados | Postgres, banco `clara`: `pacientes`, `config` (`_instrucoes`, `_base`, `modelo`, `aprovador`, `prefixo_teste`...), `mensagens_recebidas`, `saidas_teste` |
| Instruções e base | `clientes/clinica-demo/instrucoes-sarah.md` e `base-clinica.md` (copiar para `config` depois de mudar) |
| Testes | lista em `tecnico/testes-checklist.md`; números com prefixo `554199900` nunca saem pelo WhatsApp. `tecnico/teste-ab/teste_n8n.py` (56 mensagens, roda no servidor) e `tecnico/teste-ab/paciente_simulado.py` (8 pacientes simulados por IA + IA avaliadora, roda no PC) |

## O que já foi feito

1. Servidor seguro (firewall, fail2ban, SSH só por chave, versões fixas, backup diário local dos últimos 7).
2. Clara migrada do Make para o n8n: fila de 7 s, ficha, Google Agenda (marcar, remarcar, cancelar), até 3 mensagens com "digitando", avisos para a aprovadora, despedida 1 min depois de marcar, pausa de 12 h quando a doutora responde, áudio (.oga corrigido) e foto.
3. Revisão independente do Codex e correções: webhook secreto e só do canal GRNLTR-4K8ZF, mídia só do Whapi, ids repetidos ignorados, avisos antes do paciente, falhas de agenda e IA viram "chamar uma pessoa", segunda tentativa quando a IA vem vazia. Pendências em `tecnico/n8n/plano-pos-revisao-codex.md`.
4. Tom: menos cara de robô (humanizer), espelha o jeito do paciente conforme a voz definida na base de cada clínica, pede nome completo e telefone para marcar, dor e remédio sempre chamam a Dra.
5. Resultados: 56/56 no teste fixo; pacientes simulados com notas 7 a 9, todos com objetivo atingido.

## Roadmap

**Urgente (esta semana)**
- **Google Agenda:** o app do Google está em modo Teste, e a autorização expira 7 dias depois de dada (dada em 12/11, então perto de 19/11). Até publicar o app, reconectar a credencial no n8n quando expirar. Para publicar: domínio keshion.com (já registrado), página inicial e política de privacidade.

**Antes do piloto da Dra. Vivian (01/12/2026)**
1. ✅ **Estrutura por clínica** (17/11; falta só a revisão no Codex).
2. Base, instruções e voz da Dra. Vivian; nome da assistente escolhido por ela; conexão no número dela.
3. Decidir com ela o modo copiloto (aprovar antes de enviar na 1ª semana): ainda não existe.
4. Backup fora do servidor, com um teste de restauração; cópia do `.env` do servidor em local seguro.
5. Canal de alerta fora do WhatsApp (e-mail ou Telegram) para falhas.
6. Usuário de manutenção com sudo (no lugar do root).

**Depois do piloto**
Confirmações (48 h, véspera, 2 h antes), CRM em Google Planilhas, Sonnet nas mensagens clínicas, ordem de envio garantida entre respostas próximas, reservas de horário no banco, resumo do histórico longo, Postgres 17, Jev (classificador de intenção).

## Próxima feature: estrutura por clínica

Objetivo: o gerador monta os fluxos de cada clínica a partir de um arquivo de configuração, sem misturar dados entre clínicas. A demo (Dra. Suzana) vira a clínica 1, e a Dra. Vivian só preenche o arquivo dela quando mandar os dados.

O que entra no arquivo de cada clínica: nome da clínica e da assistente, número e canal do Whapi, quem recebe os avisos, agenda (credencial do Google e calendário), fuso, horário de atendimento e duração da avaliação, voz (registro e abreviações), base e instruções, prefixo e modo de teste.

O que decidir no começo: um banco por clínica ou um banco com a coluna "clínica" (recomendação: um banco por clínica no piloto, mais simples de isolar e de apagar), e um par de fluxos por clínica ou um fluxo que atende várias (recomendação: um par por clínica, gerado pelo mesmo script).

Pronto quando: a demo roda pelo arquivo de configuração e passa nos testes do portão 1 (`tecnico/testes-checklist.md`), existe um arquivo modelo para a Dra. Vivian, e o teste de isolamento (mesmo telefone em duas clínicas) passa. Depois, revisão no Codex.

**Feito em 17/11/2026:** um banco e um par de fluxos por clínica. `gerar_fluxos.py <slug>` lê `clientes/<slug>/clinica.json`; `preparar_banco.py <slug>` gera o SQL do banco; modelo em `clientes/_modelo/`, ficha da Dra. Vivian em `clientes/dra-vivian/clinica.json` (faltam os dados dela). Passo a passo de clínica nova em `tecnico/n8n/LEIA-ME.md`.
No servidor: banco `clinica_teste` (usuário próprio, senha `CLINICA_TESTE_DB_PASSWORD` no `.env`), credencial "Postgres clinica-teste" e fluxos `TesteAtendimento`/`TesteEnvio000001` no ar (clínica fictícia, canal falso, só recebe chamadas diretas); demo reimportada pelo gerador novo (cópia dos fluxos anteriores em `/opt/keshion/backups/fluxos-20261117/`); bancos `clara` e `n8n` fechados para outros usuários.
Testes: isolamento passou (`tecnico/teste-ab/teste_isolamento.py`, mesmo telefone e mesmo id nas duas clínicas); 56 de 56 respondidas, sem falha técnica; pacientes simulados (15 perfis) com notas 7 a 9 e agenda limpa. Atenção: duas rodadas de teste ao mesmo tempo (duas conversas ou Codex) usando os mesmos números se atrapalham, porque a limpeza de uma apaga as fichas da outra (aconteceu em 17/11 às 10:13 e derrubou 3 perfis para nota 3; o reteste deu 9, 9 e 8). Rodar um teste por vez.
Falta: revisão no Codex desta feature; preencher a ficha da Vivian quando ela mandar os dados.

Credencial do Google Agenda: conferida em 17/11 (atualizada às 05:16 e consultas à agenda funcionando).

## Regras de sempre

Português com acentos e sem travessão. Chaves só no `.env` (PC) ou em `/opt/keshion/.env` (servidor), nunca no chat nem no Git. Pedir OK antes de mudar produção, gastar dinheiro ou mexer em número de WhatsApp. Testar só com o prefixo `554199900`. Commit e push dentro de `Documents\keshion`; memória `keshion-migracao-n8n` com cópia no segundo cérebro.
