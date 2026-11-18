-- Banco do app da Keshion (Supabase, região São Paulo). APLICADO em 18/11/2026 no projeto keshion-app e testado (teste-isolamento.sql).
-- Regra de ouro: cada clínica só vê as linhas dela (RLS). A Clara (n8n, no Contabo) NÃO usa chave de administrador:
-- ela chama só a função clara_evento, com um token por clínica (seção 4).
-- Quem é dono de quê: a Clara é dona da conversa em andamento (fica no Contabo); o app é dono do cadastro,
-- tratamentos, orçamentos, agenda do dia e Painel. A chave de ligação é o telefone, dentro de cada clínica.

-- 1. CLÍNICAS E QUEM PODE ENTRAR ------------------------------------------------------------------------

create table if not exists clinicas (
  id               uuid primary key default gen_random_uuid(),
  slug             text unique not null,            -- igual à pasta clientes/<slug> (ex.: clinica-demo)
  nome             text not null,
  telefone         text,
  endereco         text,
  mensalidade      numeric(10,2),
  clara_token_hash text,                            -- sha256 do token da Clara desta clínica (o token em si fica só no n8n)
  criado           timestamptz not null default now()
);

create table if not exists membros (
  user_id    uuid not null references auth.users on delete cascade,
  clinica_id uuid not null references clinicas on delete cascade,
  papel      text not null check (papel in ('dono', 'recepcao', 'doutora')),
  primary key (user_id, clinica_id)
);

create or replace function minhas_clinicas() returns setof uuid
language sql stable security definer set search_path = public as $$
  select clinica_id from membros where user_id = auth.uid()
$$;

-- 2. TABELAS DO APP -------------------------------------------------------------------------------------

create table if not exists pacientes (
  id               uuid primary key default gen_random_uuid(),
  clinica_id       uuid not null references clinicas on delete cascade,
  telefone         text not null,
  nome             text,                            -- nome do perfil do WhatsApp
  nome_completo    text,
  email            text,
  nascimento       date,
  endereco         text,
  origem           text,                            -- Instagram, Anúncio, Google, Indicação, Recepção, Paciente antiga
  indicado_por     text,
  situacao         text not null default 'Novo contato' check (situacao in
                   ('Novo contato','Em conversa','Avaliação marcada','Avaliou, aguardando orçamento',
                    'Orçamento em aberto','Em tratamento','Tratamento concluído','Não fechou')),
  ja_paciente      boolean not null default false,
  motivo_nao_fechou text,
  notas            text,                            -- anotação da equipe. Anotação clínica fica no prontuário da clínica (LGPD)
  primeiro_contato date not null default current_date,
  criado           timestamptz not null default now(),
  unique (clinica_id, telefone)
);

create table if not exists tratamentos (
  id             uuid primary key default gen_random_uuid(),
  clinica_id     uuid not null references clinicas on delete cascade,
  paciente_id    uuid not null references pacientes on delete cascade,
  nome           text not null,
  valor          numeric(10,2),
  pagamento      text,
  sessoes_feitas int not null default 0,
  sessoes_total  int not null default 0,
  criado         timestamptz not null default now()
);

create table if not exists textos_orcamento (       -- textos padrão que entram no PDF, revisados pela doutora
  clinica_id uuid not null references clinicas on delete cascade,
  modelo     text not null,                         -- lentes, facetas, alinhador, clareamento, limpeza
  nome       text not null,
  como       text,
  etapas     text[] not null default '{}',
  prazo      text,
  inclui     text[] not null default '{}',
  primary key (clinica_id, modelo)
);

create table if not exists orcamentos (
  id            uuid primary key default gen_random_uuid(),
  clinica_id    uuid not null references clinicas on delete cascade,
  numero        int,                                -- preenchido pelo gatilho abaixo, por clínica
  paciente_id   uuid not null references pacientes on delete cascade,
  modelo        text not null,
  nome_livre    text,
  quantidade    int not null default 1,
  valor         numeric(10,2) not null check (valor > 0),
  pagamento     text,
  validade_dias int not null default 30,
  emitido       date not null default current_date,
  status        text not null default 'aberto' check (status in ('aberto','aceito','recusado')),
  motivo_recusa text,
  criado        timestamptz not null default now(),
  unique (clinica_id, numero)
);

create or replace function numerar_orcamento() returns trigger language plpgsql as $$
begin
  if new.numero is null then
    select coalesce(max(numero), 100) + 1 into new.numero from orcamentos where clinica_id = new.clinica_id;
  end if;
  return new;
