# Jev (TypeSafe) em MODO SOMBRA no fluxo de atendimento (plano: PLANO-JEV-SOMBRA.md, aprovado pela Erica em 25/11/2026).
# O Jev só dá a opinião e o fluxo grava na tabela jev_sombra (SQL em jev-sombra.sql). Quem decide continua sendo a regra de hoje.
# Os nós ficam num caminho lateral que sai de "Decidir a ação" e fica BEM ABAIXO no desenho: no n8n (ordem de execução v1)
# o caminho de baixo só roda depois que o de cima (a resposta ao paciente) terminou. Falha, erro ou demora do Jev só vira
# uma linha com ok = false; nenhum desses nós pode parar o fluxo (todos com onError = continuar).
# Perguntas e limiares: tecnico/jev-bancada/jev_bancada.py e RESULTADO.md (cópia fixa aqui, de propósito: mudar lá não muda o fluxo).
import json

MODELO = "jev-1.14.0"          # versão fixa; trocar só depois de repetir a bancada
LIMITE_MS = 3000               # passou disso: conta como falha (o HTTP corta em 3 s)
PRECO_ENTRADA_POR_MILHAO = 0.042
Y = 1400                       # bem abaixo de tudo: roda por último

URG = {
    "type": "noul",
    "instructions": "Na `mensagem_do_paciente`, o paciente relata que AGORA está com dificuldade para respirar, "
                    "dificuldade para engolir, sangramento, inchaço no rosto ou na boca com febre, ou dor muito forte?",
    "criteria": {
        "true": "O paciente diz que está sentindo isso neste momento (por exemplo: \"estou sangrando\", "
                "\"não consigo engolir\", \"meu rosto está inchado e estou com febre\", \"a dor está insuportável\").",
        "false": "O paciente só pergunta se algo é comum ou se um procedimento causa isso, fala de algo que passou, "
                 "diz que NÃO tem o sintoma, ou trata de outro assunto (preço, horário, cancelar)."}}
DOR = {
    "type": "choice",
    "instructions": "A `mensagem_do_paciente` relata uma dor que o paciente sente agora, ou pergunta se um procedimento dói?",
    "criteria": {
        "relato_de_dor": "O paciente diz que está com dor ou sensibilidade agora ou há pouco (\"estou com dor\", \"está doendo\", \"não consigo comer de tanta dor\").",
        "pergunta_sobre_o_procedimento": "O paciente pergunta se um tratamento ou procedimento dói ou incomoda, sem dizer que sente dor agora (\"dói?\", \"a limpeza dói?\", \"e se ela falar que dói muito?\").",
        "outro": "A mensagem não fala de dor."}}
FORA = {
    "type": "noul",
    "instructions": "A `mensagem_do_paciente` pede ou pergunta sobre algo que a clínica não faz: implante, dentadura ou prótese removível, ou coroa sobre implante?",
    "criteria": {
        "true": "O paciente quer saber preço, prazo ou se fazem implante, dentadura/prótese total ou coroa sobre implante.",
        "false": "O paciente fala de outro assunto (limpeza, clareamento, lentes, alinhador, restauração, canal, extração, preço de outro serviço, horário)."}}
CONF = {
    "type": "choice",
    "instructions": "Considerando `ultima_fala_da_clara`, a `mensagem_do_paciente` responde com um sim claro, um não, uma dúvida ou fala de outro assunto?",
    "criteria": {
        "sim_claro": "O paciente concorda de forma direta com o que a Clara perguntou (\"sim\", \"isso mesmo\", \"pode cancelar\", \"sim, pode cancelar, mas antes me responde X\"). Perguntas extras do paciente não tiram o sim, desde que ele confirme o que foi perguntado.",
        "nao": "O paciente recusa ou corrige o que a Clara perguntou (\"não\", \"quero manter\", \"não é a minha, é da minha filha\").",
        "duvida": "O paciente não decide: está inseguro, pede para esperar ou responde com outra pergunta no lugar da resposta (\"sim?\", \"não sei\", \"espera\").",
        "outro_assunto": "O paciente não responde ao que a Clara perguntou e fala de outra coisa (preço, endereço, sintoma)."}}
