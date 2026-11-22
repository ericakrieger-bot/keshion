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
  [PERG_CANC, 'sim, mas quanto custa a limpeza?', 'responder', 'C1 "sim" com pergunta no meio não cancela'],
  [PERG_CANC, 'sim. aliás, vocês atendem sábado', 'responder', 'C1 "sim" com outro assunto não cancela'],
  [PERG_CANC, 'sim', 'cancelar', 'C1 "sim" simples depois de pergunta de cancelar cancela'],
  [PERG_CANC, 'Sim, pode cancelar por favor', 'cancelar', 'C1 "Sim, pode cancelar por favor" cancela'],
  [PERG_CANC, 'isso mesmo', 'cancelar', 'C1 "isso mesmo" cancela'],
  ['Just to confirm: you would like to cancel your evaluation on Thursday, Nov 19, at 11:00, correct?', 'Yes, please cancel it', 'cancelar', 'C1 en "Yes, please cancel it" cancela'],
  ['Just to confirm: you would like to cancel your evaluation on Thursday, Nov 19, at 11:00, correct?', "yes that's right", 'cancelar', "C1 en \"yes that's right\" cancela"],
  ['Solo para confirmar: ¿quieres cancelar tu evaluación del jueves 19 de noviembre a las 11:00, correcto?', 'Sí, cancélala', 'cancelar', 'C1 es "Sí, cancélala" cancela'],
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
  ['sim, e o endereço?', 'sim, mas qual o endereço?', 'responder', 'C1b 2ª rodada: "sim" com pergunta continua sem cancelar'],
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
  ['I am bleeding, what should I do?', iaR, 'humano', 'C3 en urgência com "?"'],
  ['mi cara está hinchada, ¿qué hago?', iaR, 'humano', 'C3 es urgência com "?"'],
  ['tengo mucho dolor, ¿qué puedo hacer?', iaR, 'humano', 'C3 es "tengo mucho dolor ¿?"'],
  ['estou com febre e dor forte', { acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!' }, 'humano', 'C3 urgência vale mesmo se a IA escolheu agendar'],
  ['tô com o rosto inchado, quero cancelar', { acao: 'cancelar', mensagem1: 'Cancelada.' }, 'humano', 'C3 urgência vale mesmo se a IA escolheu cancelar'],
  ['minha gengiva está sangrando muito', iaR, 'humano', 'C3 pt sem "?" continua urgente'],
  ['não estou com febre', iaR, 'responder', 'C3 negação pt "não estou com febre"'],
  ['não tenho dor forte nem inchaço', iaR, 'responder', 'C3 negação pt dupla'],
  ['sem febre e sem sangramento', iaR, 'responder', 'C3 negação pt "sem"'],
  ['no tengo fiebre', iaR, 'responder', 'C3 negação es "no tengo fiebre"'],
  ['no he tenido hinchazón', iaR, 'responder', 'C3 negação es "no he tenido"'],
  ["I don't have a fever", iaR, 'responder', "C3 negação en \"I don't have a fever\""],
  ['I do not have any swelling', iaR, 'responder', 'C3 negação en "I do not have any swelling"'],
  ['não estou com febre mas estou sangrando', iaR, 'humano', 'C3 negação de um sintoma não esconde outro'],
  ['clareamento faz a gengiva sangrar?', iaR, 'responder', 'C3 dúvida geral sobre sangramento continua responder'],
  ['depois do implante é normal sangrar?', iaR, 'responder', 'C3 dúvida geral "é normal sangrar?" continua responder'],
  ['quero marcar uma avaliação', { acao: 'agendar', inicio: '2026-11-19T11:00:00-03:00', mensagem1: 'Marcado!' }, 'agenda', 'C3 sem urgência a agenda segue normal'],
];
for (const [pend, ia, esperado, desc] of casosC3) tenta(desc, () => {
  const d = decidir({ ...ia }, { pendente: pend });
  const ok = esperado === 'agenda' ? d.rota !== 'humano' : d.rota === esperado;
  t(desc, ok, d.rota + ' / ' + d.mensagem1);
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
