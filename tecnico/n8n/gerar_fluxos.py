# Gera os fluxos da Clara para o n8n (importar com "n8n import:workflow").
# Saída: clara-envio.json e clara-atendimento.json, nesta mesma pasta.
# Nenhuma chave aqui: os fluxos apontam para credenciais já criadas no n8n (só o id).
import json, uuid, pathlib

PASTA = pathlib.Path(__file__).parent

CRED = {
    "anthropic": {"anthropicApi": {"id": "EVx1CbzgsBjsOfBS", "name": "Anthropic account"}},
    "google": {"googleCalendarOAuth2Api": {"id": "PoLFn2QYsgfjLmeI", "name": "Google Calendar account"}},
    "whapi": {"httpHeaderAuth": {"id": "HpXFZlusXDEZjQm4", "name": "Header Auth account"}},
    "openai": {"openAiApi": {"id": "eRxSt3V4rGOaTIAI", "name": "OpenAI account"}},
    "pg": {"postgres": {"id": "clarapg0000001", "name": "Postgres Clara"}},
}
ID_ENVIO = "ClaraEnvio000001"
ID_ATEND = "ClaraAtendimento"
WEBHOOK_PATH = "clara-whapi-7f3c9a2e51b84d06"
AVISO_FALHA_ENVIO = "972584285541"   # Erica
TZ = "America/Sao_Paulo"
GCAL = "https://www.googleapis.com/calendar/v3"


class Fluxo:
    def __init__(self, nome, wid):
        self.nome, self.wid, self.nodes, self.conns = nome, wid, [], {}

    def add(self, name, typ, ver, params, pos, **extra):
        n = {"id": str(uuid.uuid5(uuid.NAMESPACE_URL, self.wid + name)), "name": name,
             "type": typ, "typeVersion": ver, "position": list(pos), "parameters": params}
        n.update(extra)
        self.nodes.append(n)
        return name

    def link(self, a, b, out=0, inp=0):
        outs = self.conns.setdefault(a, {}).setdefault("main", [])
        while len(outs) <= out:
            outs.append([])
        outs[out].append({"node": b, "type": "main", "index": inp})

    def json(self):
        return {"id": self.wid, "name": self.nome, "nodes": self.nodes, "connections": self.conns,
                "active": False, "pinData": {},
                "settings": {"executionOrder": "v1", "timezone": TZ, "saveManualExecutions": True,
                             "callerPolicy": "workflowsFromSameOwner"}}


# ---------- ajudantes de nós ----------
def code(f, name, js, pos, **kw):
    return f.add(name, "n8n-nodes-base.code", 2, {"jsCode": js.strip()}, pos, **kw)


def pg(f, name, sql, params_expr, pos, **kw):
    p = {"operation": "executeQuery", "query": sql.strip(), "options": {}}
    if params_expr:
        p["options"]["queryReplacement"] = "={{ " + params_expr + " }}"
    return f.add(name, "n8n-nodes-base.postgres", 2.5, p, pos, credentials=CRED["pg"], **kw)


def http(f, name, method, url, pos, cred=None, body_expr=None, headers=None, file_out=False, **kw):
    p = {"method": method, "url": url, "options": {"timeout": 120000}}
    if cred:
        ctype = list(CRED[cred].keys())[0]
        if ctype == "httpHeaderAuth":
            p.update({"authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth"})
        else:
            p.update({"authentication": "predefinedCredentialType", "nodeCredentialType": ctype})
        kw["credentials"] = CRED[cred]
    if headers:
        p["sendHeaders"] = True
        p["headerParameters"] = {"parameters": [{"name": k, "value": v} for k, v in headers.items()]}
    if body_expr:
        p.update({"sendBody": True, "specifyBody": "json", "jsonBody": "={{ JSON.stringify(" + body_expr + ") }}"})
    if file_out:
        p["options"]["response"] = {"response": {"responseFormat": "file"}}
    return f.add(name, "n8n-nodes-base.httpRequest", 4.2, p, pos, **kw)


def cond(left, op, right=None, typ="string"):
    c = {"id": str(uuid.uuid4()), "leftValue": left, "operator": {"type": typ, "operation": op}}
    if right is not None:
        c["rightValue"] = right
    if op in ("true", "false", "exists", "notExists", "empty", "notEmpty"):
        c["operator"]["singleValue"] = True
    return c


def condicoes(*cs):
    return {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
            "conditions": list(cs), "combinator": "and"}


def se(f, name, c, pos):
    return f.add(name, "n8n-nodes-base.if", 2.2, {"conditions": condicoes(c), "options": {}}, pos)


def escolha(f, name, campo, valores, pos):
    regras = [{"conditions": condicoes(cond("={{ $json." + campo + " }}", "equals", v)),
               "renameOutput": True, "outputKey": v} for v in valores]
    return f.add(name, "n8n-nodes-base.switch", 3.2, {"rules": {"values": regras}, "options": {}}, pos)


