-- Banco da Clara (n8n). Rodar dentro do banco "clara", como dono.
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

-- Só usada quando config.modo_teste = '1': guarda o que seria enviado, sem mandar pelo WhatsApp.
CREATE TABLE IF NOT EXISTS saidas_teste (
  id        bigserial PRIMARY KEY,
  criado    timestamptz NOT NULL DEFAULT now(),
  telefone  text,
  texto     text
);

INSERT INTO config (chave, valor) VALUES
  ('modelo', 'claude-haiku-5-5'),
  ('aprovador', '972584285541'),
  ('modo_teste', '0'),
  ('local_avaliacao', 'Rua Desembargador Motta, 2000, sala 1404, Batel, Curitiba/PR'),
  ('numeros_keshion', '972584285541,972552994413'),
  -- Números que começam com este prefixo nunca recebem WhatsApp de verdade: o lote vai para saidas_teste.
  ('prefixo_teste', '554199900')
ON CONFLICT (chave) DO NOTHING;