ESPERA = {
    "type": "noul",
    "instructions": "O paciente pede para esperar, para não cancelar ainda, ou quer manter a avaliação?",
    "criteria": {"true": "O paciente diz \"não cancela ainda\", \"espera\", \"quero manter\" ou deixa a decisão para depois.",
                 "false": "O paciente não pede para esperar nem para manter."}}
PEDE = {
    "type": "noul",
    "instructions": "O paciente pede de forma explícita para cancelar a avaliação (por exemplo \"pode cancelar\", \"cancela\")?",
    "criteria": {"true": "A mensagem diz com palavras próprias que quer cancelar ou manda cancelar.",
                 "false": "A mensagem só diz \"sim\" ou \"isso\" e depois fala de outro assunto, ou não pede para cancelar."}}

PERGUNTAS = {"urg": URG, "dor": DOR, "fora": FORA}
PERGUNTAS_CANCELAR = {"conf": CONF, "espera": ESPERA, "pede_cancelar": PEDE}

MONTAR_JS = r"""
// Modo sombra: nada aqui muda a resposta ao paciente. Qualquer erro vira "não chamar" e o caminho termina.
try {
  const f = $('Ler ficha e instruções (só a última responde)').first().json;
  const d = $input.first().json || {};   // o que "Decidir a ação" decidiu (regra de hoje)
  const pend = String(f.pendente || '').trim();
  if (!pend) return [{ json: { chamar: false } }];
  const falas = [];
  for (const l of String(f.conversa || '').split('\n')) {
    if (/^--- .* ---$/.test(l.trim())) continue;
    const m = l.match(/^(Paciente|__ASSISTENTE__|Doutora \(pelo celular\)): ?(.*)$/);
    if (m) falas.push({ quem: m[1], texto: m[2] });
    else if (falas.length && l.trim()) falas[falas.length - 1].texto += ' ' + l.trim();
  }
  const NOMES = { 'Paciente': 'Paciente', '__ASSISTENTE__': '__ASSISTENTE__ (atendente virtual da clínica)', 'Doutora (pelo celular)': 'Dentista da clínica' };
  const daClara = falas.filter(x => x.quem === '__ASSISTENTE__');
  const ultima = daClara.length ? daClara[daClara.length - 1].texto : '';
  // Só pergunta do cancelar quando o CÓDIGO sabe que a última fala da assistente foi a pergunta de cancelar esta avaliação
  // (na bancada, sem esse filtro, o Jev dava "sim claro" alto em falas que nada tinham a ver com cancelar).
  // 26/11: vale também a pendência gravada na ficha (a pergunta da IA "é a de 01/12, certo?" não tem a palavra "cancelar").
  const gate = !!f.avaliacao_evento && ultima.includes('?')
    && (/cancel/.test(norm(ultima)) || (!!f.cancelar_evento && f.cancelar_evento === f.avaliacao_evento));
  const state = {
    conversa_recente: falas.slice(-12).map(x => ({ quem: NOMES[x.quem], texto: x.texto.slice(0, 1000) })),
    ultima_fala_da_clara: ultima ? ultima.slice(0, 1000) : '(a __ASSISTENTE__ ainda não falou)',
    mensagem_do_paciente: pend.slice(0, 2000)
  };
  const questions = Object.assign({}, __PERGUNTAS__, gate ? __PERGUNTAS_CANCELAR__ : {});
  return [{ json: {
    chamar: true, inicio: Date.now(), gate, telefone: f.telefone, msg_id: f.ultimo_id || '', mensagem: pend.slice(0, 2000),
    corpo: { model: '__MODELO__', state, questions },
    regra: { urgencia: ehUrgente(pend), rota: String(d.rota || ''), acao: String(d.acao || ''), cancelou: d.rota === 'cancelar',
             motivo: String(d.motivo || '').slice(0, 300) }
  } }];
} catch (e) {
  return [{ json: { chamar: false, erro: String(e && e.message || e).slice(0, 200) } }];
}
"""

