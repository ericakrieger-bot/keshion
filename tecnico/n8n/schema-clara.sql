-- Tabelas do banco de cada clínica (um banco por clínica; o da demo se chama "clara").
-- Não rodar sozinho: preparar_banco.py <slug> junta este arquivo com a config da clínica.
-- Substitui o data store 240983 do Make.

CREATE TABLE IF NOT EXISTS pacientes (
  telefone         text PRIMARY KEY,
  nome             text,                 -- nome do perfil do WhatsApp
  nome_paciente    text,                 -- nome que a pessoa disse
  conversa         text NOT NULL DEFAULT '',
  pendente         text NOT NULL DEFAULT '',  -- mensagens ainda sem resposta (fila de 7 s)
  ultimo_id        text,
  atualizado       timestamptz NOT NULL DEFAULT now(),
  tratamento       text,
  avaliacao_texto  text,
  avaliacao_evento text,
  avaliacao_inicio text,
  nome_completo    text,                 -- nome e sobrenome, pedidos ao marcar
  telefone_contato text,                 -- telefone de contato informado ao marcar
  ultimo_aviso_humano timestamptz,      -- último "chamar uma pessoa" (evita aviso repetido)
  pausado_ate      timestamptz           -- doutora respondeu pelo celular: Clara em silêncio
);

CREATE TABLE IF NOT EXISTS config (
  chave text PRIMARY KEY,
  valor text NOT NULL
);

-- Ids de mensagens do Whapi já recebidas: evita responder de novo a um reenvio (revisão Codex, item 2).
CREATE TABLE IF NOT EXISTS mensagens_recebidas (
  id       text PRIMARY KEY,
  telefone text,
  recebido timestamptz NOT NULL DEFAULT now()
);

-- Colunas acrescentadas em 17/11/2026 (correções da revisão do Codex). Seguro rodar de novo.
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS ultimo_motivo_humano text;   -- motivo do último "chamar uma pessoa" (evita aviso repetido)
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS envio_ate timestamptz;       -- até quando as mensagens do turno anterior ainda estão saindo

-- Colunas acrescentadas em 18/11/2026 (Pacote A da revisão do Codex). Seguro rodar de novo.
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS recusas_agenda int NOT NULL DEFAULT 0;  -- recusas seguidas de horário (na 2ª, avisa a equipe)
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS ultimo_complemento timestamptz;        -- último "complemento do aviso" (no máximo 1 a cada 15 min)

-- Trava curta do horário (5 min desde 18/11): duas conversas não reservam a mesma vaga ao mesmo tempo.
CREATE TABLE IF NOT EXISTS reservas_horario (
  inicio   timestamptz PRIMARY KEY,
  telefone text NOT NULL,
  criado   timestamptz NOT NULL DEFAULT now()
);

-- Só usada quando config.modo_teste = '1': guarda o que seria enviado, sem mandar pelo WhatsApp.
CREATE TABLE IF NOT EXISTS saidas_teste (
  id        bigserial PRIMARY KEY,
  criado    timestamptz NOT NULL DEFAULT now(),
  telefone  text,
  texto     text
);

-- Modo copiloto (22/11/2026): respostas da assistente esperando o dentista aprovar (ok, não ou texto corrigido).
-- status: pendente, aprovada, corrigida, descartada, substituida. Seguro rodar de novo.
CREATE TABLE IF NOT EXISTS copiloto_pendentes (
  codigo    bigserial PRIMARY KEY,           -- aparece para o dentista como C<codigo>
  telefone  text NOT NULL,
  nome      text,
  pedido    text,                            -- o que a paciente escreveu
  texto     text NOT NULL,                   -- sugestão da assistente (como entrou na conversa)
  envio     text NOT NULL,                   -- mensagens a enviar (JSON com m1, m2, m3)
  status    text NOT NULL DEFAULT 'pendente',
  resposta  text,                            -- texto que saiu (aprovado ou corrigido)
  criado    timestamptz NOT NULL DEFAULT now(),
  resolvido timestamptz
);
CREATE INDEX IF NOT EXISTS copiloto_pendentes_pendentes ON copiloto_pendentes (status, telefone);

-- Os valores da tabela config (aprovador, prefixo_teste, instruções, base...) vêm do clinica.json
-- de cada clínica: rodar preparar_banco.py <slug>, que inclui este arquivo e preenche a config.
