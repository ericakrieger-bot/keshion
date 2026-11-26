// Teste local do Jev em modo sombra (25/11/2026). Sem servidor, sem WhatsApp, sem banco.
// Uso (dentro de tecnico/n8n):
//   python gerar_fluxos.py clinica-demo && python gerar_fluxos.py clinica-demo --jev-teste && python gerar_fluxos.py clinica-demo --sem-jev
//   node teste_jev_sombra.js            (só local, sem custo)
// (26/11: a demo já tem a credencial typesafe, então a comparação "sem Jev" usa gerados/clinica-demo-sem-jev/.)
//   node teste_jev_sombra.js --real     (também 2 chamadas de verdade ao Jev com conversa inventada; chave lida do .env, nunca impressa)
const fs = require('fs');
const path = require('path');
const ler = p => JSON.parse(fs.readFileSync(path.join(__dirname, p), 'utf8'));
const comJev = ler('gerados/clinica-demo-jev-teste/atendimento.json');
const semJev = ler('gerados/clinica-demo-sem-jev/atendimento.json');
const fluxoReal = ler('gerados/clinica-demo/atendimento.json');   // o que vai ser publicado
const nos = Object.fromEntries(comJev.nodes.map(n => [n.name, n]));
const ASS = comJev.name.split(' · ')[0];
const T = [];
const t = (desc, ok, info) => T.push({ desc, ok: !!ok, info });
const tenta = (desc, fn) => { try { fn(); } catch (e) { t(desc, false, 'erro: ' + e.message); } };

function rodar(nome, entrada, refs, quebrar) {
  const $ = n => { if (quebrar) throw new Error('falha simulada'); return { first: () => ({ json: refs[n] || {} }) }; };
  return new Function('$input', '$', nos[nome].parameters.jsCode)({ first: () => ({ json: entrada }), all: () => [{ json: entrada }] }, $)[0].json;
}
const FICHA = 'Ler ficha e instruções (só a última responde)';
const MONTAR = 'Jev: montar a pergunta (sombra)';
const ANOTAR = 'Jev: anotar a resposta (sombra)';
const montar = (ficha, decidir, quebrar) => rodar(MONTAR, decidir || { rota: 'responder', acao: 'responder', motivo: '' },
  { [FICHA]: { telefone: '554199900990', ultimo_id: 'id1', conversa: '', pendente: '', ...ficha } }, quebrar);
const anotar = (m, resp) => rodar(ANOTAR, resp, { [MONTAR]: m }).linha;

// ---------- estrutura ----------
const JEV = ['Jev: montar a pergunta (sombra)', 'Jev: chamar? (sombra)', 'Jev: perguntar (sombra)', 'Jev: anotar a resposta (sombra)', 'Jev: gravar (sombra)'];
t('sem a credencial typesafe o fluxo sai igual ao de hoje (nenhum nó do Jev)', !semJev.nodes.some(n => /Jev/.test(n.name)));
t('com a credencial, os 5 nós do Jev existem', JEV.every(n => nos[n]));
t('nenhum nó do Jev pode parar o fluxo (onError = continuar), menos o "se"',
  JEV.filter(n => !/chamar\?/.test(n)).every(n => nos[n].onError === 'continueRegularOutput'));
const h = nos['Jev: perguntar (sombra)'];
t('HTTP: POST na URL do Jev, limite de 3 s, credencial TypeSafe', h.parameters.method === 'POST' && h.parameters.url === 'https://api.typesafe.ai/v1/systemone'
  && h.parameters.options.timeout === 3000 && h.credentials && h.credentials.httpHeaderAuth && !h.retryOnFail);