ANOTAR_JS = r"""
// Lê a resposta do Jev e calcula o que ELE decidiria (limiares da bancada, RESULTADO.md). Só para gravar e comparar.
const m = $('Jev: montar a pergunta (sombra)').first().json;
const r = $input.first().json || {};
const ms = Math.max(0, Date.now() - Number(m.inicio || Date.now()));
const L = { telefone: m.telefone, msg_id: m.msg_id, mensagem: m.mensagem, perguntou_cancelar: !!m.gate,
  regra_urgencia: !!(m.regra && m.regra.urgencia), regra_rota: m.regra && m.regra.rota, regra_acao: m.regra && m.regra.acao,
  regra_cancelou: !!(m.regra && m.regra.cancelou), regra_motivo: m.regra && m.regra.motivo,
  ok: false, erro: null, ms, modelo: null, tokens: null, custo_usd: null,
  jev_urgencia: null, jev_dor: null, jev_dor_p: null, jev_fora: null, jev_conf: null, jev_conf_sim: null, jev_espera: null, jev_pede_cancelar: null,
  decide_urgencia: null, decide_dor: null, decide_fora: null, decide_cancelar: null, resposta: null };
try {
  if (r.error) throw new Error('erro na chamada: ' + String(r.error.message || r.error.description || r.error.code || JSON.stringify(r.error)));
  const a = r.answers;
  if (!a || typeof a !== 'object') throw new Error('resposta sem answers');
  const p = x => (typeof x === 'number' && x >= 0 && x <= 1) ? x : null;
  const urg = p(a.urg && a.urg.noul), fora = p(a.fora && a.fora.noul);
  const dor = a.dor && a.dor.choice, dorP = p(a.dor && a.dor.probabilities && a.dor.probabilities[dor]);
  if (urg === null || fora === null || !['relato_de_dor', 'pergunta_sobre_o_procedimento', 'outro'].includes(dor) || dorP === null)
    throw new Error('resposta estranha');
  Object.assign(L, { jev_urgencia: urg, jev_dor: dor, jev_dor_p: dorP, jev_fora: fora, modelo: String(r.model || '').slice(0, 40) || null,
    resposta: a });
  L.decide_urgencia = urg >= 0.3;
  // "Dói?" só vale como pergunta com 0,67 ou mais; abaixo disso fica como relato (lado seguro).
  L.decide_dor = dor === 'outro' ? 'outro' : (dor === 'pergunta_sobre_o_procedimento' && dorP >= 0.67 ? 'pergunta' : 'relato');
  L.decide_fora = fora >= 0.7 ? 'nao_fazemos' : (fora >= 0.3 ? 'equipe' : 'nao');
  if (m.gate) {
    const conf = a.conf && a.conf.choice, sim = p(a.conf && a.conf.probabilities && a.conf.probabilities.sim_claro);
    const esp = p(a.espera && a.espera.noul), pede = p(a.pede_cancelar && a.pede_cancelar.noul);
    if (!conf || sim === null || esp === null || pede === null) throw new Error('resposta estranha (cancelar)');
    Object.assign(L, { jev_conf: String(conf).slice(0, 30), jev_conf_sim: sim, jev_espera: esp, jev_pede_cancelar: pede });
    // Regra mista: sim claro 0,93+; não pede para esperar (<0,3); e sem "?" ou pede explicitamente para cancelar (0,7+).
    L.decide_cancelar = (sim >= 0.93 && esp < 0.3 && (!String(m.mensagem || '').includes('?') || pede >= 0.7)) ? 'cancela' : 'pergunta_de_novo';
  }
  const tk = r.usage && Number(r.usage.input_tokens);
  if (tk >= 0) { L.tokens = Math.round(tk); L.custo_usd = tk * __PRECO__ / 1e6; }
  if (ms > __LIMITE_MS__) throw new Error('passou de __LIMITE_MS__ ms');
  L.ok = true;
} catch (e) {
  L.ok = false;
  L.erro = String(e && e.message || e).replace(/Bearer\s+\S+/gi, 'Bearer ***').slice(0, 200);
}
return [{ json: { linha: L } }];
"""

