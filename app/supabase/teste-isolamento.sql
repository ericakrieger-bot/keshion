-- Teste do banco do app (rodar no SQL Editor do Supabase). Cria duas clínicas de mentira, exercita a função da Clara
-- e as regras por clínica, e DESFAZ TUDO no final: o bloco termina com um erro de propósito ("RESULTADO: {...}"),
-- que mostra o resumo e cancela as gravações. Resultado esperado (18/11/2026, passou):
--   usuário A vê só os dados da clínica A (da_B=0); inserir na B é bloqueado e update na B afeta 0 linhas;
--   visitante sem login é bloqueado em pacientes e clínicas; token errado e tipo desconhecido são recusados;
--   motivo desconhecido vira "outro"; o mesmo evento de consulta atualiza em vez de duplicar;
--   numeração de orçamento por clínica (A: 101, 102; B: 101); mesmo telefone vira 2 pacientes (um por clínica).
do $$
declare
  r text; v_a uuid; v_b uuid; v_err text; v_ins text; v_anon text; v_ve text;
  ua uuid := '00000000-0000-0000-0000-0000000000a1';
  ub uuid := '00000000-0000-0000-0000-0000000000b1';
begin
  insert into clinicas (slug, nome, clara_token_hash) values ('teste-a','Clínica A', encode(extensions.digest('token-a','sha256'),'hex')) returning id into v_a;
  insert into clinicas (slug, nome, clara_token_hash) values ('teste-b','Clínica B', encode(extensions.digest('token-b','sha256'),'hex')) returning id into v_b;
  perform clara_evento('token-a','contato','{"telefone":"5541999990001","nome":"Maria Teste","nome_completo":"Maria da Silva Teste","origem":"Instagram"}'::jsonb);
  perform clara_evento('token-a','encaminhamento','{"telefone":"5541999990001","motivo":"desconto","texto":"Consigo desconto?"}'::jsonb);
  perform clara_evento('token-a','encaminhamento','{"telefone":"5541999990001","motivo":"assunto-estranho","texto":"outra coisa"}'::jsonb);
  perform clara_evento('token-a','consulta','{"telefone":"5541999990002","nome":"Joao Teste","inicio":"2026-11-20T14:00:00-03:00","google_event_id":"evt1","confirmacao":"Confirmou"}'::jsonb);
  perform clara_evento('token-a','consulta','{"telefone":"5541999990002","inicio":"2026-11-20T15:00:00-03:00","google_event_id":"evt1","confirmacao":"Sem resposta"}'::jsonb);
  perform clara_evento('token-b','contato','{"telefone":"5541999990001","nome":"Paciente da B"}'::jsonb);
  insert into orcamentos (clinica_id, paciente_id, modelo, valor) select clinica_id, id, 'lentes', 22000 from pacientes where clinica_id = v_a and telefone='5541999990001';
  insert into orcamentos (clinica_id, paciente_id, modelo, valor) select clinica_id, id, 'facetas', 12000 from pacientes where clinica_id = v_a and telefone='5541999990001';
  insert into orcamentos (clinica_id, paciente_id, modelo, valor) select clinica_id, id, 'lentes', 5000 from pacientes where clinica_id = v_b;
  begin perform clara_evento('token-errado','contato','{"telefone":"5541999990001"}'::jsonb); v_err := 'ACEITOU TOKEN ERRADO';
  exception when others then v_err := sqlerrm; end;
  begin perform clara_evento('token-a','tipo-que-nao-existe','{"telefone":"5541999990001"}'::jsonb); v_err := v_err || ' | TIPO INVALIDO ACEITO';
  exception when others then v_err := v_err || ' | ' || sqlerrm; end;
  insert into auth.users (id, aud, role, email) values (ua,'authenticated','authenticated','a@teste.invalid'), (ub,'authenticated','authenticated','b@teste.invalid');
  insert into membros values (ua, v_a, 'dono'), (ub, v_b, 'dono');
  perform set_config('request.jwt.claims', '{"sub":"00000000-0000-0000-0000-0000000000a1","role":"authenticated"}', true);
  set local role authenticated;
  select format('pacientes=%s, orcamentos=%s, clinicas=%s, membros=%s, da_B=%s',
    (select count(*) from pacientes), (select count(*) from orcamentos), (select count(*) from clinicas), (select count(*) from membros),
    (select count(*) from pacientes where nome = 'Paciente da B')) into v_ve;
  begin insert into pacientes (clinica_id, telefone) values (v_b, '5541777770001'); v_ins := 'ENTROU NA CLINICA B (ERRO)';
  exception when others then v_ins := 'bloqueado'; end;
  begin update pacientes set notas = 'invasao' where clinica_id = v_b; get diagnostics r = row_count; v_ins := v_ins || ' | update na B afetou ' || r || ' linhas';
  exception when others then v_ins := v_ins || ' | update bloqueado'; end;
  reset role;
  perform set_config('request.jwt.claims', '{"role":"anon"}', true);
  set local role anon;
  begin perform count(*) from pacientes; v_anon := 'ANON LEU PACIENTES (ERRO)'; exception when others then v_anon := 'anon bloqueado em pacientes'; end;
  begin perform count(*) from clinicas; v_anon := v_anon || ' | ANON LEU CLINICAS (ERRO)'; exception when others then v_anon := v_anon || ' | anon bloqueado em clinicas'; end;
  reset role;
  select jsonb_build_object(
    'pacientes', (select count(*) from pacientes),
    'encaminhamentos', (select count(*) from encaminhamentos),
    'tipos', (select array_agg(tipo order by tipo) from encaminhamentos),
    'estado_conversa', (select estado from conversas where paciente_id = (select id from pacientes where clinica_id=v_a and telefone='5541999990001')),
    'situacao_joao', (select situacao from pacientes where clinica_id=v_a and telefone='5541999990002'),
    'consultas', (select count(*) from consultas),
    'consulta_confirmacao', (select confirmacao from consultas limit 1),
    'numeros_A', (select array_agg(numero order by numero) from orcamentos where clinica_id=v_a),
    'numeros_B', (select array_agg(numero order by numero) from orcamentos where clinica_id=v_b),
    'mesmo_telefone_nas_duas', (select count(*) from pacientes where telefone='5541999990001'),
    'token_errado', v_err, 'usuario_A_ve', v_ve, 'usuario_A_tenta_invadir_B', v_ins, 'visitante', v_anon)::text into r;
  raise exception 'RESULTADO: %', r;
end $$;
