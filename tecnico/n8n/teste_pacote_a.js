// Teste local (sem servidor, sem WhatsApp, sem custo) do Pacote A de 18/11: avisos para a equipe (A1), recusas seguidas (A2),
// confirmação de cancelamento (A5), frases fixas em pt/en/es (A6), promessa de encaminhar em en/es (A7) e trava/limites (A8).
// Roda o código dos nós do fluxo gerado com dados fictícios.
// Uso (dentro de tecnico/n8n):  python gerar_fluxos.py clinica-demo   e depois   node teste_pacote_a.js [clinica-demo]
const fs = require('fs');
const slug = process.argv[2] || 'clinica-demo';
const fluxo = JSON.parse(fs.readFileSync(__dirname + '/gerados/' + slug + '/atendimento.json', 'utf8'));
const nos = Object.fromEntries(fluxo.nodes.map(n => [n.name, n]));
const ASS = fluxo.name.split(' · ')[0];   // nome da assistente (Clara na demo)
function rodar(nome, entrada, refs) {
  const $ = n => ({ first: () => ({ json: refs[n] || {} }), last: () => ({ json: refs[n] || {} }) });
  return new Function('$input', '$', nos[nome].parameters.jsCode)({ first: () => ({ json: entrada }), all: () => [{ json: entrada }] }, $);
}
const agora = Date.now();
const FICHA = { telefone: '554199900990', aprovador: '554199900991', nome_paciente: 'Ana', ultimo_id: 'x1', conversa: '', pendente: '' };
const decidir = (ia, ficha) => rodar('Decidir a ação', ia, { 'Ler ficha e instruções (só a última responde)': { ...FICHA, ...ficha }, 'Montar o pedido para a IA': { agenda_ok: true } })[0].json;
const resultado = (tipo, ia, ficha, entrada) => {
  const ia2 = decidir(ia, ficha);
  return rodar('Resultado · ' + tipo, entrada || {}, { 'Decidir a ação': ia2, 'Ler ficha e instruções (só a última responde)': { ...FICHA, ...ficha } })[0].json;
};
const avisos = r => JSON.parse(r.envios).filter(e => e.phone === FICHA.aprovador).map(e => e.m1);
const paraPaciente = r => JSON.parse(r.envios).filter(e => e.phone === FICHA.telefone).map(e => [e.m1, e.m2, e.m3].filter(Boolean).join(' ')).join(' ');
const recente = min => new Date(agora - min * 60000).toISOString();

const T = [];
const t = (desc, ok, info) => T.push({ desc, ok: !!ok, info });

