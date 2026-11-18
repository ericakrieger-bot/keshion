# Revisão independente de data e hora antes de marcar

## Resumo em cinco linhas

1. A correção permite reconhecer os formatos de inglês e espanhol cobertos pelos 61 testes originais, todos aprovados nesta revisão.
2. Eu ainda não liberaria a Vivian em 01/12/2026: a barreira pode aceitar dia, mês, ano ou minutos diferentes do que a pessoa escreveu.
3. Data e hora são procuradas separadamente no histórico inteiro, sem vínculo seguro com a escolha mais recente nem com o aceite.
4. Na segunda ou terceira recusa não existe escalada automática; frases fixas continuam em português e podem manter um ciclo sem ajuda.
5. Os resultados das conversas reais de teste e a limpeza estão registrados no complemento ao fim deste relatório.

## Método e limites

Esta parte começou após encerrar a limpeza da parte 1. Executei `node tecnico/n8n/teste_validacao_data_hora.js` na cópia original, sem gerar ou alterar seus arquivos. Resultado: **61 de 61 casos certos**. O teste lê o trecho do detector de texto do JSON gerado; ele não testa toda a decisão de agenda, o aceite ou o Google.

Para ir além, executei o JavaScript atual do gerador em memória em 33 exemplos novos e cinco chamadas do nó completo com relógio fixado em 18/11/2026, 09h de Curitiba. Foram 10 resultados compatíveis e 23 divergências em relação às expectativas definidas para os exemplos. Isso não significa que 70% das pacientes falham: são casos de borda escolhidos para expor limites, alguns intencionalmente artificiais, e incluem formatos que o código não prometeu suportar. Os casos ambíguos exigem esclarecimento, não aceitação automática. As quatro conversas ao vivo foram sequenciais e não incluíram remarcação; criar e cancelar foram exercitados. A remarcação compartilha o validador inspecionado, mas seu funcionamento ponta a ponta não foi revalidado nesta parte.

Evidência reproduzível: `testes_data_hora_extras_2026_11_18.js`, `auditoria_2026_11_18.py`, `evidencias-revisao-2026-11-18/parte2-casos-extras.json`. Nenhuma saída adversarial foi enviada ao Google para tentar marcar errado. Somente as conversas normais com finais 954, 955 e 956 puderam criar eventos.

## Tabela de testes

| Teste | Como fiz | Resultado | Evidência |
|---|---|---|---|
| Suíte original | Node.js, arquivo original, sem alteração | OK | `61 de 61 casos certos (clinica-demo)` |
| Formatos positivos principais | Casos novos de `Nov 19`, `19 de noviembre` e `19/11` | OK | JSON extra: três controles aprovados |
| Confundir hora com data, reais, CEP, telefone e ano solto | Detector atual com dados sintéticos | OK nos controles usuais | `Thursday 11am`, `R$ 1.019,00`, `81911-190`, `554199900919` e `2019` não viraram data |
| Minutos diferentes | Conversa “19/11 às 9:30”, candidato 19/11 às 9h | Falhou | Nó completo retornou `passo: ok` |
| Mês explicitamente diferente | “dia 19 de dezembro às 9h”, candidato 19/11 | Falhou | Nó completo retornou `ok`; “the 19th of December” também passa no detector para novembro |
| Ano explicitamente diferente | Texto de 2025 ou 2027, candidato de 2026 | Falhou no detector | Ano não é comparado com o ano do candidato |
| Data de uma opção, hora de outra | Oferta 19/11 às 9h ou 24/11 às 16h; candidato 19/11 às 16h | Falhou | Nó completo retornou `ok` para combinação não oferecida nem escolhida |
| Escolha negada ou corrigida | Histórico contém opção antiga e depois recusa/correção | Falhou como prova de aceite | Detector aceita a opção antiga; a decisão final depende da IA |
| Segundos fora da grade | Texto 9h, candidato 09:00:59 | Falhou | Nó completo retornou `ok`; validação compara apenas hora e minuto formatados |
| Relativa válida | Texto “amanhã às 9h”, relógio 18/11, candidato 19/11 às 9h | Não reconhece | Nó completo retorna `invalido`, salvo se houver outra menção explícita no histórico |
| “next Friday” e “daqui a 3 dias” | Detector com data calculada para 20/11 e 21/11 | Não reconhece | A demo também não atende avaliações na sexta ou sábado; recusa final nesses dois dias é correta por outra regra |
| Data com ponto/hífen e hora por extenso | `19.11`, `19-11`, `às nove`, `a las nueve`, `nineteenth` | Não reconhece | Lacunas de formato, não prova de falha em toda conversa real |
| Formato americano ambíguo | `12/1` para 1º de dezembro | Recusa pelo desenho atual | Mês/dia americano só habilitado quando o dia é maior que 12; precisa perguntar, não adivinhar |
| Ordinal e valor artificial | Parcela `19th`, fração `R$ 19/11` e `dia 19h` | Aceitação indevida no detector | Não há contexto suficiente para distinguir ordinal, parcela e data |
| Repetir recusa duas ou três vezes | Código e conversa ao vivo no final 957 | Falhou | Três recusas idênticas para “amanhã às 11h”, saídas 3803 a 3808, sem aviso novo à equipe |
| Publicado versus gerado | Comparação de nós e ligações, sem importação | OK na demo | Evidência da parte 1, versões ativa e atual iguais; teste só difere no validador |
| Conversas em inglês, espanhol e português | Marcar, cancelar e consultar Google, uma conversa por vez | Ver complemento | Arquivos `parte2-*-resultado.json` e conversas dos finais 954 a 956 |

