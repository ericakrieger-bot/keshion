# Keshion: segunda opinião para o piloto de 01/12/2026

**Minha recomendação: manter a arquitetura e corrigir os bloqueios abaixo antes de ligar a Dra. Vivian.** Houve melhorias reais, mas alguns itens descritos como corrigidos ainda estão pela metade. Nenhuma correção de código ou configuração foi aplicada nesta revisão.

O que ficou certo: a demo publicada coincide com o gerador atual; base e instruções também coincidem. O isolamento entre as duas clínicas passou com o mesmo telefone e IDs. A resposta nova em inglês evitou prometer anestesia universal ou ausência de dor. As quatro conversas de agenda chegaram à marcação e ao cancelamento. O backup externo existe: último status OK de 18/11 às 07h10 de Curitiba, arquivo de banco de 68.234.517 bytes no Drive, acompanhado da configuração criptografada. As permissões principais estão restritas.

**O que corrigir primeiro, nesta ordem:**

1. **Avisos que somem.** Depois de um pedido de recibo, a mensagem fictícia “Agora comecei a sangrar muito” recebeu promessa de encaminhamento, mas nenhum aviso novo para a equipe. A regra trata mensagem curta sem `?` como simples confirmação. Informação nova e agravamento precisam sempre chegar à equipe.
2. **Escolha e aceite antes de mexer na agenda.** O código aceita a data de uma opção junto com a hora de outra, ignora certos minutos, meses e anos e não verifica sozinho o aceite do cancelamento. Reproduzi esses desvios localmente, sem criar eventos errados. É preciso vincular a operação à opção completa escolhida e à confirmação mais recente. A trava de vaga ajuda, mas ainda não cobre todas as duplicações.
3. **Sair do ciclo de recusa.** “Amanhã às 11h” foi recusado três vezes sem aviso; ao trocar por “19/11/2026 às 11h”, a mesma vaga foi marcada. Os 61 testes originais passaram, mas não cobriam esse problema. Avisar na segunda recusa e traduzir as frases fixas são medidas urgentes. No cancelamento em inglês, houve confirmação extra forçada em português.
4. **Monitoramento fora do WhatsApp e do servidor.** O alerta de envio ainda depende do canal da Keshion. O backup não avisa ninguém sozinho e algumas falhas deixam o OK anterior. Monitorar falha, atraso e ausência de execução, com responsável e substituto, antes do piloto.
5. **Consolidar recuperação e instalação.** Migrar o client_id do backup antes que o compartilhado seja desativado, verificando acesso às cópias antigas. Corrigir o roteiro de restauração para parar em erro e permitir execução por outra pessoa. Sete arquivos locais não garantem sete dias. Aplicar os usuários limitados do banco com autorização, completar dados e aceite da Vivian e retirar o reinício do n8n do roteiro de clínica nova.

O que ainda não foi comprovado: nova restauração independente, primeira rodada automática do backup novo em 19/11 às 03h de Curitiba, entrega de alerta real de falha, concorrência simultânea e todos os casos antigos de mídia e atendimento. Não há dia oficial confirmado para a quebra do client_id compartilhado; não recomendo esperar a falha para migrar.

**Limpeza confirmada:** finais 951 a 957 com zero registros nas quatro tabelas verificadas dos dois bancos; eventos desta revisão cancelados pela conversa e sem sobra na consulta direta ao Google Agenda. O evento antigo informado de Henrique, final 810, não foi alterado. Não foram apagados backups nem registros de execução do n8n.

Relatórios completos: `revisao-codex-correcoes-17-11-2026-11-18.md`, `revisao-codex-data-hora-2026-11-18.md` e `revisao-codex-backup-2026-11-18.md`. Evidências e ferramentas de reprodução estão nesta mesma pasta, com dados sintéticos e sem segredos.
