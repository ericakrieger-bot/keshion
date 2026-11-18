# Prompt para o Codex revisar as correções de 17/11 (noite)

Abra o Codex na pasta `Documents\Claude Code\keshion` (repositório privado `ericakrieger-bot/keshion`). Antes de colar, confira que nenhuma outra conversa está rodando teste da Clara: duas rodadas ao mesmo tempo apagam as fichas uma da outra. **Antes, recarregue o saldo da Anthropic:** sem saldo, a Clara responde "Só um instante, vou verificar" a tudo e os testes não valem. Copie tudo abaixo da linha e cole no Codex.

---

Você vai fazer uma revisão independente de mudanças que outra IA (Claude) fez, publicou e testou na assistente de WhatsApp da Keshion. Elas respondem às duas revisões que você fez em 17/11: `tecnico/teste-ab/relatorio-codex-20261117.md` (testes) e `tecnico/n8n/revisao-codex-estrutura-por-clinica-2026-11-17.md` (estrutura por clínica). Quero uma segunda opinião honesta: o que ficou certo, o que ficou errado ou pela metade, o que é arriscado e o que não foi testado. Responda em português do Brasil, com acentos e sem travessão. Eu não sou programadora: explique cada problema em linguagem simples, além do detalhe técnico.

## Regras de segurança (obrigatórias, a demo está no ar)

Leia e siga a seção "Regras de segurança" de `tecnico/n8n/PROMPT-CODEX-REVISAO.md`. Em resumo:
- só números com prefixo `554199900`;
- nada em produção sem me perguntar (fluxos, config, .env, credenciais, Docker, Whapi, usuários do Postgres);
- nunca mostrar senha, token ou caminho do webhook;
- o Google Agenda é real: cancele o que marcar e confira que nada sobrou;
- não use os números 972584285541 e 972552994413, e **não force uma falha de envio real** para ver o alerta (ele manda mensagem de verdade).

Para a clínica de teste, valem as mesmas regras, no banco `clinica_teste` (senha `CLINICA_TESTE_DB_PASSWORD` no `/opt/keshion/.env`). Se quiser testar permissões do Postgres, use um contêiner descartável, sem rede (`docker run --rm --network none ...` com a mesma imagem do Postgres do compose), nunca o Postgres de produção.

## O que mudou

Commits `110f4d1` e `877df8d` (veja `git show`). O `877df8d` também traz as correções dos seus achados nos testes, feitas por outra conversa e já publicadas antes.

**A. Correções dos achados dos testes** (descritas em `tecnico/n8n/LEIA-ME.md`, seção "17/11/2026 (noite): correções da revisão do Codex"):
- o fluxo confere a agenda por conta própria antes de criar ou mudar um evento: dia da semana, horário, 90 dias, antecedência mínima, feriados e recesso, nome, sobrenome e telefone, e se o dia e a hora apareceram na conversa. As regras ficam em `agenda.regras` do `clinica.json`;
- trava de vaga de 2 minutos (tabela `reservas_horario`);
- cancelamento só depois de a assistente pedir confirmação;
- aviso para a equipe sempre que a Clara promete encaminhar, sem repetir (colunas `ultimo_motivo_humano` e `envio_ate`);
- ordem das mensagens: o turno seguinte espera o anterior terminar de sair (máximo 60 s);
- instruções novas da demo: regras R (idioma), S (quem já é paciente), T (não prometer o que a base não diz), cancelamento com menos de 24 h. Base sem promessa de lembrete e acompanhamento.

**B. Decisões da Erica sobre a revisão da estrutura:**
1. **Alerta de falha do WhatsApp:** saía pelo canal da própria clínica, com o texto do paciente. Agora vai só para a Keshion, pelo canal do Whapi da Keshion (`tecnico/n8n/alerta-keshion.json`), sem o texto: clínica, final do telefone e erro do Whapi (até 120 caracteres). Nó "Avisar a Keshion da falha" no fluxo de envio. O campo `aviso_falha_envio` saiu do modelo e da ficha da Vivian.
2. **`modo_teste` ausente:** antes virava envio real; agora vale como teste (`coalesce(..., '1') <> '0'`). O `preparar_banco.py` exige "1" ou "0".
3. **`#reiniciar`:** só na demo e na clínica de teste. Nas outras, `numeros_keshion` fica vazio e o `preparar_banco.py` recusa número.
4. **Dois usuários por banco:** dono `<banco>` só para instalar e `<banco>_app` para o n8n. O `banco.sql` dá ao `_app` leitura e gravação de linhas em todas as tabelas, só leitura na `config`, e nada de mudar estrutura. Se o `_app` não existir, o bloco não faz nada. **Ainda não aplicado na demo nem na clínica de teste**, que continuam usando o dono.
5. **Roteiro geral de clínica nova:** `tecnico/n8n/CLINICA-NOVA.md`.
6. A clínica de teste pode marcar na agenda real da demo (decisão: aceitável).

