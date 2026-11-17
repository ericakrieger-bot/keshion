# Teste de isolamento entre clínicas: o MESMO telefone (e o mesmo id de mensagem) conversa com duas
# clínicas ao mesmo tempo, e cada uma só pode enxergar a própria conversa.
# Roda NO SERVIDOR: python3 teste_isolamento.py <caminho webhook demo> <caminho webhook clinica-teste>
# Usa o número fictício 554199900777 (prefixo de teste: nada sai pelo WhatsApp) e apaga tudo no fim.
import json, subprocess, sys, time, urllib.request

SERVIDOR = "https://n8n.169-58-41-107.sslip.io/webhook/"
ENV = dict(l.split("=", 1) for l in open("/opt/keshion/.env").read().splitlines() if "=" in l)
TEL = "554199900777"
RODADA = time.strftime("%Y%m%d%H%M%S")
CLINICAS = {
    "demo": {"url": SERVIDOR + sys.argv[1], "canal": "GRNLTR-4K8ZF", "banco": "clara", "usuario": "clara",
             "senha": ENV["CLARA_DB_PASSWORD"], "assistente": "Clara", "nome": "Ana", "trat": "clareamento"},
    "teste": {"url": SERVIDOR + sys.argv[2], "canal": "TESTE-ISOLAMENTO", "banco": "clinica_teste",
              "usuario": "clinica_teste", "senha": ENV["CLINICA_TESTE_DB_PASSWORD"], "assistente": "Teste",
              "nome": "Bruno", "trat": "implante"},
}
OUTRA = {"demo": "teste", "teste": "demo"}


def sql(c, q):
    r = subprocess.run(["docker", "compose", "exec", "-T", "-e", "PGPASSWORD=" + c["senha"], "postgres", "psql",
                        "-h", "localhost", "-U", c["usuario"], "-d", c["banco"], "-At", "-c", q],
                       cwd="/opt/keshion", capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return r.stdout.strip()


def ficha(c):
    s = sql(c, f"select row_to_json(p) from pacientes p where telefone = '{TEL}'")
    return json.loads(s) if s else {}


def enviar(c, mid, texto, canal=None):
    corpo = {"channel_id": canal or c["canal"], "event": {"type": "messages", "event": "post"},
             "messages": [{"id": mid, "from_me": False, "type": "text", "chat_id": TEL + "@s.whatsapp.net",
                           "from": TEL, "from_name": "Teste isolamento", "source": "mobile", "text": {"body": texto}}]}
    urllib.request.urlopen(urllib.request.Request(c["url"], json.dumps(corpo, ensure_ascii=False).encode("utf-8"),
                                                  {"Content-Type": "application/json; charset=utf-8"}), timeout=30)


def limpar():
    for c in CLINICAS.values():
        sql(c, f"DELETE FROM pacientes WHERE telefone = '{TEL}'; DELETE FROM mensagens_recebidas WHERE telefone = '{TEL}'; "
               f"DELETE FROM saidas_teste WHERE telefone = '{TEL}' OR texto LIKE '%({TEL})%';")


def esperar(mid, voltas):
    t0 = time.time()
    feitas = set()
    while time.time() - t0 < 150 and len(feitas) < len(CLINICAS):
        time.sleep(4)
        for k, c in CLINICAS.items():
            f = ficha(c)
            if f.get("ultimo_id") == mid and f.get("pendente", "x") == "" and \
                    (f.get("conversa") or "").count("Paciente: ") >= voltas:
                feitas.add(k)
    return feitas


def main():
    for c in CLINICAS.values():   # segurança: só roda se o número for de teste nas duas clínicas
        assert TEL.startswith(sql(c, "select valor from config where chave = 'prefixo_teste'") or "x"), c["banco"]
    limpar()
    falhas = []
    def checar(ok, texto):
        print(("OK    " if ok else "FALHA ") + texto, flush=True)
        if not ok:
            falhas.append(texto)

    # 1. Mesmo telefone e MESMO id de mensagem nas duas clínicas, assuntos diferentes.
    mid1 = f"iso-{RODADA}-1"
    for c in CLINICAS.values():
        enviar(c, mid1, f"Oi, meu nome é {c['nome']} e quero saber sobre {c['trat']}")
    checar(esperar(mid1, 1) == set(CLINICAS), "as duas clínicas responderam à 1ª mensagem (mesmo id não foi tratado como repetido)")

    # 2. Pergunta de memória: cada uma deve lembrar só do próprio paciente.
    mid2 = f"iso-{RODADA}-2"
    for c in CLINICAS.values():
        enviar(c, mid2, "Você lembra qual é o meu nome e o que eu queria?")
    checar(esperar(mid2, 2) == set(CLINICAS), "as duas clínicas responderam à 2ª mensagem")

    # 3. Mensagem com o canal da demo enviada ao webhook da clínica de teste: deve ser ignorada.
    antes = ficha(CLINICAS["teste"]).get("conversa") or ""
    enviar(CLINICAS["teste"], f"iso-{RODADA}-3", "Mensagem com canal errado", canal=CLINICAS["demo"]["canal"])
    time.sleep(20)
    checar((ficha(CLINICAS["teste"]).get("conversa") or "") == antes and "canal errado" not in (ficha(CLINICAS["demo"]).get("conversa") or ""),
           "mensagem com canal de outra clínica ignorada")

    time.sleep(10)
    for k, c in CLINICAS.items():
        o = CLINICAS[OUTRA[k]]
        f = ficha(c)
        conv = f.get("conversa") or ""
        saidas = sql(c, f"select coalesce(string_agg(texto, ' | '), '') from saidas_teste where telefone = '{TEL}'")
        ultima = conv.rsplit("\n" + c["assistente"] + ": ", 1)[-1]
        print(f"\n[{k}] ficha: nome={f.get('nome_paciente')} tratamento={f.get('tratamento')}\n[{k}] última resposta: {ultima}", flush=True)
        checar(c["nome"] in conv and c["trat"] in conv.lower(), f"{k}: conversa tem o próprio paciente")
        checar(o["nome"] not in conv and o["trat"] not in conv.lower(), f"{k}: conversa não tem nada da outra clínica")
        checar(c["trat"] in ultima.lower() and o["nome"] not in ultima and o["trat"] not in ultima.lower(),
               f"{k}: resposta de memória lembra o próprio tratamento e nada da outra clínica")
        checar(("\n" + c["assistente"] + ": ") in conv, f"{k}: conversa registrada com o nome da assistente ({c['assistente']})")
        checar(bool(saidas) and o["nome"] not in saidas, f"{k}: saídas de teste só no próprio banco, sem dados da outra")
        checar((f.get("nome_paciente") or "") in ("", c["nome"]), f"{k}: ficha com o nome certo")

    limpar()
    print("\nRESULTADO:", "PASSOU" if not falhas else f"{len(falhas)} FALHA(S)", flush=True)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