// ---------- A1: avisos ----------
let r = resultado('humano', { acao: 'humano', motivo: 'Paciente relatou sangramento forte', mensagem1: 'Vou passar para a doutora agora.' },
  { pendente: 'Agora comecei a sangrar muito', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento' });
t('A1 sangramento depois de aviso de recibo gera aviso URGENTE', avisos(r).length === 1 && /URGENTE/.test(avisos(r)[0]) && r.aviso_humano === 'sim', avisos(r));
r = resultado('humano', { acao: 'humano', motivo: 'Paciente pediu recibo do pagamento', mensagem1: 'Vou verificar.' },
  { pendente: 'ok obrigada 👍', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento' });
t('A1 "ok obrigada 👍" logo depois do aviso não gera aviso', avisos(r).length === 0 && r.aviso_humano === '', avisos(r));
r = resultado('humano', { acao: 'humano', motivo: 'Paciente pediu recibo do pagamento', mensagem1: 'Vou verificar.' },
  { pendente: 'thanks', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento' });
t('A1 "thanks" não gera aviso', avisos(r).length === 0);
r = resultado('humano', { acao: 'humano', motivo: 'Paciente pediu recibo do pagamento em nome da empresa', mensagem1: 'Vou verificar.' },
  { pendente: 'é no CNPJ da empresa', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento' });
t('A1 informação nova curta (mesmo assunto) vira complemento', avisos(r).length === 1 && /Complemento/.test(avisos(r)[0]) && r.complemento === 'sim', avisos(r));
r = resultado('humano', { acao: 'humano', motivo: 'Paciente pediu recibo do pagamento em nome da empresa', mensagem1: 'Vou verificar.' },
  { pendente: 'o CNPJ é 12.345', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento', ultimo_complemento: recente(5) });
t('A1 segundo complemento em menos de 15 min não sai', avisos(r).length === 0);
r = resultado('humano', { acao: 'humano', motivo: 'Paciente pediu recibo do pagamento', mensagem1: 'Vou verificar.' },
  { pendente: 'tô com o rosto inchado', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento', ultimo_complemento: recente(5) });
t('A1 urgência passa mesmo com complemento recente', avisos(r).length === 1 && /URGENTE/.test(avisos(r)[0]));
r = resultado('humano', { acao: 'humano', motivo: 'Paciente quer saber sobre clareamento', mensagem1: 'Vou verificar.' },
  { pendente: 'e clareamento?', ultimo_aviso_humano: recente(3), ultimo_motivo_humano: 'Paciente pediu recibo do pagamento' });
t('A1 assunto novo curto depois de aviso gera aviso', avisos(r).length === 1 && /Chamar uma pessoa/.test(avisos(r)[0]));
let d = decidir({ acao: 'responder', mensagem1: 'Entendo, faça compressa fria.' }, { pendente: 'minha gengiva está sangrando muito' });
t('A1 urgência com ação "responder" vira "humano"', d.rota === 'humano', d.rota);
d = decidir({ acao: 'responder', mensagem1: 'Pode acontecer uma leve sensibilidade.' }, { pendente: 'clareamento faz a gengiva sangrar?' });
t('A1 pergunta sobre sangramento continua "responder"', d.rota === 'responder', d.rota);

// ---------- A2: recusas seguidas ----------
const iaAg = { acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!', nome_completo: 'Ana Souza', telefone_contato: '41999990000' };
r = resultado('invalido', iaAg, { pendente: 'amanhã às 11h', recusas_agenda: 0 }, { passo: 'invalido', motivo: 'horário que não foi oferecido nem pedido na conversa' });
t('A2 1ª recusa por formato pede a data, sem dizer indisponível', /confirma o dia e o mês/.test(paraPaciente(r)) && !/não está disponível/.test(paraPaciente(r)) && r.recusas === 'somar' && avisos(r).length === 0, paraPaciente(r));
r = resultado('invalido', iaAg, { pendente: 'quarta às 10h', recusas_agenda: 0 }, { passo: 'invalido', motivo: 'dia da semana sem avaliação' });
t('A2 1ª recusa por regra diz indisponível e oferece outras', /não está disponível/.test(paraPaciente(r)) && avisos(r).length === 0);
r = resultado('invalido', iaAg, { pendente: 'amanhã às 11h', recusas_agenda: 1 }, { passo: 'invalido', motivo: 'horário que não foi oferecido nem pedido na conversa' });
t('A2 2ª recusa avisa a equipe com motivo e pedido', avisos(r).length === 1 && /2ª recusa/.test(avisos(r)[0]) && /Motivo técnico/.test(avisos(r)[0]) && /amanhã às 11h/.test(avisos(r)[0]) && /equipe confirmar/.test(paraPaciente(r)) && r.aviso_humano === 'sim', avisos(r));
r = resultado('invalido', iaAg, { pendente: 'amanhã às 11h', recusas_agenda: 2 }, { passo: 'invalido', motivo: 'horário que não foi oferecido nem pedido na conversa' });
t('A2 3ª recusa não repete recusa nem aviso', avisos(r).length === 0 && /equipe confirmar/.test(paraPaciente(r)) && !/não está disponível/.test(paraPaciente(r)));
r = resultado('ocupado', iaAg, { pendente: 'pode ser 19/11 11h', recusas_agenda: 1 }, { passo: 'ocupado' });
t('A2 ocupado também conta (2ª vez avisa)', avisos(r).length === 1 && /ocupado/.test(avisos(r)[0]));
r = resultado('agenda', iaAg, { pendente: 'pode ser', recusas_agenda: 1 }, { id: 'evento-ficticio' });
t('A2 marcar com sucesso zera o contador', r.recusas === 'zerar' && r.aval === 'definir');
const sql = nos['Salvar conversa e ficha'].parameters.query;
t('A2 o banco grava o contador (recusas_agenda)', /recusas_agenda = CASE \$19/.test(sql) && /ultimo_complemento = CASE WHEN \$20/.test(sql));

// ---------- A5: cancelar ----------
const fichaCanc = (ultima, pend) => ({ avaliacao_evento: 'ev1', avaliacao_texto: '19/11 às 11:00', avaliacao_inicio: '2026-11-19T14:00:00.000Z',
  conversa: 'Paciente: quero cancelar\n' + ASS + ': ' + ultima, pendente: pend });
const casosCanc = [
  ['Só para confirmar: você quer cancelar a sua avaliação de 19/11 às 11:00, certo?', 'sim', 'cancelar', 'pt "sim" depois de "certo?"'],
  ['Just to confirm: you would like to cancel your evaluation on Thursday, Nov 19, at 11:00, correct?', 'Yes', 'cancelar', 'en "Yes" depois de "correct?"'],
  ['Just to confirm: you would like to cancel your evaluation on Thursday, Nov 19, at 11:00, correct?', 'Yes, I confirm', 'cancelar', 'en "Yes, I confirm"'],
  ['Solo para confirmar: ¿quieres cancelar tu evaluación del jueves 19 de noviembre a las 11:00, correcto?', 'Sí, confirmo', 'cancelar', 'es "Sí, confirmo"'],
  ['A sua avaliação de quinta, 19/11, às 11h, certo?', 'Não, quero manter', 'responder', 'pt "Não, quero manter" não cancela'],
  ['Posso cancelar sua avaliação?', 'Não, quero manter.', 'responder', 'Codex: "Não, quero manter"'],
  ['Your appointment can be canceled.', 'Please keep it.', 'responder', 'Codex: sem pergunta'],
  ['A sua avaliação é quinta, certo?', 'Quero saber o preço.', 'responder', 'Codex: pergunta de preço não é "sim"'],
  ['Claro! Posso te ajudar com mais alguma coisa?', 'sim', 'responder', 'pergunta que não é de confirmação'],
];
for (const [ultima, pend, esperado, desc] of casosCanc) {
  d = decidir({ acao: 'cancelar', mensagem1: 'Cancelada.' }, fichaCanc(ultima, pend));
  t('A5 ' + desc, d.rota === esperado, d.rota + ' / ' + d.mensagem1);
}
d = decidir({ acao: 'cancelar', mensagem1: 'Cancelada.', idioma: 'pt' }, fichaCanc('A sua avaliação de quinta, 19/11, às 11h, certo?', 'Não, quero manter'));
t('A5 negativa recebe "continua marcada"', /continua marcada/.test(d.mensagem1), d.mensagem1);
d = decidir({ acao: 'cancelar', mensagem1: 'Cancelled.', idioma: 'en' }, fichaCanc('Sure!', 'I want to cancel'));
t('A5 pergunta de confirmação em inglês', /Só para confirmar/.test(d.mensagem1) && /19\/11/.test(d.mensagem1) && d.rota === 'responder', d.mensagem1);

// ---------- A6: idioma das frases fixas ----------
r = resultado('invalido', { ...iaAg, idioma: 'en' }, { pendente: 'tomorrow at 11', recusas_agenda: 0 }, { passo: 'invalido', motivo: 'dia da semana sem avaliação' });
t('A6 recusa em inglês', /não está disponível/.test(paraPaciente(r)), paraPaciente(r));
r = resultado('invalido', { ...iaAg, idioma: 'es' }, { pendente: 'mañana a las 11', recusas_agenda: 1 }, { passo: 'invalido', motivo: 'x' });
t('A6 2ª recusa em espanhol, responde em português', /equipe/.test(paraPaciente(r)), paraPaciente(r));
r = resultado('ocupado', { ...iaAg, idioma: '' }, { pendente: 'Hi, can I book Nov 19 at 11am please?', recusas_agenda: 0 }, { passo: 'ocupado' });
t('A6 sem campo idioma, adivinha inglês pela mensagem', /acabou de ser preenchido/.test(paraPaciente(r)), paraPaciente(r));
r = resultado('dados', { ...iaAg, idioma: 'es' }, { pendente: 'quiero el jueves' }, { passo: 'dados' });
t('A6 pedido de dados em espanhol', /nome completo/.test(paraPaciente(r)));
r = resultado('falha', { ...iaAg, idioma: 'en' }, { pendente: 'Nov 19 at 11am' }, {});
t('A6 falha em inglês', /Só um instante/.test(paraPaciente(r)) && /Falha ao marcar/.test(avisos(r)[0] || ''));
r = resultado('ja_marcada', { acao: 'agendar', idioma: 'es', mensagem1: 'x' }, { pendente: 'quiero agendar', avaliacao_texto: '19/11 às 11:00', avaliacao_inicio: '2026-11-19T14:00:00.000Z' }, {});
t('A6 avaliação já marcada em espanhol', /Vi aqui que você já tem/.test(paraPaciente(r)), paraPaciente(r));
const falha = rodar('Falha técnica: avisar', { erro: 'x' }, { 'Ler ficha e instruções (só a última responde)': { ...FICHA, pendente: 'Hola, quiero una cita para mañana por favor' } });
t('A6 falha técnica em espanhol', falha[1].json.m1.startsWith('Só um instante'), falha[1].json.m1);
t('A6 a IA é pedida a responder sempre em português', /sempre em português/.test(nos['Montar o pedido para a IA'].parameters.jsCode));

// ---------- A7: promessa de encaminhar ----------
for (const [txt, esperado] of [["I'll forward your message to the doctor.", 'humano'], ["Let me check with the team and get back to you.", 'humano'],
  ['Voy a pasar su mensaje a la doctora.', 'humano'], ['Le paso tu pregunta a la doctora.', 'humano'], ['Vou passar sua mensagem para a doutora.', 'humano'],
  ["I'll check the available times for you: Thursday, Nov 19, at 9am.", 'responder'], ['Voy a verificar los horarios: jueves 19 a las 9.', 'responder'],
  ['The evaluation costs R$ 300.', 'responder']]) {
  d = decidir({ acao: 'responder', mensagem1: txt }, { pendente: 'hello' });
  t('A7 "' + txt + '" -> ' + esperado, d.rota === esperado, d.rota);
}

// ---------- A8: trava e tempo limite ----------
const trava = nos['Reservar o horário (trava de 5 min)'];
t('A8 trava de 5 minutos', trava && /interval '5 minutes'/.test(trava.parameters.query));
for (const n of ['Conferir se o horário segue livre', 'Criar a avaliação na agenda', 'Mudar a avaliação na agenda', 'Cancelar a avaliação na agenda'])
  t('A8 limite de 30 s: ' + n, nos[n].parameters.options.timeout === 30000);

let falhas = 0;
for (const x of T) if (!x.ok) { falhas++; console.log('FALHOU  ' + x.desc + '  ' + JSON.stringify(x.info)); }
console.log((T.length - falhas) + ' de ' + T.length + ' testes do Pacote A certos (' + slug + ')');
process.exit(falhas ? 1 : 0);
