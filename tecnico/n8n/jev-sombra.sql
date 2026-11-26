-- Jev em modo sombra (25/11/2026, PLANO-JEV-SOMBRA.md): uma linha por resposta da assistente com o que a regra de hoje fez
-- e o que o Jev diria. Aplicar no banco de cada clínica (clara = demo, clinica_teste = teste), com OK da Erica.
-- Pode rodar de novo sem problema. O próprio fluxo apaga linhas com mais de 60 dias.
CREATE TABLE IF NOT EXISTS jev_sombra (
  id                 bigserial PRIMARY KEY,
  criado_em          timestamptz NOT NULL DEFAULT now(),
  telefone           text,
  msg_id             text,
  mensagem           text,          -- mensagem do paciente (para entender as diferenças)
  perguntou_cancelar boolean,       -- o código sabia que a última fala da assistente era a pergunta de cancelar
  regra_urgencia     boolean,       -- regra de palavras de hoje
  regra_rota         text,          -- caminho que o fluxo seguiu: responder, humano, agenda, cancelar...
  regra_acao         text,
  regra_cancelou     boolean,
  regra_motivo       text,
  ok                 boolean,       -- false = o Jev falhou, demorou mais de 3 s ou respondeu algo estranho
  erro               text,
  ms                 int,
  modelo             text,
  tokens             int,
  custo_usd          numeric(14, 10),
  jev_urgencia       real,
  jev_dor            text,
  jev_dor_p          real,
  jev_fora           real,
  jev_conf           text,
  jev_conf_sim       real,
  jev_espera         real,
  jev_pede_cancelar  real,
  decide_urgencia    boolean,       -- o que o Jev decidiria com os limiares da bancada
  decide_dor         text,          -- relato, pergunta ou outro
  decide_fora        text,          -- nao_fazemos, equipe ou nao
  decide_cancelar    text,          -- cancela ou pergunta_de_novo (só quando perguntou_cancelar)
  resposta           jsonb
);
CREATE INDEX IF NOT EXISTS jev_sombra_criado_em ON jev_sombra (criado_em);
