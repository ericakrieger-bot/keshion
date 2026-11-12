# Migração da Clara do Make para o n8n · LEIA PRIMEIRO

Documento de passagem para uma conversa nova do Claude Code. Escrito em 12/11/2026.
Leia também `negocio-ia-clinicas/CLAUDE.md` (contexto completo do negócio Keshion).

## 1. Onde estamos

- **Clara** é a assistente de WhatsApp da clínica demo (Dra. Suzana, fictícia). Antes se chamava Sarah.
- Hoje ela roda no **Make** (cenários 1A, 1B, 1C e 1D) e responde com o **Claude Haiku 5.5** (`claude-haiku-5-5`), escolhido no teste A/B de 11/11/2026.
- **Decisão de 11/11/2026:** levar a Clara para o **n8n** agora. No Make fica só o cenário `Keshion · Questionário Dra. Vivian (respostas)` (id 8491037).
- **Piloto com a Dra. Vivian:** previsto para **01/12/2026** (ela está de férias). A Clara precisa estar no n8n, testada, antes disso.
- A Clara continua no Make até o n8n estar pronto e testado. A virada é trocar o webhook no Whapi. Dá para voltar atrás.

## 2. O servidor (VPS)

| Item | Valor |
|---|---|
| Provedor | Contabo (painel: my.contabo.com) |
| IP | 169.58.41.107 |
| Sistema | Ubuntu 24.04 (OpenSSH 9.6) |
| O que tinha | Hermes. A Erica autorizou apagar; ela reinstala depois, se quiser |
| Acesso | Chave SSH dedicada: `~/.ssh/keshion_vps` (privada) e `~/.ssh/keshion_vps.pub` (pública), já criadas no computador da Erica |
| Chave pública (pode ser colada no painel) | `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHOqjJmoB9SMAdXavzyRBDGHtcpJ7QacwOF7/X/bZbGG keshion-n8n` |

A senha de root não funcionou, nem depois de redefinida. A Erica escolheu o **Caminho 2**: reinstalar o servidor pelo painel da Contabo colando a chave pública acima. A reinstalação apaga tudo (inclusive o Hermes), e a Erica já aceitou isso.

## 3. Próximos passos, em ordem

> **Estado em 12/11/2026 (noite):** passos 1 a 6 feitos e o 7 quase todo. Servidor no ar (`tecnico/servidor-n8n.md`). Credenciais criadas. Clara reconstruída em dois fluxos ativos, com banco `clara` próprio e **modo teste ligado** (nada sai pelo WhatsApp). Como está montada e o que foi testado: `tecnico/n8n/LEIA-ME.md`. Passo 8 feito na manhã de 12/11 (56 de 56). Próximo: a virada do webhook (passo 9, com OK da Erica), desligando o modo teste no mesmo momento.

1. ✅ **Reinstalar o VPS** pelo painel da Contabo (a Erica abre no Chrome; o Claude pode guiar ou operar pela extensão Claude in Chrome):
   - Your services → VPS 169.58.41.107 → Manage → **Reinstall**.
   - Sistema: **Ubuntu 24.04**.
   - Colar a chave pública da tabela no campo de SSH key.
   - Antes de clicar no botão final de reinstalar, confirmar com a Erica (ação irreversível).
   - Esperar de 10 a 20 minutos.
2. ✅ **Testar o acesso:** `ssh -i ~/.ssh/keshion_vps root@169.58.41.107 "hostname; free -h; df -h /"`.
   - Se der aviso de chave de servidor mudada, é esperado depois da reinstalação: remover a linha antiga com `ssh-keygen -R 169.58.41.107`.
3. ✅ **Preparar o servidor:** atualizar pacotes, firewall (portas 22, 80 e 443), fail2ban, trocas automáticas de segurança, Docker. (Usuário não root com sudo: não feito, em aberto.)
4. ✅ **Instalar com Docker Compose** (n8n, Postgres 16 e Caddy em `/opt/keshion`, backup diário dos últimos 7; o Postgres da Clara ainda será criado no passo 7):
   - **n8n** (com Postgres como banco do próprio n8n);
   - **Postgres** também para os dados da Clara (substitui o data store 240983 do Make: fichas, conversas, `_instrucoes`, `_base`);
   - **Caddy** para HTTPS automático.
   - Endereço provisório sem domínio: `n8n.169-58-41-107.sslip.io` (o sslip.io aponta para o IP e o Caddy gera o certificado). Trocar para `n8n.keshion.com.br` quando o domínio for registrado.
   - Senhas e chaves geradas no servidor, num arquivo `.env` dentro do servidor, nunca no chat nem no repositório. A Erica cria o usuário de login do n8n ela mesma na primeira tela.
5. ✅ **Credenciais no n8n** (feito em 12/11: Anthropic, OpenAI, Whapi como "Header Auth account", Google Agenda; mais "Postgres Clara", criada pelo servidor. O app do Google ficou em modo Teste: a autorização expira a cada 7 dias até publicar o app, o que exige domínio, página inicial e política de privacidade. Resolver antes do piloto.) (a Erica cola as chaves direto na tela do n8n, nunca no chat): Anthropic, OpenAI (áudio e foto), Whapi, Google (Agenda).
6. ✅ **Reconstruir os fluxos** (feito em 12/11: `Clara · Atendimento` e `Clara · Envio`, gerados por `tecnico/n8n/gerar_fluxos.py`) a partir das cópias em `tecnico/make-cenarios/` (1A, 1B, 1C, 1D, com LEIA-ME). Pontos de atenção:
   - **1B no Make lê o bloco de texto da resposta do Haiku**, porque o primeiro bloco vem como "thinking" vazio. No n8n, pegar o bloco `type = text` e tirar as cercas ```json.
   - Fila de 7 s (só a última mensagem responde), ficha do paciente, marcar sem duplicar, remarcar, cancelar, até 3 mensagens com "digitando", aviso de falha para a Erica (972584285541), pausa de 12 h quando a doutora responde pelo celular, comando `#reiniciar` (remover antes do piloto ou limitar aos números da Keshion).
   - No n8n dá para filtrar as próprias mensagens da Clara que voltam do Whapi (no Make isso gastava crédito).
   - Aproveitar para incluir a proteção contra chamada sem telefone.
