# Plano de produto e diferenciais (16/11/2026)

> Decisões da Erica sobre a análise do relatório do Codex (`pesquisa/funcionalidades-concorrentes.md`). Roadmap e tarefas atualizados no Notion no mesmo dia.

## Decisões

- **Diferenciais aprovados:** jornada do orçamento alto por tratamento, relatório de reais recuperados auditável, voz de alto padrão, modo copiloto, sucesso do cliente dedicado (no lugar de "serviço feito para você"), diagnóstico grátis, custo total transparente. **Garantia só depois de ter mais clínicas operando.**
- **3 pacotes:** Essencial, Recupera e Completo. Preços a definir até 05/12.
- **Cobrança por resultado:** testar como bônus, medido pelo relatório de reais recuperados.
- **Integração com software odontológico:** fora do roadmap até um cliente pedir. A Dra. Vivian não usa nenhum.
- **Voz:** 2º semestre de 2027 (etapa 1: áudio no WhatsApp; etapa 2: ligação).
- **Recuperação de receita antecipada para dezembro**, testada na demo e no piloto.
- **Público inicial do app:** dentista solo ou clínica com até 2 ou 3 dentistas, geralmente sem software e às vezes sem secretária. App v1 em dezembro e janeiro.

## Relatório de reais recuperados (como funciona)

1. Todo agendamento recebe uma **origem** automática: fora do horário, retomada de conversa, lembrete de orçamento, falta remarcada, encaixe da lista de espera, retorno ou reativação.
2. A clínica confirma no app: **compareceu** ou **faltou**, e **orçamento aceito** com valor.
3. Só entra no relatório o que foi **confirmado pela clínica**. Cada linha tem data, iniciais do paciente, origem, link da conversa e valor.
4. Total do mês = soma das linhas confirmadas. Faltas: mostrar a taxa de antes (informada pela clínica) ao lado da atual, como comparação, nunca como "faltas evitadas".

## Diagnóstico do atendimento (passo a passo)

1. Escolher clínica A ou B do Funil que anuncia no Instagram.
2. Três contatos como paciente interessado em lente ou alinhador: horário comercial, noite (21h) e sábado.
3. Ficha com 12 critérios: tempo da 1ª resposta, respondeu fora do horário, perguntou o nome, entendeu a necessidade, falou de preço, ofereceu avaliação, ofereceu horário, convidou a marcar, follow-up em 24 h, follow-up em 72 h, tom, erros.
4. Nota de 0 a 100 e valor em risco por mês = contatos estimados × % perdido × conversão × ticket.
5. Página do diagnóstico na marca Keshion: nota, prints sem expor ninguém, 3 acertos, 3 perdas, valor em risco, vídeo curto da demo, convite para 30 minutos.
6. Sérgio envia na janela do almoço. Tempo: cerca de 1 hora por clínica no começo.

## Custo total na proposta

Bloco "Seu investimento no primeiro ano": implantação, 12 mensalidades, estimativa de mensagens da Meta pelo volume da clínica, excedentes (nenhum até o limite do pacote), total do ano e custo real por mês. Ao lado, a comparação: custo de uma secretária e quantos tratamentos de lente pagam o ano.

## Cobrança por resultado (como medir)

- Resultado elegível: (a) paciente que voltou por mensagem de retorno ou reativação e compareceu; (b) orçamento parado há 7 dias ou mais que foi aceito depois de lembrete da assistente.
- Confirmação: a clínica marca no app (compareceu ou orçamento aceito com valor).
- Cobrança: valor fixo por resultado (ex.: R$ 30 a 50) ou percentual com teto. Lista mensal que a clínica pode contestar antes da fatura.
- Referência: a We Ramp cobra R$ 30 por paciente atendido no recall.

## Recuperação de receita: o que entra já (dezembro)

| Ordem | Fluxo | Prazo | Depende de |
|---|---|---|---|
| 1 | Confirmação e lembrete de consulta | 29/11 | Agenda (já existe) |
| 2 | Retomada de conversa sem resposta (até 3 tentativas) | 03/12 | Fila e ficha da Clara (já existem) |
| 3 | Lembretes de orçamento (dias 1, 3, 7, 15 e 30) | 05/12 | Registrar orçamento entregue |
| 4 | Retomada de faltas | 12/12 | Marcar falta (app ou resposta à confirmação) |
| 5 | Lista de espera para encaixe | 18/12 | Cancelamento na agenda |
| Depois | Retornos e reativação, aniversários, avaliação no Google | jan e fev/27 | Base de pacientes antigos |

## App v1 (dezembro e janeiro)

