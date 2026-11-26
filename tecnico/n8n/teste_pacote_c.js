// Teste local (sem servidor, sem WhatsApp, sem custo) do Pacote C de 19/11: C1 (cancelar), C2 (horário negado),
// C3 (urgência), C4 (pausa antes de cada envio), C5 (aviso de falha sem texto livre) e C6 (nome do áudio).
// O C7 (cadastro de clínica real com numeros_keshion vazio) fica em teste_pacote_c_cadastro.py.
// Uso (dentro de tecnico/n8n):  python gerar_fluxos.py clinica-demo   e depois   node teste_pacote_c.js [clinica-demo | caminho/do/atendimento.json]
// Para ver o "antes": node teste_pacote_c.js caminho/do/atendimento-antigo.json  (e, para C4/C5, o envio-antigo.json ao lado).
const fs = require('fs');
const arg = process.argv[2] || 'clinica-demo';
const caminhoAt = arg.endsWith('.json') ? arg : __dirname + '/gerados/' + arg + '/atendimento.json';
const caminhoEn = caminhoAt.replace(/atendimento([^\\/]*)\.json$/, 'envio$1.json');
const fluxo = JSON.parse(fs.readFileSync(caminhoAt, 'utf8'));
const envio = fs.existsSync(caminhoEn) ? JSON.parse(fs.readFileSync(caminhoEn, 'utf8')) : { nodes: [], connections: {} };
const nos = Object.fromEntries(fluxo.nodes.map(n => [n.name, n]));
const nosE = Object.fromEntries(envio.nodes.map(n => [n.name, n]));
const ASS = fluxo.name.split(' · ')[0];
function rodar(nome, entrada, refs, extra) {
  const $ = n => ({ first: () => ({ json: refs[n] || {} }), last: () => ({ json: refs[n] || {} }), item: { json: refs[n] || {} }, all: () => [{ json: refs[n] || {} }] });
  return new Function('$input', '$', nos[nome].parameters.jsCode)({ first: () => ({ json: entrada }), all: () => [{ json: entrada }] }, $);
}
const FICHA = { telefone: '554199900990', aprovador: '554199900991', nome_paciente: 'Ana', ultimo_id: 'x1', conversa: '', pendente: '' };
const decidir = (ia, ficha) => rodar('Decidir a ação', ia, { 'Ler ficha e instruções (só a última responde)': { ...FICHA, ...ficha }, 'Montar o pedido para a IA': { agenda_ok: true } })[0].json;
const resultado = (tipo, ia, ficha, entrada) => {
  const ia2 = decidir(ia, ficha);
  return rodar('Resultado · ' + tipo, entrada || {}, { 'Decidir a ação': ia2, 'Ler ficha e instruções (só a última responde)': { ...FICHA, ...ficha } })[0].json;
};
const avisos = r => JSON.parse(r.envios).filter(e => e.phone === FICHA.aprovador).map(e => e.m1);
const T = [];
const t = (desc, ok, info) => T.push({ desc, ok: !!ok, info });
const tenta = (desc, fn) => { try { fn(); } catch (e) { t(desc, false, 'erro: ' + e.message); } };

// ---------- C1: cancelar ----------
const ficha = (ultima, pend) => ({ avaliacao_evento: 'ev1', avaliacao_texto: '19/11 às 11:00', avaliacao_inicio: '2026-11-19T14:00:00.000Z',
  conversa: 'Paciente: oi\n' + ASS + ': ' + ultima, pendente: pend });
