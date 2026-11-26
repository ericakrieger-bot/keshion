-- Tabelas do banco de cada clínica (um banco por clínica; o da demo se chama "clara").
-- Não rodar sozinho: preparar_banco.py <slug> junta este arquivo com a config da clínica.
-- Substitui o data store 240983 do Make.

CREATE TABLE IF NOT EXISTS pacientes (
  telefone         text PRIMARY KEY,
  nome             text,                 -- nome do perfil do WhatsApp
  nome_paciente    text,                 -- nome que a pessoa disse
  conversa         text NOT NULL DEFAULT '',
  pendente         text NOT NULL DEFAULT '',  -- mensagens ainda sem resposta (fila de 20 s)
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

-- Colunas acrescentadas em 25/11/2026 (Pacote E, cancelar sem loop). Seguro rodar de novo.
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS cancelar_evento text;                    -- avaliação que espera o "sim" para cancelar
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS cancelar_pedido_em timestamptz;           -- quando a confirmação foi pedida (vale 24 h)
ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS cancelar_tentativas int NOT NULL DEFAULT 0; -- respostas sem decisão (na 3ª, chama a equipe)

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

-- Os valores da tabela config (aprovador, prefixo_teste, instruções, base...) vêm do clinica.json
-- de cada clínica: rodar preparar_banco.py <slug>, que inclui este arquivo e preenche a config.