def espera(f, name, amount_expr, pos):
    return f.add(name, "n8n-nodes-base.wait", 1.1, {"amount": amount_expr, "unit": "seconds"}, pos,
                 webhookId=str(uuid.uuid5(uuid.NAMESPACE_URL, f.wid + name + "wh")))


def chamar_envio(f, name, pos):
    return f.add(name, "n8n-nodes-base.executeWorkflow", 1.2, {
        "workflowId": {"__rl": True, "value": ID_ENVIO, "mode": "id"},
        "options": {"waitForSubWorkflow": False}}, pos)


# =====================================================================
# FLUXO 1: Clara · Envio (antigo 1D). Recebe itens {phone, m1, m2, m3, sem_digitar}.
# =====================================================================
E = Fluxo("Clara · Envio (até 3 mensagens)", ID_ENVIO)
E.add("Recebe pedido de envio", "n8n-nodes-base.executeWorkflowTrigger", 1.1,
      {"inputSource": "passthrough"}, (0, 0))
pg(E, "Modo teste?", "SELECT coalesce((SELECT valor FROM config WHERE chave = 'modo_teste'), '0') = '1' AS teste;",
   None, (220, 0), executeOnce=True)
code(E, "Montar mensagens", r"""
const teste = !!$('Modo teste?').first().json.teste;
const saida = [];
for (const it of $('Recebe pedido de envio').all()) {
  const j = it.json;
  const phone = String(j.phone || '').replace(/\D/g, '');
  if (!phone) continue;   // proteção: sem telefone não envia nada
  const ms = [j.m1, j.m2, j.m3].map(x => (x == null ? '' : String(x)).trim()).filter(Boolean);
  ms.forEach((body, i) => {
    const typing = j.sem_digitar ? 1 : Math.min(30, Math.max(3, Math.round(body.length / 5)));
    saida.push({ json: { to: phone, body, typing_time: typing,
      espera: i < ms.length - 1 ? typing + 1 : 1, teste } });
  });
}
return saida;
""", (440, 0))
E.add("Uma por vez", "n8n-nodes-base.splitInBatches", 3, {"batchSize": 1, "options": {}}, (660, 0))
se(E, "Modo teste ligado?", cond("={{ $json.teste }}", "true", typ="boolean"), (880, 0))
pg(E, "Guardar saída de teste", "INSERT INTO saidas_teste (telefone, texto) VALUES ($1, $2);",
   "[ $json.to, $json.body ]", (1100, -200))
http(E, "Enviar pelo WhatsApp (digitando)", "POST", "https://gate.whapi.cloud/messages/text", (1100, 100),
     cred="whapi", body_expr="{ to: $json.to, body: $json.body, typing_time: $json.typing_time }",
     onError="continueErrorOutput")
http(E, "Avisar a Erica da falha", "POST", "https://gate.whapi.cloud/messages/text", (1340, 300),
     cred="whapi", onError="continueRegularOutput",
     body_expr="{ to: '" + AVISO_FALHA_ENVIO + "', typing_time: 1, body: '⚠️ Aviso Keshion: a mensagem da Clara para ' + $('Uma por vez').item.json.to + ' não foi entregue pelo WhatsApp. Texto que não saiu: ' + $('Uma por vez').item.json.body }")
espera(E, "Esperar a mensagem sair", "={{ $('Uma por vez').item.json.espera }}", (1580, 0))

E.link("Recebe pedido de envio", "Modo teste?")
E.link("Modo teste?", "Montar mensagens")
E.link("Montar mensagens", "Uma por vez")
E.link("Uma por vez", "Modo teste ligado?", out=1)
E.link("Modo teste ligado?", "Guardar saída de teste", out=0)
E.link("Modo teste ligado?", "Enviar pelo WhatsApp (digitando)", out=1)
E.link("Guardar saída de teste", "Esperar a mensagem sair")
E.link("Enviar pelo WhatsApp (digitando)", "Esperar a mensagem sair", out=0)
E.link("Enviar pelo WhatsApp (digitando)", "Avisar a Erica da falha", out=1)
E.link("Avisar a Erica da falha", "Esperar a mensagem sair")
E.link("Esperar a mensagem sair", "Uma por vez")

# =====================================================================
# FLUXO 2: Clara · Atendimento (antigos 1A + 1B + 1C)
# =====================================================================
A = Fluxo("Clara · Atendimento (WhatsApp)", ID_ATEND)
A.add("Mensagem recebida (Whapi)", "n8n-nodes-base.webhook", 2.1,
      {"httpMethod": "POST", "path": WEBHOOK_PATH, "responseMode": "onReceived", "options": {}}, (0, 0),
      webhookId=str(uuid.uuid5(uuid.NAMESPACE_URL, "clara-webhook")))

