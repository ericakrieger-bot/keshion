# Gera os fluxos de atendimento de UMA clínica para o n8n (importar com "n8n import:workflow").
# Uso: python gerar_fluxos.py <slug>   (lê clientes/<slug>/clinica.json; sem slug, usa clinica-demo)
# Saída: gerados/<slug>/envio.json e gerados/<slug>/atendimento.json (fora do Git: contêm o caminho secreto).
# Nenhuma chave aqui nem no clinica.json: os fluxos apontam para credenciais já criadas no n8n (só o id).
# Cada clínica tem os próprios fluxos, o próprio banco e as próprias credenciais (Whapi, Google, Postgres).
import json, uuid, pathlib, sys, urllib.parse

PASTA = pathlib.Path(__file__).parent
RAIZ = PASTA.parent.parent
SLUG = sys.argv[1] if len(sys.argv) > 1 else "clinica-demo"
_ARQ = RAIZ / "clientes" / SLUG / "clinica.json"
if not _ARQ.exists():
    sys.exit("Não achei " + str(_ARQ) + ". Copie clientes/_modelo/clinica.json para a pasta da clínica e preencha.")
CLI = json.loads(_ARQ.read_text(encoding="utf-8"))
if CLI.get("slug") != SLUG:
    sys.exit("O campo slug de " + str(_ARQ) + " precisa ser '" + SLUG + "' (igual ao nome da pasta).")

def _faltando(o, caminho=""):
    if isinstance(o, dict):
        return [x for k, v in o.items() if not k.startswith("_") for x in _faltando(v, caminho + "." + k)]
    if isinstance(o, str) and caminho.endswith(".numeros_keshion"):
        return ["numeros_keshion"] if "PREENCHER" in o else []   # vazio é o certo em clínica real (C7, 19/11)
    return [caminho[1:]] if isinstance(o, str) and ("PREENCHER" in o or not o.strip()) else []
if _faltando(CLI):
    sys.exit("Ainda falta preencher em " + str(_ARQ) + ": " + ", ".join(_faltando(CLI)))
CRED = {k: {v["tipo"]: {"id": v["id"], "name": v["nome"]}} for k, v in CLI["credenciais_n8n"].items()}
for _k in ("anthropic", "openai", "whapi", "google", "pg"):
    if _k not in CRED:
        sys.exit("Falta a credencial '" + _k + "' em credenciais_n8n de " + str(_ARQ) + ".")
ID_ENVIO = CLI["fluxos"]["id_envio"]
ID_ATEND = CLI["fluxos"]["id_atendimento"]
SEMENTE_WEBHOOK = CLI["fluxos"].get("semente_webhook") or (SLUG + "-webhook")
# O caminho do webhook funciona como senha: fica só em segredos.local.json (fora do Git), uma entrada por clínica.
_SEG = PASTA / "segredos.local.json"
_seg = json.loads(_SEG.read_text(encoding="utf-8")) if _SEG.exists() else {}
WEBHOOK_PATH = (_seg.get(SLUG) or {}).get("webhook_path")
if not WEBHOOK_PATH:
    sys.exit("Falta o caminho do webhook de '" + SLUG + "' em tecnico/n8n/segredos.local.json "
             "(formato {\"" + SLUG + "\": {\"webhook_path\": \"...\"}}, fora do Git).")
BASE_URL = CLI["servidor"].rstrip("/")             # trocar quando o domínio keshion.com entrar
CANAL_WHAPI = CLI["whapi"]["canal"]                # só aceita mensagens deste canal
# Alerta de falha do WhatsApp: só para a Keshion, sem texto do paciente, pelo canal da Keshion (decisão 17/11).
_ALERTA = json.loads((PASTA / "alerta-keshion.json").read_text(encoding="utf-8"))
AVISO_FALHA_ENVIO = _ALERTA["numero"]
CRED["alerta"] = {_ALERTA["whapi"]["tipo"]: {"id": _ALERTA["whapi"]["id"], "name": _ALERTA["whapi"]["nome"]}}
TZ = CLI["fuso"]
CIDADE = CLI["cidade"]
ASSISTENTE = CLI["nome_assistente"]
CALENDARIO = CLI["agenda"].get("calendario") or "primary"
DURACAO_MS = int(CLI["duracao_avaliacao_min"]) * 60000
# Regras da agenda que o próprio fluxo confere antes de criar ou mudar um evento (revisão Codex 17/11).
REGRAS_AGENDA = CLI["agenda"].get("regras")
if not REGRAS_AGENDA:
    sys.exit("Falta agenda.regras em " + str(_ARQ) + " (dias_semana, horarios, antecedencia_max_dias, bloqueios, feriados).")

# ---------- validações (revisão Codex 17/11: uma cópia mal feita não pode sobrescrever outra clínica) ----------
import re
_erros = []
for _campo, _valor in (("nome_assistente", ASSISTENTE), ("cidade", CIDADE), ("whapi.canal", CANAL_WHAPI),
                       ("fuso", TZ), ("agenda.calendario", CALENDARIO)):
    if re.search(r"['\"\\`$\n\r{}]", _valor):   # vão para dentro de código JavaScript e SQL
        _erros.append(_campo + " não pode ter aspas, crase, barra invertida, cifrão, chaves ou quebra de linha")
if not re.fullmatch(r"[A-Za-z]+(/[A-Za-z_+-]+)+", TZ):
    _erros.append("fuso precisa ser um fuso IANA, ex.: America/Sao_Paulo")