t('modelo fixo jev-1.14.0 (nunca jev-latest)', /'jev-1\.14\.0'/.test(nos[MONTAR].parameters.jsCode) && !/jev-latest/.test(JSON.stringify(comJev)));
const yMax = Math.max(...comJev.nodes.filter(n => !/Jev/.test(n.name)).map(n => n.position[1]));
t('caminho do Jev fica abaixo de todos os outros nós (roda depois da resposta ao paciente)', JEV.every(n => nos[n].position[1] > yMax), 'yMax=' + yMax);
const saidasDecidir = comJev.connections['Decidir a ação'].main[0].map(c => c.node);
t('"Decidir a ação" continua indo para "Qual ação?" e ganha só o ramo do Jev', saidasDecidir.length === 2 && saidasDecidir.includes('Qual ação?') && saidasDecidir.includes(MONTAR));
// (os "se" ganham um id aleatório a cada geração: esse campo fica fora da comparação)
const limpo = ns => JSON.stringify(ns).replace(/"id":"[0-9a-f-]{36}","leftValue"/g, '"leftValue"');
t('fora do Jev, os nós são idênticos aos do fluxo sem Jev', limpo(comJev.nodes.filter(n => !/Jev/.test(n.name))) === limpo(semJev.nodes));
// 26/11: o fluxo real da demo (credencial de verdade) é o mesmo do teste, só muda a credencial do HTTP do Jev.
const semCred = ns => limpo(ns.map(n => ({ ...n, credentials: /Jev/.test(n.name) ? undefined : n.credentials })));
t('o fluxo real da demo tem o Jev e é igual ao do teste (menos a credencial)', fluxoReal.nodes.some(n => /Jev/.test(n.name)) && semCred(fluxoReal.nodes) === semCred(comJev.nodes));
t('o fluxo real usa a credencial typesafejev00001', fluxoReal.nodes.some(n => n.name === 'Jev: perguntar (sombra)' && n.credentials.httpHeaderAuth.id === 'typesafejev00001'));
// Colunas do INSERT batem com a tabela (jev-sombra.sql)
const sql = fs.readFileSync(path.join(__dirname, 'jev-sombra.sql'), 'utf8');
const colsTabela = [...sql.matchAll(/^\s{2}([a-z_]+)\s+(?:bigserial|timestamptz|text|boolean|int|numeric|real|jsonb)/gm)].map(m => m[1]).filter(c => !['id', 'criado_em'].includes(c));
const ins = nos['Jev: gravar (sombra)'].parameters.query.match(/INSERT INTO jev_sombra \(([^)]+)\)/)[1].split(',').map(s => s.trim());
t('colunas do INSERT = colunas da tabela', JSON.stringify(ins.slice().sort()) === JSON.stringify(colsTabela.slice().sort()), ins.length + ' x ' + colsTabela.length);
t('gravar recebe um parâmetro só (JSON), sem vírgulas soltas', nos['Jev: gravar (sombra)'].parameters.options.queryReplacement === '={{ [ JSON.stringify($json.linha) ] }}');

// ---------- montar ----------
const PERG = 'Só para confirmar: você quer cancelar a sua avaliação de 19/11 às 11:00, certo?';
const conv = n => Array.from({ length: n }, (_, i) => (i % 2 ? ASS + ': resposta ' + i : 'Paciente: pergunta ' + i)).join('\n');
tenta('montar: mensagem comum', () => {
  const m = montar({ conversa: conv(30) + '\n--- 25/11/2026 (outro dia) ---\nDoutora (pelo celular): oi', pendente: 'quanto custa a limpeza?' });
  const q = Object.keys(m.corpo.questions);
  t('montar: chama o Jev com urgência, dor e fora da lista (sem cancelar)', m.chamar && q.join() === 'urg,dor,fora' && !m.gate, q.join());
  t('montar: só as últimas 12 falas, sem a linha "outro dia"', m.corpo.state.conversa_recente.length === 12
    && !m.corpo.state.conversa_recente.some(x => /outro dia/.test(x.texto)) && m.corpo.state.conversa_recente[11].quem === 'Dentista da clínica');
  t('montar: guarda a regra de hoje', m.regra.rota === 'responder' && m.regra.urgencia === false && m.regra.cancelou === false);
});
tenta('montar: depois da pergunta de cancelar', () => {
  const m = montar({ avaliacao_evento: 'ev1', conversa: 'Paciente: quero cancelar\n' + ASS + ': ' + PERG, pendente: 'sim, pode cancelar' },
    { rota: 'cancelar', acao: 'cancelar' });
  t('montar: com a pergunta de cancelar, inclui confirmação, espera e pede_cancelar', m.gate && ['conf', 'espera', 'pede_cancelar'].every(k => m.corpo.questions[k]));
  t('montar: última fala da Clara vai no state', m.corpo.state.ultima_fala_da_clara === PERG && m.regra.cancelou === true);
});
tenta('montar: sem avaliação marcada, pergunta com "cancel" não liga o cancelar', () => {
  const m = montar({ conversa: 'Paciente: oi\n' + ASS + ': ' + PERG, pendente: 'sim' });
  t('montar: sem avaliação marcada, não pergunta do cancelar', m.chamar && !m.gate);
});
tenta('montar: fala da Clara sem pergunta de cancelar', () => {
  const m = montar({ avaliacao_evento: 'ev1', conversa: 'Paciente: oi\n' + ASS + ': Posso usar este número?', pendente: 'sim' });
  t('montar: "sim" para outra pergunta não liga o cancelar', !m.gate);
});
tenta('montar: pergunta da IA sem "cancelar", com a pendência na ficha', () => {
  const m = montar({ avaliacao_evento: 'ev1', cancelar_evento: 'ev1', conversa: 'Paciente: quero cancelar\n' + ASS + ': A sua avaliação é a de 01/12 às 9h, certo?', pendente: 'Valeu!' });
  t('montar: com a pendência na ficha, a pergunta sem "cancelar" liga o cancelar (26/11)', m.gate);
});
tenta('montar: urgência pela regra de hoje', () => {
  t('montar: regra de hoje marca urgência em "estou sangrando"', montar({ pendente: 'estou sangrando muito' }).regra.urgencia === true);
});
tenta('montar: sem mensagem', () => t('montar: sem mensagem pendente, não chama', montar({ pendente: '   ' }).chamar === false));
tenta('montar: erro interno', () => {
  const m = montar({ pendente: 'oi' }, null, true);
  t('montar: erro interno vira "não chamar", sem quebrar', m.chamar === false && /falha simulada/.test(m.erro));
});
const se = nos['Jev: chamar? (sombra)'].parameters.conditions.conditions[0];
t('"chamar?" olha o campo chamar (true)', se.leftValue === '={{ $json.chamar }}' && se.operator.operation === 'true');

