# Testes da Clara (checklist completo)

Regras: números de teste com prefixo `554199900` (nada sai pelo WhatsApp). A agenda do Google é real: todo teste que marca precisa cancelar no fim e conferir que não sobrou evento. Quem executa: **C** = Claude (conversa de testes), **X** = Codex (revisão independente), **E** = Erica (celular real), **V** = dentista da clínica piloto.

## Portão 1: a cada mudança publicada (fluxo, instruções ou base)

| # | Teste | Quem | Como | Situação |
|---|---|---|---|---|
| 1.1 | Teste rápido (5 conversas: oi, preço, marcar e cancelar, dor, foto) em 2 minutos | C | script `teste_rapido.py` | **criar** |
| 1.2 | 56 mensagens fixas (tom e regras) | C | `teste_n8n.py` no servidor + `comparar_antes_depois.py` | pronto |
| 1.3 | Pacientes simulados (22 perfis, nota de outra IA; aceita filtro por telefone; guarda `historico-notas.csv`) | C | `paciente_simulado.py` no PC | pronto |
| 1.4 | Agenda limpa e banco de teste limpo depois dos testes | C | consulta no banco `clara` | pronto (os scripts limpam) |
| 1.5 | Revisão independente da feature | X | `PROMPT-CODEX-REVISAO.md` com a feature indicada | pronto |

## Portão 2: antes de ligar uma clínica real (1º piloto com clínica conhecida, até 30/11)

| # | Teste | Quem | Situação |
|---|---|---|---|
| 2.1 | Mídia real pelo celular: áudio, foto, documento, figurinha, vídeo, localização | E | áudio corrigido em 12/11; refazer todos no número da clínica |
| 2.2 | Doutora respondendo pelo celular: Clara fica 12 h em silêncio naquela conversa | E | testado com simulação; falta no celular real |
| 2.3 | Falhas simuladas: IA fora, lenta ou com resposta quebrada; Google fora ou sem permissão; Whapi recusando envio. Conferir "só um instante", aviso para a equipe, ficha certa e nada de resposta errada | C, X | **por fazer** (cópia do fluxo apontando para endereços falsos) |
| 2.4 | Agenda: fora do expediente, sábado, domingo, feriado, recesso, mais de 90 dias, mesmo dia, horário que acabou de passar | C | parcial; **criar roteiro próprio** |
| 2.5 | Concorrência: duas pessoas pegando o mesmo horário; 3 mensagens seguidas; reenvio do Whapi; resposta rápida antes da Clara terminar | C, X | parcial (ordem entre respostas ainda pode trocar) |
| 2.6 | Segurança: canal errado, caminho antigo do webhook, mídia de site de fora, grupo, mensagem da própria Clara voltando | C, X | feito em 12/11; repetir a cada mudança na entrada |
| 2.7 | Isolamento por clínica: mesmo telefone (e mesmo id de mensagem) em duas clínicas; fichas, conversas, saídas e canal separados | C, X | **passou em 17/11** com demo x `clinica-teste` (`teste_isolamento.py` no servidor). Repetir com a Vivian no ar |
| 2.8 | Autorização do Google renovando sozinha (app publicado) | E, C | depende da página e da política de privacidade |
| 2.9 | Carga: 20 conversas ao mesmo tempo (tempo de resposta e erros) | C | **por fazer** |
| 2.10 | Custo por conversa (tokens da IA e mensagens) para fechar o preço | C | **por fazer** |
| 2.11 | Recuperação: reiniciar o servidor; restaurar o backup numa cópia; backup fora do servidor | C | **por fazer** |
| 2.12 | Aceite da clínica: roteiro com os casos reais da clínica piloto; o dentista aprova tom, regras e avisos | V, E | antes de ligar o número |
| 2.13 | Avisos chegando no número certo da clínica (não no da Erica) | E | quando a estrutura por clínica existir |

## Portão 3: durante o piloto (toda semana)

| # | Teste | Quem |
|---|---|---|
| 3.1 | Ler 10 conversas reais da semana e anotar erros de tom ou de regra | E, C |
| 3.2 | Conferir avisos para a doutora: chegaram, eram necessários, nenhum faltou | V, E |
| 3.3 | Conferir agenda x ficha: marcações da Clara batem com a agenda | C |
| 3.4 | Rodar os pacientes simulados depois de cada ajuste pedido pela clínica | C |
| 3.5 | Conferir a autorização do Google e o vencimento do plano do Whapi | E |

## Registro de rodadas

**18/11/2026, manhã (06h56 a 08h, Curitiba, clínica FECHADA o tempo todo), correções de avisos, idioma, "encaixe" e hora em inglês:**