code(A, "Normalizar mensagem", r"""
const body = $input.first().json.body || {};
const m = (body.messages || [])[0];
if (!m) return [];                                  // status, eventos sem mensagem
const chat = String(m.chat_id || '');
if (chat.includes('@g.us')) return [];              // grupos
const tipo = String(m.type || '');
if (tipo === 'action' || tipo === 'system') return [];
const fromMe = m.from_me === true || m.from_me === 'true';
const texto = (m.text && m.text.body) || '';
const legenda = (m.image && m.image.caption) || (m.video && m.video.caption) || (m.document && m.document.caption) || '';
const audio = (m.voice && m.voice.link) || (m.audio && m.audio.link) || '';
const imagem = (m.image && m.image.link) || '';
let rota, telefone;
if (fromMe) {
  if (m.source === 'api' || m.source === 'system') return [];  // mensagens da própria Clara voltando
  rota = 'doutora';
  telefone = chat.replace('@s.whatsapp.net', '').replace(/\D/g, '');
} else {
  rota = 'paciente';
  telefone = String(m.from || '').replace(/\D/g, '');
}
if (!telefone) return [];                           // proteção contra chamada sem telefone
let midia = 'texto';
if (audio) midia = 'audio'; else if (imagem) midia = 'imagem'; else if (!texto) midia = 'outro';
return [{ json: {
  rota, telefone, nome: m.from_name || '', id: m.id || ('sem-id-' + Date.now()), tipo, midia,
  texto, legenda, audio, imagem,
  arquivo: (m.document && m.document.filename) || '',
  resumo: texto || legenda || '(enviou áudio, foto ou arquivo)'
} }];
""", (220, 0))
se(A, "Doutora respondeu pelo celular?", cond("={{ $json.rota }}", "equals", "doutora"), (440, 0))

pg(A, "Guardar resposta da doutora e pausar 12 h", r"""
INSERT INTO pacientes (telefone, conversa, pendente, ultimo_id, pausado_ate, atualizado)
VALUES ($1::text, 'Doutora (pelo celular): ' || $2::text, '', $3::text, now() + interval '12 hours', now())
ON CONFLICT (telefone) DO UPDATE SET
  conversa = ltrim(right(pacientes.conversa
    || CASE WHEN length(trim(pacientes.pendente)) > 0 THEN E'\nPaciente: ' || trim(pacientes.pendente) ELSE '' END
    || E'\nDoutora (pelo celular): ' || $2::text, 11000), E'\n'),
  pendente = '', ultimo_id = $3::text, pausado_ate = now() + interval '12 hours', atualizado = now();
""", "[ $json.telefone, $json.resumo, $json.id ]", (660, -300))

pg(A, "Ler a ficha (pausa e comando)", r"""
SELECT p.*, coalesce(p.pausado_ate > now(), false) AS pausado,
       (SELECT valor FROM config WHERE chave = 'numeros_keshion') AS numeros_keshion
FROM (SELECT 1) x LEFT JOIN pacientes p ON p.telefone = $1::text;
""", "[ $json.telefone ]", (660, 100))
code(A, "Decidir caminho", r"""
const msg = $('Normalizar mensagem').first().json;
const f = $input.first().json;
const cmd = (msg.texto || '').trim().toLowerCase();
const keshion = String(f.numeros_keshion || '').split(',').map(s => s.trim());
let caminho;
if (cmd === '#reiniciar' && keshion.includes(msg.telefone)) caminho = 'reiniciar';  // só números da Keshion
else if (f.pausado) caminho = 'pausado';
else caminho = msg.midia;   // texto, audio, imagem ou outro
return [{ json: { ...msg, caminho } }];
""", (880, 100))
escolha(A, "Tipo de mensagem", "caminho", ["reiniciar", "pausado", "audio", "imagem", "texto", "outro"], (1100, 100))

# reiniciar (só demo)
pg(A, "Apagar a conversa de teste", r"""
INSERT INTO pacientes (telefone, nome) VALUES ($1::text, $2::text)
ON CONFLICT (telefone) DO UPDATE SET nome = EXCLUDED.nome, conversa = '', pendente = '', ultimo_id = NULL,
  nome_paciente = NULL, tratamento = NULL, avaliacao_texto = NULL, avaliacao_evento = NULL,
  avaliacao_inicio = NULL, pausado_ate = NULL, atualizado = now();
""", "[ $json.telefone, $json.nome ]", (1340, -500))
code(A, "Aviso de reinício", r"""
return [{ json: { phone: $('Decidir caminho').first().json.telefone, sem_digitar: true,
  m1: 'Conversa reiniciada. A próxima mensagem conta como primeiro contato. Se você tinha uma avaliação de teste marcada, apague o evento na agenda.' } }];
""", (1580, -500))
chamar_envio(A, "Enviar aviso de reinício", (1820, -500))

# pausado: só guarda
pg(A, "Só guardar na conversa", r"""
UPDATE pacientes SET conversa = ltrim(right(conversa || E'\nPaciente: ' || $2::text, 11000), E'\n'),
  pendente = '', ultimo_id = $3::text, atualizado = now()
WHERE telefone = $1::text;
""", "[ $json.telefone, $json.resumo, $json.id ]", (1340, -300))

