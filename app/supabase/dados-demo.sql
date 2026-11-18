-- Clínica de demonstração (fictícia): dados de exemplo para a Dra. Suzana Vidal, usados para ver o app funcionando.
-- Aplicado em 18/11/2026 no projeto keshion-app. Telefones com prefixo 554199900: nunca reais.
-- Rodar só uma vez (cria a clínica 'clinica-demo'). Para dar acesso a alguém, depois de criar o usuário em
-- Authentication > Users:  insert into membros select id, (select id from clinicas where slug='clinica-demo'), 'dono' from auth.users where email = '<e-mail>';
do $$
declare c uuid;
begin
  insert into clinicas (slug, nome, telefone, endereco, mensalidade)
  values ('clinica-demo','Clínica Dra. Suzana Vidal','(41) 3000-0000','Rua Desembargador Motta, 2000, sala 1404, Batel, Curitiba/PR', 3000)
  returning id into c;

  insert into pacientes (clinica_id, telefone, nome, nome_completo, origem, situacao, ja_paciente) values
    (c,'5541999000011','Paula Antunes','Paula Antunes','Indicação','Em tratamento',true),
    (c,'5541999000012','Carlos Mendes','Carlos Mendes','Google','Orçamento em aberto',false),
    (c,'5541999000013','Henrique Sá','Henrique Sá','Instagram','Em conversa',false),
    (c,'5541999000014','Mariana Costa','Mariana Costa','Anúncio','Orçamento em aberto',false),
    (c,'5541999000015','Juliana Prado','Juliana Prado','Indicação','Avaliação marcada',false),
    (c,'5541999000017','Beatriz Lima','Beatriz Lima','Anúncio','Avaliação marcada',false),
    (c,'5541999000018','Thiago Alves','Thiago Alves','Anúncio','Em tratamento',true),
    (c,'5541999000019','Rafael Nogueira','Rafael Nogueira','Instagram','Avaliação marcada',false),
    (c,'5541999000023','Gustavo Pires','Gustavo Pires','Google','Orçamento em aberto',false);

  insert into conversas (clinica_id, paciente_id, ultima_mensagem, ultimo_horario, estado, fora_do_horario)
  select c, p.id, v.msg, now() - v.atras, v.estado, v.fora
  from (values
    ('5541999000012','Queria falar com a Dra. Suzana antes de decidir.', interval '35 minutes','aguardando_equipe',false),
    ('5541999000014','Consigo um desconto maior à vista?', interval '20 minutes','aguardando_equipe',false),
    ('5541999000013','Vocês aceitam o convênio OdontoPrev?', interval '12 minutes','aguardando_equipe',false),
    ('5541999000011','Uma das lentes parece solta desde ontem à noite.', interval '8 minutes','aguardando_equipe',true),
    ('5541999000018','Esperei 40 minutos e ninguém me avisou do atraso.', interval '5 minutes','aguardando_equipe',false),
    ('5541999000019','Ótimo, então fica amanhã às 15h?', interval '2 hours','agendou',false),
    ('5541999000017','Pode ser amanhã às 10h, obrigada.', interval '4 hours','agendou',true),
    ('5541999000015','Confirmado, até amanhã.', interval '26 hours','ia_respondeu',true),
    ('5541999000023','Obrigado, vou ver e te falo.', interval '27 hours','ia_respondeu',true)
  ) as v(tel, msg, atras, estado, fora)
  join pacientes p on p.clinica_id = c and p.telefone = v.tel;

  insert into encaminhamentos (clinica_id, paciente_id, tipo, mensagem, criado)
  select c, p.id, v.tipo, v.msg, now() - v.atras
  from (values
    ('5541999000011','urgencia','Estou com muita sensibilidade e uma das lentes parece solta desde ontem à noite.', interval '8 minutes'),
    ('5541999000012','pediu_doutora','Queria falar com a Dra. Suzana antes de decidir. Tenho dúvida sobre o prazo do alinhador.', interval '35 minutes'),
    ('5541999000013','ia_nao_sabe','Vocês aceitam o convênio OdontoPrev?', interval '12 minutes'),
    ('5541999000014','desconto','Se eu fechar as 10 lentes à vista, consigo um desconto maior que os 5% do Pix?', interval '20 minutes'),
    ('5541999000018','reclamacao','Hoje esperei 40 minutos para ser atendido e ninguém me avisou do atraso.', interval '5 minutes')
  ) as v(tel, tipo, msg, atras)
  join pacientes p on p.clinica_id = c and p.telefone = v.tel;
end $$;