## Problemas por prioridade

### 1. Alta: o detector pode liberar um horário que a paciente não escolheu

Em linguagem simples: ele procura o dia em qualquer lugar e a hora em qualquer outro lugar. Assim, pode juntar pedaços de duas opções e considerar confirmado um horário que nunca foi oferecido como conjunto.

Exemplo reproduzido no nó completo: “19/11 às 9h ou 24/11 às 16h” permite passar o candidato “19/11 às 16h”, mesmo depois de a paciente escolher 24/11. Uma oferta antiga recusada também continua disponível como evidência dentro dos últimos 11 mil caracteres. Isso é uma falha da barreira independente: uma IA que se confunda ainda consegue mandar gravar o horário errado.

Como corrigir: guardar as opções oferecidas como intervalos completos, com identificador, fuso e validade; guardar a escolha mais recente e o aceite vinculados à opção. Invalidar opções recusadas ou substituídas. Validar criar e remarcar contra esse estado antes de acessar o Google. A mesma validação atual está ligada às duas rotas, o que é bom, mas ela precisa representar a decisão real.

### 2. Alta: a comparação ignora partes importantes da data e hora

Em linguagem simples: 9h30 pode ser tratado como prova de 9h; “dia 19 de dezembro” pode ser aceito como prova de 19 de novembro. Isso deixa a assistente parecer mais segura do que realmente está.

Detalhe técnico: o padrão português de hora permite `:\d\d`, sem comparar os minutos, e `às 9` também casa com o começo de “às 9:30”. O padrão `dia 19` passa sem validar o mês que vem depois. Os padrões numéricos/ISO não amarram o ano mencionado ao candidato. Ordinais e dias da semana também admitem correspondência parcial antes de um mês contraditório. O candidato de evento é formatado sem segundos para comparar a grade, por isso 09:00:59 passa como 09:00.

Como corrigir: interpretar data e hora completas em formato canônico, validar ano/mês/dia/hora/minuto/segundo, resolver fuso e comparar o instante ou intervalo exato. Uma informação explícita contraditória deve exigir esclarecimento. Para expressões sem mês ou ano, usar contexto da proposta ativa, sem varrer o histórico inteiro por fragmentos soltos.

### 3. Alta: a segunda e a terceira recusa não chamam ninguém

O ramo `invalido` devolve sempre “Esse horário não está disponível para avaliação” e “Quer que eu veja outras opções para você?”. Ele não usa o motivo técnico para explicar o problema, não cria aviso e não incrementa contador. Portanto, se o modelo continuar tentando uma marcação que o detector rejeita, pode repetir indefinidamente sem alerta. O histórico de Emily com dez recusas é coerente com esse desenho; a ampliação de formatos reduz uma causa, mas não elimina o mecanismo do ciclo.

O quarto caso ao vivo confirmou o defeito também em português: três tentativas de “amanhã às 11h”, com nome completo e telefone informados, produziram as mesmas duas frases e nenhum aviso à equipe. Saídas 3803 a 3808. A proposta de avisar a equipe na segunda recusa faz sentido e é urgente antes do piloto. Recomendo contar recusas consecutivas da mesma solicitação, distinguir falha de entendimento de vaga realmente ocupada, avisar uma vez com motivo útil e interromper a repetição. Zerar o contador após sucesso ou mudança efetiva de pedido. O aviso não pode cair no mesmo filtro que hoje suprime informação nova curta.

### 4. Média: uma data correta em linguagem natural pode ser bloqueada

“Amanhã às nove” é uma solicitação compreensível, mas não tem suporte direto no detector. Isso não exige que o sistema adivinhe toda expressão: a saída segura é confirmar a data completa no idioma da paciente e pedir aceite. Hoje a mensagem fixa diz indisponibilidade mesmo quando o problema é só não reconhecer o formato.