# áudio
http(A, "Baixar o áudio", "GET", "={{ $json.audio }}", (1340, -100), file_out=True, onError="continueRegularOutput")
A.add("Transcrever o áudio (OpenAI)", "n8n-nodes-base.httpRequest", 4.2, {
    "method": "POST", "url": "https://api.openai.com/v1/audio/transcriptions",
    "authentication": "predefinedCredentialType", "nodeCredentialType": "openAiApi",
    "sendBody": True, "contentType": "multipart-form-data",
    "bodyParameters": {"parameters": [
        {"parameterType": "formBinaryData", "name": "file", "inputDataFieldName": "data"},
        {"name": "model", "value": "gpt-4o-mini-transcribe"},
        {"name": "language", "value": "pt"},
        {"name": "prompt", "value": "Áudio de paciente para uma clínica odontológica, em português do Brasil."}]},
    "options": {"timeout": 120000}}, (1580, -100), credentials=CRED["openai"], onError="continueRegularOutput")

# foto
http(A, "Ler a foto (OpenAI)", "POST", "https://api.openai.com/v1/chat/completions", (1340, 100), cred="openai",
     onError="continueRegularOutput",
     body_expr="{ model: 'gpt-5.4-mini', max_completion_tokens: 1500, messages: [{ role: 'user', content: ["
               "{ type: 'text', text: 'Descreva em português, em até 4 frases, o que aparece nesta imagem enviada por um paciente a uma clínica odontológica. Se houver texto (comprovante de pagamento, orçamento, pedido de exame, receita), transcreva os dados principais: valores, datas, nomes e tratamentos. Se for foto de dentes ou do sorriso, descreva apenas o que se vê, sem diagnóstico.' },"
               "{ type: 'image_url', image_url: { url: $json.imagem } }] }] }")

code(A, "Texto final da mensagem", r"""
// Junta os quatro caminhos (áudio, foto, texto, outros) num texto só para a fila.
const msg = $('Decidir caminho').first().json;
const j = $input.first().json || {};
let texto;
if (msg.caminho === 'audio') {
  texto = j.text ? '[Áudio transcrito] ' + j.text
                 : '[O paciente enviou um áudio que não foi possível ouvir. Peça com gentileza que escreva a mensagem.]';
} else if (msg.caminho === 'imagem') {
  const d = j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content;
  texto = '[O paciente enviou uma foto. Descrição: ' + (d || 'não foi possível ler a imagem') + '] ' + (msg.legenda || '');
} else if (msg.caminho === 'outro') {
  texto = '[O paciente enviou um conteúdo que não é texto, foto nem áudio (tipo: ' + msg.tipo + '). Nome do arquivo ou legenda, se houver: '
        + msg.arquivo + ' ' + msg.legenda + '. Se for documento ou comprovante, diga que vai verificar e já retorna (ação humano). Se for figurinha, responda de forma leve e natural.]';
} else {
  texto = msg.texto;
}
return [{ json: { telefone: msg.telefone, nome: msg.nome, id: msg.id, tipo: msg.midia, texto: texto.trim() } }];
""", (1820, 100))

# fila de 7 s
pg(A, "Guardar na fila (ignora repetida)", r"""
INSERT INTO pacientes (telefone, nome, pendente, ultimo_id, atualizado)
VALUES ($1::text, $2::text, $3::text, $4::text, now())
ON CONFLICT (telefone) DO UPDATE SET
  nome = EXCLUDED.nome,
  pendente = CASE WHEN pacientes.pendente = '' THEN EXCLUDED.pendente ELSE pacientes.pendente || E'\n' || EXCLUDED.pendente END,
  ultimo_id = EXCLUDED.ultimo_id, atualizado = now()
WHERE pacientes.ultimo_id IS DISTINCT FROM EXCLUDED.ultimo_id
RETURNING telefone, ultimo_id, nome, $5::text AS tipo;
""", "[ $json.telefone, $json.nome, $json.texto, $json.id, $json.tipo ]", (2060, 100))
espera(A, "Esperar 7 s (a pessoa pode mandar mais)", 7, (2300, 100))
pg(A, "Ler ficha e instruções (só a última responde)", r"""
SELECT p.*,
  (SELECT valor FROM config WHERE chave = '_instrucoes') AS instrucoes,
  (SELECT valor FROM config WHERE chave = '_base') AS base,
  coalesce((SELECT valor FROM config WHERE chave = 'modelo'), 'claude-haiku-5-5') AS modelo,
  (SELECT valor FROM config WHERE chave = 'aprovador') AS aprovador,
  (SELECT valor FROM config WHERE chave = 'local_avaliacao') AS local_avaliacao
FROM pacientes p WHERE p.telefone = $1::text AND p.ultimo_id = $2::text;
""", "[ $json.telefone, $json.ultimo_id ]", (2540, 100))
http(A, "Ver horários ocupados (90 dias)", "POST", GCAL + "/freeBusy", (2780, 100), cred="google",
     onError="continueRegularOutput",
     body_expr="{ timeMin: new Date().toISOString(), timeMax: new Date(Date.now() + 91 * 86400000).toISOString(), timeZone: '" + TZ + "', items: [{ id: 'primary' }] }")

