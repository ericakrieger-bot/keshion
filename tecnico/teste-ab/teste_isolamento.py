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
             "senha": ENV["CLARA_DB_PASSWORD"], "assistente": "Clara", "nome": "Ana", "trat": "clareamento", "codigo": "GIRASSOL"},
    "teste": {"url": SERVIDOR + sys.argv[2], "canal": "TESTE-ISOLAMENTO", "banco": "clinica_teste",
              "usuario": "clinica_teste", "senha": ENV["CLINICA_TESTE_DB_PASSWORD"], "assistente": "Teste",
              "nome": "Bruno", "trat": "implante", "codigo": "CATAVENTO"},
}
OUTRA = {"demo": "teste", "teste": "demo"}


def sql(c, q):
    r = subprocess.run(["docker", "compose", "exec", "-T", "-e", "PGPASSWORD=" + c["senha"], "postgres", "psql",
                        "-h", "localhost", "-U", c["usuario"], "-d", c["banco"], "-At", "-c", q],
                       cwd="/opt/keshion", capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0 or "ERROR" in r.stderr:   # erro de consulta não pode parecer ficha vazia
        raise RuntimeError("SQL falhou em " + c["banco"] + ": " + r.stderr.strip()[:300])
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
        # Exclusividade: se outro teste mexeu neste número nos últimos 15 min, não apaga nada e para.
        if sql(c, f"select count(*) from pacientes where telefone = '{TEL}' and atualizado > now() - interval '15 minutes'") != "0":
            sys.exit("O número " + TEL + " foi usado nos últimos 15 minutos em " + c["banco"] + ": outro teste rodando? Abortado.")
    limpar()
    try:
        rodar()
    finally:
        limpar()   # mesmo se der erro ou for interrompido


def rodar():
    falhas = []
    def checar(ok, texto):
        print(("OK    " if ok else "FALHA ") + texto, flush=True)
        if not ok:
            falhas.append(texto)

    # 1. Mesmo telefone e MESMO id de mensagem nas duas clínicas, assuntos diferentes.
    mid1 = f"iso-{RODADA}-1"
    for c in CLINICAS.values():
        enviar(c, mid1, f"Oi, meu nome é {c['nome']}, quero saber sobre {c['trat']}. Vim por indicação, o código da indicação é {c['codigo']}")
    checar(esperar(mid1, 1) == set(CLINICAS), "as duas clínicas responderam à 1ª mensagem (mesmo id não foi tratado como repetido)")

    # 2. Pergunta de memória: cada uma deve lembrar só do próprio paciente.
    mid2 = f"iso-{RODADA}-2"
    for c in CLINICAS.values():
        enviar(c, mid2, "Você lembra qual é o meu nome e o código da indicação que eu te passei?")
    checar(esperar(mid2, 2) == set(CLINICAS), "as duas clínicas responderam à 2ª mensagem")

    # 3. Canal de uma clínica no webhook da outra, nos dois sentidos: tem que ser ignorado (nem id guardado).
    antes = {k: ficha(c).get("conversa") or "" for k, c in CLINICAS.items()}
    for k, c in CLINICAS.items():
        enviar(c, f"iso-{RODADA}-3{k}", "Mensagem com canal errado", canal=CLINICAS[OUTRA[k]]["canal"])
    time.sleep(20)
    for k, c in CLINICAS.items():
        ids = sql(c, f"select count(*) from mensagens_recebidas where id like 'iso-{RODADA}-3%'")
        checar((ficha(c).get("conversa") or "") == antes[k] and ids == "0",
               f"{k}: mensagem com canal da outra clínica ignorada (sem resposta e sem id guardado)")

    time.sleep(10)
    for k, c in CLINICAS.items():
        o = CLINICAS[OUTRA[k]]
        f = ficha(c)
        conv = f.get("conversa") or ""
        saidas = sql(c, f"select coalesce(string_agg(texto, ' | '), '') from saidas_teste where telefone = '{TEL}'")
        ultima = conv.rsplit("\n" + c["assistente"] + ": ", 1)[-1]
        print(f"\n[{k}] ficha: nome={f.get('nome_paciente')} tratamento={f.get('tratamento')}\n[{k}] última resposta: {ultima}", flush=True)
        checar(c["nome"] in conv and c["trat"] in conv.lower(), f"{k}: conversa tem o próprio paciente")
        checar(o["nome"] not in conv and o["codigo"] not in conv.upper(), f"{k}: conversa não tem nome nem código do paciente da outra clínica")
        checar(c["codigo"] in ultima.upper() and o["nome"] not in ultima and o["codigo"] not in ultima.upper(),
               f"{k}: resposta de memória lembra o próprio código e nada da outra clínica")
        checar(("\n" + c["assistente"] + ": ") in conv, f"{k}: conversa registrada com o nome da assistente ({c['assistente']})")
        checar(bool(saidas) and o["nome"] not in saidas and o["codigo"] not in saidas.upper(), f"{k}: saídas de teste só no próprio banco, sem dados da outra")
        checar((f.get("nome_paciente") or "") in ("", c["nome"]), f"{k}: ficha com o nome certo")

    print("\nRESULTADO:", "PASSOU" if not falhas else f"{len(falhas)} FALHA(S)", flush=True)
    if falhas:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