O caso `12/1` em inglês é particularmente importante: pode significar 1º de dezembro ou 12 de janeiro. Restringir a interpretação automática reduz erros; falta explicar a ambiguidade e pedir a data por extenso. “Next Friday” também varia por uso, e no calendário atual uma sexta não é dia de avaliação. “Daqui a 3 dias” em 18/11 aponta para sábado, também não permitido. Os testes desses dois textos medem reconhecimento, não defendem marcação em dia fechado.

Como corrigir: normalizar expressões relativas com data de referência e fuso da clínica e, quando houver dúvida, perguntar uma vez por confirmação explícita. Horas por extenso precisam de suporte ou reformulação clara. Não é necessário liberar todo formato novo para o piloto se houver uma alternativa curta e compreensível que evite o ciclo.

### 5. Média: as mensagens fixas desfazem o avanço de idioma

O texto da IA pode estar correto em inglês ou espanhol, mas o fluxo o substitui por português justamente quando há erro, dados faltantes, horário ocupado ou confirmação forçada de cancelamento. O campo `idioma` ainda não faz parte da resposta lida. O lembrete no prompt não traduz o texto definido no código.

Como corrigir: catálogo de frases fixas por idioma, com idioma validado e alternativa segura quando desconhecido. Manter datas, valores e endereço claros. A proposta de localizar as frases é apropriada e urgente, junto com a segunda recusa, porque a paciente precisa compreender como sair do impasse.

## O que ficou certo

Os casos originais que motivaram a correção agora passam. O detector distingue os exemplos usuais de preço, hora, telefone e ano isolado testados aqui. A validação independente também aplica dias de avaliação, grade, antecedência, feriados/recesso e dados mínimos antes de criar ou mudar evento; não encontrei uma ligação alternativa de criação ou remarcação que pule esse nó na demo publicada. Essas proteções são úteis, mas reconhecer uma menção não comprova a escolha nem corrige sozinho uma interpretação errada da IA.

## Conversas e limpeza

Inglês, final 954: recusou corretamente 19/11 às 9h, que estava ocupado; marcou a alternativa oferecida em inglês, “Thursday, Nov 19, at 11am”. Google devolveu o identificador `m2tt309em6145fab9g3ot18r4c`. Depois de pedir cancelamento, recebeu confirmação em inglês com “correct?”. O “Yes, I confirm” seguinte não bastou: o fluxo substituiu a resposta por “Só para confirmar: é a sua avaliação de 19/11 às 11:00, certo?”. Após confirmação adicional, cancelou; ficha sem evento e consulta direta completa ao Google sem o telefone desse teste. Saídas 3771 a 3784. Isso confirma a regressão de idioma e o atrito no cancelamento, além do sucesso da data em inglês.

Espanhol, final 955: marcou diretamente 19/11 às 11h a partir de “jueves 19 de noviembre de 2026 a las 11”. Evento `ackdl6mpju851nfnc4pi732b8k`. Pediu confirmação de cancelamento em espanhol e cancelou após o aceite, sem exigir português. Saídas 3785 a 3793; ficha sem evento e consulta direta completa sem sobra desse telefone.

Português, final 956: marcou diretamente terça, 24/11/2026, às 14h; pediu confirmação antes de cancelar e cancelou após o aceite. Evento `srn0mc7slva4h3qdqi6gdf33sc`. Saídas 3794 a 3802; ficha sem evento e consulta direta completa sem sobra desse telefone.

Data relativa, final 957: três pedidos com “amanhã às 11h” foram recusados, sem aviso, saídas 3803 a 3808. Ao esclarecer “19/11/2026 às 11h”, a mesma vaga foi marcada, evento `3dr8mmkh424umfes9etu6p8t0c`, saídas 3809 a 3812. Depois do pedido de cancelamento e da confirmação, o evento foi cancelado, saídas 3813 a 3816; ficha sem evento e Google sem sobra desse telefone. Esse caso prova um falso negativo ao vivo, inclusive o ciclo na segunda e terceira tentativas.

No total, quatro conversas chegaram à marcação e cancelamento: inglês, espanhol e dois casos em português. A conversa em inglês precisou escolher alternativa livre e confirmar o cancelamento uma vez a mais por causa da frase fixa em português. Não houve teste paralelo, envio real de WhatsApp, alteração de fluxo ou correção de código. Os pedidos de retorno da clínica continuam sendo textos da assistente, não compromissos assumidos por esta revisão.

Limpeza geral confirmada após o encerramento dos quatro casos: zero linhas dos finais 954 a 957 em `pacientes`, `mensagens_recebidas`, `saidas_teste` e `reservas_horario` nos dois bancos, inclusive avisos simulados associados a esses números. Consulta direta completa ao Google sem eventos ativos com os telefones da rodada nas descrições. Evidência final: `limpeza-554199900954.json`. O evento antigo de Henrique, final 810, não foi apagado nem alterado. Não declaro resolvidas sobras de rodadas antigas. Execuções do n8n seguem a retenção normal e não foram apagadas.