- 1.3, 5 perfis (06h57, US$ 0,14): Bia 8, Camila 8, Fernanda 6, Patrícia 9, Emily 6 (17/11: 9, 8, 9, 9,5, 8; 18/11 22h37: 8, 7, 6, 7, 7). Emily ofereceu horários em inglês, marcou e cancelou; sem "Esse horário não está disponível"; Camila sem "encaixe".
- 1.3, 22 perfis (07h11, US$ 0,58): notas de 6 a 9, **exceto Emily 2**. Em inglês com a data escrita "Nov 19" a conferência de horário não reconhece a data (só aceita "19/11" ou "dia 19") e a Clara repetiu "Esse horário não está disponível" 10 vezes. Nos 5 perfis a Clara escreveu "19/11" e funcionou: depende de como a IA escreve a data. Sem "SEM RESPOSTA" em nenhuma das duas rodadas.
- 1.2, 56 mensagens: 56 de 56 respondidas, nenhuma sem resposta, maior tempo 58 s, 4 avisos, sem "só um instante" de falha. Resultado em `tecnico/teste-ab/teste-n8n-resultado-20261118-avisos-idioma-hora.json`.
- 1.4: fichas 8xx apagadas pelo script; fichas 101 a 107 do teste das 56 ficam no banco (sem evento de agenda). **Agenda da demo NÃO conferida:** esta sessão não enxerga a conta keshion.ai.2026 (precisa ser compartilhada). Conferir à mão os eventos de 19/11 em diante.
- Não rodado em horário comercial (clínica aberta): repetir os perfis de agenda depois das 8h.

**18/11/2026, noite (18h08 a 18h56 de Curitiba, clínica ABERTA), Pacote A, casos 1 a 7 e 5 perfis:**

- Casos 1 a 7 (conversas sintéticas, finais 961 a 967): **todos OK.** 1 sangramento depois de aviso de recibo gerou "URGENTE: chamar uma pessoa agora" e "ok obrigada" não gerou aviso; 2 "amanhã às 11h" marcou 19/11 às 11h; 3 sábado e 24/11 às 10h: a IA recusou sozinha (contador em 0, a trava do fluxo não foi acionada, mas a equipe foi avisada); 4 "Yes" em inglês cancelou na hora, tudo em inglês; 5 "Não, quero manter" respondeu "continua marcada"; 6 espanhol inteiro sem português para a paciente; 7 "26/11 às 14h" gravou 26/11 às 14h no Google. Agenda do Google conferida (nada sobrou).
- **Problema 2 (leve): cancelamento perguntado duas vezes** em português (Bia, 801): depois do "certo?" da IA, a resposta "sim, pode cancelar ... || e a armadilha ainda não rolou" (duas mensagens juntas) fez o fluxo perguntar de novo "Só para confirmar...".
- 1.3, 5 perfis (18h46, US$ 0,14): Bia 6, Camila 7, Fernanda 7, Patrícia 8, Emily 8 (média 7,2; manhã 8, 8, 6, 9, 6 = 7,4). Quem marcou antes continuou marcando; Emily em inglês e espanhol sem frase fixa em português.

**19/11/2026, 08h20 (Curitiba, clínica aberta), 22 perfis: INVÁLIDA, a repetir.** Notas 0 a 4 e 137 "SEM RESPOSTA" vieram do teste, não da Clara: por volta das 08h28 o `paciente_simulado.py` (no PC) parou de ler as respostas no banco (provável: o Claude fechou sozinho e o processo ficou solto). O n8n processou tudo sem erro (233 atendimentos e 160 envios, todos com sucesso, sem "credit balance", sem "Só um instante"), e a Clara respondeu em cerca de 20 s a cada mensagem. O teste também não limpou no fim: sobraram 22 fichas, 454 saídas, 232 mensagens recebidas, 4 reservas e 3 eventos no Google (Bia 24/11, Paula 26/11, Júlia 26/11), apagados à mão depois, sobrando só o evento antigo do Sergio. As notas dessa rodada foram tiradas do `historico-notas.csv`. A rodada anterior (18/11 de noite, 22h) também travou (PC suspendeu). **Lição:** rodar `paciente_simulado.py` com o PC sem suspender e sem fechar o Claude; conferir no meio se a ficha ainda é lida.
- **Ainda por fazer:** 22 perfis (comparar com 18/11 manhã, 6 a 9, Emily 2) e as 56 mensagens fixas.

## Melhorias nos scripts

1. Criar `teste_rapido.py` (1.1).
2. Pacientes simulados: perfis novos (3 mensagens seguidas, some e volta no dia seguinte, pergunta de outro paciente, reclamação de tratamento feito na clínica, pessoa que só manda áudio na vida real), critérios lidos da base de cada clínica, e um histórico de notas para ver a evolução.
3. Roteiro de datas difíceis (2.4).
4. Cópia do fluxo com endereços falsos para as falhas (2.3).