const PERG_CANC = 'Só para confirmar: você quer cancelar a sua avaliação de 19/11 às 11:00, certo?';
const casosC1 = [
  ['Esse é o seu telefone certo? Posso usar este número?', 'sim, esse é meu telefone', 'responder', 'C1 "sim, esse é meu telefone" (pergunta do telefone) não cancela'],
  ['Para confirmar: o telefone de contato é este mesmo, correto?', 'sim', 'responder', 'C1 "sim" depois de pergunta sem cancelar não cancela'],
  ['Qual o seu nome completo?', 'Ana Souza', 'responder', 'C1 IA escolhe cancelar do nada: não cancela'],
  [PERG_CANC, 'isso é só uma dúvida, pode dizer o preço?', 'responder', 'C1 dúvida com "isso" e "pode" não conta como sim'],
  // Pacote E (25/11): "sim" no começo e uma pergunta depois cancela (a IA responde a pergunta junto); antes entrava em loop (Bia).
  [PERG_CANC, 'sim, mas quanto custa a limpeza?', 'cancelar', 'E1 "sim" no começo com pergunta depois cancela'],
  [PERG_CANC, 'sim. aliás, vocês atendem sábado', 'cancelar', 'E1 "sim" com outro assunto cancela'],
  [PERG_CANC, 'sim', 'cancelar', 'C1 "sim" simples depois de pergunta de cancelar cancela'],
  [PERG_CANC, 'Sim, pode cancelar por favor', 'cancelar', 'C1 "Sim, pode cancelar por favor" cancela'],
  [PERG_CANC, 'isso mesmo', 'cancelar', 'C1 "isso mesmo" cancela'],
  [PERG_CANC, 'Valeu!', 'cancelar', 'E1 "Valeu!" cancela (Thiago)'],
  [PERG_CANC, 'Sim, quero cancelar a avaliação da minha filha Laura Souza, dia 19/11 às 11h, ela não vai poder ir', 'cancelar', 'E1 confirmação longa cancela (Sandra)'],
  ['Você quer marcar para 26/11 às 10h, certo?', 'sim', 'responder', 'E1 C04 "sim" sobre outra data não cancela'],
  ['Posso cancelar a de 26/11?', 'sim', 'responder', 'E1 C04 pergunta de cancelar com outra data não cancela'],
  [PERG_CANC, 'não, quero manter', 'responder', 'C1 negativa vence'],
  [PERG_CANC, 'sim, mas não cancela ainda', 'responder', 'C1 "sim, mas não" vence a negativa'],
  [PERG_CANC, 'sim?', 'responder', 'C1 "sim?" (com pergunta) não cancela'],
];
// Diagnóstico de 20/11: pergunta de cancelar repetida. Segunda rodada: a fala anterior da assistente também era a pergunta.
const ficha2 = (resp1, pend) => ({ avaliacao_evento: 'ev1', avaliacao_texto: '19/11 às 11:00', avaliacao_inicio: '2026-11-19T14:00:00.000Z',
  conversa: ['Paciente: oi', ASS + ': ' + PERG_CANC, 'Paciente: ' + resp1, ASS + ': ' + PERG_CANC].join('\n'), pendente: pend });
const casosC1b = [
  ['sim, esse horário mesmo', 'sim, pode cancelar esse horário mesmo', 'cancelar', 'C1b 2ª rodada: "sim" com palavras a mais cancela'],
  ['sim, obrigada', 'sim, claro, pode ser', 'cancelar', 'C1b 2ª rodada: "sim, claro, pode ser" cancela'],
  ['sim, e o endereço?', 'qual o endereço mesmo?', 'responder', 'C1b 2ª rodada: só pergunta continua sem cancelar'],
  ['sim, esse horário mesmo', 'sim, mas não cancela ainda', 'responder', 'C1b 2ª rodada: negativa vence'],
  ['sim, esse horário mesmo', 'não, quero manter', 'responder', 'C1b 2ª rodada: "não, quero manter" não cancela'],
];
for (const [r1, pend, esperado, desc] of casosC1b) tenta(desc, () => {
  const d = decidir({ acao: 'cancelar', mensagem1: 'Cancelada.' }, ficha2(r1, pend));
  t(desc, d.rota === esperado, d.rota + ' / ' + d.mensagem1);
});
for (const [ultima, pend, esperado, desc] of casosC1) tenta(desc, () => {
  const d = decidir({ acao: 'cancelar', mensagem1: 'Cancelada.' }, ficha(ultima, pend));
  t(desc, d.rota === esperado, d.rota + ' / ' + d.mensagem1);
});

