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

**24/11/2026 (Curitiba, 09h37 a 17h43, clínica ABERTA em todas as rodadas), Pacote C + cancelar (23/11) + correções de 24/11:**

- **Casos 1 a 10, 12 e alinhador (conversas sintéticas, finais 961 a 982): OK, com 3 ressalvas.** 1 marcou 01/12 às 9h com evento no Google e sem pergunta de cancelamento; 2 "isso é só uma dúvida" não cancelou, e o "sim" de verdade cancelou com uma pergunta só; 3, 4, 5 e 6 aviso URGENTE (pt, en, es e meio de marcação, nada marcado); 7 negações em pt, es e en sem aviso; 9 horário negado em pt, en e es sem marcar (usado 01/12 às 9h, oferecido pela Clara); 10 a Dra. assumiu às 10h29:14, pausa até 22h29, saiu 1 mensagem antes e 2 foram descartadas; 12 cadastro 7 de 7. **Ressalvas:** (a) **caso 8** ("clareamento faz a gengiva sangrar?"): a Clara não respondeu sozinha, mandou "Chamar uma pessoa" (sem URGENTE); (b) **caso 11 (áudio WAV e Ogg) NÃO RODADO:** o fluxo só aceita áudio hospedado no Whapi e o arquivo do Codex (`midia-integrada-audio-pt.json`) não está no repositório; (c) **cancelar em loop** (ver abaixo).
- **PROBLEMA GRAVE: cancelar ainda é perguntado duas vezes ou em loop.** No caso 2 foi uma pergunta só, mas no teste manual do final 961 ("preciso cancelar, pode cancelar?") a IA perguntou "certo?" sem a palavra "cancelar" e o fluxo perguntou de novo "Só para confirmar: você quer cancelar...". Nos 22 perfis: Bia (nota 2, ~7 vezes, nunca cancelou), Sandra (nota 2, mais de 8 vezes, nunca cancelou), Thiago (3 vezes), Júlia e Emily (2 vezes). Nos 5 perfis: Bia e Emily (2 vezes). A correção de 23/11 não cobre a pergunta da IA sem a palavra "cancelar".
- **Parte 2:** (1) espera de 20 s: uma resposta só para 2 e 3 mensagens seguidas; mínimo 25 s no caso 8 manual e 27 s nas 56 (nenhuma abaixo de 20 s); caso à parte com 12 s entre as mensagens: uma resposta só, 28 s depois da segunda. (2) "digitando": `saidas_teste` NÃO guarda `typing_time` (só o texto); conferi a regra no código publicado (1 s a cada 4 letras, mínimo 4, máximo 50) e pelo intervalo entre as mensagens de uma resposta, que bate com o tempo calculado (ex.: 118 letras = 30 s e intervalo de 31 s; 176 = 44 s; 187 = 47 s); nenhuma passou de 50 s. (3) ordem: nenhuma resposta fora de ordem. (4) alinhador: "cada visita de retorno do alinhador é paga à parte, R$ 150, não incluída" (não disse "a cada 2 meses"). (5) marcar e cancelar: evento criado e apagado (ficha), aviso para a equipe; a despedida vem na própria resposta ("Te esperamos na terça!"), sem mensagem separada 1 minuto depois. Remarcar só nos perfis.
- **Caso 13, 5 perfis (US$ 0,13; a 1ª tentativa foi interrompida pelo app, apagada e refeita):** Bia 7, Camila 7, Fernanda 8, Patrícia 9, Emily 8 (média 7,8; 18/11 noite 7,2). Emily em inglês sem frase fixa em português.
- **Caso 14, 22 perfis (16h46 a 17h26, US$ 0,60, válida, sem "SEM RESPOSTA" nem "ERRO DE LEITURA"): média 6,64** (17/11 7,23; 18/11 7,05; Codex 19/11 7,32). Notas: Bia 2, Ricardo 8, Camila 7, Marcos 8, Paula 8, Sandra 2, Fernanda 8, Dona Lourdes 5, Júlia 6, Henrique 8, Patrícia 7, Gustavo 7, Wagner 8, Rafaela 8, Emily 6, Cláudio 7, Dona Marta 7, Eduardo 9, Letícia 8, Thiago 5, Bruna 8, Diego 4. **Paciente antigo** (Wagner, Cláudio, Dona Marta): 7,33 (regra nova só em 27/11). Abaixo de 6: Bia e Sandra (loop de cancelar), Diego (não ofereceu horário para remarcar, ficha sem telefone), Dona Lourdes (não disse que a clínica não faz implante nem dentadura; "a clínica está aberta" às 17h13, depois do expediente da Dra.), Thiago (cancelar pedido 3 vezes). Relatório: `paciente-simulado-20261124-214610.md`.
- **Caso 15, 56 mensagens (17h31 a 17h43, servidor):** 56 de 56 respondidas, 0 sem resposta, 0 "só um instante", menor tempo 27 s, maior 84 s, 8 avisos para a equipe. As 3 mensagens seguidas do C6 geraram uma resposta só (30 s). Resultado em `teste-n8n-resultado-20261124-pacote-c.json`.
- **Caso 16, limpeza:** banco com 0 fichas, saídas, mensagens recebidas e reservas `554199900%`. Google: a Erica apagou à mão os eventos de 26/11 11h e 14h (perfis 807 e 815 da 1ª tentativa) e de 26/11 11h e 01/12 11h (perfis 801 e 805 da rodada interrompida dos 22 perfis). **Agenda do Google da demo não conferida por mim** (esta sessão não enxerga a conta); conferir à mão os eventos de 26/11 em diante. Não mexi no evento antigo do Henrique (final 810).