end $$;
drop trigger if exists orcamento_numero on orcamentos;
create trigger orcamento_numero before insert on orcamentos for each row execute function numerar_orcamento();

create table if not exists consultas (
  id              uuid primary key default gen_random_uuid(),
  clinica_id      uuid not null references clinicas on delete cascade,
  paciente_id     uuid not null references pacientes on delete cascade,
  inicio          timestamptz not null,
  tipo            text not null default 'Avaliação',
  confirmacao     text not null default 'Aguardando confirmação'
                  check (confirmacao in ('Confirmou','Sem resposta','Remarcou pela IA','Aguardando confirmação')),
  presenca        text check (presenca in ('Compareceu','Faltou')),
  remarcar        boolean not null default false,   -- a equipe pediu para a IA oferecer novo horário
  google_event_id text,
  criado          timestamptz not null default now(),
  unique (clinica_id, google_event_id)
);

create table if not exists conversas (               -- resumo para a aba Conversas; o texto completo fica no Contabo
  clinica_id      uuid not null references clinicas on delete cascade,
  paciente_id     uuid not null references pacientes on delete cascade,
  ultima_mensagem text,
  ultimo_horario  timestamptz not null default now(),
  estado          text not null default 'ia_respondeu'
                  check (estado in ('ia_respondeu','agendou','aguardando_equipe','equipe_assumiu')),
  fora_do_horario boolean not null default false,
  primary key (clinica_id, paciente_id)
);

create table if not exists encaminhamentos (         -- o que a Clara passou para a equipe ("Precisa de você")
  id          uuid primary key default gen_random_uuid(),
  clinica_id  uuid not null references clinicas on delete cascade,
  paciente_id uuid not null references pacientes on delete cascade,
  tipo        text not null check (tipo in ('urgencia','pediu_doutora','ia_nao_sabe','desconto','reclamacao','outro')),
  mensagem    text,
  criado      timestamptz not null default now(),
  resolvido   timestamptz,
  resposta    text
);

create table if not exists recuperacoes (            -- base do "Recuperado pela assistente" no Painel
  id           uuid primary key default gen_random_uuid(),
  clinica_id   uuid not null references clinicas on delete cascade,
  paciente_id  uuid not null references pacientes on delete cascade,
  orcamento_id uuid references orcamentos on delete set null,
  tipo         text not null default 'recuperado' check (tipo in ('recuperado','influenciado')),
  valor        numeric(10,2) not null,
  como         text,
  estado       text not null default 'a_confirmar' check (estado in ('a_confirmar','confirmado','contestado')),
  criado       timestamptz not null default now()
);

-- 3. RLS: CADA CLÍNICA SÓ VÊ O QUE É DELA ---------------------------------------------------------------

