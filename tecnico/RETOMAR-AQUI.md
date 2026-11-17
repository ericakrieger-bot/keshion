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
| Testes | números com prefixo `554199900` nunca saem pelo WhatsApp. `tecnico/teste-ab/teste_n8n.py` (56 mensagens, roda no servidor) e `tecnico/teste-ab/paciente_simulado.py` (8 pacientes simulados por IA + IA avaliadora, roda no PC) |

## O que já foi feito

1. Servidor seguro (firewall, fail2ban, SSH só por chave, versões fixas, backup diário local dos últimos 7).
2. Clara migrada do Make para o n8n: fila de 7 s, ficha, Google Agenda (marcar, remarcar, cancelar), até 3 mensagens com "digitando", avisos para a aprovadora, despedida 1 min depois de marcar, pausa de 12 h quando a doutora responde, áudio (.oga corrigido) e foto.
3. Revisão independente do Codex e correções: webhook secreto e só do canal GRNLTR-4K8ZF, mídia só do Whapi, ids repetidos ignorados, avisos antes do paciente, falhas de agenda e IA viram "chamar uma pessoa", segunda tentativa quando a IA vem vazia. Pendências em `tecnico/n8n/plano-pos-revisao-codex.md`.
4. Tom: menos cara de robô (humanizer), espelha o jeito do paciente conforme a voz definida na base de cada clínica, pede nome completo e telefone para marcar, dor e remédio sempre chamam a Dra.
5. Resultados: 56/56 no teste fixo; pacientes simulados com notas 7 a 9, todos com objetivo atingido.

## Roadmap

**Urgente (esta semana)**
- **Google Agenda:** o app do Google está em modo Teste, e a autorização expira 7 dias depois de dada (dada em 12/11, então perto de 19/11). Até publicar o app, reconectar a credencial no n8n quando expirar. Para publicar: domínio keshion.com.br, página inicial e política de privacidade.

**Antes do piloto da Dra. Vivian (01/12/2026)**
1. **Estrutura por clínica (próxima feature):** o gerador recebe um arquivo por clínica (nome da assistente, agenda, aprovador, voz, credenciais, banco ou chave de clínica) e gera os fluxos dela, sem misturar dados com a demo.
2. Base, instruções e voz da Dra. Vivian; nome da assistente escolhido por ela; conexão no número dela.
3. Decidir com ela o modo copiloto (aprovar antes de enviar na 1ª semana): ainda não existe.
4. Backup fora do servidor, com um teste de restauração; cópia do `.env` do servidor em local seguro.
5. Canal de alerta fora do WhatsApp (e-mail ou Telegram) para falhas.
6. Usuário de manutenção com sudo (no lugar do root).

**Depois do piloto**
Confirmações (48 h, véspera, 2 h antes), CRM em Google Planilhas, Sonnet nas mensagens clínicas, ordem de envio garantida entre respostas próximas, reservas de horário no banco, resumo do histórico longo, Postgres 17, Jev (classificador de intenção).

## Próxima feature

**Estrutura por clínica**, para a Clara da Dra. Vivian rodar separada da demo. Antes dela, conferir se a credencial do Google ainda está válida.

## Regras de sempre

Português com acentos e sem travessão. Chaves só no `.env` (PC) ou em `/opt/keshion/.env` (servidor), nunca no chat nem no Git. Pedir OK antes de mudar produção, gastar dinheiro ou mexer em número de WhatsApp. Testar só com o prefixo `554199900`. Commit e push dentro de `negocio-ia-clinicas/`; memória `keshion-migracao-n8n` com cópia no segundo cérebro.