// ---------- Pacote E (25/11): pendência de cancelamento na ficha ----------
const agoraMenos = min => new Date(Date.now() - min * 60000).toISOString();
const fichaE = (ultima, pend, extra) => ({ ...ficha(ultima, pend), cancelar_evento: 'ev1', cancelar_pedido_em: agoraMenos(5), cancelar_tentativas: 0, ...extra });
const casosE = [
  // [última fala, mensagem, ação da IA, extra da ficha, rota esperada, cancel_op esperado, descrição]
  [PERG_CANC, 'sim', { acao: 'cancelar', mensagem1: 'Cancelada.' }, {}, 'cancelar', 'manter', 'E2 com pendência, "sim" cancela'],
  [PERG_CANC, 'mas antes me responde: tem multa?', { acao: 'responder', mensagem1: 'Não tem multa.' }, {}, 'responder', 'somar', 'E2 Bia: pergunta no meio não perde a pendência'],
  [PERG_CANC, 'não é minha, é da Laura', { acao: 'responder', mensagem1: 'Entendi, é da Laura.' }, {}, 'responder', 'somar', 'E2 Sandra: "não é minha" não é recusa'],
  [PERG_CANC, 'não, quero manter', { acao: 'responder', mensagem1: 'Combinado, continua marcada.' }, {}, 'responder', 'limpar', 'E2 "quero manter" encerra a pendência'],
  [PERG_CANC, 'hmm deixa eu ver', { acao: 'responder', mensagem1: 'Claro, sem pressa.' }, { cancelar_tentativas: 2 }, 'humano', 'equipe', 'E2 3ª resposta sem decisão chama a equipe e marca "com a equipe"'],
  [PERG_CANC, 'sim', { acao: 'cancelar', mensagem1: 'Cancelada.' }, { cancelar_evento: 'outro' }, 'cancelar', 'limpar', 'E2 pendência de outra avaliação é descartada (mas pergunta citava a data)'],
  ['Qual o seu nome completo?', 'Ana', { acao: 'cancelar', mensagem1: 'Cancelada.' }, { cancelar_evento: null, cancelar_pedido_em: null }, 'responder', 'definir', 'E2 IA quer cancelar sem pergunta: pergunta e guarda a pendência'],
  [PERG_CANC, 'quero remarcar para outro dia', { acao: 'remarcar', mensagem1: 'Claro.' }, {}, 'agenda', 'limpar', 'E2 mudou para remarcar: limpa a pendência'],
  [PERG_CANC, 'sim', { acao: 'cancelar', mensagem1: 'Cancelada.' }, { cancelar_pedido_em: agoraMenos(60 * 25) }, 'cancelar', 'limpar', 'E2 pendência de mais de 24 h é descartada'],
];
for (const [ultima, pend, ia, extra, rota, op, desc] of casosE) tenta(desc, () => {
  const d = decidir(ia, fichaE(ultima, pend, extra));
  t(desc, d.rota === rota && d.cancel_op === op, d.rota + ' / ' + d.cancel_op + ' / ' + d.mensagem1 + ' | ' + (d.mensagem2 || ''));
});
// ---------- Pacote E, correção de 26/11 (teste ao vivo de 25/11: casos 1 e 6 e Júlia) ----------
const PERG_IA = 'A sua avaliação marcada é de terça, 19/11, às 11h, certo?';   // pergunta da própria IA, sem a palavra "cancelar"
const casos26 = [
  // [última fala, mensagem, ação da IA, extra da ficha, rota esperada, cancel_op esperado, descrição]
  // (a) a IA pergunta sozinha com "responder": abre a pendência
  ['Prontinho, sua avaliação está marcada.', 'quero cancelar minha avaliação', { acao: 'responder', mensagem1: PERG_IA }, { cancelar_evento: null, cancelar_pedido_em: null }, 'responder', 'definir', 'E1 caso 1: IA pergunta "certo?" sozinha e a pendência é gravada'],
  ['Prontinho.', 'hmm', { acao: 'responder', mensagem1: 'Quer que eu cancele a avaliação de 19/11 às 11h, ou ficou alguma dúvida?' }, { cancelar_evento: null, cancelar_pedido_em: null }, 'responder', 'definir', 'E1 caso 6: IA pergunta "quer que eu cancele" e a pendência é gravada'],
  ['Prontinho.', 'qual o endereço?', { acao: 'responder', mensagem1: 'Fica na Rua X. Seu telefone é este, certo?' }, { cancelar_evento: null, cancelar_pedido_em: null }, 'responder', 'manter', 'E1 "certo?" sem falar de cancelar não abre pendência'],
  ['Prontinho.', 'posso cancelar com quanto tempo de antecedência?', { acao: 'responder', mensagem1: 'Com 24 horas. Sua avaliação é 19/11 às 11h, certo?' }, { cancelar_evento: null, cancelar_pedido_em: null }, 'responder', 'manter', 'E1 dúvida sobre a regra de cancelar não abre pendência'],
  // depois da pergunta da IA, "Valeu!" cancela (caso 1)
  [PERG_IA, 'Valeu!', { acao: 'responder', mensagem1: 'Só para confirmar: posso cancelar?' }, {}, 'cancelar', 'manter', 'E1 caso 1: "Valeu!" depois da pergunta da IA cancela'],
  [PERG_IA, 'Valeu!', { acao: 'cancelar', mensagem1: 'Sem problemas, sua avaliação foi cancelada.' }, {}, 'cancelar', 'manter', 'E1 caso 1: "Valeu!" com a IA cancelando cancela'],
  // (b) sim firme com outra pergunta junto (Júlia)
  [PERG_CANC, 'Isso, pode cancelar sim / obrigada pela paciência / tem como aproveitar essa avaliação? tem desconto?', { acao: 'cancelar', mensagem1: 'Cancelada. Sobre o desconto, a equipe vê.' }, {}, 'cancelar', 'manter', 'E1 Júlia: "Isso, pode cancelar sim" com pergunta junto cancela'],
  [PERG_CANC, 'já confirmei sim, pode cancelar / tô no trabalho / e a avaliação aproveita ou tem desconto?', { acao: 'responder', mensagem1: PERG_CANC }, {}, 'cancelar', 'manter', 'E1 Júlia: "já confirmei sim" com pergunta cancela'],
  [PERG_CANC, 'já falei que pode cancelar, mano / tô sem tempo / a avaliação aproveita? / ainda não sei nada, tô confusa', { acao: 'cancelar', mensagem1: 'Cancelada.' }, { cancelar_tentativas: 2 }, 'cancelar', 'manter', 'E1 Júlia: "já falei que pode cancelar" com "ainda não sei" cancela'],
  [PERG_CANC, 'isso é só uma dúvida, pode dizer o preço?', { acao: 'responder', mensagem1: 'Custa R$ 150.' }, {}, 'responder', 'somar', 'E1 "isso é só uma dúvida" continua sem cancelar'],
  [PERG_CANC, 'pode cancelar?', { acao: 'responder', mensagem1: 'Posso sim.' }, {}, 'responder', 'somar', 'E1 "pode cancelar?" (pergunta) não cancela'],
  // trocar em vez de cancelar e manter com "pode" no meio (Júlia)
  ['A avaliação de 19/11 às 11h é a que você quer cancelar, certo?', 'Isso, quinta às 16h. / quer dizer, queria ver outro horário, sexta de manhã? / prefiro reagendar do que cancelar', { acao: 'responder', mensagem1: 'Tenho terça às 9h.' }, {}, 'responder', 'limpar', 'E1 Júlia: "prefiro reagendar" não cancela e limpa a pendência'],
  [PERG_CANC, 'sério que parcela em 12x? / então talvez eu não cancele não / deixa eu ver, pode deixar marcado por enquanto?', { acao: 'responder', mensagem1: 'Pode deixar, segue marcada.' }, {}, 'responder', 'limpar', 'E1 Júlia: "não cancele não, pode deixar marcado" mantém'],
  // caso 6: três respostas sem decisão
  [PERG_IA, 'hmm', { acao: 'responder', mensagem1: 'Quer que eu cancele ou ficou alguma dúvida?' }, { cancelar_tentativas: 0 }, 'responder', 'somar', 'E2 caso 6: "hmm" soma 1'],
  [PERG_CANC, 'deixa eu ver', { acao: 'responder', mensagem1: 'Sem pressa.' }, { cancelar_tentativas: 1 }, 'responder', 'somar', 'E2 caso 6: "deixa eu ver" soma 2'],
  [PERG_CANC, 'não sei', { acao: 'responder', mensagem1: 'Tudo bem, continua marcada.' }, { cancelar_tentativas: 2 }, 'humano', 'equipe', 'E2 caso 6: "não sei" na 3ª chama a equipe (não é "manter")'],
  // (c) depois de passar para a equipe, não recomeça
  [F_EQUIPE(), 'ok, obrigada / só não entendi se a avaliação aproveita', { acao: 'responder', mensagem1: 'A equipe te explica isso.' }, { cancelar_tentativas: 99 }, 'responder', 'manter', 'E2 Júlia: com a equipe, "ok, obrigada" não pergunta de novo'],
  [F_EQUIPE(), 'ok, obrigada', { acao: 'cancelar', mensagem1: 'Cancelada.' }, { cancelar_tentativas: 99 }, 'responder', 'manter', 'E2 com a equipe, "ok" não cancela'],
  [F_EQUIPE(), 'já disse que pode cancelar, sim / cancela aí / e o desconto?', { acao: 'responder', mensagem1: 'Só para confirmar: você quer cancelar, certo?' }, { cancelar_tentativas: 99 }, 'cancelar', 'manter', 'E2 Júlia: com a equipe, "cancela aí" cancela'],
  [F_EQUIPE(), 'não, quero manter', { acao: 'responder', mensagem1: 'Combinado.' }, { cancelar_tentativas: 99 }, 'responder', 'limpar', 'E2 com a equipe, "quero manter" limpa'],
];
function F_EQUIPE() { return 'Vou pedir para a equipe confirmar o cancelamento com você por aqui, tá bom?'; }
for (const [ultima, pend, ia, extra, rota, op, desc] of casos26) tenta(desc, () => {
  const d = decidir({ ...ia }, fichaE(ultima, pend, extra));
  t(desc, d.rota === rota && d.cancel_op === op, d.rota + ' / ' + d.cancel_op + ' / ' + d.mensagem1 + ' | ' + (d.mensagem2 || ''));
});
tenta('E1 caso 1: a pergunta da IA não ganha uma 2ª pergunta colada', () => {
  const d = decidir({ acao: 'responder', mensagem1: PERG_IA }, fichaE('Prontinho.', 'quero cancelar', { cancelar_evento: null, cancelar_pedido_em: null }));
  t('E1 caso 1: a pergunta da IA não ganha uma 2ª pergunta colada', !d.mensagem2, d.mensagem2);
});
tenta('E1 cancelar com a IA perguntando de novo usa a frase fixa de cancelada', () => {
  const d = decidir({ acao: 'responder', mensagem1: PERG_CANC }, fichaE(PERG_CANC, 'já confirmei sim, pode cancelar'));
  t('E1 cancelar com a IA perguntando de novo usa a frase fixa de cancelada', d.rota === 'cancelar' && /foi cancelada/.test(d.mensagem1) && !/\bcerto\?/.test(d.mensagem1), d.mensagem1);
});
tenta('E2 com a equipe, a IA não pergunta de novo', () => {
  const d = decidir({ acao: 'responder', mensagem1: 'Posso cancelar a sua avaliação de 19/11?' }, fichaE(F_EQUIPE(), 'e o desconto?', { cancelar_tentativas: 99 }));
  t('E2 com a equipe, a IA não pergunta de novo', /equipe já está vendo/.test(d.mensagem1) && !d.mensagem2, d.mensagem1 + ' | ' + d.mensagem2);
});
tenta('E2 a ficha grava "com a equipe" (99)', () => {
  const sql = nos['Salvar conversa e ficha'].parameters.query;
  t('E2 a ficha grava "com a equipe" (99)', /WHEN 'equipe' THEN 99/.test(sql));
});
tenta('E2 o pedido para a IA avisa que a equipe assumiu', () => {
  const js = nos['Montar o pedido para a IA'].parameters.jsCode;
  t('E2 o pedido para a IA avisa que a equipe assumiu', /CANCELAMENTO COM A EQUIPE/.test(js) && /Não pergunte de novo/.test(js));
});