// ---------- anotar ----------
const mBase = montar({ pendente: 'estou com muita dor' });
const mCanc = msg => montar({ avaliacao_evento: 'ev1', conversa: 'Paciente: quero cancelar\n' + ASS + ': ' + PERG, pendente: msg }, { rota: 'responder', acao: 'responder' });
const resp = (o = {}) => ({ model: 'jev-1.14.0', usage: { input_tokens: 1761, output_tokens: 20 }, answers: {
  urg: { type: 'noul', noul: o.urg ?? 0.85 }, fora: { type: 'noul', noul: o.fora ?? 0.02 },
  dor: { type: 'choice', choice: o.dor || 'relato_de_dor', probabilities: { relato_de_dor: 0.03, pergunta_sobre_o_procedimento: 0.02, outro: 0.01, [o.dor || 'relato_de_dor']: o.dorP ?? 0.95 }, confidence: 0.9 },
  ...(o.canc ? { conf: { type: 'choice', choice: 'sim_claro', probabilities: { sim_claro: o.canc[0], nao: 0, duvida: 0, outro_assunto: 0 } },
    espera: { type: 'noul', noul: o.canc[1] }, pede_cancelar: { type: 'noul', noul: o.canc[2] } } : {}) } });
tenta('anotar: resposta boa', () => {
  const L = anotar(mBase, resp());
  t('anotar: resposta boa fica ok, com custo e decisões', L.ok && L.erro === null && L.decide_urgencia === true && L.decide_dor === 'relato'
    && L.decide_fora === 'nao' && L.decide_cancelar === null && Math.abs(L.custo_usd - 1761 * 0.042 / 1e6) < 1e-12 && L.modelo === 'jev-1.14.0', JSON.stringify(L).slice(0, 200));
  t('anotar: urgência com 0,3 já avisa; 0,29 não', anotar(mBase, resp({ urg: 0.3 })).decide_urgencia === true && anotar(mBase, resp({ urg: 0.29 })).decide_urgencia === false);
  t('anotar: "dói?" só vira pergunta com 0,67 ou mais', anotar(mBase, resp({ dor: 'pergunta_sobre_o_procedimento', dorP: 0.7 })).decide_dor === 'pergunta'
    && anotar(mBase, resp({ dor: 'pergunta_sobre_o_procedimento', dorP: 0.55 })).decide_dor === 'relato');
  t('anotar: fora da lista 0,7 = não fazemos; 0,5 = equipe', anotar(mBase, resp({ fora: 0.94 })).decide_fora === 'nao_fazemos' && anotar(mBase, resp({ fora: 0.5 })).decide_fora === 'equipe');
});
tenta('anotar: cancelar pela regra mista', () => {
  t('cancelar: "sim, pode cancelar" (1,00 / 0,01 / 0,99) cancela', anotar(mCanc('sim, pode cancelar'), resp({ canc: [1, 0.01, 0.99] })).decide_cancelar === 'cancela');
  t('cancelar: "sim, mas quanto custa a limpeza?" (1,00 / 0,05 / 0,2) pergunta de novo', anotar(mCanc('sim, mas quanto custa a limpeza?'), resp({ canc: [1, 0.05, 0.2] })).decide_cancelar === 'pergunta_de_novo');
  t('cancelar: "sim, mas não cancela ainda" (0,56 / 0,97 / 0,1) pergunta de novo', anotar(mCanc('sim, mas não cancela ainda'), resp({ canc: [0.56, 0.97, 0.1] })).decide_cancelar === 'pergunta_de_novo');
  t('cancelar: "sim, cancela, mas a lente estraga?" (1,00 / 0,02 / 0,9) cancela', anotar(mCanc('sim, cancela, mas a lente estraga o dente?'), resp({ canc: [1, 0.02, 0.9] })).decide_cancelar === 'cancela');
  t('cancelar: sim 0,92 não cancela', anotar(mCanc('isso'), resp({ canc: [0.92, 0.01, 0.9] })).decide_cancelar === 'pergunta_de_novo');
  t('cancelar: pergunta de cancelar sem as respostas de cancelar = estranha (ok false)', anotar(mCanc('sim'), resp()).ok === false);
});
// Queda do Jev: nada disso pode quebrar nem virar "não"
const quedas = [
  ['erro HTTP 500', { error: { message: '500 - Internal Server Error' } }],
  ['tempo esgotado', { error: { message: 'timeout of 3000ms exceeded', code: 'ECONNABORTED' } }],
  ['chave inválida (sem vazar a chave)', { error: { message: 'Authorization failed: Bearer ts_live_abc123 invalid' } }],
  ['resposta vazia', {}],
  ['resposta em texto', { data: '<html>erro</html>' }],
  ['probabilidade fora de 0 a 1', resp({ urg: 7 })],
  ['escolha desconhecida', resp({ dor: 'talvez' })]
];
for (const [nome, r] of quedas) tenta('queda: ' + nome, () => {
  const L = anotar(mBase, r);
  t('queda do Jev (' + nome + '): ok false, motivo gravado, nenhuma decisão do Jev', L.ok === false && !!L.erro
    && L.decide_urgencia === null && L.decide_cancelar === null && L.regra_urgencia === mBase.regra.urgencia && L.regra_rota === 'responder' && !/abc123/.test(JSON.stringify(L)), L.erro);
});
tenta('queda: demorou', () => {
  const L = anotar({ ...mBase, inicio: Date.now() - 4000 }, resp());
  t('queda do Jev (passou de 3 s): ok false', L.ok === false && /3000/.test(L.erro) && L.ms >= 4000);
});
tenta('queda: entrada sem nada', () => {
  const L = rodar(ANOTAR, null, { [MONTAR]: {} }).linha;
  t('anotar com tudo vazio não quebra', L.ok === false);
});