7. ✅ **Copiar os dados** do data store 240983 do Make para o Postgres. Feito em 12/11: `_instrucoes` e `_base` (conferidos, idênticos ao Make) no banco `clara`, tabela `config`. As fichas de teste não foram copiadas, de propósito: o banco começa limpo.
8. ✅ **Testar** com as 56 mensagens do teste A/B (feito em 12/11 pelo fluxo inteiro do n8n, em modo teste: 56 de 56 respondidas, ações certas, tom igual ao da rodada 2; ver `tecnico/teste-ab/relatorio-n8n.md`; script `tecnico/teste-ab/teste_n8n.py`, roda no servidor). Script e conversas em `tecnico/teste-ab/teste_ab.py`. Comparar com a 2ª rodada (planilha "Keshion · Teste da Sarah", aba "Teste A/B 2", id `1hvF2r7wvUsax7mZ7m0Ja3sAODjntbpm-HnIOhCNkVyU`).
   - Nunca testar com números fictícios que façam o fluxo enviar pelo Whapi: cada número conta como conversa no plano.
9. ✅ **Virar** (feito em 12/11, manhã: modo teste desligado e webhook 1 do Whapi trocado para `https://n8n.169-58-41-107.sslip.io/webhook/clara-whapi-7f3c9a2e51b84d06`; Auto Download de imagem, áudio e voz conferido. A Erica testou texto pelo número dela, e funcionou. 1A, 1B, 1C e 1D desativados no Make (não apagados). **Para voltar ao Make:** reativar os quatro e recolocar `https://hook.eu1.make.com/1mi58p7lag4dr5hlsogrpnaxst78bcjq` no webhook 1. Ainda não testados pelo celular real: áudio, foto e marcação.) Texto original do passo: trocar o webhook no painel do Whapi (canal GRNLTR-4K8ZF) do Make para o n8n. Testar com o número da Erica. Depois desativar 1A, 1B, 1C e 1D no Make (sem apagar ainda).
10. **Atualizar** `negocio-ia-clinicas/CLAUDE.md`, a memória e o repositório (`git push` dentro de `negocio-ia-clinicas/`).

## 4. Regras que valem em toda a migração

- Português do Brasil com acentos, sem travessão. A Erica não é programadora: explicar em linguagem simples, passo a passo.
- **Chaves e senhas nunca no chat nem no repositório.** No computador ficam só no `.env` da raiz do projeto; no servidor, no `.env` do servidor.
- Pedir confirmação antes de ações irreversíveis (reinstalar, apagar, trocar webhook) e antes de gastar dinheiro.
- Dados de pacientes reais nunca na pasta do projeto.
- Repositório privado: `negocio-ia-clinicas/` tem Git próprio, remoto `ericakrieger-bot/keshion`. A raiz `fluxo-criativo` é o repositório do curso e ignora essa pasta.
- Toda memória nova ou alterada também vai para o segundo cérebro (`Documents\segundo-cerebro`, GitHub `ericakrieger-bot/segundocerebro`).

## 5. IDs úteis

| O quê | ID |
|---|---|
| Make, equipe | 3084523 (zona eu1) |
| 1A Entrada | 8302405 |
| 1B Resposta | 8302452 |
| 1C Fechamento | 8463643 (webhook 4068828) |
| 1D Envio | 8464848 |
| Questionário Dra. Vivian (fica no Make) | 8491037 |
| Data store da Clara | 240983 |
| Conexão Anthropic no Make | 12954190 |
| Whapi, canal | GRNLTR-4K8ZF (pago até 12/12/2026) |
| Google da demo | keshion.ai.2026@gmail.com |

## 6. Depois da migração (fila de trabalho)

- **PRIMEIRO DA FILA (12/11/2026): áudio não funciona.** A Erica mandou um áudio real pelo WhatsApp e a Clara respondeu pedindo para ela escrever, ou seja, caiu no caminho "não foi possível ouvir" do nó `Texto final da mensagem`. Falhou o `Baixar o áudio` ou o `Transcrever o áudio (OpenAI)` (os dois estão com "continuar mesmo com erro", por isso não apareceu como falha). Para investigar: ler a execução do número 972584285541 em `execution_data` (banco `n8n`) e ver o erro desses dois nós. Suspeitas: o link de mídia do Whapi pede autenticação (token) ao contrário do que o Make fazia, o arquivo chega sem nome ou extensão (a OpenAI exige `.ogg`/`.mp3` no nome do arquivo), ou o tipo do campo binário. Corrigir em `tecnico/n8n/gerar_fluxos.py`, reimportar e testar com um áudio real (só o número da Erica). A Erica pediu para não corrigir antes do reset do limite dela.

- Rota de rascunho para a doutora aprovar antes de enviar (primeira semana do piloto).
- Haiku no dia a dia e Sonnet nas mensagens clínicas (dor, gravidez, reclamação).
- Confirmações (48 h, véspera às 18h, 2 h antes) e CRM em Google Planilhas.
- Versão da Dra. Vivian: base, manual de voz, nome da assistente, ligação no número dela, termo do piloto assinado.
- Teste do Jev (ver memória `pendencia-teste-jev`).
- Logística: domínio keshion.com.br, e-mail @keshion.com.br, site, perfis, acordo de sócios, contador.