GRAVAR_SQL = r"""
WITH limpa AS (DELETE FROM jev_sombra WHERE criado_em < now() - interval '60 days' RETURNING 1)
INSERT INTO jev_sombra (telefone, msg_id, mensagem, perguntou_cancelar, regra_urgencia, regra_rota, regra_acao, regra_cancelou,
  regra_motivo, ok, erro, ms, modelo, tokens, custo_usd, jev_urgencia, jev_dor, jev_dor_p, jev_fora, jev_conf, jev_conf_sim,
  jev_espera, jev_pede_cancelar, decide_urgencia, decide_dor, decide_fora, decide_cancelar, resposta)
SELECT telefone, msg_id, mensagem, perguntou_cancelar, regra_urgencia, regra_rota, regra_acao, regra_cancelou,
  regra_motivo, ok, erro, ms, modelo, tokens, custo_usd, jev_urgencia, jev_dor, jev_dor_p, jev_fora, jev_conf, jev_conf_sim,
  jev_espera, jev_pede_cancelar, decide_urgencia, decide_dor, decide_fora, decide_cancelar, resposta
FROM jsonb_populate_record(NULL::jev_sombra, $1::jsonb);
"""


def adicionar(A, code, http, pg, se, cond, comum_js, x0=3980):
    """Acrescenta ao fluxo A o caminho lateral do Jev, saindo de "Decidir a ação"."""
    montar = (comum_js + MONTAR_JS
              .replace("__PERGUNTAS__", json.dumps(PERGUNTAS, ensure_ascii=False))
              .replace("__PERGUNTAS_CANCELAR__", json.dumps(PERGUNTAS_CANCELAR, ensure_ascii=False))
              .replace("__MODELO__", MODELO))
    anotar = (ANOTAR_JS.replace("__PRECO__", repr(PRECO_ENTRADA_POR_MILHAO))
              .replace("__LIMITE_MS__", str(LIMITE_MS)))
    code(A, "Jev: montar a pergunta (sombra)", montar, (x0 + 240, Y), onError="continueRegularOutput")
    se(A, "Jev: chamar? (sombra)", cond("={{ $json.chamar }}", "true", typ="boolean"), (x0 + 480, Y))
    http(A, "Jev: perguntar (sombra)", "POST", "https://api.typesafe.ai/v1/systemone", (x0 + 720, Y),
         cred="typesafe", body_expr="$json.corpo", timeout=LIMITE_MS, onError="continueRegularOutput")
    code(A, "Jev: anotar a resposta (sombra)", anotar, (x0 + 960, Y), onError="continueRegularOutput")
    pg(A, "Jev: gravar (sombra)", GRAVAR_SQL, "[ JSON.stringify($json.linha) ]", (x0 + 1200, Y), onError="continueRegularOutput")
    A.link("Decidir a ação", "Jev: montar a pergunta (sombra)")
    A.link("Jev: montar a pergunta (sombra)", "Jev: chamar? (sombra)")
    A.link("Jev: chamar? (sombra)", "Jev: perguntar (sombra)", out=0)
    A.link("Jev: perguntar (sombra)", "Jev: anotar a resposta (sombra)")
    A.link("Jev: anotar a resposta (sombra)", "Jev: gravar (sombra)")