async function real() {
  const env = fs.readFileSync(path.join(__dirname, '..', '..', '.env'), 'utf8');
  const k = (env.match(/^TYPESAFE_API_KEY=(.*)$/m) || [])[1];
  if (!k) { t('chamada real: TYPESAFE_API_KEY no .env', false); return; }
  const chave = k.trim().replace(/^["']|["']$/g, '');
  for (const [desc, m, espera] of [
    ['urgência', montar({ conversa: 'Paciente: oi\n' + ASS + ': Oi! Como posso ajudar?', pendente: 'não consigo engolir direito, a garganta está fechando' }), L => L.decide_urgencia === true],
    ['cancelar', mCanc('Isso, pode cancelar sim. Valeu!'), L => L.decide_cancelar === 'cancela']]) {
    const t0 = Date.now();
    const r = await fetch('https://api.typesafe.ai/v1/systemone', { method: 'POST', headers: { Authorization: 'Bearer ' + chave, 'Content-Type': 'application/json' },
      body: JSON.stringify(m.corpo), signal: AbortSignal.timeout(3000) }).then(x => x.json()).catch(e => ({ error: { message: String(e.message) } }));
    const L = anotar({ ...m, inicio: t0 }, r);
    t('chamada real (' + desc + '): ok, modelo 1.14.0 e decisão esperada', L.ok && /1\.14/.test(L.modelo || '') && espera(L),
      `ms=${L.ms} modelo=${L.modelo} erro=${L.erro} urg=${L.jev_urgencia} sim=${L.jev_conf_sim} custo=${L.custo_usd}`);
  }
}

(async () => {
  if (process.argv.includes('--real')) await real();
  for (const x of T) console.log((x.ok ? 'ok   ' : 'FALHA') + ' ' + x.desc + (x.ok || !x.info ? '' : '  -> ' + x.info));
  const certos = T.filter(x => x.ok).length;
  console.log(`\n${certos} de ${T.length} testes do Jev em modo sombra certos`);
  process.exit(certos === T.length ? 0 : 1);
})();
