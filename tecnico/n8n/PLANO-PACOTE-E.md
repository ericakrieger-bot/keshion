# Pacote E: correções antes do piloto (plano de 25/11/2026)

Origem: revisão do Codex de 25/11 (`tecnico/codex/revisao-codex-2026-11-25.md`), rodada de 22 perfis de 24/11 (média 6,64) e decisões da Erica em 25/11. **25/11, 09h26: itens 1, 2 e 8 publicados na demo e na clínica de teste** (teste: `tecnico/teste-ab/PROMPT-TESTE-25-11-pacote-e-cancelar.md`). O resto ainda não foi implementado. Ordem pensada para a Clara poder ser ligada só fora do horário na semana 1.

## Decisões da Erica (25/11)

1. **Tom único da Clara.** Sem espelhar o jeito do paciente. Educada, simpática, profissional e um pouco informal, como uma secretária de clínica. Vale para todos os pacientes. Tirar o espelhamento das instruções e do critério da juíza. Tom robótico (frases repetidas, "só um instante, estou verificando" várias vezes) é **quase deal breaker**: a promessa do produto é resposta fluida e humana.
2. **Só português**, em tudo: instruções, base, frases fixas, testes e clientes. Retirar toda menção a inglês e espanhol (perfil Emily, frases em en e es no gerador, testes de idioma, critérios). Já existe o commit `be5ff46` (só no Git, não publicado).
3. **Mensagem padrão de confirmação de marcação.** Avaliação: "Avaliação confirmada para [dia], [hora], com a Dra. Suzana. Valor R$ 150. Endereço: [endereço]." Outros procedimentos (limpeza, etc.): mesma mensagem **sem o preço**. Vale também para paciente antigo.
4. **Base com listas "o que fazemos" e "o que não fazemos"** (ex.: fazemos clareamento, alinhador, lente de contato; não fazemos implante, dentadura, coroa sobre implante). Mais uma regra: o que não estiver em nenhuma lista, verificar com a equipe e não afirmar.
5. **Mais tempo antes de responder** para ler todas as mensagens seguidas e entender. Hoje 20 s; avaliar subir mais e testar com perfil de várias mensagens.
6. **"Dói?" sobre um procedimento não é relato de dor.** A Clara deve usar o contexto da conversa.
7. **Google fora do ar não pode oferecer horário** (item 6 do Codex sobe de pequeno para **médio a grande**).
8. **Juíza do teste:** regras mais claras e menos peso em detalhes de tom. Avaliar duas juízas ou critérios fixos (ver `tecnico/teste-ab/COMO-FUNCIONA-O-TESTE.md`, seção 7).
9. **Prioridade 1 absoluta: loop do cancelar.**

## Lista de correções, por prioridade

| # | Correção | Tipo | Fecha qual ponto do Codex |
|---|---|---|---|
| 1 | **Cancelar sem loop e sem cancelar o evento errado**: guardar na ficha a operação pendente (qual evento, data e hora) e só cancelar com "sim" para aquela pergunta; aceitar confirmação longa, "Valeu!" e dúvida no meio sem perder a pendência; "não é minha, é da Laura" não é recusa. Se repetir sem resolver, passar para a equipe com contexto | fluxo | 2 |
| 2 | **Urgência**: ampliar sinais (dificuldade de engolir, de respirar, falta de ar, inchaço com febre) com a clínica; texto fixo coerente quando a barreira atua | fluxo e base | 1 |
| 3 | **Marcar só com escolha atual do paciente**: oferta antiga não vale como escolha; texto do paciente começando com "Clara:" não vira fala da clínica | fluxo | 3 |
| 4 | **Google fora do ar, "nove da manhã" e vaga ocupada**: não oferecer horário sem consulta válida; se ocupado, recalcular alternativas ou encaminhar | fluxo | 6 |
| 5 | **Remarcar depois de falta (Diego)**: a equipe decide a multa; a Clara oferece o próximo horário. Ficha com telefone | regra e fluxo | 11 |
| 6 | **Base**: listas fazemos/não fazemos; mensagem padrão de confirmação; retorno depois do expediente (doutora até 17h, secretária até 18h) sem prometer "em breve" | base | 11 |
| 7 | **Tom e espera**: tom único, sem robô, "dói?" em contexto; tempo maior de espera | instruções e fluxo | decisões 1, 5 e 6 |
| 8 | **Só português** em tudo | instruções, gerador e testes | decisão 2 |
| 9 | **Teste de aceitação com agenda de verdade**: verificar evento criado, remarcado, cancelado; telefones exclusivos por rodada; limpeza que não apaga evidência | testes | 5 |
| 10 | **Juíza**: critérios alinhados à base (30 dias de validade, sem cobrar o que a base não diz), sem espelhamento, gravidade por problema | testes | 5 e decisão 8 |
| 11 | Esperas e versão da mensagem (resposta antiga não grava por cima de mensagem nova, reinício ou doutora) | fluxo | 4 |
| 12 | Fila e histórico por mensagem com id; validar tipos da resposta da IA; erro sem texto livre | fluxo | 7 e 9 |
| 13 | Webhook com autenticação e deduplicação antes de chamar mídia paga | fluxo e Whapi | 8 |
| 14 | Retenção de dados, usuário `_app`, alerta externo (Healthchecks.io), restauração real do backup | operação (com OK) | 10 e 12 |

Operação em paralelo (Erica): renovar o Google no n8n (vence ~26/11) e apagar eventos de teste da agenda.

## Como publicar

Mesmo roteiro de sempre: `gerar_fluxos.py`, testes locais, cópia da versão atual no servidor, import e publish sem reiniciar o n8n, com OK da Erica. Teste ao vivo só na conversa de testes, um por vez. Depois, nova revisão do Codex com o prompt atualizado (salva em `tecnico/codex/`).