code(A, "Montar o pedido para a IA", r"""
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const fila = $('Guardar na fila (ignora repetida)').first().json;
const r = $input.first().json || {};
const tz = 'America/Sao_Paulo';
const agora = new Date();
const fAgora = new Intl.DateTimeFormat('pt-BR', { timeZone: tz, weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
const fDia = new Intl.DateTimeFormat('pt-BR', { timeZone: tz, weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' });
const dias = [];
for (let i = 1; i <= 90; i++) dias.push(fDia.format(new Date(agora.getTime() + i * 86400000)).replace(',', ''));
const busy = r.calendars && r.calendars.primary && r.calendars.primary.busy;
const ocupados = Array.isArray(busy) ? JSON.stringify(busy)
  : 'AGENDA INDISPONÍVEL AGORA: não ofereça horários nem marque. Diga que vai verificar e já retorna (ação humano).';
const conteudo =
  'Data e hora em Curitiba agora: ' + fAgora.format(agora) + '\n\n' +
  'Próximos 90 dias (dia da semana e data):\n' + dias.join('\n') + '\n\n' +
  'HORÁRIOS OCUPADOS NA AGENDA (horário de Curitiba):\n' + ocupados + '\n\n' +
  'FICHA DO PACIENTE\n' +
  'Nome dito pelo paciente: ' + (f.nome_paciente || 'ainda não disse') + '\n' +
  'Tratamento de interesse: ' + (f.tratamento || 'ainda não disse') + '\n' +
  'Avaliação marcada: ' + (f.avaliacao_texto || 'nenhuma') + '\n\n' +
  'Nome no perfil do WhatsApp (não usar na conversa): ' + (f.nome || '') + '\n' +
  'Tipo da última mensagem: ' + (fila.tipo || 'texto') + '\n\n' +
  'Conversa até agora:\n' + (f.conversa || '(primeiro contato)') + '\n\n' +
  'Mensagens novas do paciente, ainda sem resposta (responda a todas juntas):\n' + (f.pendente || '').trim();
return [{ json: { pedido: {
  model: f.modelo, max_tokens: 2000,
  system: (f.instrucoes || '') + '\n\nBASE DA CLÍNICA:\n' + (f.base || ''),
  messages: [{ role: 'user', content: conteudo }]
} } }];
""", (3020, 100))
http(A, "Pedir a resposta (Claude)", "POST", "https://api.anthropic.com/v1/messages", (3260, 100),
     cred="anthropic", headers={"anthropic-version": "2023-06-01"}, body_expr="$json.pedido",
     onError="continueRegularOutput", retryOnFail=True, maxTries=2, waitBetweenTries=3000)
code(A, "Ler as mensagens e a ação", r"""
// O Haiku pode mandar antes um bloco de pensamento: pega o bloco de texto e tira as cercas ```json.
const r = $input.first().json || {};
let d = null;
try {
  const bloco = (r.content || []).find(b => b.type === 'text');
  let t = (bloco && bloco.text) || '';
  t = t.replace(/```json/g, '').replace(/```/g, '').trim();
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a >= 0 && b > a) t = t.slice(a, b + 1);
  d = JSON.parse(t);
} catch (e) { d = null; }
const s = v => (v == null ? '' : String(v)).trim();
if (!d || !s(d.mensagem1)) {
  return [{ json: { ok: false, erro: r.error ? JSON.stringify(r.error).slice(0, 300) : 'resposta ilegível' } }];
}
return [{ json: { ok: true, mensagem1: s(d.mensagem1), mensagem2: s(d.mensagem2), mensagem3: s(d.mensagem3),
  acao: (s(d.acao) || 'responder').toLowerCase(), motivo: s(d.motivo), inicio: s(d.inicio), titulo: s(d.titulo),
  fechamento: s(d.fechamento), nome_paciente: s(d.nome_paciente), tratamento: s(d.tratamento) } }];
""", (3500, 100))
se(A, "Resposta válida?", cond("={{ $json.ok }}", "true", typ="boolean"), (3740, 100))

code(A, "Falha técnica: avisar", r"""
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const erro = $input.first().json.erro || '';
const espera = 'Só um instante, vou verificar aqui e já te retorno.';
return [
  { json: { phone: f.telefone, m1: espera } },
  { json: { phone: f.aprovador, sem_digitar: true, m1: '*Falha técnica na Clara (' + erro + ')*\nPaciente: ' + (f.nome_paciente || f.nome || '') + ' (' + f.telefone + ')\nMensagem: ' + (f.pendente || '').trim() + '\nO paciente recebeu: ' + espera } }
];
""", (3980, 400))
chamar_envio(A, "Enviar aviso de falha", (4220, 400))