if not (15 <= DURACAO_MS // 60000 <= 240):
    _erros.append("duracao_avaliacao_min precisa estar entre 15 e 240")
for _campo in ("id_atendimento", "id_envio"):
    if not re.fullmatch(r"[A-Za-z0-9]{16}", CLI["fluxos"][_campo]):
        _erros.append("fluxos." + _campo + " precisa ter exatamente 16 letras ou números")
_r = REGRAS_AGENDA
if not (isinstance(_r.get("dias_semana"), list) and _r["dias_semana"] and all(isinstance(x, int) and 0 <= x <= 6 for x in _r["dias_semana"])):
    _erros.append("agenda.regras.dias_semana precisa ser uma lista de 0 a 6 (0 = domingo)")
if not (isinstance(_r.get("horarios"), list) and _r["horarios"] and all(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", str(x)) for x in _r["horarios"])):
    _erros.append("agenda.regras.horarios precisa ser uma lista como [\"09:00\", \"14:00\"]")
if not (isinstance(_r.get("antecedencia_max_dias"), int) and 1 <= _r["antecedencia_max_dias"] <= 365):
    _erros.append("agenda.regras.antecedencia_max_dias precisa ser um número de 1 a 365")
if not isinstance(_r.get("antecedencia_min_minutos"), int):
    _erros.append("agenda.regras.antecedencia_min_minutos precisa ser um número")
if not all(re.fullmatch(r"(\d{4}-)?\d\d-\d\d", str(x)) for x in _r.get("feriados", [])):
    _erros.append("agenda.regras.feriados precisa ter itens MM-DD ou AAAA-MM-DD")
if not all(re.fullmatch(r"\d\d-\d\d", str(b.get("de"))) and re.fullmatch(r"\d\d-\d\d", str(b.get("ate"))) for b in _r.get("bloqueios", [])):
    _erros.append("agenda.regras.bloqueios precisa ter itens {\"de\": \"MM-DD\", \"ate\": \"MM-DD\"}")
if ID_ATEND == ID_ENVIO:
    _erros.append("id_atendimento e id_envio precisam ser diferentes")
if not re.fullmatch(r"\d{10,15}", AVISO_FALHA_ENVIO):
    _erros.append("numero em alerta-keshion.json precisa ser só números, com o código do país")
if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", SLUG):
    _erros.append("o slug precisa ter só letras minúsculas, números e -")
if not re.fullmatch(r"[A-Za-z0-9_-]{16,}", WEBHOOK_PATH):
    _erros.append("o caminho do webhook em segredos.local.json precisa ter 16 ou mais letras, números, - ou _")
# Nada pode coincidir com outra clínica, salvo credenciais declaradas em "compartilha_para_teste" (clínica de teste).
_meu = CLI.get("compartilha_para_teste") or []
for _outra in sorted((RAIZ / "clientes").glob("*/clinica.json")):
    o = json.loads(_outra.read_text(encoding="utf-8"))
    os_ = o.get("slug")
    if os_ == SLUG or os_ is None or "PREENCHER" in str(os_):
        continue
    def _igual(rotulo, a, b):
        if a and b and a == b and "PREENCHER" not in str(a):
            _erros.append(rotulo + " igual ao de " + os_ + " (" + str(_outra.relative_to(RAIZ)) + ")")
    _ids_outra = {o["fluxos"].get("id_atendimento"), o["fluxos"].get("id_envio")}
    for _id in (ID_ATEND, ID_ENVIO):
        if _id in _ids_outra:
            _erros.append("id de fluxo " + _id + " já é usado por " + os_)
    _igual("semente_webhook", SEMENTE_WEBHOOK, o["fluxos"].get("semente_webhook") or (os_ + "-webhook"))
    _igual("caminho do webhook", WEBHOOK_PATH, (_seg.get(os_) or {}).get("webhook_path"))
    _igual("whapi.canal", CANAL_WHAPI, o["whapi"].get("canal"))
    _igual("banco", CLI["banco"], o.get("banco"))
    _compartilha = set(_meu) | set(o.get("compartilha_para_teste") or [])
    for _k in ("whapi", "google", "pg"):
        if _k in _compartilha:
            continue
        _igual("credencial " + _k, CLI["credenciais_n8n"][_k]["id"], o["credenciais_n8n"].get(_k, {}).get("id"))
if "pg" in _meu:
    _erros.append("o banco (credencial pg) nunca pode ser compartilhado, nem em teste")
if _erros:
    sys.exit("clinica.json de " + SLUG + " recusado:\n- " + "\n- ".join(_erros))

GCAL = "https://www.googleapis.com/calendar/v3"
GCAL_EVENTOS = GCAL + "/calendars/" + urllib.parse.quote(CALENDARIO, safe="@") + "/events"
# Trocas feitas em todo código JavaScript e texto dos nós (nada de nome de clínica escrito à mão).
TROCAS = {"__FUSO__": TZ, "__CIDADE__": CIDADE, "__ASSISTENTE__": ASSISTENTE, "__CALENDARIO__": CALENDARIO,
          "__DURACAO_MS__": str(DURACAO_MS), "__CANAL__": CANAL_WHAPI,
          "__REGRAS__": json.dumps(REGRAS_AGENDA, ensure_ascii=False)}


def trocar(s):
    if isinstance(s, str):
        for k, v in TROCAS.items():
            s = s.replace(k, v)
        return s
    if isinstance(s, dict):
        return {k: trocar(v) for k, v in s.items()}
    if isinstance(s, list):
        return [trocar(v) for v in s]
    return s


class Fluxo:
    def __init__(self, nome, wid):
        self.nome, self.wid, self.nodes, self.conns = nome, wid, [], {}

    def add(self, name, typ, ver, params, pos, **extra):
        n = {"id": str(uuid.uuid5(uuid.NAMESPACE_URL, self.wid + name)), "name": name,
             "type": typ, "typeVersion": ver, "position": list(pos), "parameters": trocar(params)}
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


def http(f, name, method, url, pos, cred=None, body_expr=None, headers=None, file_out=False, timeout=120000, **kw):
    p = {"method": method, "url": url, "options": {"timeout": timeout}}
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
# FLUXO 1: Envio (antigo 1D). Recebe itens {phone, m1, m2, m3, sem_digitar}.
# =====================================================================
E = Fluxo(ASSISTENTE + " · Envio (até 3 mensagens)" + ("" if SLUG == "clinica-demo" else " · " + SLUG), ID_ENVIO)
E.add("Recebe pedido de envio", "n8n-nodes-base.executeWorkflowTrigger", 1.1,
      {"inputSource": "passthrough"}, (0, 0))
pg(E, "Modo teste?", "SELECT coalesce((SELECT valor FROM config WHERE chave = 'modo_teste'), '1') <> '0' AS teste, "
   "coalesce((SELECT valor FROM config WHERE chave = 'prefixo_teste'), '') AS prefixo;",
   None, (220, 0), executeOnce=True)
code(E, "Montar mensagens", r"""
// Teste quando o modo teste geral está ligado OU quando o pedido envolve um número de teste
// (prefixo em config.prefixo_teste). Nesse caso o lote inteiro, inclusive os avisos para a
// equipe, vai para a tabela saidas_teste e nada sai pelo WhatsApp.
const cfg = $('Modo teste?').first().json;
const pedidos = $('Recebe pedido de envio').all();
const prefixo = String(cfg.prefixo || '').trim();
const loteTeste = !!prefixo && pedidos.some(it => String(it.json.phone || '').replace(/\D/g, '').startsWith(prefixo));
const teste = !!cfg.teste || loteTeste;
const saida = [];
for (const it of pedidos) {
  const j = it.json;
  const phone = String(j.phone || '').replace(/\D/g, '');
  if (!phone) continue;   // proteção: sem telefone não envia nada
  const ms = [j.m1, j.m2, j.m3].map(x => (x == null ? '' : String(x)).trim()).filter(Boolean);
  ms.forEach((body, i) => {
    const typing = j.sem_digitar ? 1 : Math.min(50, Math.max(4, Math.round(body.length / 4)));
    saida.push({ json: { to: phone, body, typing_time: typing,
      espera: i < ms.length - 1 ? typing + 1 : 1, teste } });
  });
}
return saida;
""", (440, 0))
E.add("Uma por vez", "n8n-nodes-base.splitInBatches", 3, {"batchSize": 1, "options": {}}, (660, 0))
# C4 (19/11): a Dra. pode assumir pelo celular com mensagens da assistente já na fila. Antes de CADA mensagem
# para a paciente, relê a pausa no banco; pausada = descarta (avisos para a equipe não estão na tabela de pacientes e seguem).
pg(E, "Ler a pausa agora", r"""
SELECT $1::text AS "to", $2::text AS body, $3::int AS typing_time, $4::int AS espera, $5::boolean AS teste,
       coalesce((SELECT pausado_ate > now() FROM pacientes WHERE telefone = $1::text), false) AS pausada;
""", "[ $json.to, $json.body, $json.typing_time, $json.espera, $json.teste ]", (770, 0))
se(E, "Paciente pausada?", cond("={{ $json.pausada }}", "true", typ="boolean"), (880, 150))
se(E, "Modo teste ligado?", cond("={{ $json.teste }}", "true", typ="boolean"), (990, 0))
pg(E, "Guardar saída de teste", "INSERT INTO saidas_teste (telefone, texto) VALUES ($1, $2);",
   "[ $json.to, $json.body ]", (1100, -200))
http(E, "Enviar pelo WhatsApp (digitando)", "POST", "https://gate.whapi.cloud/messages/text", (1100, 100),
     cred="whapi", body_expr="{ to: $json.to, body: $json.body, typing_time: $json.typing_time }",
     onError="continueErrorOutput")
http(E, "Avisar a Keshion da falha", "POST", "https://gate.whapi.cloud/messages/text", (1340, 300),
     cred="alerta", onError="continueRegularOutput",
     body_expr="{ to: '" + AVISO_FALHA_ENVIO + "', typing_time: 1, body: '⚠️ Aviso Keshion (" + SLUG + "): uma mensagem da __ASSISTENTE__ para a paciente não saiu pelo WhatsApp da clínica. Código do erro: ' + String(($json.error && ($json.error.httpCode || $json.error.code || $json.error.name)) || 'sem código').replace(/[^A-Za-z0-9_.-]/g, '').slice(0, 30) + '. Execução: ' + $execution.id + '.' }")
espera(E, "Esperar a mensagem sair", "={{ $('Uma por vez').item.json.espera }}", (1580, 0))

E.link("Recebe pedido de envio", "Modo teste?")
E.link("Modo teste?", "Montar mensagens")
E.link("Montar mensagens", "Uma por vez")
E.link("Uma por vez", "Ler a pausa agora", out=1)
E.link("Ler a pausa agora", "Paciente pausada?")
E.link("Paciente pausada?", "Uma por vez", out=0)      # pausada: descarta esta mensagem e passa à próxima
E.link("Paciente pausada?", "Modo teste ligado?", out=1)
E.link("Modo teste ligado?", "Guardar saída de teste", out=0)
E.link("Modo teste ligado?", "Enviar pelo WhatsApp (digitando)", out=1)
E.link("Guardar saída de teste", "Esperar a mensagem sair")
E.link("Enviar pelo WhatsApp (digitando)", "Esperar a mensagem sair", out=0)
E.link("Enviar pelo WhatsApp (digitando)", "Avisar a Keshion da falha", out=1)
E.link("Avisar a Keshion da falha", "Esperar a mensagem sair")
E.link("Esperar a mensagem sair", "Uma por vez")

# Trecho comum (Pacote A, 18/11): idioma da paciente, frases fixas em pt/en/es e palavras de urgência.
# Entra no começo dos nós "Decidir a ação", "Falha técnica: avisar" e "Resultado · ...".
COMUM_JS = r"""
const norm = x => String(x || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
// Urgência: sempre gera aviso novo para a equipe (nunca fica escondida como "complemento").
const URGENCIA = /sangr|bleed|inchad|inchac|swell|hinchad|hinchaz|febre|fever|fiebre|dor (muito )?forte|muita dor|dor insuport|severe pain|lot of pain|mucho dolor|dolor (muy )?fuerte|\bpus\b|desmai|fainted|passed out/;
// C3 (19/11): urgência vale para qualquer ação da IA e também para pergunta ("estou sangrando, o que faço?"),
// mas não quando há negação ("não estou com febre", "no tengo fiebre", "I don't have a fever") nem quando é só dúvida
// geral ("clareamento faz a gengiva sangrar?": sem relato em primeira pessoa e sem "o que faço").
const NEGACAO = /(?:^|\s)(?:nao|nunca|sem|nem|ni|not|never|without|(?:do|does|did|have|has|is|are|was|were)n'?t|no(?=\s+(?:tengo|tiene|tienes|estoy|esta|hay|siento|he|ha|presento|fever|bleeding|swelling|pus|pain|signs?)))(?:\s+[a-z']+){0,3}\s*$/;
const RELATO = /\b(estou|estoy|minha|meu|meus|minhas|comecei|comecou|ficou|fiquei|agora|ontem|desde|i'?m|i am|i have|i'?ve|i got|i fainted|my|started|now|since|tengo|mi|mis|empece|empezo|ahora|hace)\b|\b(to|ta|esta) (com|sangr\w*|inchad\w*|sentindo)\b/;
const PEDE_AJUDA = /o que (eu )?faco|what (should )?i do|que hago|que debo hacer|help|ajuda|ayuda/;
function ehUrgente(texto) {
  const t = norm(texto);
  let achou = false;
  for (const m of t.matchAll(new RegExp(URGENCIA.source, 'g'))) {
    const antes = t.slice(0, m.index).split(/[.!?;,\n]|\b(?:mas|pero|but|porem|embora)\b/).pop();
    if (!NEGACAO.test(antes)) { achou = true; break; }
  }
  if (!achou) return false;
  return !t.includes('?') || RELATO.test(t) || PEDE_AJUDA.test(t);
}
// Idioma quando a IA não informou: conta palavras típicas; empate ou nada = português.
function detectaIdioma(t) {
  return 'pt';   // 24/11: a assistente fala só português; o resto abaixo fica sem uso até a limpeza do código
  const s = ' ' + norm(t) + ' ';
  const n = re => (s.match(re) || []).length;
  const en = n(/\b(the|you|your|my|is|are|can|could|would|please|thanks|thank|yes|hello|hi|appointment|what|how|when|tomorrow|today|want|need|have|i'?m|it'?s|book|cancel)\b/g);
  const es = n(/\b(usted|quiero|quisiera|puedo|gracias|hola|cita|manana|hoy|tengo|necesito|estoy|muy|pero|donde|cuanto|cuando|tambien|buenos|buenas|si|una|el|los|las|es|con|para mi)\b/g);
  const pt = n(/\b(voce|quero|queria|posso|obrigad[oa]|oi|ola|amanha|hoje|tenho|preciso|estou|muito|mas|onde|quanto|quando|tambem|bom dia|boa tarde|sim|nao|uma|o|os|as|e|com|do|da|pra)\b/g);
  if (en > pt && en >= es) return 'en';
  if (es > pt && es > en) return 'es';
  return 'pt';
}
const FRASES = {
  pt: { espera: 'Só um instante, vou verificar aqui e já te retorno.',
    ja_marcada: t => ['Vi aqui que você já tem uma avaliação marcada para ' + t + '.', 'Prefere manter esse horário ou trocar por outro?'],
    sem_avaliacao: 'Vou verificar aqui a sua avaliação e já te retorno.',
    sem_agenda: 'Vou conferir a agenda aqui e já te retorno com os horários.',
    ocupado: 'Sinto muito, esse horário acabou de ser preenchido.',
    invalido: 'Esse horário não está disponível para avaliação.',
    outras: 'Quer que eu veja outras opções para você?',
    formato: 'Não consegui identificar a data certinho.',
    formato2: 'Me confirma o dia e o mês, por exemplo 19/11, e o horário?',
    equipe: 'Vou pedir para a equipe confirmar esse horário com você e já te retorno.',
    dados: ['Para confirmar, me passa seu nome completo e um telefone de contato?', 'Pode ser este mesmo número.'],
    conf_cancelar: t => 'Só para confirmar: você quer cancelar a sua avaliação de ' + t + ', certo?',
    mantida: t => 'Combinado, sua avaliação de ' + t + ' continua marcada.',
    urgencia: 'Sinto muito que você esteja assim. Já avisei a nossa equipe agora para falar com você o quanto antes. Se piorar muito, procure um pronto atendimento.' },
  en: { espera: 'Just a moment, I will check this and get back to you.',
    ja_marcada: t => ['I see you already have an evaluation scheduled for ' + t + '.', 'Would you like to keep it or change it to another time?'],
    sem_avaliacao: 'I will check your evaluation here and get back to you.',
    sem_agenda: 'I will check the schedule and get back to you with the available times.',
    ocupado: "I'm sorry, that time has just been taken.",
    invalido: 'That time is not available for an evaluation.',
    outras: 'Would you like me to check other options for you?',
    formato: "I couldn't identify the exact date.",
    formato2: 'Could you confirm the day and month, for example Nov 19, and the time?',
    equipe: 'I will ask our team to confirm this time with you and get back to you.',
    dados: ['To confirm, could you send me your full name and a contact phone number?', 'It can be this same number.'],
    conf_cancelar: t => 'Just to confirm: you would like to cancel your evaluation on ' + t + ', correct?',
    mantida: t => 'Sure, your evaluation on ' + t + ' is still scheduled.',
    urgencia: "I'm sorry you are going through this. I have alerted our team right now so someone can reach you as soon as possible. If it gets much worse, please go to an urgent care." },
  es: { espera: 'Un momento, voy a verificarlo y ya te respondo.',
    ja_marcada: t => ['Veo que ya tienes una evaluación agendada para el ' + t + '.', '¿Prefieres mantener ese horario o cambiarlo por otro?'],
    sem_avaliacao: 'Voy a verificar tu evaluación y ya te respondo.',
    sem_agenda: 'Voy a revisar la agenda y ya te respondo con los horarios.',
    ocupado: 'Lo siento, ese horario se acaba de ocupar.',
    invalido: 'Ese horario no está disponible para evaluación.',
    outras: '¿Quieres que busque otras opciones para ti?',
    formato: 'No logré identificar la fecha exacta.',
    formato2: '¿Me confirmas el día y el mes, por ejemplo 19 de noviembre, y la hora?',
    equipe: 'Voy a pedirle al equipo que confirme este horario contigo y ya te respondo.',
    dados: ['Para confirmar, ¿me pasas tu nombre completo y un teléfono de contacto?', 'Puede ser este mismo número.'],
    conf_cancelar: t => 'Solo para confirmar: ¿quieres cancelar tu evaluación del ' + t + ', correcto?',
    mantida: t => 'De acuerdo, tu evaluación del ' + t + ' sigue agendada.',
    urgencia: 'Lamento que estés así. Ya avisé a nuestro equipo ahora para que hablen contigo lo antes posible. Si empeora mucho, acude a urgencias.' }
};
// Data da avaliação no idioma da paciente (português usa o texto já guardado na ficha).
function quandoLg(iso, lg, padrao) {
  const d = new Date(iso || '');
  if (lg === 'pt' || !iso || isNaN(d.getTime())) return padrao || (lg === 'en' ? 'the scheduled date' : lg === 'es' ? 'la fecha agendada' : 'que está marcada');
  const p = Object.fromEntries(new Intl.DateTimeFormat(lg === 'en' ? 'en-US' : 'es-ES', { timeZone: '__FUSO__', weekday: 'long',
    day: 'numeric', month: lg === 'en' ? 'short' : 'long', hour: 'numeric', minute: '2-digit', hourCycle: 'h23' })
    .formatToParts(d).map(x => [x.type, x.value]));
  if (lg === 'en') return p.weekday + ', ' + p.month + ' ' + p.day + ', at ' + Number(p.hour) + ':' + p.minute;
  return p.weekday + ' ' + p.day + ' de ' + p.month + ' a las ' + Number(p.hour) + ':' + p.minute;
}
"""

# =====================================================================
# FLUXO 2: Atendimento (antigos 1A + 1B + 1C)
# =====================================================================
A = Fluxo(ASSISTENTE + " · Atendimento (WhatsApp)" + ("" if SLUG == "clinica-demo" else " · " + SLUG), ID_ATEND)
A.add("Mensagem recebida (Whapi)", "n8n-nodes-base.webhook", 2.1,
      {"httpMethod": "POST", "path": WEBHOOK_PATH, "responseMode": "onReceived", "options": {}}, (0, 0),
      webhookId=str(uuid.uuid5(uuid.NAMESPACE_URL, SEMENTE_WEBHOOK)))

code(A, "Normalizar mensagem", r"""
const body = $input.first().json.body || {};
if (body.channel_id !== '__CANAL__') return [];     // só o canal da Keshion (revisão Codex, item 1)
const m = (body.messages || [])[0];                 // as demais do mesmo pacote são reenviadas ao webhook
if (!m) return [];                                  // status, eventos sem mensagem
const chat = String(m.chat_id || '');
if (chat.includes('@g.us')) return [];              // grupos
const tipo = String(m.type || '');
if (tipo === 'action' || tipo === 'system') return [];
const fromMe = m.from_me === true || m.from_me === 'true';
const texto = (m.text && m.text.body) || '';
const legenda = (m.image && m.image.caption) || (m.video && m.video.caption) || (m.document && m.document.caption) || '';
// Mídia só de endereços do Whapi (Wasabi): o servidor não baixa links de qualquer lugar.
const doWhapi = u => /^https:\/\/([a-z0-9-]+\.)*(wasabisys\.com|whapi\.cloud)\//i.test(String(u || ''));
const audioBruto = (m.voice && m.voice.link) || (m.audio && m.audio.link) || '';
const imagemBruta = (m.image && m.image.link) || '';
const audio = doWhapi(audioBruto) ? audioBruto : '';
const imagem = doWhapi(imagemBruta) ? imagemBruta : '';
let rota, telefone;
if (fromMe) {
  if (m.source === 'api' || m.source === 'system') return [];  // mensagens da própria assistente voltando
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

# Pacote com mais de uma mensagem: cada extra volta ao webhook sozinha e entra na fila normal.
code(A, "Separar mensagens extras do pacote", r"""
const body = $input.first().json.body || {};
if (body.channel_id !== '__CANAL__') return [];
const ms = body.messages || [];
return ms.slice(1).map(m => ({ json: { corpo: { channel_id: body.channel_id, event: body.event, messages: [m] } } }));
""", (220, -250))
http(A, "Reenviar cada extra ao webhook", "POST", BASE_URL + "/webhook/" + WEBHOOK_PATH, (440, -250),
     body_expr="$json.corpo", onError="continueRegularOutput")
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
// 24/11: aceita '#reiniciar', '# reiniciar' e 'reiniciar' (o corretor do celular às vezes separa ou tira o #)
if (/^#?\s*reiniciar[.!]?$/.test(cmd) && keshion.includes(msg.telefone)) caminho = 'reiniciar';  // só números da Keshion
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
  avaliacao_inicio = NULL, pausado_ate = NULL, recusas_agenda = 0, ultimo_complemento = NULL,
  nome_completo = NULL, telefone_contato = NULL, ultimo_aviso_humano = NULL, ultimo_motivo_humano = NULL,
  envio_ate = NULL, atualizado = now();   -- 24/11: apaga a ficha inteira (antes o nome completo e o telefone ficavam)
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
code(A, "Ajustar o nome do áudio", r"""
// A voz do WhatsApp chega como .oga (Ogg com outra extensão) e a OpenAI recusa esse nome
// ("Unsupported file format oga"). O Make mandava sempre "audio.ogg". Aqui (C6, 19/11): só vira .ogg o que é
// oga, opus ou sem extensão nenhuma (nem no nome, nem no campo de extensão, nem no tipo). Trocar a etiqueta não
// converte o formato: um WAV, MP3 etc. mantém nome, extensão e tipo.
const aceitos = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'ogg', 'wav', 'webm'];
const doTipo = { 'audio/wav': 'wav', 'audio/x-wav': 'wav', 'audio/wave': 'wav', 'audio/mpeg': 'mp3', 'audio/mp3': 'mp3', 'audio/mp4': 'm4a',
  'audio/x-m4a': 'm4a', 'audio/m4a': 'm4a', 'audio/webm': 'webm', 'audio/flac': 'flac', 'audio/x-flac': 'flac', 'audio/ogg': 'ogg' };
return $input.all().map(it => {
  const b = it.binary && it.binary.data;
  if (b) {
    const nome = String(b.fileName || 'audio');
    const extNome = (nome.match(/\.([a-z0-9]+)$/i) || [, ''])[1].toLowerCase();
    const extCampo = String(b.fileExtension || '').toLowerCase().replace(/^\./, '');
    const tipo = String(b.mimeType || '').toLowerCase().split(';')[0].trim();
    const ext = extNome || extCampo || doTipo[tipo] || '';
    if (aceitos.includes(ext)) {
      if (!extNome) b.fileName = nome + '.' + ext;          // nome sem ponto, formato já conhecido: só acrescenta a extensão certa
      b.fileExtension = ext;
    } else if (!ext || ext === 'oga' || ext === 'opus') {
      b.fileName = nome.replace(/\.[a-z0-9]+$/i, '') + '.ogg';
      b.fileExtension = 'ogg';
      b.mimeType = 'audio/ogg';
    }
  }
  return it;
});
""", (1460, -220))
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

# fila de 20 s (24/11: 7 s era pouco, a paciente ainda estava escrevendo)
pg(A, "Guardar na fila (ignora repetida)", r"""
WITH novo AS (   -- id já recebido antes (reenvio do Whapi, mesmo horas depois): para aqui
  INSERT INTO mensagens_recebidas (id, telefone) VALUES ($4::text, $1::text)
  ON CONFLICT (id) DO NOTHING RETURNING id
)
INSERT INTO pacientes (telefone, nome, pendente, ultimo_id, atualizado)
SELECT $1::text, $2::text, $3::text, $4::text, now() FROM novo
ON CONFLICT (telefone) DO UPDATE SET
  nome = EXCLUDED.nome,
  conversa = CASE WHEN pacientes.conversa <> '' AND (pacientes.atualizado AT TIME ZONE '__FUSO__')::date < (now() AT TIME ZONE '__FUSO__')::date
    THEN pacientes.conversa || E'\n--- ' || to_char(now() AT TIME ZONE '__FUSO__', 'DD/MM/YYYY') || ' (outro dia) ---' ELSE pacientes.conversa END,
  pendente = CASE WHEN pacientes.pendente = '' THEN EXCLUDED.pendente ELSE pacientes.pendente || E'\n' || EXCLUDED.pendente END,
  ultimo_id = EXCLUDED.ultimo_id, atualizado = now()
WHERE pacientes.ultimo_id IS DISTINCT FROM EXCLUDED.ultimo_id
RETURNING telefone, ultimo_id, nome, $5::text AS tipo;
""", "[ $json.telefone, $json.nome, $json.texto, $json.id, $json.tipo ]", (2060, 100))
espera(A, "Esperar 20 s (a pessoa pode mandar mais)", 20, (2300, 100))
pg(A, "Ver se o envio anterior terminou", r"""
-- As mensagens do turno anterior ainda estão saindo (digitando)? Espera, no máximo 180 s, para não misturar a ordem.
SELECT coalesce((SELECT least(180, greatest(0, ceil(extract(epoch FROM (envio_ate - now())))))
                 FROM pacientes WHERE telefone = $1::text), 0)::int AS falta;
""", "[ $json.telefone ]", (2420, 300))
espera(A, "Esperar o envio anterior terminar", "={{ $json.falta }}", (2480, 300))
pg(A, "Ler ficha e instruções (só a última responde)", r"""
SELECT p.*,
  (SELECT valor FROM config WHERE chave = '_instrucoes') AS instrucoes,
  (SELECT valor FROM config WHERE chave = '_base') AS base,
  coalesce((SELECT valor FROM config WHERE chave = 'modelo'), 'claude-haiku-5-5') AS modelo,
  (SELECT valor FROM config WHERE chave = 'aprovador') AS aprovador,
  (SELECT valor FROM config WHERE chave = 'local_avaliacao') AS local_avaliacao
FROM pacientes p WHERE p.telefone = $1::text AND p.ultimo_id = $2::text;
""", "[ $('Guardar na fila (ignora repetida)').first().json.telefone, $('Guardar na fila (ignora repetida)').first().json.ultimo_id ]", (2540, 100))
http(A, "Ver horários ocupados (90 dias)", "POST", GCAL + "/freeBusy", (2780, 100), cred="google",
     onError="continueRegularOutput",
     body_expr="{ timeMin: new Date().toISOString(), timeMax: new Date(Date.now() + 91 * 86400000).toISOString(), timeZone: '" + TZ + "', items: [{ id: '__CALENDARIO__' }] }")

code(A, "Montar o pedido para a IA", r"""
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const fila = $('Guardar na fila (ignora repetida)').first().json;
const r = $input.first().json || {};
const tz = '__FUSO__';
const agora = new Date();
const fAgora = new Intl.DateTimeFormat('pt-BR', { timeZone: tz, weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
const fDia = new Intl.DateTimeFormat('pt-BR', { timeZone: tz, weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' });
const dias = [];
for (let i = 1; i <= 90; i++) dias.push(fDia.format(new Date(agora.getTime() + i * 86400000)).replace(',', ''));
const prim = (r.calendars && r.calendars['__CALENDARIO__']) || {};
const busy = prim.busy;
const agendaOk = Array.isArray(busy) && !(Array.isArray(prim.errors) && prim.errors.length);
const ocupados = agendaOk ? JSON.stringify(busy)
  : 'AGENDA INDISPONÍVEL AGORA: não ofereça horários nem marque. Diga que vai verificar e já retorna (ação humano).';
const conteudo =
  'Data e hora em __CIDADE__ agora: ' + fAgora.format(agora) + '\n\n' +
  'Próximos 90 dias (dia da semana e data):\n' + dias.join('\n') + '\n\n' +
  'HORÁRIOS OCUPADOS NA AGENDA (horário de __CIDADE__):\n' + ocupados + '\n\n' +
  'FICHA DO PACIENTE\n' +
  'Nome dito pelo paciente: ' + (f.nome_paciente || 'ainda não disse') + '\n' +
  'Tratamento de interesse: ' + (f.tratamento || 'ainda não disse') + '\n' +
  'Avaliação marcada: ' + (f.avaliacao_texto || 'nenhuma') + '\n' +
  'Nome completo: ' + (f.nome_completo || 'ainda não disse') + '\n' +
  'Telefone de contato: ' + (f.telefone_contato || 'ainda não disse') + '\n' +
  'Telefone desta conversa: ' + f.telefone + '\n\n' +
  'Nome no perfil do WhatsApp (não usar na conversa): ' + (f.nome || '') + '\n' +
  'Tipo da última mensagem: ' + (fila.tipo || 'texto') + '\n\n' +
  'Conversa até agora:\n' + (f.conversa || '(primeiro contato)') + '\n\n' +
  'Mensagens novas do paciente, ainda sem resposta (responda a todas juntas):\n' + (f.pendente || '').trim() + '\n\n' +
  '(Responda sempre em português do Brasil, mesmo que o paciente escreva em outro idioma.)';
return [{ json: { agenda_ok: agendaOk, pedido: {
  model: f.modelo, max_tokens: 6000,   // o pensamento interno do Haiku gasta parte disso; 2000 cortava o JSON
  system: (f.instrucoes || '') + '\n\nBASE DA CLÍNICA:\n' + (f.base || ''),
  messages: [{ role: 'user', content: conteudo }]
} } }];
""", (3020, 100))
http(A, "Pedir a resposta (Claude)", "POST", "https://api.anthropic.com/v1/messages", (3260, 100),
     cred="anthropic", headers={"anthropic-version": "2023-06-01"}, body_expr="$json.pedido",
     onError="continueRegularOutput", retryOnFail=True, maxTries=2, waitBetweenTries=3000)
LEITOR_JS = r"""
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
if (!d) {
  // Às vezes o Haiku responde em linhas "mensagem1: ..." em vez de JSON: lê esse formato também.
  const bloco = (r.content || []).find(b => b.type === 'text');
  const txt = (bloco && bloco.text) || '';
  const campos = ['mensagem1', 'mensagem2', 'mensagem3', 'acao', 'motivo', 'inicio', 'titulo', 'fechamento',
                  'nome_completo', 'telefone_contato', 'nome_paciente', 'tratamento', 'idioma'];
  const achados = {};
  for (const linha of txt.split('\n')) {
    const m = linha.match(/^\s*"?([a-z_0-9]+)"?\s*:\s*(.*?)\s*,?\s*$/i);
    if (m && campos.includes(m[1])) achados[m[1]] = m[2].replace(/^"(.*)"$/, '$1');
  }
  // Só para resposta que não é JSON: um JSON cortado no meio continua sendo falha técnica.
  if (achados.mensagem1 && !txt.includes('{') && 'acao' in achados) d = achados;
}
const s = v => (v == null ? '' : String(v)).trim();
if (!d || !s(d.mensagem1)) {
  return [{ json: { ok: false, erro: r.error ? JSON.stringify(r.error).slice(0, 300) : 'resposta ilegível' } }];
}
return [{ json: { ok: true, mensagem1: s(d.mensagem1), mensagem2: s(d.mensagem2), mensagem3: s(d.mensagem3),
  acao: (s(d.acao) || 'responder').toLowerCase(), motivo: s(d.motivo), inicio: s(d.inicio), titulo: s(d.titulo),
  fechamento: s(d.fechamento), nome_paciente: s(d.nome_paciente), tratamento: s(d.tratamento),
  nome_completo: s(d.nome_completo), telefone_contato: s(d.telefone_contato).replace(/\D/g, ''),
  idioma: (s(d.idioma).toLowerCase().match(/^(pt|en|es)/) || [, ''])[1] } }];
"""
code(A, "Ler as mensagens e a ação", LEITOR_JS, (3500, 100))
se(A, "Resposta válida?", cond("={{ $json.ok }}", "true", typ="boolean"), (3740, 100))
# Às vezes o Haiku devolve só o pensamento, sem texto, ou um JSON cortado: pede de novo uma vez antes da falha técnica.
http(A, "Pedir de novo (Claude)", "POST", "https://api.anthropic.com/v1/messages", (3740, 300),
     cred="anthropic", headers={"anthropic-version": "2023-06-01"},
     body_expr="$('Montar o pedido para a IA').first().json.pedido", onError="continueRegularOutput")
code(A, "Ler a segunda tentativa", LEITOR_JS, (3980, 300))
se(A, "Segunda resposta válida?", cond("={{ $json.ok }}", "true", typ="boolean"), (4220, 300))

code(A, "Falha técnica: avisar", COMUM_JS + r"""
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const erro = $input.first().json.erro || '';
const espera = FRASES[detectaIdioma(f.pendente)].espera;
return [   // aviso para a equipe primeiro, sem esperar o "digitando" do paciente
  { json: { phone: f.aprovador, sem_digitar: true, m1: '*Falha técnica na __ASSISTENTE__ (' + erro + ')*\nPaciente: ' + (f.nome_paciente || f.nome || '') + ' (' + f.telefone + ')\nMensagem: ' + (f.pendente || '').trim() + '\nO paciente recebeu: ' + espera } },
  { json: { phone: f.telefone, m1: espera } }
];
""", (3980, 400))
chamar_envio(A, "Enviar aviso de falha", (4220, 400))
# Na falha, também registra o turno e esvazia a fila; senão a próxima mensagem se mistura com esta (revisão Codex, item 4).
pg(A, "Registrar a falha na conversa", r"""
UPDATE pacientes SET
  conversa = ltrim(right(conversa || E'\nPaciente: ' || $2::text || E'\n__ASSISTENTE__: ' || $5::text, 11000), E'\n'),
  pendente = CASE WHEN ultimo_id = $3::text THEN '' ELSE replace(pendente, $4::text, '') END,
  atualizado = now()
WHERE telefone = $1::text;
""", "[ $('Ler ficha e instruções (só a última responde)').first().json.telefone, ($('Ler ficha e instruções (só a última responde)').first().json.pendente || '').trim(), "
     "$('Ler ficha e instruções (só a última responde)').first().json.ultimo_id, $('Ler ficha e instruções (só a última responde)').first().json.pendente || '', "
     "$('Falha técnica: avisar').last().json.m1 ]",
   (4220, 600), executeOnce=True)

code(A, "Decidir a ação", COMUM_JS + r"""
const ia = { ...$input.first().json };
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const futura = !!f.avaliacao_inicio && new Date(f.avaliacao_inicio) > new Date();
const agendaOk = $('Montar o pedido para a IA').first().json.agenda_ok;
const pend = String(f.pendente || '');
// Idioma da paciente (campo "idioma" da IA; se faltar, adivinha pelas mensagens novas). Usado nas frases fixas.
ia.idioma = 'pt';   // 24/11: só português
const F = FRASES[ia.idioma];
// Cancelar só quando (1) a última fala da assistente foi uma pergunta de confirmação e (2) a paciente respondeu que sim.
// Senão, pergunta de novo no idioma dela; se ela disse que quer manter, confirma que a avaliação continua (Pacote A, item A5).
if (ia.acao === 'cancelar' && f.avaliacao_evento) {
  const partes = String(f.conversa || '').split('\n__ASSISTENTE__: ');
  const ultima = partes.length > 1 ? partes[partes.length - 1].split('\nPaciente:')[0] : '';
  const u = norm(ultima), p = norm(pend);
  // C1 (19/11): a última fala da assistente tem de falar de cancelar (cancelar, cancel) e ser uma pergunta; só "certo?" ou
  // "esse é o seu telefone?" não bastam. O "sim" tem de ser curto, sem pergunta e só com palavras de confirmação.
  const perguntou = ultima.includes('?') && /cancel/.test(u);
  const perguntouAlgo = ultima.includes('?') && /\b(certo|correto|correct|right|confirm\w*|correcto|cancel\w*)\b/.test(u);   // só para responder "continua marcada"
  const SIM_OK = new Set(['sim', 'pode', 'confirmo', 'confirmado', 'confirma', 'isso', 'mesmo', 'exato', 'correto', 'certo', 'certeza', 'tenho', 'quero', 'gostaria',
    'por', 'favor', 'pfv', 'obrigado', 'obrigada', 'de', 'que', 'o', 'a', 'e', 'ok', 'okay', 'claro', 'yes', 'yep', 'yeah', 'sure', 'confirm', 'confirmed', 'correct', 'right',
    'that', 'thats', "that's", 'is', 'please', 'do', 'it', 'i', 'would', 'like', 'to', 'thanks', 'thank', 'you', 'si', 'dale', 'correcto', 'estoy', 'seguro', 'segura',
    'quiero', 'gracias', 'favor', 'esta', 'bien', 'eso', 'asi']);
  const palavras = p.replace(/[!.,;:]+/g, ' ').split(/\s+/).filter(Boolean);
  const curto = palavras.length <= 8 && !pend.includes('?') && palavras.every(w => SIM_OK.has(w) || /^cancel/.test(w));
  const nega = /\b(nao|no(?!\s+(?:dia|horario|mesmo|meu|momento))|not|nope|keep|manter|mantenha|mantener|mantengo|wait|espera)\b|don'?t cancel|do not cancel/.test(p);
  const afirma = /\b(sim|pode|confirmo|confirmado|confirma|isso|exato|correto|certo|yes|yep|yeah|confirm|confirmed|sure|correct|si|claro|correcto|dale|ok|okay)\b|please do/.test(p);
  // Diagnóstico de 20/11: com "sim" mais outro assunto ("sim, esse horário mesmo", "sim, obrigada") o "curto" falha e a pergunta de
  // cancelar era repetida sem fim. Se a fala anterior da assistente também era a pergunta de cancelar (já perguntou uma vez), um "sim"
  // sem pergunta e sem negativa na própria mensagem vale como confirmação.
  const anterior = partes.length > 2 ? norm(partes[partes.length - 2].split('\nPaciente:')[0]) : '';
  const jaPerguntouAntes = partes.length > 2 && partes[partes.length - 2].split('\nPaciente:')[0].includes('?') && /cancel/.test(anterior);
  const simSegundaVez = perguntou && jaPerguntouAntes && afirma && !nega && !pend.includes('?') && palavras.length <= 12;
  if (!(perguntou && afirma && !nega && curto) && !simSegundaVez) {
    const t = quandoLg(f.avaliacao_inicio, ia.idioma, f.avaliacao_texto);
    ia.acao = 'responder';
    ia.mensagem1 = perguntouAlgo && nega && !afirma ? F.mantida(t) : F.conf_cancelar(t);
    ia.mensagem2 = ''; ia.mensagem3 = '';
    ia.motivo = 'Confirmação antes de cancelar (pedida pelo fluxo)';
  }
}
const texto = [ia.mensagem1, ia.mensagem2, ia.mensagem3].join(' ');
const ofereceHorario = /\b\d{1,2}h\b|\b\d{1,2}:\d{2}\b|\b\d{1,2}\s*[ap]\.?\s*m\b/i.test(texto);
// Se a resposta diz que vai passar o assunto ou verificar, a equipe tem de receber o aviso, mesmo que a IA tenha marcado "responder".
// Português, inglês e espanhol (A7). Conferir horários não conta: isso a própria assistente faz.
const promete = /(vou|vamos|irei)\s+(passar|encaminhar|verificar|conferir|consultar|checar|perguntar)(?![^.!?]*hor[aá]rio)|j[aá] te (retorno|respondo|dou um retorno)|te dou um retorno|passar (a |o |sua |seu |essa |esta )?(mensagem|pedido|solicita)/i.test(texto)
  || /\b(I['’]?ll|I will|we['’]?ll|we will)\s+(forward|pass|check|ask|confirm)(?![^.!?]*\b(schedule|availability|available|times?|slots?|calendar)\b)|\blet me (check|ask|confirm)(?![^.!?]*\b(schedule|availability|available|times?|slots?|calendar)\b)|\bwill get back\b|\bget back to you\b/i.test(texto)
  || /\bvoy a (pasar|consultar|verificar|confirmar|preguntar)(?![^.!?]*horario)|\b(le|te) paso\b|\bte confirmo (en breve|enseguida|luego|pronto|m[aá]s tarde)|\bte aviso\b|\bya te (respondo|confirmo|aviso)\b/i.test(texto);
if (ia.acao === 'responder' && promete) {
  ia.acao = 'humano';
  ia.motivo = ia.motivo || 'A assistente disse que ia passar ou verificar o assunto';
}
// Urgência relatada (sangramento, inchaço, febre, dor forte) sempre vai para a equipe, mesmo que a IA só tenha respondido.
// C3: vale para qualquer ação (se a IA ia marcar, cancelar etc., a mensagem dela é trocada por um aviso de que a equipe foi chamada).
if (ia.acao !== 'humano' && ehUrgente(pend)) {
  if (ia.acao !== 'responder') { ia.mensagem1 = F.urgencia; ia.mensagem2 = ''; ia.mensagem3 = ''; }
  ia.motivo = 'Paciente relatou possível urgência' + (ia.motivo ? ' (' + ia.motivo + ')' : '');
  ia.acao = 'humano';
}
let rota = 'responder';
// Decisões que não dependem do texto da IA (revisão Codex, item 4):
if (!['responder', 'humano', 'agendar', 'remarcar', 'cancelar'].includes(ia.acao)) rota = 'humano';
else if (!agendaOk && (ia.acao === 'agendar' || ia.acao === 'remarcar' || ofereceHorario)) rota = 'sem_agenda';
else if (ia.acao === 'humano') rota = 'humano';
else if (ia.acao === 'agendar') rota = futura ? 'ja_marcada' : 'agenda';
else if (ia.acao === 'remarcar') rota = f.avaliacao_evento ? 'agenda' : 'sem_avaliacao';
else if (ia.acao === 'cancelar') rota = f.avaliacao_evento ? 'cancelar' : 'sem_avaliacao';
return [{ json: { ...ia, rota } }];
""", (3980, 0))
escolha(A, "Qual ação?", "rota", ["responder", "humano", "ja_marcada", "sem_avaliacao", "agenda", "cancelar", "sem_agenda"], (4220, 0))

code(A, "Validar o pedido de agenda", r"""
// O fluxo confere sozinho as regras da agenda (a IA pode errar): dia, horário, prazo, feriado, recesso,
// nome e telefone (ao marcar) e se o horário foi mesmo oferecido ou dito na conversa.
const R = __REGRAS__;
const tz = '__FUSO__';
const ia = $('Decidir a ação').first().json;
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const fim = (passo, motivo) => [{ json: { passo, motivo: motivo || '' } }];
const d = new Date(ia.inicio);
if (!ia.inicio || isNaN(d.getTime())) return fim('invalido', 'sem horário válido');
const fmt = (dt, extra) => Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', ...extra })
  .formatToParts(dt).map(x => [x.type, x.value]));
const q = fmt(d, { weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
const hoje = fmt(new Date(), {});
const dow = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }[q.weekday];
const data = q.year + '-' + q.month + '-' + q.day, md = q.month + '-' + q.day, hora = q.hour + ':' + q.minute;
const dias = Math.round((Date.UTC(+q.year, +q.month - 1, +q.day) - Date.UTC(+hoje.year, +hoje.month - 1, +hoje.day)) / 86400000);
const fer = R.feriados || [], blo = R.bloqueios || [];
let erro = '';
if (d.getUTCSeconds() || d.getUTCMilliseconds()) erro = 'horário com segundos fora da grade';
else if (d.getTime() < Date.now() + R.antecedencia_min_minutos * 60000) erro = 'horário já passou ou está perto demais';
else if (dias > R.antecedencia_max_dias) erro = 'além do prazo de ' + R.antecedencia_max_dias + ' dias';
else if (!R.dias_semana.includes(dow)) erro = 'dia da semana sem avaliação';
else if (!R.horarios.includes(hora)) erro = 'horário fora dos horários de avaliação';
else if (fer.includes(md) || fer.includes(data)) erro = 'feriado';
else if (blo.some(b => b.de <= b.ate ? (md >= b.de && md <= b.ate) : (md >= b.de || md <= b.ate))) erro = 'recesso';
if (erro) return fim('invalido', erro);
if (ia.acao === 'agendar') {
  const nome = String(ia.nome_completo || f.nome_completo || '').trim();
  const tel = String(ia.telefone_contato || f.telefone_contato || '').replace(/\D/g, '');
  if (nome.split(/\s+/).filter(Boolean).length < 2 || tel.length < 10) return fim('dados', 'falta nome completo ou telefone');
}
// O horário precisa ter aparecido na conversa (oferta da assistente ou fala do paciente): data e hora.
const conversa = String(f.conversa || '') + '\n' + String(f.pendente || '');
const dd = String(+q.day), mm = String(+q.month), hh = String(+q.hour);
// INICIO-DATAS
// Pacote A (18/11, revisão do Codex): data e hora precisam aparecer JUNTAS, na mesma mensagem (da assistente ou da paciente),
// e a hora tem de ficar ligada a essa data (não vale juntar o dia de uma opção com a hora de outra). Vale a mensagem mais
// recente que fala de dia ou hora: se ela traz outro dia ou outra hora, o pedido é recusado; se só repete o dia, a hora
// ou o dia da semana do pedido ("pode ser às 9h", "a de quinta"), procura o par completo nas mensagens anteriores.
// Uma recusa da paciente depois da oferta ("não quero", "não posso", "outro horário") também invalida a oferta.
// Minutos, mês e ano precisam bater. Aceita hoje/amanhã/depois de amanhã (today/tomorrow, hoy/mañana/pasado mañana)
// pela data de hoje na clínica. Formatos: 19/11, 19.11, 19-11, 11/19 (EUA, só com dia > 12), 2026-11-19, "dia 19",
// "19 de novembro", "Nov 19", "19th of November", "Thursday 19", "the 19th", "el 19". Um 19 solto não vale.
const normD = x => String(x || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
const mi = String(q.minute || '00').padStart(2, '0');
const hojeTz = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: '__FUSO__', year: 'numeric', month: '2-digit', day: '2-digit' })
  .formatToParts(new Date()).map(x => [x.type, x.value]));
const ano = String(q.year || hojeTz.year);
const diasAteCand = Math.round((Date.UTC(+ano, +mm - 1, +dd) - Date.UTC(+hojeTz.year, +hojeTz.month - 1, +hojeTz.day)) / 86400000);
const dowCand = new Date(Date.UTC(+ano, +mm - 1, +dd)).getUTCDay();
const MESES = [
  ['janeiro', 'jan', 'january', 'enero', 'ene'], ['fevereiro', 'fev', 'february', 'feb', 'febrero'],
  ['março', 'marco', 'mar', 'march', 'marzo'], ['abril', 'abr', 'april', 'apr'], ['maio', 'mai', 'may', 'mayo'],
  ['junho', 'jun', 'june', 'junio'], ['julho', 'jul', 'july', 'julio'], ['agosto', 'ago', 'august', 'aug'],
  ['setembro', 'set', 'september', 'sep', 'sept', 'septiembre', 'setiembre'], ['outubro', 'out', 'october', 'oct', 'octubre'],
  ['novembro', 'nov', 'november', 'noviembre'], ['dezembro', 'dez', 'december', 'dec', 'diciembre', 'dic']
];
// [nomes por extenso, abreviações], 0 = domingo. "segunda opção" não é segunda-feira.
const SEMANAS = [
  ['domingo|sunday', 'dom|sun'], ['segunda(?!\\s+(?:op|alternativ|vez|via|chance))|monday|lunes', 'seg|mon'],
  ['ter[cç]a|tuesday|martes', 'ter|tues?'], ['quarta|wednesday|mi[eé]rcoles', 'qua|wed'],
  ['quinta|thursday|jueves', 'qui|thu|thur|thurs'], ['sexta|friday|viernes', 'sex|fri'], ['s[aá]bado|saturday', 's[aá]b|sat']
];
const L = '[a-zà-ú]';
const SEM_TODAS = '(?:' + SEMANAS.map(s => s.join('|')).join('|') + ')';
const SEM_LONGA = '(?:' + SEMANAS.map(s => s[0]).join('|') + ')';
const MES_TODOS = '(?:' + MESES.flat().join('|') + ')';
const Mc = '(?:' + MESES[+mm - 1].join('|') + ')';
const OUTROS = '(?:' + MESES.filter((_, i) => i !== +mm - 1).flat().filter(x => x !== 'may').join('|') + ')';
const SUF = '(?:st|nd|rd|th|º|°)?';
const D = '0?' + dd;
const NAO_HORA = '(?!\\d)(?!\\s*(?:[:h/]|hs\\b|horas?\\b|[ap]\\.?\\s*m\\b|in the\\b|o.?clock))';  // depois do dia não pode vir hora
const NAO_OUTRO = '(?!(?:st|nd|rd|th|º|°)?\\.?,?\\s*(?:of\\s+|de\\s+|del\\s+)?(?:the\\s+)?' + OUTROS + '(?!' + L + '))(?!\\s*[/.\\-]\\s*\\d)'; // "dia 19 de dezembro"
const ANO_OK = '(?!,?\\s*(?:de\\s+|del\\s+)?(?!' + ano + '(?!\\d))\\d{4}(?!\\d))';  // ano escrito diferente do pedido
const mesDepois = '\\s*(?:of\\s+|de\\s+|del\\s+)?(?:the\\s+)?' + Mc + '(?!' + L + ')';
const padroes = [
  '(?<![\\d:.,/])(?<!R\\$\\s{0,2})' + D + '\\s*[/.\\-]\\s*0?' + mm + '(?!\\d)(?!\\s*[/.\\-]\\s*(?!(?:' + ano + '|' + ano.slice(2) + ')(?!\\d))\\d)', // 19/11, 19.11, 19-11, 19/11/2026
  '\\b' + ano + '-0?' + mm + '-' + D + '(?!\\d)',                                     // 2026-11-19
  '(?<!' + L + ')d[ií]a\\s+' + D + NAO_HORA + NAO_OUTRO,                               // dia 19, día 19
  '(?<![\\d:.,/])' + D + SUF + mesDepois + ANO_OK,                                    // 19 de novembro, 19th of November, 19 Nov
  '(?<!' + L + ')' + Mc + '\\.?,?\\s*(?:the\\s+)?' + D + SUF + '(?!\\d)(?!:\\d)' + ANO_OK, // Nov 19, November 19th
  '(?<!' + L + ')' + SEM_TODAS + '(?:-feira)?\\.?,?\\s+(?:the\\s+|el\\s+|dia\\s+)?' + D + SUF + NAO_HORA + NAO_OUTRO, // quinta 19, jueves 19
  '(?<!' + L + ')(?:the|el)\\s+' + D + SUF + NAO_HORA + NAO_OUTRO,                     // the 19th, el 19
  '(?<![\\d:.,/])' + D + '(?:st|nd|rd|th)\\b' + NAO_OUTRO + '(?!\\s+(?:installment|payment|parcela|row|floor|time|try|attempt|birthday|anniversary))' // 19th
];
if (+dd > 12) padroes.push('(?<![\\d:.,/])0?' + mm + '\\s*/\\s*' + D + '(?!\\d)');  // 11/19 só pode ser mês/dia
const RELATIVAS = [
  [0, '(?<!' + L + ')(?:hoje|today|hoy)(?!' + L + ')'],
  [1, '(?<!' + L + ')(?<!depois de )(?<!after )(?<!pasado )(?<!(?:la|esta|de)\\s)(?:amanh[ãa]|tomorrow|ma[ñn]ana)(?!' + L + ')'],
  [2, '(?<!' + L + ')(?:depois de amanh[ãa]|pasado ma[ñn]ana|day after tomorrow)(?!' + L + ')']
];
const fontesCand = padroes.concat(RELATIVAS.filter(r => r[0] === diasAteCand).map(r => r[1]));
const spans = (texto, fontes) => fontes.flatMap(p => [...String(texto).matchAll(new RegExp(p, 'gi'))].map(m => [m.index, m.index + m[0].length]));
const temDataNaConversa = texto => spans(texto, fontesCand).length > 0;
// Qualquer menção de dia (para saber se a mensagem fala de OUTRO dia) e de hora.
const RE_DATA = new RegExp([
  '(?<![\\d:.,/])\\d{1,2}\\s*[/.\\-]\\s*\\d{1,2}(?:\\s*[/.\\-]\\s*\\d{2,4})?(?![\\d:])',
  '\\b\\d{4}-\\d{1,2}-\\d{1,2}\\b',
  '(?<!' + L + ')d[ií]a\\s+\\d{1,2}(?!\\d)(?!\\s*(?:h|hs|horas?)(?!' + L + '))',
  '(?<![\\d:.,/])\\d{1,2}(?:st|nd|rd|th|º|°)?\\s*(?:of\\s+|de\\s+|del\\s+)?(?:the\\s+)?' + MES_TODOS + '(?!' + L + ')',
  '(?<!' + L + ')' + MES_TODOS + '\\.?,?\\s*(?:the\\s+)?\\d{1,2}(?:st|nd|rd|th)?(?![\\d:])',
  '(?<!' + L + ')(?:the|el)\\s+\\d{1,2}(?:st|nd|rd|th|º)?(?![\\d:])(?!\\s*(?:[ap]\\.?\\s*m|h\\b|hs\\b|horas?))',
  '(?<![\\d:.,/])\\d{1,2}(?:st|nd|rd|th)(?!' + L + ')',
  '(?<!' + L + ')' + SEM_LONGA + '(?:-feira)?(?!' + L + ')',
  '(?<!' + L + ')(?:hoje|today|hoy|amanh[ãa]|tomorrow|day after tomorrow|depois de amanh[ãa]|pasado ma[ñn]ana)(?!' + L + ')',
  '(?<!' + L + ')(?<!(?:la|esta|de)\\s)ma[ñn]ana(?!' + L + ')'
].join('|'), 'gi');
const RE_HORA = new RegExp([
  '(?<!' + L + ')(?:às|as|a\\s+las|at)\\s+\\d{1,2}(?:\\s*[:h]\\s*\\d{2})?(?:\\s*(?:hs?(?![a-z\\d])|horas?\\b|[ap]\\.?\\s*m\\b\\.?))?',
  '(?<![\\d:./,])\\d{1,2}(?::\\d{2})?\\s*[ap]\\.?\\s*m\\b\\.?',
  '(?<![\\d:./,])\\d{1,2}\\s*hs?(?:\\s*\\d{2})?(?![a-z\\d])',
  '(?<![\\d:./,])\\d{1,2}:\\d{2}(?!\\d)',
  '(?<![\\d:./,])\\d{1,2}\\s*horas?\\b'
].join('|'), 'gi');
// Lê a hora de uma menção: [hora 0 a 23, minutos]. "at 4" sem am/pm pode ser 4h ou 16h; "a las 4 de la tarde" = 16h.
const lerHora = (t, depois) => {
  const s = t.toLowerCase(), n = s.match(/(\d{1,2})(?:\s*(?::|h)\s*(\d{2}))?/);
  if (!n) return [];
  let h = +n[1]; const m = n[2] ? +n[2] : 0;
  const ap = s.match(/([ap])\.?\s*m/);
  if (ap) return h > 12 ? [] : [[h % 12 + (ap[1] === 'p' ? 12 : 0), m]];
  if (/^at\s/.test(s) && h <= 12) return [[h, m], [h % 12 + 12, m]];
  if (h < 12 && /^\s*(?:da|de la|à|a|in the)\s+(?:tarde|noite|noche|afternoon|evening)/.test(String(depois).toLowerCase())) h += 12;
  return [[h, m]];
};
const juntar = lista => lista.sort((a, b) => a.i - b.i || b.f - a.f).reduce((acc, x) => {
  const u = acc[acc.length - 1];
  if (u && x.i < u.f) { u.f = Math.max(u.f, x.f); u.cand = u.cand || x.cand; } else acc.push({ ...x });
  return acc;
}, []);
const SO_SEMANA = new RegExp('^' + SEM_TODAS + '(?:-feira)?$', 'i');
const DOW_LONGA = SEMANAS.map(s => new RegExp('^(?:' + s[0] + ')(?:-feira)?$', 'i'));
function mencoes(b) {
  const cand = spans(b, fontesCand);
  let datas = [...b.matchAll(RE_DATA)].map(m => ({ tipo: 'data', i: m.index, f: m.index + m[0].length, cand: false }))
    .concat(cand.map(([i, f]) => ({ tipo: 'data', i, f, cand: true })));
  datas = juntar(datas).map(x => ({ ...x, cand: x.cand || cand.some(([i, f]) => i < x.f && f > x.i) }));
  // dia da semana sozinho: vale como o pedido se for o mesmo dia da semana; colado numa data, faz parte dela
  datas.forEach(x => { const t = b.slice(x.i, x.f).trim(); x.semana = SO_SEMANA.test(t); if (x.semana && !x.cand) x.cand = !!DOW_LONGA[dowCand] && DOW_LONGA[dowCand].test(t); });
  datas = datas.filter((x, k) => {
    if (!x.semana) return true;
    const viz = [datas[k - 1], datas[k + 1]].filter(Boolean).filter(y => !y.semana);
    return !viz.some(y => /^[\s,.\-]*(?:feira[\s,.]*)?$/i.test(y.i > x.i ? b.slice(x.f, y.i) : b.slice(y.f, x.i)));
  });
  const horas = juntar([...b.matchAll(RE_HORA)].map(m => ({ tipo: 'hora', i: m.index, f: m.index + m[0].length })))
    .map(x => ({ ...x, cand: lerHora(b.slice(x.i, x.f), b.slice(x.f, x.f + 20)).some(([h, m]) => h === +hh && m === +mi) }));
  return { datas, horas };
}
// Cada hora pertence à data mais próxima antes dela (português e espanhol: "19/11 às 9h"); se entre as duas houver
// "ou/or/o/y/e", pertence à data seguinte ("11am on Nov 19 or 4pm on Nov 24").
const SEP = /(?:^|[^a-zà-ú])(?:ou|or|o|y|e|and)(?![a-zà-ú])|;/i;
function parNaMensagem(b, mc) {
  return mc.horas.filter(h => h.cand).some(h => {
    const antes = mc.datas.filter(x => x.f <= h.i).pop(), depois = mc.datas.find(x => x.i >= h.f);
    let dono;
    if (antes && !SEP.test(b.slice(antes.f, h.i))) dono = antes;
    else if (depois && !SEP.test(b.slice(h.f, depois.i))) dono = depois;
    else dono = antes || depois;
    return !!(dono && dono.cand);
  });
}
const NEGA = /\b(nao|no)\s+(quero|posso|consigo|da|vou|puedo|quiero|me sirve|funciona|serve|pode|podera|tenho como|marque|marca|marcar|agende|agenda|agendar|reserve|reservar|confirme|marques|agendes|reserves|lo agende|lo marque)\b|\b(can'?t|cannot|doesn'?t work|won'?t work|not good|don'?t (book|schedule|reserve|confirm)|do not (book|schedule|reserve|confirm))\b|\b(outro|otro)\s+(horario|dia)\b|\banother (time|day|slot)\b|\bnenhum\b|\bninguno\b|\bainda nao\b|\baun no\b|\btodavia no\b|\bnot yet\b|\bhold off\b|\b(espera|espere|aguarde|wait)\b/;
const ehAssistente = b => /^(__ASSISTENTE__|Doutora)\b/.test(b);
// C2 (19/11): a negativa da própria mensagem da paciente vale (cada trecho entre ponto, "mas", "pero", "but" é conferido sozinho).
function parNaMensagemLivre(b) {
  const trechos = b.split(/\.(?!\d)|(?<!\d)\.|[;!]|,\s*(?=(?:pode|poderia|podemos|tem como|que tal|e se|puede|podemos|can|could|how about|what about)\b)|\b(?:mas|pero|but|porem|embora)\b/i).map(x => x.trim()).filter(Boolean);
  return trechos.some(tr => {
    const mt = mencoes(tr);
    return (mt.datas.length || mt.horas.length) && parNaMensagem(tr, mt) && !NEGA.test(normD(tr));
  });
}
function parNaConversa(texto) {
  const blocos = String(texto).split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('---'));
  let negou = false;
  for (let k = blocos.length - 1; k >= Math.max(0, blocos.length - 40); k--) {
    const b = blocos[k], mc = mencoes(b);
    if (!mc.datas.length && !mc.horas.length) {
      if (!ehAssistente(b) && NEGA.test(normD(b))) negou = true;
      continue;
    }
    if (parNaMensagem(b, mc)) {
      if (ehAssistente(b)) return !negou;                      // horário oferecido pela assistente
      return !negou && parNaMensagemLivre(b);                  // pedido da paciente, sem negativa no mesmo trecho
    }
    if (!mc.datas.concat(mc.horas).every(x => x.cand)) return false;   // fala de outro dia ou outra hora
  }
  return false;
}
// FIM-DATAS
const temData = temDataNaConversa(conversa);
const horaSolta = [...conversa.matchAll(RE_HORA)].some(m => lerHora(m[0], conversa.slice(m.index + m[0].length, m.index + m[0].length + 20)).some(([h, m2]) => h === +hh && m2 === +mi));
// temHora só vale se a hora estiver ligada à data pedida (ou se não houver data nenhuma, para o teste da hora sozinha).
const temHora = horaSolta && (!temData || parNaConversa(conversa));
if (!temData || !temHora) return fim('invalido', 'horário que não foi oferecido nem pedido na conversa');
return fim('ok');
""", (4460, 300))
escolha(A, "Resultado da validação", "passo", ["ok", "dados", "invalido"], (4700, 300))
pg(A, "Reservar o horário (trava de 5 min)", r"""
-- Duas conversas não pegam a mesma vaga: quem chega primeiro segura o horário por 5 minutos (as chamadas ao Google têm limite de 30 s) (o evento criado depois passa a aparecer na agenda).
WITH limpa AS (DELETE FROM reservas_horario WHERE criado < now() - interval '1 day'),
t AS (
  INSERT INTO reservas_horario (inicio, telefone, criado) VALUES ($1::timestamptz, $2::text, now())
  ON CONFLICT (inicio) DO UPDATE SET telefone = EXCLUDED.telefone, criado = now()
  WHERE reservas_horario.telefone = EXCLUDED.telefone OR reservas_horario.criado < now() - interval '5 minutes'
  RETURNING 1
)
SELECT EXISTS (SELECT 1 FROM t) AS reservado;
""", "[ $('Decidir a ação').first().json.inicio, $('Ler ficha e instruções (só a última responde)').first().json.telefone ]", (4940, 300))
se(A, "Conseguiu reservar?", cond("={{ $json.reservado }}", "true", typ="boolean"), (5180, 300))
http(A, "Conferir se o horário segue livre", "POST", GCAL + "/freeBusy", (5420, 200), cred="google", timeout=30000,
     onError="continueRegularOutput",
     body_expr="{ timeMin: $('Decidir a ação').first().json.inicio, timeMax: new Date(new Date($('Decidir a ação').first().json.inicio).getTime() + __DURACAO_MS__).toISOString(), timeZone: '" + TZ + "', items: [{ id: '__CALENDARIO__' }] }")
code(A, "Horário livre?", r"""
const ia = $('Decidir a ação').first().json;
const r = $input.first().json || {};
const prim = (r.calendars && r.calendars['__CALENDARIO__']) || {};
const busy = prim.busy;
const ini = new Date(ia.inicio);
let passo;
if (!Array.isArray(busy) || (Array.isArray(prim.errors) && prim.errors.length) || isNaN(ini.getTime())) passo = 'erro';
else if (busy.length > 0) passo = 'ocupado';
else passo = ia.acao === 'remarcar' ? 'mudar' : 'criar';
return [{ json: { passo, inicio: ia.inicio, fim: isNaN(ini.getTime()) ? '' : new Date(ini.getTime() + __DURACAO_MS__).toISOString(), titulo: ia.titulo } }];
""", (4700, 300))
escolha(A, "Próximo passo na agenda", "passo", ["criar", "mudar", "ocupado", "erro"], (4940, 300))
http(A, "Criar a avaliação na agenda", "POST", GCAL_EVENTOS, (5180, 200), cred="google", timeout=30000,
     onError="continueRegularOutput",
     body_expr="{ summary: $json.titulo, location: $('Ler ficha e instruções (só a última responde)').first().json.local_avaliacao, "
               "description: 'Marcado pela __ASSISTENTE__ pelo WhatsApp. Paciente: ' + ($('Decidir a ação').first().json.nome_completo || $('Ler ficha e instruções (só a última responde)').first().json.nome_completo || $('Decidir a ação').first().json.nome_paciente || $('Ler ficha e instruções (só a última responde)').first().json.nome_paciente || '') + '. Telefone de contato: ' + ($('Decidir a ação').first().json.telefone_contato || $('Ler ficha e instruções (só a última responde)').first().json.telefone_contato || $('Ler ficha e instruções (só a última responde)').first().json.telefone) + '. WhatsApp: ' + $('Ler ficha e instruções (só a última responde)').first().json.telefone, "
               "start: { dateTime: $json.inicio, timeZone: '" + TZ + "' }, end: { dateTime: $json.fim, timeZone: '" + TZ + "' } }")
http(A, "Mudar a avaliação na agenda", "PATCH",
     "=" + GCAL_EVENTOS + "/{{ $('Ler ficha e instruções (só a última responde)').first().json.avaliacao_evento }}",
     (5180, 400), cred="google", timeout=30000, onError="continueRegularOutput",
     body_expr="{ summary: $json.titulo, start: { dateTime: $json.inicio, timeZone: '" + TZ + "' }, end: { dateTime: $json.fim, timeZone: '" + TZ + "' } }")
http(A, "Cancelar a avaliação na agenda", "DELETE",
     "=" + GCAL_EVENTOS + "/{{ $('Ler ficha e instruções (só a última responde)').first().json.avaliacao_evento }}",
     (4460, 600), cred="google", timeout=30000, onError="continueRegularOutput")

# Resultado: cada caminho monta o mesmo formato (mensagens, ficha, avisos para a equipe).
RESULTADO_JS = COMUM_JS + r"""
const TIPO = '__TIPO__';
const ia = $('Decidir a ação').first().json;
const f = $('Ler ficha e instruções (só a última responde)').first().json;
const j = $input.first().json || {};
const tel = f.telefone;
const nome = ia.nome_paciente || f.nome_paciente || f.nome || '';
const pend = (f.pendente || '').trim();
const quem = 'Paciente: ' + nome + ' (' + tel + ')';
const lg = 'pt';   // 24/11: só português
const F = FRASES[lg];
const espera = F.espera;
function quando(iso) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('pt-BR', { timeZone: '__FUSO__', day: '2-digit', month: '2-digit', hour: 'numeric', minute: '2-digit', hourCycle: 'h23' })
    .formatToParts(new Date(iso)).map(x => [x.type, x.value]));
  return p.day + '/' + p.month + ' às ' + Number(p.hour) + ':' + p.minute;
}
let m = [ia.mensagem1, ia.mensagem2, ia.mensagem3];
let aval = 'manter', aval_inicio = '', aval_texto = '', aval_evento = '', fechamento = '';
const avisos = [];
let aviso_humano = '', motivo_humano = '', complemento = '', recusas = 'manter';
let tipo = TIPO;
if (tipo === 'agenda') {
  if (j.error) tipo = 'falha';
  else if ((ia.acao === 'agendar' || ia.acao === 'remarcar') && !j.id) tipo = 'falha';   // Google não devolveu o evento
  else tipo = { agendar: 'marcado', remarcar: 'remarcado', cancelar: 'cancelado' }[ia.acao] || 'falha';
}
const verbo = { agendar: 'marcar', remarcar: 'remarcar', cancelar: 'cancelar' }[ia.acao] || ia.acao;
switch (tipo) {
  case 'humano': {
    // Pacote A (A1, 18/11): só deixa de avisar quando a mensagem nova é uma confirmação pura (ok, obrigada, valeu, 👍...).
    // Informação nova gera aviso (ou complemento, se o assunto é o mesmo do último aviso). Urgência sempre gera aviso novo.
    // Complementos: no máximo 1 a cada 15 minutos por paciente (Camila recebeu 5).
    const idade = f.ultimo_aviso_humano ? Date.now() - new Date(f.ultimo_aviso_humano).getTime() : Infinity;
    const idadeComp = f.ultimo_complemento ? Date.now() - new Date(f.ultimo_complemento).getTime() : Infinity;
    const urgente = ehUrgente(pend);
    const CONFIRMA = new Set(['ok', 'okay', 'okk', 'obrigado', 'obrigada', 'obg', 'muito', 'valeu', 'vlw', 'blz', 'beleza', 'certo',
      'combinado', 'thanks', 'thank', 'you', 'gracias', 'muchas', 'perfecto', 'vale']);
    const pal = norm(pend).replace(/[\u{1F44D}\u{1F64F}\u{1F3FB}-\u{1F3FF}️]/gu, ' ').replace(/[!.,;]+/g, ' ').split(/\s+/).filter(Boolean);
    const pura = !!pend && !pend.includes('?') && pal.every(w => CONFIRMA.has(w))
      && (pal.length === 0 || pal.some(w => !['muito', 'you', 'muchas'].includes(w)));
    if (!urgente && pura && idade < 15 * 60000) break;
    const GENERICAS = new Set(['paciente', 'clinica', 'fechada', 'aberta', 'suzana', 'passar', 'verificar', 'retorna', 'retorno',
      'abrir', 'quando', 'amanha', 'pediu', 'perguntou', 'pergunta', 'sobre', 'saber', 'equipe', 'informacao', 'nesta', 'dessa', 'desta']);
    const palavras = x => new Set(norm(x).split(/[^a-z0-9]+/).filter(w => w.length > 4 && !GENERICAS.has(w)));
    const pa = palavras(ia.motivo), pb = palavras(f.ultimo_motivo_humano);
    const comum = [...pa].filter(w => pb.has(w)).length;
    if (!urgente && idade < 90 * 60000 && pa.size && pb.size && comum / Math.min(pa.size, pb.size) >= 0.6) {
      if (pura || idadeComp < 15 * 60000) break;
      aviso_humano = 'sim'; complemento = 'sim';
      motivo_humano = f.ultimo_motivo_humano || ia.motivo || '';
      avisos.push('*Complemento do aviso anterior*\n' + quem + '\nMensagem nova: ' + pend + '\nMotivo: ' + ia.motivo);
      break;
    }
    aviso_humano = 'sim';
    motivo_humano = ia.motivo || '';
    avisos.push((urgente ? '*URGENTE: chamar uma pessoa agora*' : '*Chamar uma pessoa*') + '\n' + quem + '\nMensagem: ' + pend + '\nMotivo: ' + ia.motivo + '\n\nO que a __ASSISTENTE__ respondeu:\n' + m.filter(Boolean).join(' '));
    break;
  }
  case 'ja_marcada':
    m = F.ja_marcada(quandoLg(f.avaliacao_inicio, lg, f.avaliacao_texto)).concat(['']);
    break;
  case 'sem_avaliacao':
    m = [F.sem_avaliacao, '', ''];
    avisos.push('*Pedido de ' + ia.acao + ' sem avaliação registrada*\n' + quem + '\nMensagem: ' + pend + '\nConfira a agenda e responda o paciente.');
    break;
  case 'sem_agenda':
    m = [F.sem_agenda, '', ''];
    avisos.push('*Agenda do Google não respondeu*\n' + quem + '\nMensagem: ' + pend + '\nResponda o paciente com os horários.');
    break;
  case 'ocupado':
  case 'invalido': {
    // Pacote A (A2): conta as recusas seguidas na ficha. Na 1ª, explica (ou pede a data por extenso, se o problema foi
    // não reconhecer o dia); da 2ª em diante, não repete a recusa: diz que a equipe vai confirmar e avisa a equipe.
    const n = (Number(f.recusas_agenda) || 0) + 1;
    recusas = 'somar';
    const motivoTec = tipo === 'ocupado' ? 'horário ocupado na agenda' : (j.motivo || '-');
    const pedido = ia.inicio && !isNaN(new Date(ia.inicio).getTime()) ? quando(ia.inicio) : '(sem horário válido)';
    if (n >= 2) {
      m = [F.equipe, '', ''];
      if (n === 2 || (n - 2) % 3 === 0) {
        aviso_humano = 'sim';
        motivo_humano = 'Pedido de horário recusado ' + n + ' vezes seguidas';
        avisos.push('*Confirmar horário com o paciente (' + n + 'ª recusa seguida)*\n' + quem + '\nHorário pedido: ' + pedido +
          '\nMotivo técnico: ' + motivoTec + '\nMensagem: ' + pend + '\nO paciente recebeu: ' + F.equipe);
      }
    } else if (tipo === 'ocupado') m = [F.ocupado, F.outras, ''];
    else if (/conversa|sem horário válido/.test(j.motivo || '')) m = [F.formato, F.formato2, ''];
    else m = [F.invalido, F.outras, ''];
    break;
  }
  case 'dados':
    m = F.dados.concat(['']);
    break;
  case 'falha':
    m = [espera, '', ''];
    avisos.push('*Falha ao ' + verbo + ' na agenda*\n' + quem + (f.avaliacao_texto ? '\nAvaliação atual: ' + f.avaliacao_texto : '') + (ia.inicio ? '\nHorário pedido: ' + ia.inicio : '') + '\nO paciente recebeu: ' + espera);
    break;
  case 'marcado':
    aval = 'definir'; aval_inicio = ia.inicio; aval_texto = quando(ia.inicio); aval_evento = j.id || ''; recusas = 'zerar';
    fechamento = ia.fechamento;
    avisos.push('*Nova avaliação marcada*\n' + ia.titulo + '\nQuando: ' + aval_texto + '\n' + quem +
      '\nNome completo: ' + (ia.nome_completo || f.nome_completo || '-') + '\nTelefone de contato: ' + (ia.telefone_contato || f.telefone_contato || tel));
    break;
  case 'remarcado':
    aval = 'definir'; aval_inicio = ia.inicio; aval_texto = quando(ia.inicio); recusas = 'zerar';
    avisos.push('*Avaliação remarcada*\nDe: ' + f.avaliacao_texto + '\nPara: ' + aval_texto + '\n' + quem);
    break;
  case 'cancelado':
    aval = 'limpar'; recusas = 'zerar';
    avisos.push('*Avaliação cancelada*\n' + f.avaliacao_texto + '\n' + quem);
    break;
}
m = m.map(x => (x || '').trim());
// Avisos para a equipe primeiro: uma urgência não espera o "digitando" do paciente (revisão Codex).
const envios = avisos.map(a => ({ phone: f.aprovador, m1: a, sem_digitar: true }))
  .concat([{ phone: tel, m1: m[0], m2: m[1], m3: m[2] }]);
// Quanto tempo as mensagens deste turno levam para sair (o próximo turno espera, para a ordem não se misturar).
const envio_seg = envios.reduce((t, e) => t + [e.m1, e.m2, e.m3].filter(Boolean)
  .reduce((u, b) => u + (e.sem_digitar ? 1 : Math.min(50, Math.max(4, Math.round(String(b).length / 4)))) + 1, 0), 0);
return [{ json: {
  telefone: tel, pend, pend_bruto: f.pendente || '', texto: m.filter(Boolean).join(' '), id_msg: f.ultimo_id,
  envio_seg: Math.min(180, envio_seg), motivo_humano, recusas, complemento,
  nome_ia: ia.nome_paciente, trat_ia: ia.tratamento, nome_completo: ia.nome_completo, tel_contato: ia.telefone_contato,
  aval, aval_inicio, aval_texto, aval_evento, aviso_humano,
  fechamento, envios: JSON.stringify(envios)
} }];
"""
RES = {}
for tipo, pos in [("responder", (4460, -600)), ("humano", (4460, -400)), ("ja_marcada", (4460, -200)),
                  ("sem_avaliacao", (4460, 0)), ("ocupado", (5420, 600)), ("falha", (5180, 800)),
                  ("invalido", (4940, 500)), ("dados", (4940, 700)),
                  ("agenda", (5420, 300)), ("sem_agenda", (4460, 900))]:
    RES[tipo] = code(A, "Resultado · " + tipo, RESULTADO_JS.replace("__TIPO__", tipo), pos)

pg(A, "Salvar conversa e ficha", r"""
UPDATE pacientes SET
  conversa = ltrim(right(conversa || E'\nPaciente: ' || $2::text || E'\n__ASSISTENTE__: ' || $3::text, 11000), E'\n'),
  pendente = CASE WHEN ultimo_id = $4::text THEN '' ELSE replace(pendente, $5::text, '') END,
  nome_paciente = coalesce(nullif($6::text, ''), nome_paciente),
  tratamento = coalesce(nullif($7::text, ''), tratamento),
  nome_completo = coalesce(nullif($14::text, ''), nome_completo),
  telefone_contato = coalesce(nullif($15::text, ''), telefone_contato),
  ultimo_aviso_humano = CASE WHEN $16::text = 'sim' THEN now() ELSE ultimo_aviso_humano END,
  ultimo_motivo_humano = CASE WHEN $16::text = 'sim' THEN $18::text ELSE ultimo_motivo_humano END,
  ultimo_complemento = CASE WHEN $20::text = 'sim' THEN now() ELSE ultimo_complemento END,
  recusas_agenda = CASE $19::text WHEN 'zerar' THEN 0 WHEN 'somar' THEN coalesce(recusas_agenda, 0) + 1 ELSE recusas_agenda END,
  envio_ate = now() + make_interval(secs => $17::int),
  avaliacao_inicio = CASE $8::text WHEN 'definir' THEN $9::text WHEN 'limpar' THEN NULL ELSE avaliacao_inicio END,
  avaliacao_texto = CASE $8::text WHEN 'definir' THEN $10::text WHEN 'limpar' THEN NULL ELSE avaliacao_texto END,
  avaliacao_evento = CASE $8::text WHEN 'definir' THEN coalesce(nullif($11::text, ''), avaliacao_evento) WHEN 'limpar' THEN NULL ELSE avaliacao_evento END,
  atualizado = now()
WHERE telefone = $1::text
  AND ultimo_id IS NOT NULL   -- 24/11: #reiniciar no meio da resposta (ultimo_id vira NULL): descarta, não traz a conversa velha de volta
RETURNING telefone, ultimo_id, coalesce(avaliacao_evento, '') AS evento, $12::text AS fechamento, $13::text AS envios;
""", "[ $json.telefone, $json.pend, $json.texto, $json.id_msg, $json.pend_bruto, $json.nome_ia, $json.trat_ia, "
     "$json.aval, $json.aval_inicio, $json.aval_texto, $json.aval_evento, $json.fechamento, $json.envios, $json.nome_completo, $json.tel_contato, $json.aviso_humano, "
     "$json.envio_seg, $json.motivo_humano, $json.recusas, $json.complemento ]", (5700, 0))
code(A, "Montar os envios", "return JSON.parse($input.first().json.envios).map(e => ({ json: e }));", (5940, -100))
chamar_envio(A, "Enviar ao paciente e à equipe", (6180, -100))

# fechamento (antigo 1C): 1 minuto depois de marcar, se o paciente não respondeu
se(A, "Tem despedida para depois?", cond("={{ $json.fechamento }}", "notEmpty"), (5940, 200))
espera(A, "Esperar 1 minuto", 60, (6180, 200))
pg(A, "O paciente respondeu?", r"""
-- Sem mensagem nova (mesmo último id), sem pendência, sem a doutora ter assumido e com a mesma avaliação.
SELECT ultimo_id = $2::text AND pendente = '' AND coalesce(pausado_ate < now(), true)
       AND coalesce(avaliacao_evento, '') = $3::text AS sem_resposta
FROM pacientes WHERE telefone = $1::text;
""", "[ $('Salvar conversa e ficha').first().json.telefone, $('Salvar conversa e ficha').first().json.ultimo_id, $('Salvar conversa e ficha').first().json.evento ]", (6420, 200))
se(A, "Ninguém respondeu?", cond("={{ $json.sem_resposta }}", "true", typ="boolean"), (6660, 200))
code(A, "Montar a despedida", r"""
const s = $('Salvar conversa e ficha').first().json;
return [{ json: { phone: s.telefone, m1: s.fechamento } }];
""", (6900, 200))
chamar_envio(A, "Enviar a despedida", (7140, 200))

# ---------- ligações ----------
L = A.link
L("Mensagem recebida (Whapi)", "Normalizar mensagem")
L("Mensagem recebida (Whapi)", "Separar mensagens extras do pacote")
L("Separar mensagens extras do pacote", "Reenviar cada extra ao webhook")
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
L("Baixar o áudio", "Ajustar o nome do áudio")
L("Ajustar o nome do áudio", "Transcrever o áudio (OpenAI)")
L("Transcrever o áudio (OpenAI)", "Texto final da mensagem")
L("Tipo de mensagem", "Ler a foto (OpenAI)", out=3)
L("Ler a foto (OpenAI)", "Texto final da mensagem")
L("Tipo de mensagem", "Texto final da mensagem", out=4)
L("Tipo de mensagem", "Texto final da mensagem", out=5)
L("Texto final da mensagem", "Guardar na fila (ignora repetida)")
L("Guardar na fila (ignora repetida)", "Esperar 20 s (a pessoa pode mandar mais)")
L("Esperar 20 s (a pessoa pode mandar mais)", "Ver se o envio anterior terminou")
L("Ver se o envio anterior terminou", "Esperar o envio anterior terminar")
L("Esperar o envio anterior terminar", "Ler ficha e instruções (só a última responde)")
L("Ler ficha e instruções (só a última responde)", "Ver horários ocupados (90 dias)")
L("Ver horários ocupados (90 dias)", "Montar o pedido para a IA")
L("Montar o pedido para a IA", "Pedir a resposta (Claude)")
L("Pedir a resposta (Claude)", "Ler as mensagens e a ação")
L("Ler as mensagens e a ação", "Resposta válida?")
L("Resposta válida?", "Decidir a ação", out=0)
L("Resposta válida?", "Pedir de novo (Claude)", out=1)
L("Pedir de novo (Claude)", "Ler a segunda tentativa")
L("Ler a segunda tentativa", "Segunda resposta válida?")
L("Segunda resposta válida?", "Decidir a ação", out=0)
L("Segunda resposta válida?", "Falha técnica: avisar", out=1)
L("Falha técnica: avisar", "Enviar aviso de falha")
L("Falha técnica: avisar", "Registrar a falha na conversa")
L("Decidir a ação", "Qual ação?")
for i, t in enumerate(["responder", "humano", "ja_marcada", "sem_avaliacao"]):
    L("Qual ação?", RES[t], out=i)
L("Qual ação?", "Validar o pedido de agenda", out=4)
L("Validar o pedido de agenda", "Resultado da validação")
L("Resultado da validação", "Reservar o horário (trava de 5 min)", out=0)
L("Resultado da validação", RES["dados"], out=1)
L("Resultado da validação", RES["invalido"], out=2)
L("Reservar o horário (trava de 5 min)", "Conseguiu reservar?")
L("Conseguiu reservar?", "Conferir se o horário segue livre", out=0)
L("Conseguiu reservar?", RES["ocupado"], out=1)
L("Qual ação?", "Cancelar a avaliação na agenda", out=5)
L("Qual ação?", RES["sem_agenda"], out=6)
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

SAIDA = PASTA / "gerados" / SLUG
SAIDA.mkdir(parents=True, exist_ok=True)
for fluxo, arq in ((E, "envio.json"), (A, "atendimento.json")):
    nomes = {n["name"] for n in fluxo.nodes}
    for a, v in fluxo.conns.items():
        assert a in nomes, a
        for saida in v["main"]:
            for c in saida:
                assert c["node"] in nomes, c["node"]
    (SAIDA / arq).write_text(json.dumps(fluxo.json(), ensure_ascii=False, indent=1), encoding="utf-8")
    print(SLUG + "/" + arq, len(fluxo.nodes), "nós")
print("Webhook: " + BASE_URL + "/webhook/<caminho em segredos.local.json>")