tenta('E2 Bia: a resposta volta a perguntar se pode cancelar', () => {
  const d = decidir({ acao: 'responder', mensagem1: 'Não tem multa.' }, fichaE(PERG_CANC, 'tem multa?'));
  t('E2 Bia: a resposta volta a perguntar se pode cancelar', /posso cancelar\?/.test(d.mensagem2), d.mensagem2);
});
tenta('E2 a ficha grava a pendência', () => {
  const sql = nos['Salvar conversa e ficha'].parameters.query;
  t('E2 a ficha grava a pendência', /cancelar_evento = CASE \$21/.test(sql) && /cancelar_tentativas = CASE \$21/.test(sql));
});
tenta('E2 cancelado limpa a pendência', () => {
  const r = resultado('agenda', { acao: 'cancelar', mensagem1: 'Cancelada.' }, fichaE(PERG_CANC, 'sim'), {});
  t('E2 cancelado limpa a pendência', r.cancel_op === 'limpar', r.cancel_op);
});

// ---------- C2: horário negado ----------
const nVal = nos['Validar o pedido de agenda'];
const js = nVal.parameters.jsCode;
const ini = js.indexOf('const dd = String('), fim = js.indexOf('if (!temData || !temHora)');
const confere = new Function('conversa', 'q', js.slice(ini, fim) + '; return { temData, temHora };');
// [conversa, dia, mês, hora, esperado temHora, descrição]
const casosC2 = [
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: não posso 19/11 às 11h', 19, 11, 11, false, 'C2 pt "não posso 19/11 às 11h" nega o par'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: não posso 19/11 às 11h, pode ser outro dia?', 19, 11, 11, false, 'C2 pt negativa + "outro dia"'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: não marque ainda', 19, 11, 11, false, 'C2 pt "não marque ainda"'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: pode ser 19/11 às 11h\n' + ASS + ': Qual o seu nome?\nPaciente: ainda não, espera', 19, 11, 11, false, 'C2 pt "ainda não, espera" depois do pedido'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: pode ser 19/11 às 11h', 19, 11, 11, true, 'C2 pt aceitar 19/11 às 11h continua valendo'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: não posso dia 18, mas 19/11 às 11h dá', 19, 11, 11, true, 'C2 pt negativa de OUTRO dia não atrapalha'],
  [ASS + ': Tenho quinta 19/11 às 11h.\nPaciente: não posso 24/11, pode ser 19/11 às 11h', 19, 11, 11, true, 'C2 pt negativa de outro dia, depois pede o certo'],
  [ASS + ': I have Thursday Nov 19 at 11am.\nPaciente: I can\'t do Nov 19 at 11am', 19, 11, 11, false, "C2 en \"I can't do Nov 19 at 11am\""],
  [ASS + ': I have Thursday Nov 19 at 11am.\nPaciente: don\'t book it yet', 19, 11, 11, false, "C2 en \"don't book it yet\""],
  [ASS + ': I have Thursday Nov 19 at 11am.\nPaciente: not yet, please wait', 19, 11, 11, false, 'C2 en "not yet, please wait"'],
  [ASS + ': I have Thursday Nov 19 at 11am.\nPaciente: Nov 19 at 11am works', 19, 11, 11, true, 'C2 en aceitar continua valendo'],
  [ASS + ': Tengo jueves 19/11 a las 11h.\nPaciente: no puedo el 19/11 a las 11h', 19, 11, 11, false, 'C2 es "no puedo el 19/11 a las 11h"'],
  [ASS + ': Tengo jueves 19/11 a las 11h.\nPaciente: no lo agende todavía', 19, 11, 11, false, 'C2 es "no lo agende todavía"'],
  [ASS + ': Tengo jueves 19/11 a las 11h.\nPaciente: aún no, espera', 19, 11, 11, false, 'C2 es "aún no, espera"'],
  [ASS + ': Tengo jueves 19/11 a las 11h.\nPaciente: sí, el 19/11 a las 11h', 19, 11, 11, true, 'C2 es aceitar continua valendo'],
  ['Paciente: pode ser 19.11 às 11h', 19, 11, 11, true, 'C2 pt "19.11" com ponto continua valendo'],
];
for (const [conv, dd, mm, hh, esperado, desc] of casosC2) tenta(desc, () => {
  const r = confere(conv, { day: String(dd).padStart(2, '0'), month: String(mm).padStart(2, '0'), hour: String(hh).padStart(2, '0') });
  t(desc, r.temHora === esperado, 'temData=' + r.temData + ' temHora=' + r.temHora);
});