code(A, "Decidir a ação", r"""
const ia = $input.first().json;
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const futura = !!f.avaliacao_inicio && new Date(f.avaliacao_inicio) > new Date();
let rota = 'responder';
if (ia.acao === 'humano') rota = 'humano';
else if (ia.acao === 'agendar') rota = futura ? 'ja_marcada' : 'agenda';
else if (ia.acao === 'remarcar') rota = f.avaliacao_evento ? 'agenda' : 'sem_avaliacao';
else if (ia.acao === 'cancelar') rota = f.avaliacao_evento ? 'cancelar' : 'sem_avaliacao';
return [{ json: { ...ia, rota } }];
""", (3980, 0))
escolha(A, "Qual ação?", "rota", ["responder", "humano", "ja_marcada", "sem_avaliacao", "agenda", "cancelar"], (4220, 0))

http(A, "Conferir se o horário segue livre", "POST", GCAL + "/freeBusy", (4460, 300), cred="google",
     onError="continueRegularOutput",
     body_expr="{ timeMin: $json.inicio, timeMax: new Date(new Date($json.inicio).getTime() + 3600000).toISOString(), timeZone: '" + TZ + "', items: [{ id: 'primary' }] }")
code(A, "Horário livre?", r"""
const ia = $('Decidir a ação').first().json;
const r = $input.first().json || {};
const busy = r.calendars && r.calendars.primary && r.calendars.primary.busy;
const ini = new Date(ia.inicio);
let passo;
if (!Array.isArray(busy) || isNaN(ini.getTime())) passo = 'erro';
else if (busy.length > 0) passo = 'ocupado';
else passo = ia.acao === 'remarcar' ? 'mudar' : 'criar';
return [{ json: { passo, inicio: ia.inicio, fim: isNaN(ini.getTime()) ? '' : new Date(ini.getTime() + 3600000).toISOString(), titulo: ia.titulo } }];
""", (4700, 300))
escolha(A, "Próximo passo na agenda", "passo", ["criar", "mudar", "ocupado", "erro"], (4940, 300))
http(A, "Criar a avaliação na agenda", "POST", GCAL + "/calendars/primary/events", (5180, 200), cred="google",
     onError="continueRegularOutput",
     body_expr="{ summary: $json.titulo, location: $('Ler ficha e instruções (só a última responde)').first().json.local_avaliacao, "
               "description: 'Marcado pela Clara pelo WhatsApp. Paciente: ' + ($('Decidir a ação').first().json.nome_paciente || $('Ler ficha e instruções (só a última responde)').first().json.nome_paciente || $('Ler ficha e instruções (só a última responde)').first().json.nome || '') + ' (' + $('Ler ficha e instruções (só a última responde)').first().json.telefone + ')', "
               "start: { dateTime: $json.inicio, timeZone: '" + TZ + "' }, end: { dateTime: $json.fim, timeZone: '" + TZ + "' } }")
http(A, "Mudar a avaliação na agenda", "PATCH",
     "=" + GCAL + "/calendars/primary/events/{{ $('Ler ficha e instruções (só a última responde)').first().json.avaliacao_evento }}",
     (5180, 400), cred="google", onError="continueRegularOutput",
     body_expr="{ summary: $json.titulo, start: { dateTime: $json.inicio, timeZone: '" + TZ + "' }, end: { dateTime: $json.fim, timeZone: '" + TZ + "' } }")
http(A, "Cancelar a avaliação na agenda", "DELETE",
     "=" + GCAL + "/calendars/primary/events/{{ $('Ler ficha e instruções (só a última responde)').first().json.avaliacao_evento }}",
     (4460, 600), cred="google", onError="continueRegularOutput")