- **Dezembro:** Pendências, Conversas (assumir e devolver para a IA), Agenda do dia (Google Agenda) com botões compareceu e faltou, Pacientes (ficha simples).
- **Janeiro:** Orçamentos com PDF e envio pelo WhatsApp, Resultados (reais recuperados), Retornos.
- **Fora do v1:** prontuário, nota fiscal, financeiro completo, integrações.
- **Orçamento no app:** paciente, procedimentos da tabela de preços da clínica, sessões, desconto, formas de pagamento (Pix com desconto, cartão em X vezes), validade, observações. Gera PDF com a marca da clínica, a assistente envia pelo WhatsApp com botão "Quero fazer" e começa a jornada do orçamento. Situações: enviado, visto, aceito, recusado (com motivo).

## Voz e áudio (2º semestre de 2027)

- **Etapa 1, áudio no WhatsApp:** texto da Clara convertido em voz (ElevenLabs, OpenAI ou similar) e enviado como mensagem de voz, só quando o paciente mandou áudio ou a clínica quiser. Custo estimado: R$ 0,07 a 0,15 por áudio de 300 caracteres.
- **Etapa 2, ligação:** plataforma de voz (Retell, Vapi ou ElevenLabs Agents) mais número brasileiro por SIP, ligada ao n8n para agenda. Desvio do fixo da clínica quando ocupado ou fora do horário. Alternativa: chamadas do WhatsApp pela API oficial. Custo estimado: US$ 0,07 a 0,30 por minuto mais telefonia (cerca de R$ 0,40 a 1,70 por minuto).
- **Riscos:** demora na resposta e sotaque, paciente que desliga ao perceber robô, aviso de gravação (LGPD), erro de agenda, custo por minuto variável, regras de numeração e dependência do fornecedor. Voz clonada da doutora só com autorização escrita.

## Decisões de 16/11/2026 (tarde)

- **App:** um único app web (Next.js) que abre no navegador do computador e instala no celular como aplicativo (PWA). Hospedagem recomendada: Vercel Pro (US$ 20 por mês; o plano Hobby proíbe uso comercial) ou Netlify (o plano grátis permite uso comercial). Os dados dos pacientes ficam no banco da Keshion, não na hospedagem.
- **Orçamento da Dra. Vivian:** formato e tabela de preços definidos na reunião de levantamento.
- **Voz do áudio:** voz genérica, natural e sem sotaque. Escolha por teste cego entre ElevenLabs, OpenAI, Azure, Google, Cartesia e um modelo aberto. Custo por áudio de 300 caracteres fica entre R$ 0,03 e 0,15 em todos (estimativa de terceiros, confirmar no site oficial).
- **Cliente oculto:** chip próprio, comprado pelo Sérgio.

## Como provar que o valor recuperado veio da assistente (16/11/2026)

Lógica de "link de afiliado": a venda conta para a assistente quando o paciente volta pela mensagem dela, dentro de uma janela de tempo.

| Etiqueta | Regra | Entra no total? |
|---|---|---|
| Recuperado pela assistente | Orçamento ou conversa parada há 7 dias ou mais, sem contato da equipe nesse período; o paciente respondeu a uma mensagem da assistente; aceite ou comparecimento em até 30 dias depois dessa resposta | Sim (total principal) |
| Influenciado | A assistente fez contato, mas a equipe também conversou com o paciente antes do aceite, ou o aceite veio por outro canal | Linha separada, fora do total |
| Orgânico | Aceite sem nenhum toque da assistente | Não |

Provas de cada linha: data e hora do orçamento, da mensagem da assistente e da resposta do paciente, link da conversa, valor confirmado pela clínica. A clínica pode contestar antes do fechamento do mês. Comparação de apoio: taxa de fechamento de orçamentos antes (levantamento dos últimos 20 orçamentos na implantação) e depois.

## Hospedagem do app (opções levantadas em 16/11/2026, decisão pendente)

- **Recomendação:** tela do app na Vercel Pro (US$ 20) ou Netlify (grátis no começo) e banco, login e arquivos no Supabase Pro (US$ 25, região São Paulo). Total perto de US$ 45 por mês para todas as clínicas.
- **Desenvolvimento (dezembro):** Netlify grátis e Supabase grátis. Passar para o Supabase Pro antes de entrar dado real da Dra. Vivian (o grátis pausa sem uso e não tem backup diário).
- **Alternativas:** tudo no servidor Contabo com Coolify (sem custo novo, mas backup e segurança ficam com a Keshion); Firebase (custo variável, banco não SQL); Render ou Railway (app e banco juntos, US$ 5 a 7 mais uso); Cloudflare (US$ 5, mais trabalho para montar login).
- **A decidir junto:** se o banco `clara` sai do Contabo e vai para o Supabase (um banco só para n8n e app) ou se o app lê do Contabo.