do $$
declare t text;
begin
  foreach t in array array['pacientes','tratamentos','textos_orcamento','orcamentos','consultas',
                           'conversas','encaminhamentos','recuperacoes'] loop
    execute format('alter table %I enable row level security', t);
    execute format('drop policy if exists clinica_ve_o_proprio on %I', t);
    execute format('create policy clinica_ve_o_proprio on %I for all to authenticated
                    using (clinica_id in (select minhas_clinicas()))
                    with check (clinica_id in (select minhas_clinicas()))', t);
  end loop;
end $$;

alter table clinicas enable row level security;
drop policy if exists ver_minha_clinica on clinicas;
create policy ver_minha_clinica on clinicas for select to authenticated using (id in (select minhas_clinicas()));

alter table membros enable row level security;
drop policy if exists ver_meu_acesso on membros;
create policy ver_meu_acesso on membros for select to authenticated using (user_id = auth.uid());

-- 3b. LIBERAÇÃO DA API --------------------------------------------------------------------------------------
-- O projeto keshion-app (sa-east-1) foi criado com "Grant API access to new tables automatically" DESLIGADO e
-- "Enable RLS on new tables automatically" LIGADO. Por isso cada tabela é liberada aqui, de propósito, só para quem
-- está logado. Visitante sem login (anon) não lê nada, só chama a função da Clara (seção 4).
grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on pacientes, tratamentos, textos_orcamento, orcamentos, consultas,
      conversas, encaminhamentos, recuperacoes to authenticated;
grant select on clinicas, membros to authenticated;
revoke all on all tables in schema public from anon;
revoke all on function minhas_clinicas() from public, anon;
grant execute on function minhas_clinicas() to authenticated;

-- 4. ENTRADA DA CLARA: UMA FUNÇÃO, UM TOKEN POR CLÍNICA --------------------------------------------------
-- O n8n guarda só a chave pública do projeto e o token da clínica. Se o token vazar, o estrago fica numa clínica
-- e só nestas operações. Gerar o token: 32 bytes aleatórios; no banco entra só o hash:
--   update clinicas set clara_token_hash = encode(extensions.digest('<token>', 'sha256'), 'hex') where slug = '<slug>';

create or replace function clara_evento(p_token text, p_tipo text, p_dados jsonb) returns void
language plpgsql security definer set search_path = public, extensions as $$
declare
  v_clinica uuid;
  v_pac     uuid;
  v_tel     text := regexp_replace(coalesce(p_dados->>'telefone', ''), '\D', '', 'g');
begin
  select id into v_clinica from clinicas
   where clara_token_hash = encode(digest(convert_to(p_token, 'utf8'), 'sha256'), 'hex');
  if v_clinica is null then raise exception 'token inválido'; end if;
  if length(v_tel) < 10 then raise exception 'telefone obrigatório'; end if;

  insert into pacientes (clinica_id, telefone, nome)
  values (v_clinica, v_tel, nullif(p_dados->>'nome', ''))
  on conflict (clinica_id, telefone) do update set nome = coalesce(excluded.nome, pacientes.nome)
  returning id into v_pac;

  if p_tipo = 'contato' then
    update pacientes set
      nome_completo = coalesce(nullif(p_dados->>'nome_completo', ''), nome_completo),
      origem        = coalesce(nullif(p_dados->>'origem', ''), origem)
    where id = v_pac;

  elsif p_tipo = 'mensagem' then
    insert into conversas (clinica_id, paciente_id, ultima_mensagem, estado, fora_do_horario)
    values (v_clinica, v_pac, left(p_dados->>'texto', 300), case when p_dados->>'estado' in ('ia_respondeu','agendou','aguardando_equipe','equipe_assumiu') then p_dados->>'estado' else 'ia_respondeu' end,
            coalesce((p_dados->>'fora_do_horario')::boolean, false))
    on conflict (clinica_id, paciente_id) do update set
      ultima_mensagem = excluded.ultima_mensagem, ultimo_horario = now(),
      estado = excluded.estado, fora_do_horario = excluded.fora_do_horario;

  elsif p_tipo = 'encaminhamento' then
    insert into encaminhamentos (clinica_id, paciente_id, tipo, mensagem)
    values (v_clinica, v_pac,
            case when p_dados->>'motivo' in ('urgencia','pediu_doutora','ia_nao_sabe','desconto','reclamacao') then p_dados->>'motivo' else 'outro' end,
            left(p_dados->>'texto', 1000));
    insert into conversas (clinica_id, paciente_id, ultima_mensagem, estado)
    values (v_clinica, v_pac, left(p_dados->>'texto', 300), 'aguardando_equipe')
    on conflict (clinica_id, paciente_id) do update set
      ultima_mensagem = excluded.ultima_mensagem, ultimo_horario = now(), estado = 'aguardando_equipe';

  elsif p_tipo = 'consulta' then
    insert into consultas (clinica_id, paciente_id, inicio, tipo, confirmacao, google_event_id)
    values (v_clinica, v_pac, (p_dados->>'inicio')::timestamptz, coalesce(p_dados->>'tipo', 'Avaliação'),
            case when p_dados->>'confirmacao' in ('Confirmou','Sem resposta','Remarcou pela IA') then p_dados->>'confirmacao' else 'Aguardando confirmação' end, p_dados->>'google_event_id')
    on conflict (clinica_id, google_event_id) do update set
      inicio = excluded.inicio, tipo = excluded.tipo, confirmacao = excluded.confirmacao;
    update pacientes set situacao = 'Avaliação marcada'
     where id = v_pac and situacao in ('Novo contato', 'Em conversa');

  else
    raise exception 'tipo de evento desconhecido: %', p_tipo;
  end if;
end $$;

revoke all on function clara_evento(text, text, jsonb) from public;
grant execute on function clara_evento(text, text, jsonb) to anon, authenticated;

-- 5. DO APP PARA A CLARA (assumir ou devolver conversa, responder, ensinar a IA, enviar orçamento) NÃO passa pelo banco:
-- o app chama um endereço do n8n de cada clínica. Desenho pendente em app-crm-painel/ (próximo passo).