// ---------- C3: urgência ----------
const iaR = { acao: 'responder', mensagem1: 'Entendo.' };
const casosC3 = [
  ['estou sangrando, o que faço?', iaR, 'humano', 'C3 pt urgência com "?" vira humano'],
  ['minha gengiva está sangrando muito, é normal?', iaR, 'humano', 'C3 pt relato com "?" vira humano'],
  ['estou com febre e dor forte', { acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!' }, 'humano', 'C3 urgência vale mesmo se a IA escolheu agendar'],
  ['tô com o rosto inchado, quero cancelar', { acao: 'cancelar', mensagem1: 'Cancelada.' }, 'humano', 'C3 urgência vale mesmo se a IA escolheu cancelar'],
  ['minha gengiva está sangrando muito', iaR, 'humano', 'C3 pt sem "?" continua urgente'],
  ['não estou com febre', iaR, 'responder', 'C3 negação pt "não estou com febre"'],
  ['não tenho dor forte nem inchaço', iaR, 'responder', 'C3 negação pt dupla'],
  ['sem febre e sem sangramento', iaR, 'responder', 'C3 negação pt "sem"'],
  ['não estou com febre mas estou sangrando', iaR, 'humano', 'C3 negação de um sintoma não esconde outro'],
  ['clareamento faz a gengiva sangrar?', iaR, 'responder', 'C3 dúvida geral sobre sangramento continua responder'],
  ['depois do implante é normal sangrar?', iaR, 'responder', 'C3 dúvida geral "é normal sangrar?" continua responder'],
  ['quero marcar uma avaliação', { acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!' }, 'agenda', 'C3 sem urgência a agenda segue normal'],
  // Pacote E (25/11, Codex item 1)
  ['não consigo engolir direito desde ontem', iaR, 'humano', 'E3 "não consigo engolir" vira humano'],
  ['estou com falta de ar e o rosto inchando', iaR, 'humano', 'E3 "falta de ar" vira humano'],
  ['tô com dificuldade pra respirar, é normal?', iaR, 'humano', 'E3 "dificuldade pra respirar" com "?" vira humano'],
  ['não consigo abrir a boca de tanta dor', iaR, 'humano', 'E3 "não consigo abrir a boca" vira humano'],
  ['dói pra engolir depois da extração?', iaR, 'responder', 'E3 dúvida geral "dói pra engolir depois da extração?" continua responder'],
  ['não estou com falta de ar', iaR, 'responder', 'E3 negação "não estou com falta de ar"'],
  ['o clareamento dói?', iaR, 'responder', 'E3 "dói?" sobre procedimento não é urgência'],
];
for (const [pend, ia, esperado, desc] of casosC3) tenta(desc, () => {
  const d = decidir({ ...ia }, { pendente: pend });
  const ok = esperado === 'agenda' ? d.rota !== 'humano' : d.rota === esperado;
  t(desc, ok, d.rota + ' / ' + d.mensagem1);
});
// Pacote E (26/11): resposta fixa sempre (25/11: a IA escreveu o próprio texto e prometeu encaixe com a Dra. fora).
const iaEncaixe = { acao: 'humano', mensagem1: 'Vou passar para a Dra. Suzana ver um encaixe ainda hoje.', motivo: 'Dificuldade para engolir' };
const casosE3 = [
  ['não consigo engolir direito desde ontem', iaEncaixe, 'urgencia_grave', 'E3 IA escolheu "humano" com encaixe: sai a frase fixa grave'],
  ['estou com falta de ar e o rosto inchando', { acao: 'responder', mensagem1: 'Vou ver um encaixe hoje.' }, 'urgencia_grave', 'E3 "falta de ar" com "responder": sai a frase fixa grave'],
  ['tô com dificuldade pra respirar, é normal?', iaEncaixe, 'urgencia_grave', 'E3 "dificuldade pra respirar?": sai a frase fixa grave'],
  ['minha gengiva está sangrando muito', { acao: 'responder', mensagem1: 'A Dra. te encaixa hoje.' }, 'urgencia', 'E3 sangramento: sai a frase fixa comum'],
];
for (const [pend, ia, chave, desc] of casosE3) tenta(desc, () => {
  const d = decidir({ ...ia }, { pendente: pend });
  const ok = d.rota === 'humano' && !/encaix/i.test(d.mensagem1) && !d.mensagem2 && !d.mensagem3
    && (chave === 'urgencia_grave' ? /192/.test(d.mensagem1) : (!/192/.test(d.mensagem1) && /equipe/.test(d.mensagem1)))
    && /^Paciente relatou possível urgência/.test(d.motivo);
  t(desc, ok, d.rota + ' / ' + d.mensagem1 + ' / ' + d.motivo);
});
tenta('E3 aviso URGENTE quando a IA já escolheu "humano"', () => {
  const r = resultado('humano', iaEncaixe, { pendente: 'não consigo engolir direito desde ontem' });
  const av = avisos(r);
  t('E3 aviso URGENTE quando a IA já escolheu "humano"', av.length === 1 && /URGENTE/.test(av[0]) && !/encaix/i.test(r.texto), av);
});
tenta('C3 resultado "humano" por urgência traz a marca URGENTE', () => {
  const r = resultado('humano', iaR, { pendente: 'estou sangrando, o que faço?' });
  t('C3 aviso URGENTE para a equipe quando a paciente pergunta', avisos(r).length === 1 && /URGENTE/.test(avisos(r)[0]), avisos(r));
});
tenta('C3 resposta fixa quando a IA ia marcar', () => {
  const d = decidir({ acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!' }, { pendente: 'estou com febre e dor forte' });
  t('C3 a mensagem "Marcado!" é trocada pelo aviso de que a equipe foi chamada', !/Marcado/.test(d.mensagem1) && /equipe/.test(d.mensagem1), d.mensagem1);
});

// ---------- C4: pausa relida antes de cada envio ----------
tenta('C4', () => {
  const lerPausa = nosE['Ler a pausa agora'], pausada = nosE['Paciente pausada?'];
  t('C4 o envio relê a pausa (pausado_ate) antes de cada mensagem', !!lerPausa && /pausado_ate/.test(lerPausa.parameters.query) && /FROM pacientes/.test(lerPausa.parameters.query), lerPausa ? 'ok' : 'nó não existe');
  const c = envio.connections;
  const dest = (a, o) => ((c[a] || {}).main || [])[o] ? c[a].main[o].map(x => x.node) : [];
  t('C4 "Uma por vez" (cada mensagem) passa pela leitura da pausa', dest('Uma por vez', 1).includes('Ler a pausa agora'), JSON.stringify(dest('Uma por vez', 1)));
  t('C4 pausada: descarta e volta para a próxima mensagem', dest('Paciente pausada?', 0).includes('Uma por vez'), JSON.stringify(dest('Paciente pausada?', 0)));
  t('C4 não pausada: segue para o envio (ou saída de teste)', dest('Paciente pausada?', 1).includes('Modo teste ligado?'), JSON.stringify(dest('Paciente pausada?', 1)));
  const q = lerPausa.parameters.query;
  t('C4 a leitura devolve os campos que o envio usa (to, body, typing_time, espera, teste)', /AS "to"/.test(q) && /AS body/.test(q) && /AS typing_time/.test(q) && /AS espera/.test(q) && /AS teste/.test(q));
  t('C4 avisos para a equipe seguem: só some quem está pausado na tabela de pacientes', /coalesce\(\(SELECT pausado_ate > now\(\)/.test(q) && /, false\) AS pausada/.test(q));
});

// ---------- C5: aviso de falha sem texto livre ----------
tenta('C5', () => {
  const n = nosE['Avisar a Keshion da falha'];
  const corpo = n ? n.parameters.jsonBody : '';
  t('C5 aviso de falha não usa error.message', n && !/error\.message/.test(corpo) && !/\.message/.test(corpo), n ? 'ok' : 'nó não existe');
  t('C5 aviso de falha traz código do erro e ID da execução', /\$execution\.id/.test(corpo) && /httpCode/.test(corpo), corpo.slice(0, 80));
  t('C5 aviso de falha não traz o final do telefone da paciente', !/slice\(-4\)/.test(corpo));
});

// ---------- C6: nome do áudio ----------
function audio(b) {
  const out = rodar('Ajustar o nome do áudio', {}, {});   // só para checar que o nó existe
  const fn = new Function('$input', nos['Ajustar o nome do áudio'].parameters.jsCode);
  return fn({ all: () => [{ binary: { data: { ...b } } }] })[0].binary.data;
}
const casosC6 = [
  [{ fileName: 'audio', fileExtension: 'wav', mimeType: 'audio/wav' }, 'audio.wav', 'audio/wav', 'C6 WAV sem ponto no nome mantém o tipo WAV'],
  [{ fileName: 'audio.wav', fileExtension: 'wav', mimeType: 'audio/wav' }, 'audio.wav', 'audio/wav', 'C6 WAV com nome certo fica igual'],
  [{ fileName: 'voz.oga', fileExtension: 'oga', mimeType: 'audio/ogg' }, 'voz.ogg', 'audio/ogg', 'C6 .oga vira .ogg'],
  [{ fileName: 'voz.opus', fileExtension: 'opus', mimeType: 'audio/opus' }, 'voz.ogg', 'audio/ogg', 'C6 .opus vira .ogg'],
  [{ fileName: 'audio', fileExtension: '', mimeType: '' }, 'audio.ogg', 'audio/ogg', 'C6 sem extensão nenhuma vira .ogg'],
  [{ fileName: 'audio', mimeType: 'audio/ogg; codecs=opus' }, 'audio.ogg', 'audio/ogg; codecs=opus', 'C6 Ogg sem extensão pelo tipo vira .ogg'],
  [{ fileName: 'nota.mp3', fileExtension: 'mp3', mimeType: 'audio/mpeg' }, 'nota.mp3', 'audio/mpeg', 'C6 MP3 fica igual'],
  [{ fileName: 'nota', fileExtension: 'mp3', mimeType: 'audio/mpeg' }, 'nota.mp3', 'audio/mpeg', 'C6 MP3 sem ponto no nome ganha .mp3'],
  [{ fileName: 'audio.m4a', fileExtension: 'm4a', mimeType: 'audio/mp4' }, 'audio.m4a', 'audio/mp4', 'C6 M4A fica igual'],
];
for (const [b, nome, mime, desc] of casosC6) tenta(desc, () => {
  const r = audio(b);
  t(desc, r.fileName === nome && r.mimeType === mime, r.fileName + ' / ' + r.mimeType);
});

let falhas = 0;
for (const x of T) if (!x.ok) { falhas++; console.log('FALHOU  ' + x.desc + (x.info !== undefined ? '  ' + (typeof x.info === 'string' ? x.info : JSON.stringify(x.info)) : '')); }
console.log((T.length - falhas) + ' de ' + T.length + ' testes do Pacote C certos (' + caminhoAt.replace(/.*[\\/]/, '') + ')' + (falhas ? ', ' + falhas + ' falharam' : ''));
process.exit(falhas ? 1 : 0);