**25/11/2026 (Curitiba, 18h23 a 19h30), Pacote E parte 1 (cancelar, urgência, só português): NÃO PASSOU no cancelar.**

- Antes: saldo US$ 11,45; chave do `.env` = "Keshion-apenas-testes"; nenhuma ficha de teste no banco.
- **Parte 1, casos manuais (18h23 a 18h54, clínica aberta; Dra. já fora desde as 17h).** Conversas: `tecnico/teste-ab/pacote-e-parte1-20261125-casos-manuais.md`.
  - 1 "Valeu!": **FALHOU.** Perguntou 3 vezes e não cancelou; só cancelou com "sim, pode cancelar".
  - 2 confirmação longa: OK (1 pergunta, evento apagado).
  - 3 multa no meio: OK (respondeu, perguntou de novo com dia e hora, "sim" cancelou; 2 perguntas).
  - 4 "é da Laura": OK (não cancelou, "isso, pode cancelar" cancelou; 2 perguntas). A pergunta do fluxo disse "a sua avaliação", e era da filha.
  - 5 manter: OK (1 pergunta, "continua marcada", evento mantido).
  - 6 três sem decisão: **FALHOU.** Não passou para a equipe, nenhum aviso. Evento mantido.
  - Fichas: `cancelar_evento` vazio e `cancelar_tentativas` 0 ao fim de todos os casos (nos casos 1, 2, 3, 5 e 6 a pendência nunca chegou a ser gravada).
- **Parte 2, urgência:** 3 de 3 com aviso URGENTE. A resposta fixa não apareceu em nenhuma (a IA escreveu o próprio texto, mandou ao pronto-socorro e prometeu encaixe hoje, às 18h55, com a Dra. já fora). Controles: nenhum virou URGENTE; "dói pra engolir depois da extração?" (18h59) gerou "Chamar uma pessoa" e indicou pronto-socorro.
- **Parte 3, 6 perfis (19h11 a 19h28, clínica FECHADA; 24/11 foi com ela aberta), válida, US$ 0,16:** Bia 4 (era 2), Camila 8 (7), Sandra 7 (2), Júlia **2** (6), Larissa 6 (nova), Thiago 4 (5). Relatório: `paciente-simulado-20261126-001039.md` (nome com o relógio do PC). A 1ª tentativa foi morta por um limite de tempo posto pelo Claude; apagada e refeita.
  - Bia, Sandra e Thiago sem loop. **Júlia em loop:** confirmou várias vezes e não cancelou; depois de passar para a equipe, o fluxo voltou a perguntar.
  - Larissa: uma resposta só para as mensagens picadas, sem frase repetida. Nenhum inglês ou espanhol.
  - Thiago: a limpeza do script não conseguiu cancelar pela conversa (causa não apurada).
- **Causas (lidas em `gerar_fluxos.py`, "Decidir a ação"):** (a) a pendência só é gravada quando a IA devolve a ação `cancelar`; quando ela mesma pergunta ("certo?") com ação `responder`, nada é gravado (casos 1 e 6); (b) "sim" com outra pergunta junto, ou começando por "isso"/"já falei", não conta (Júlia); (c) depois da 3ª tentativa a pendência é apagada e o ciclo recomeça (Júlia).
- **Fora do escopo, visto na rodada:** horário cancelado ou disputado fica reservado por 5 minutos: a Clara oferece, recusa ("acabou de ser preenchido") e depois diz que está livre. `#reiniciar` só vale para os números de `numeros_keshion`, não para `554199900`.
- **Limpeza:** 0 fichas e reservas de teste. Eventos apagados da agenda: Júlia 26/11 16h e Thiago 01/12 14h (rodada interrompida), Elisa 03/12 14h e Fabia 03/12 16h (casos 5 e 6), Thiago 26/11 16h (parte 3). Já existiam antes e ficaram: Luciana 26/11 9h, Bia 26/11 11h, Paula 01/12 11h.

## Melhorias nos scripts

1. Criar `teste_rapido.py` (1.1).
2. Pacientes simulados: perfis novos (3 mensagens seguidas, some e volta no dia seguinte, pergunta de outro paciente, reclamação de tratamento feito na clínica, pessoa que só manda áudio na vida real), critérios lidos da base de cada clínica, e um histórico de notas para ver a evolução.
3. Roteiro de datas difíceis (2.4).
4. Cópia do fluxo com endereços falsos para as falhas (2.3).