# Resultado: cada caminho monta o mesmo formato (mensagens, ficha, avisos para a equipe).
RESULTADO_JS = r"""
const TIPO = '__TIPO__';
const ia = $('Ler as mensagens e a ação').first().json;
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const j = $input.first().json || {};
const tel = f.telefone;
const nome = ia.nome_paciente || f.nome_paciente || f.nome || '';
const pend = (f.pendente || '').trim();
const quem = 'Paciente: ' + nome + ' (' + tel + ')';
const espera = 'Só um instante, vou verificar aqui e já te retorno.';
function quando(iso) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('pt-BR', { timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', hour: 'numeric', minute: '2-digit', hourCycle: 'h23' })
    .formatToParts(new Date(iso)).map(x => [x.type, x.value]));
  return p.day + '/' + p.month + ' às ' + Number(p.hour) + ':' + p.minute;
}
let m = [ia.mensagem1, ia.mensagem2, ia.mensagem3];
let aval = 'manter', aval_inicio = '', aval_texto = '', aval_evento = '', fechamento = '';
const avisos = [];
let tipo = TIPO;
if (tipo === 'agenda') {
  if (j.error) tipo = 'falha';
  else tipo = { agendar: 'marcado', remarcar: 'remarcado', cancelar: 'cancelado' }[ia.acao] || 'falha';
}
const verbo = { agendar: 'marcar', remarcar: 'remarcar', cancelar: 'cancelar' }[ia.acao] || ia.acao;
switch (tipo) {
  case 'humano':
    avisos.push('*Chamar uma pessoa*\n' + quem + '\nMensagem: ' + pend + '\nMotivo: ' + ia.motivo + '\n\nO que a Clara respondeu:\n' + m.filter(Boolean).join(' '));
    break;
  case 'ja_marcada':
    m = ['Vi aqui que você já tem uma avaliação marcada para ' + f.avaliacao_texto + '.', 'Prefere manter esse horário ou trocar por outro?', ''];
    break;
  case 'sem_avaliacao':
    m = ['Vou verificar aqui a sua avaliação e já te retorno.', '', ''];
    avisos.push('*Pedido de ' + ia.acao + ' sem avaliação registrada*\n' + quem + '\nMensagem: ' + pend + '\nConfira a agenda e responda o paciente.');
    break;
  case 'ocupado':
    m = ['Sinto muito, esse horário acabou de ser preenchido.', 'Quer que eu veja outras opções para você?', ''];
    break;
  case 'falha':
    m = [espera, '', ''];
    avisos.push('*Falha ao ' + verbo + ' na agenda*\n' + quem + (f.avaliacao_texto ? '\nAvaliação atual: ' + f.avaliacao_texto : '') + (ia.inicio ? '\nHorário pedido: ' + ia.inicio : '') + '\nO paciente recebeu: ' + espera);
    break;
  case 'marcado':
    aval = 'definir'; aval_inicio = ia.inicio; aval_texto = quando(ia.inicio); aval_evento = j.id || '';
    fechamento = ia.fechamento;
    avisos.push('*Nova avaliação marcada*\n' + ia.titulo + '\nQuando: ' + aval_texto + '\n' + quem);
    break;
  case 'remarcado':
    aval = 'definir'; aval_inicio = ia.inicio; aval_texto = quando(ia.inicio);
    avisos.push('*Avaliação remarcada*\nDe: ' + f.avaliacao_texto + '\nPara: ' + aval_texto + '\n' + quem);
    break;
  case 'cancelado':
    aval = 'limpar';
    avisos.push('*Avaliação cancelada*\n' + f.avaliacao_texto + '\n' + quem);
    break;
}
m = m.map(x => (x || '').trim());
const envios = [{ phone: tel, m1: m[0], m2: m[1], m3: m[2] }]
  .concat(avisos.map(a => ({ phone: f.aprovador, m1: a, sem_digitar: true })));
return [{ json: {
  telefone: tel, pend, pend_bruto: f.pendente || '', texto: m.filter(Boolean).join(' '), id_msg: f.ultimo_id,
  nome_ia: ia.nome_paciente, trat_ia: ia.tratamento, aval, aval_inicio, aval_texto, aval_evento,
  fechamento, envios: JSON.stringify(envios)
} }];
"""
RES = {}
for tipo, pos in [("responder", (4460, -600)), ("humano", (4460, -400)), ("ja_marcada", (4460, -200)),
                  ("sem_avaliacao", (4460, 0)), ("ocupado", (5180, 600)), ("falha", (5180, 800)),
                  ("agenda", (5420, 300))]:
    RES[tipo] = code(A, "Resultado · " + tipo, RESULTADO_JS.replace("__TIPO__", tipo), pos)

pg(A, "Salvar conversa e ficha", r"""
UPDATE pacientes SET
  conversa = ltrim(right(conversa || E'\nPaciente: ' || $2::text || E'\nClara: ' || $3::text, 11000), E'\n'),
  pendente = CASE WHEN ultimo_id = $4::text THEN '' ELSE replace(pendente, $5::text, '') END,
  nome_paciente = coalesce(nullif($6::text, ''), nome_paciente),
  tratamento = coalesce(nullif($7::text, ''), tratamento),
  avaliacao_inicio = CASE $8::text WHEN 'definir' THEN $9::text WHEN 'limpar' THEN NULL ELSE avaliacao_inicio END,
  avaliacao_texto = CASE $8::text WHEN 'definir' THEN $10::text WHEN 'limpar' THEN NULL ELSE avaliacao_texto END,
  avaliacao_evento = CASE $8::text WHEN 'definir' THEN coalesce(nullif($11::text, ''), avaliacao_evento) WHEN 'limpar' THEN NULL ELSE avaliacao_evento END,
  atualizado = now()
WHERE telefone = $1::text
RETURNING telefone, length(conversa) AS tamanho, $12::text AS fechamento, $13::text AS envios;
""", "[ $json.telefone, $json.pend, $json.texto, $json.id_msg, $json.pend_bruto, $json.nome_ia, $json.trat_ia, "
     "$json.aval, $json.aval_inicio, $json.aval_texto, $json.aval_evento, $json.fechamento, $json.envios ]", (5700, 0))
code(A, "Montar os envios", "return JSON.parse($input.first().json.envios).map(e => ({ json: e }));", (5940, -100))
chamar_envio(A, "Enviar ao paciente e à equipe", (6180, -100))

