# Avaliação do relatório do Codex e plano até o piloto

Escrito em 12/11/2026 pelo Claude, depois de ler `revisao-codex-2026-11-12.md` e conferir no servidor os pontos verificáveis.

## Conclusão

O relatório é sólido e honesto. Concordo com a conclusão principal: **a Clara funciona para a demo, mas ainda não está pronta para pacientes reais da Dra. Vivian.** Discordo só da dose em alguns pontos: algumas correções propostas são pesadas demais para uma clínica com poucos contatos por dia e podem ficar para depois do piloto. Abaixo, o que conferi, onde concordo, onde discordo e o que fazer, em ordem.

## O que conferi no servidor

| Afirmação do Codex | Conferido | Resultado |
|---|---|---|
| SSH aceita senha para o root | `sshd -T` | **Verdade.** `passwordauthentication yes` e `permitrootlogin yes` (vem do arquivo `50-cloud-init.conf` da Contabo). O fail2ban registrou 219 tentativas e 18 bloqueios em 12/11. Eu tinha documentado "só por chave" sem conferir: erro meu. |
| `WEBHOOK_URL` obsoleta | log do n8n | **Verdade.** O n8n pede `N8N_WEBHOOK_URL`. Ainda funciona. |
| Áudio real não testado | execução 146 | Era o bug que a Erica viu: a OpenAI recusou a extensão `.oga`. **Corrigido em 12/11** (nó "Ajustar o nome do áudio"); testado com o mesmo arquivo real. |

## Item por item

| # | Problema do Codex | Concordo? | Gravidade para mim | O que fazer |
|---|---|---|---|---|
| 1 | Webhook sem autenticação; URL da mídia vira download pelo servidor | Sim | Alta (ele diz crítica; o endereço só está no repositório privado, mas deve ser tratado como conhecido) | Já: aceitar só o canal `GRNLTR-4K8ZF` e só links de mídia do domínio do Whapi (Wasabi), trocar o caminho do webhook. Depois: cabeçalho secreto, se o Whapi permitir |
| 2 | Lote com 2 mensagens perde a segunda; reenvio atrasado responde de novo; ordem entre execuções | Sim | Média | Já: processar todas as mensagens do lote e guardar os ids já recebidos numa tabela (não só o último). A ordem entre duas respostas quase simultâneas fica para depois |
| 3 | Agenda: duas pessoas na mesma vaga, horário fora das regras, remarcou antes da confirmação | Parcial | Média (com uma clínica, a corrida é rara) | Já: conferir o id do evento criado, e mandar a regra "remarcar só depois do sim" nas instruções (precisa do OK da Erica, porque muda o texto da Clara). Reserva no banco e vagas calculadas em código: depois do piloto |
| 4 | Falha da agenda e da IA dependem da IA; aviso de falha do WhatsApp vai pelo próprio WhatsApp | Sim | Alta | Já: erro do Google (inclusive o campo `errors`) e ação desconhecida da IA viram "chamar uma pessoa", sem depender do texto. Antes do piloto: um canal de alerta fora do WhatsApp (e-mail ou Telegram) |
| 5 | Dados espalhados; demo e piloto não isolados | Sim, forte | Alta | Antes do piloto: banco, credenciais e fluxos próprios por clínica (o gerador recebe os dados da clínica como parâmetro). Já: limitar a retenção das execuções do n8n (ex.: 14 dias) |
| 6 | Autorização do Google expira; trocar domínio é mais que DNS | Sim (já sabido) | Alta | Antes do piloto: domínio, página de privacidade, publicar o app, testar renovação. Trocar o domínio antes da entrada da Vivian, não no mesmo dia |
| 7 | Backup só no VPS; root com senha | Sim | **Urgente** (senha) e alta (backup) | Hoje: desligar senha no SSH (precisa do OK da Erica). Antes do piloto: backup cifrado fora do VPS e um teste de restauração; usuário de manutenção com sudo |
| 8 | Prefixo de teste ainda mexe na agenda real | Sim | Média | Depois: marcar "teste" na entrada e usar uma agenda de teste separada |
| 9 | Corte do histórico pode enganar a despedida | Sim | Baixa | Já (barato): a despedida confere o id da última mensagem em vez do tamanho |
| 10 | Postgres 16 e imagem `stable` flutuante | Sim | Média | Já: fixar as versões das imagens. Postgres 17: ensaiar depois, numa cópia |

## Onde o Codex discorda de mim, e o que acho

- **Aviso à equipe depois das mensagens do paciente:** ele tem razão. Em urgência, o aviso não pode esperar o "digitando". Correção barata: avisos primeiro.
- **"56 de 56" não prova que está pronto:** justo. Foi um teste de tom e de regressão, não de segurança. Também tem razão em que o script limpa a tabela antes de conferir o prefixo: vou inverter a ordem.
- **Aprovação humana (modo copiloto) não existe:** verdade. Se a Dra. Vivian quiser aprovar antes de enviar na primeira semana, isso precisa ser construído e testado. Decidir com ela.
- **A base da demo promete coisas que os fluxos não fazem** (lembretes, PDF de orçamento): verdade. A base da Vivian precisa prometer só o que existe.

## Plano

**Hoje (com OK da Erica):** ✅ desligar o login por senha no SSH (feito em 12/11, tarde; acesso por chave conferido).

**Próxima sessão (correções rápidas, cerca de meio dia):** canal e host de mídia validados, novo caminho de webhook, todas as mensagens do lote, tabela de ids recebidos, avisos antes do paciente, erros do Google e da IA virando "chamar uma pessoa", conferência do id do evento, despedida por id, `N8N_WEBHOOK_URL`, versões fixas, retenção das execuções, ordem no script de teste. Depois, repetir os testes do Codex que falharam.

**Antes de 01/12 (estrutura):** isolamento por clínica, backup externo com restauração testada, app do Google publicado com domínio, canal de alerta fora do WhatsApp, autenticação do webhook (se o Whapi permitir), decisão sobre o modo copiloto, base e instruções da Vivian.

**Depois do piloto:** fila de envio persistente, reservas no banco, resumo do histórico, Postgres 17.