**C. Correções de 18/11 (manhã), publicadas** (commits `d27a0f4` e `e58104a`):
1. Avisos: quando o motivo é parecido com o do último aviso (até 90 min) mas a mensagem nova traz pergunta ou informação, sai `*Complemento do aviso anterior*` em vez de nada; palavras genéricas não contam na comparação.
2. O pedido para a IA termina com um lembrete de responder no idioma do paciente.
3. Base da demo: "Com a clínica fechada, nunca fale em encaixe."
4. A conferência de horário antes de marcar entende "9am", "4 pm", "at 4" e "a las 9" (antes, paciente em inglês não conseguia marcar). As frases fixas do fluxo continuam só em português: avalie se é problema.

Leia, nesta ordem:
1. `tecnico/RETOMAR-AQUI.md`
2. `tecnico/n8n/LEIA-ME.md`
3. `tecnico/n8n/CLINICA-NOVA.md`
4. `tecnico/n8n/gerar_fluxos.py`
5. `tecnico/n8n/preparar_banco.py`
6. `tecnico/n8n/schema-clara.sql`
7. `tecnico/n8n/alerta-keshion.json`
8. os `clinica.json` (modelo, demo, teste, Vivian)
9. `clientes/clinica-demo/instrucoes-sarah.md` e `base-clinica.md`

## O que o Claude testou

1. Antes de publicar, os fluxos no servidor eram iguais aos gerados pelo código, a não ser pelos ids internos das condições. Depois da mudança, só três nós do envio mudaram: "Modo teste?", "Modo teste ligado?" e o nó do alerta.
2. Expressão do alerta conferida com dados de exemplo: o texto do paciente e o telefone completo não aparecem. **O alerta não foi disparado de verdade.**
3. Permissões do `_app` num Postgres descartável:
   - pode: ler a config; gravar e apagar ficha; gravar mensagem, reserva e saída de teste;
   - não pode: mudar a config, apagar, alterar, esvaziar ou criar tabela.
4. Teste de isolamento depois de publicar: passou.
5. Pelas correções da parte A, a outra conversa relatou testes com pacientes simulados. Confira em `tecnico/teste-ab/historico-notas.csv` e nos relatórios mais recentes.

## O que quero que você confira

1. **Alerta:**
   - ainda pode vazar dado de paciente pela mensagem de erro do Whapi?
   - funciona quando o canal que falhou é o próprio canal da Keshion (a demo)?
   - o que acontece quando o canal da Keshion também está fora?
   - o nó está ligado no caminho certo (saída de erro do envio)?
2. **Modo teste:** existe outro ponto dos fluxos que lê `modo_teste` e ainda trata ausência como envio real? E o atendimento?
3. **Permissões:**
   - o fluxo de atendimento faz alguma operação que o `_app` não pode (por exemplo `ALTER`, `TRUNCATE`, `SELECT ... FOR UPDATE` na config, sequências)?
   - o que falta para migrar a demo para o `_app` sem parar a Clara? Escreva o passo a passo, sem executar.
4. **Agenda (parte A):**
   - as regras do fluxo batem com a base da demo (dias, horários, 90 dias, feriados)?
   - a trava de 2 minutos resolve duas pessoas pegando a mesma vaga?
   - algum caminho cria ou muda evento sem passar pela validação?
5. **Avisos e ordem (parte A):** a deduplicação pode esconder um aviso que deveria sair? A espera de até 60 s pode atrasar ou travar uma conversa?
6. **`CLINICA-NOVA.md`:** dá para seguir do zero? Os comandos estão certos? Falta algo (backup do banco novo, conferir as credenciais certas, voltar atrás)?
7. **Instruções novas da demo:** as regras R, S e T contradizem algo? Repita alguns dos seus perfis antigos (paciente antigo, idioma, promessa sem base) e compare com as notas anteriores.
8. Repita o teste de isolamento uma vez e confira que nada sobrou nos dois bancos nem na agenda.

## Entrega

Crie `tecnico/n8n/revisao-codex-correcoes-17-11-AAAA-MM-DD.md` (data do dia) com:
1. Resumo em 5 linhas: depois disso, o que ainda impede ligar a Dra. Vivian?
2. Tabela de testes: teste, como fez, resultado (ok, falhou, não deu para testar), evidência.
3. Para cada achado das suas duas revisões anteriores: resolvido, parcial ou não resolvido, com o motivo.
4. Problemas novos, do mais grave ao mais leve: o que é, por que importa (linguagem simples), como corrigir (técnico).
5. Confirmação de limpeza: linhas de teste apagadas nos dois bancos e nenhum evento de teste na agenda.

Não corrija nada no código nem em produção: só aponte. Eu decido depois o que aplicar.