# fechamento (antigo 1C): 1 minuto depois de marcar, se o paciente não respondeu
se(A, "Tem despedida para depois?", cond("={{ $json.fechamento }}", "notEmpty"), (5940, 200))
espera(A, "Esperar 1 minuto", 60, (6180, 200))
pg(A, "O paciente respondeu?", r"""
SELECT length(conversa) = $2::int AND pendente = '' AS sem_resposta FROM pacientes WHERE telefone = $1::text;
""", "[ $('Salvar conversa e ficha').first().json.telefone, $('Salvar conversa e ficha').first().json.tamanho ]", (6420, 200))
se(A, "Ninguém respondeu?", cond("={{ $json.sem_resposta }}", "true", typ="boolean"), (6660, 200))
code(A, "Montar a despedida", r"""
const s = $('Salvar conversa e ficha').first().json;
return [{ json: { phone: s.telefone, m1: s.fechamento } }];
""", (6900, 200))
chamar_envio(A, "Enviar a despedida", (7140, 200))

# ---------- ligações ----------
L = A.link
L("Mensagem recebida (Whapi)", "Normalizar mensagem")
L("Normalizar mensagem", "Doutora respondeu pelo celular?")
L("Doutora respondeu pelo celular?", "Guardar resposta da doutora e pausar 12 h", out=0)
L("Doutora respondeu pelo celular?", "Ler a ficha (pausa e comando)", out=1)
L("Ler a ficha (pausa e comando)", "Decidir caminho")
L("Decidir caminho", "Tipo de mensagem")
L("Tipo de mensagem", "Apagar a conversa de teste", out=0)
L("Apagar a conversa de teste", "Aviso de reinício")
L("Aviso de reinício", "Enviar aviso de reinício")
L("Tipo de mensagem", "Só guardar na conversa", out=1)
L("Tipo de mensagem", "Baixar o áudio", out=2)
L("Baixar o áudio", "Transcrever o áudio (OpenAI)")
L("Transcrever o áudio (OpenAI)", "Texto final da mensagem")
L("Tipo de mensagem", "Ler a foto (OpenAI)", out=3)
L("Ler a foto (OpenAI)", "Texto final da mensagem")
L("Tipo de mensagem", "Texto final da mensagem", out=4)
L("Tipo de mensagem", "Texto final da mensagem", out=5)
L("Texto final da mensagem", "Guardar na fila (ignora repetida)")
L("Guardar na fila (ignora repetida)", "Esperar 7 s (a pessoa pode mandar mais)")
L("Esperar 7 s (a pessoa pode mandar mais)", "Ler ficha e instruções (só a última responde)")
L("Ler ficha e instruções (só a última responde)", "Ver horários ocupados (90 dias)")
L("Ver horários ocupados (90 dias)", "Montar o pedido para a IA")
L("Montar o pedido para a IA", "Pedir a resposta (Claude)")
L("Pedir a resposta (Claude)", "Ler as mensagens e a ação")
L("Ler as mensagens e a ação", "Resposta válida?")
L("Resposta válida?", "Decidir a ação", out=0)
L("Resposta válida?", "Falha técnica: avisar", out=1)
L("Falha técnica: avisar", "Enviar aviso de falha")
L("Decidir a ação", "Qual ação?")
for i, t in enumerate(["responder", "humano", "ja_marcada", "sem_avaliacao"]):
    L("Qual ação?", RES[t], out=i)
L("Qual ação?", "Conferir se o horário segue livre", out=4)
L("Qual ação?", "Cancelar a avaliação na agenda", out=5)
L("Conferir se o horário segue livre", "Horário livre?")
L("Horário livre?", "Próximo passo na agenda")
L("Próximo passo na agenda", "Criar a avaliação na agenda", out=0)
L("Próximo passo na agenda", "Mudar a avaliação na agenda", out=1)
L("Próximo passo na agenda", RES["ocupado"], out=2)
L("Próximo passo na agenda", RES["falha"], out=3)
L("Criar a avaliação na agenda", RES["agenda"])
L("Mudar a avaliação na agenda", RES["agenda"])
L("Cancelar a avaliação na agenda", RES["agenda"])
for t in RES:
    L(RES[t], "Salvar conversa e ficha")
L("Salvar conversa e ficha", "Montar os envios")
L("Montar os envios", "Enviar ao paciente e à equipe")
L("Salvar conversa e ficha", "Tem despedida para depois?")
L("Tem despedida para depois?", "Esperar 1 minuto", out=0)
L("Esperar 1 minuto", "O paciente respondeu?")
L("O paciente respondeu?", "Ninguém respondeu?")
L("Ninguém respondeu?", "Montar a despedida", out=0)
L("Montar a despedida", "Enviar a despedida")

for fluxo, arq in ((E, "clara-envio.json"), (A, "clara-atendimento.json")):
    nomes = {n["name"] for n in fluxo.nodes}
    for a, v in fluxo.conns.items():
        assert a in nomes, a
        for saida in v["main"]:
            for c in saida:
                assert c["node"] in nomes, c["node"]
    (PASTA / arq).write_text(json.dumps(fluxo.json(), ensure_ascii=False, indent=1), encoding="utf-8")
    print(arq, len(fluxo.nodes), "nós")
print("Webhook:", "https://n8n.169-58-41-107.sslip.io/webhook/" + WEBHOOK_PATH)
