# Teste LOCAL (sem custo, sem servidor, sem Anthropic, sem Clara) das ferramentas de teste corrigidas em 20/11/2026 (Pacote D3).
# Simula falha de SSH/SQL/webhook e confere que as ferramentas PARAM com erro claro, não dão nota à Clara por falha do teste,
# exigem a contagem completa, passam a senha só por ambiente e limpam as quatro tabelas (inclusive reservas) com segunda passada.
# Uso: python testar_ferramentas_teste.py
import importlib, json, os, sys, tempfile, types
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
falhas = []


def checar(ok, texto):
    print(("OK    " if ok else "FALHA ") + texto)
    if not ok:
        falhas.append(texto)


class Proc:
    def __init__(self, rc=0, out="", err=""):
        self.returncode, self.stdout, self.stderr = rc, out, err


# Todo sleep vira instantâneo (os testes simulam o servidor, não esperam).
import time
time.sleep = lambda s: None

# ---------------------------------------------------------------- paciente_simulado.py
os.environ.setdefault("ANTHROPIC_API_KEY", "x")
try:
    ps = importlib.import_module("paciente_simulado")
except Exception as e:   # sem .env/anthropic neste PC: usa um módulo de mentira só para importar
    print("(não consegui importar paciente_simulado de verdade:", type(e).__name__, e, ")")
    sys.exit(1)

chamadas = []


def fake_run_factory(codigos, saida=""):
    seq = list(codigos)

    def fake(cmd, **kw):
        chamadas.append((cmd, kw))
        rc = seq.pop(0) if len(seq) > 1 else seq[0]
        return Proc(rc, saida if rc == 0 else "", "" if rc == 0 else "ssh: connect to host: Connection timed out")
    return fake


# 1. SSH caindo sempre (255): erro claro depois das tentativas, nunca texto vazio
ps.subprocess.run = fake_run_factory([255])
try:
    ps.db("select 1")
    checar(False, "db: SSH 255 deve levantar erro")
except ps.ErroTeste as e:
    checar("ERRO DE LEITURA" in str(e) and "não é falha da Clara" in str(e), "db: SSH 255 vira ERRO DE LEITURA claro")
checar(len(chamadas) == 3, f"db: tentou 3 vezes quando o SSH não conecta (tentou {len(chamadas)})")

# 2. erro de SQL (código 3): não repete, levanta
chamadas.clear()
ps.subprocess.run = fake_run_factory([3])
try:
    ps.db("select x")
    checar(False, "db: erro SQL deve levantar")
except ps.ErroTeste:
    checar(len(chamadas) == 1, "db: erro de SQL (código 3) para na hora, sem repetir")
# comando remoto usa ON_ERROR_STOP e não carrega o valor da senha
cmd_remoto = chamadas[0][0][-1]
checar("ON_ERROR_STOP=1" in cmd_remoto and "$CLARA_DB_PASSWORD" in cmd_remoto, "db: psql com ON_ERROR_STOP e senha só como variável do servidor")

# 3. falha transitória e depois sucesso: devolve o resultado
chamadas.clear()
ps.subprocess.run = fake_run_factory([255, 0], saida="t\n")
checar(ps.db("select 1") == "t", "db: uma queda de SSH seguida de sucesso devolve o resultado")

# 4. resposta_da_clara: falha de leitura PROPAGA (não vira "sem resposta")
ps.db = lambda sql, tentativas=3: (_ for _ in ()).throw(ps.ErroTeste("ERRO DE LEITURA (teste)"))
try:
    r = ps.resposta_da_clara("554199900801", "m1")
    checar(False, f"resposta_da_clara: falha de leitura virou {r!r} em vez de erro")
except ps.ErroTeste:
    checar(True, "resposta_da_clara: falha de leitura propaga como erro (não vira SEM RESPOSTA)")

# 5. main completo com 2 perfis, um deles caindo no meio: rodada inválida, nenhuma nota gravada, limpeza das 4 tabelas
tmp = Path(tempfile.mkdtemp())
ps.AQUI = tmp
sqls = []


def db_fake(sql, tentativas=3):
    sqls.append(sql)
    if sql.startswith("select (select count(*)"):
        return "0"
    return ""


def rodar_fake(p):
    if p["tel"].endswith("802"):
        raise ps.ErroTeste("ERRO DE LEITURA (simulado): SSH caiu no meio")
    return {"paciente": p["nome"], "tel": p["tel"], "conversa": [("Paciente", "oi"), ("Clara", "olá")], "avisos": [], "ficha": "", "limpeza": "nenhuma avaliação sobrando",
            "avaliacao": {"nota": 8, "objetivo_atingido": True}}


ps.db, ps.rodar = db_fake, rodar_fake
sys.argv = ["x", "801", "802"]
try:
    ps.main()
    checar(False, "main: com uma thread falhando deveria sair com erro")
except SystemExit as e:
    checar(e.code == 2, f"main: thread que falhou deixa a rodada inválida (código de saída {e.code})")
arquivos = sorted(p.name for p in tmp.iterdir())
checar(any("INVALIDA" in a for a in arquivos) and "historico-notas.csv" not in arquivos, "main: relatório marcado INVALIDA e notas não entram no histórico")
checar(any("RODADA INVÁLIDA" in (tmp / a).read_text(encoding="utf-8") for a in arquivos if a.endswith(".md")), "main: relatório diz RODADA INVÁLIDA")
limpezas = [s for s in sqls if s.startswith("DELETE FROM pacientes")]
checar(len(limpezas) >= 2 and all("reservas_horario" in s and "mensagens_recebidas" in s and "saidas_teste" in s for s in limpezas),
       f"main: limpeza final nas 4 tabelas, em duas passadas ({len(limpezas)} limpezas)")
checar(all("554199900801" in s and "554199900802" in s and "554199900803" not in s for s in limpezas[-2:]), "main: limpeza só dos telefones da rodada")

# 6. rodada completa válida grava histórico
sqls.clear()
for f in tmp.iterdir():
    f.unlink()
ps.rodar = lambda p: rodar_fake({**p, "tel": "554199900801"})
sys.argv = ["x", "801", "802"]
try:
    ps.main()
    checar(True, "main: rodada completa termina sem erro")
except SystemExit as e:
    checar(False, f"main: rodada completa não deveria sair com erro (código {e.code})")
checar((tmp / "historico-notas.csv").exists(), "main: rodada completa grava o histórico de notas")

# 7. contagem incompleta e nota ausente
prob = ps.conferir([rodar_fake({"nome": "A", "tel": "1"})], [], 2)
checar(any("contagem incompleta" in x for x in prob), "conferir: 1 de 2 perfis é contagem incompleta")
semnota = rodar_fake({"nome": "A", "tel": "1"})
semnota["avaliacao"] = {"nota": None}
checar(any("sem nota" in x for x in ps.conferir([semnota], [], 1)), "conferir: avaliação ilegível invalida a rodada")

# ---------------------------------------------------------------- teste_n8n.py
n8 = importlib.import_module("teste_n8n")
n8.ENV = {"CLARA_DB_PASSWORD": "SENHA-FALSA-DO-TESTE"}
vistos = []


def run_n8(cmd, **kw):
    vistos.append((cmd, kw))
    return Proc(1, "", "docker: erro simulado")


n8.subprocess.run = run_n8
try:
    n8.sql("select 1")
    checar(False, "n8.sql: falha do docker deve levantar")
except n8.ErroTeste as e:
    checar("ERRO DE LEITURA" in str(e), "n8.sql: falha do docker/SQL vira ERRO DE LEITURA claro")
cmd, kw = vistos[0]
checar(not any("SENHA-FALSA" in a for a in cmd), "n8.sql: a senha NÃO aparece nos argumentos do processo")
checar(kw["env"].get("PGPASSWORD") == "SENHA-FALSA-DO-TESTE" and "PGPASSWORD" in cmd, "n8.sql: a senha vai pelo ambiente (-e PGPASSWORD sem valor)")

# main do n8: uma conversa cai, as outras terminam
sqls2 = []


def sql_fake(q):
    sqls2.append(q)
    if "from config where chave = 'prefixo_teste'" in q:
        return "554199900"
    if "chave = 'modo_teste'" in q:
        return "0"
    if q.startswith("select (select count(*)"):
        return "0"
    return ""


def rodar_n8_fake(k, nome, msgs, saida):
    if k == 3:
        raise n8.ErroTeste("ERRO DE LEITURA (simulado)")
    for i, m in enumerate(msgs, 1):
        saida.append({"conversa": nome, "ordem": i, "paciente": str(m), "resposta": "ok"})


n8.sql, n8.rodar = sql_fake, rodar_n8_fake
n8.iniciar = lambda: None
gravados = {}
real_open = open


def open_fake(path, mode="r", *a, **kw):
    if str(path).startswith("/root/"):
        path = str(tmp / Path(str(path)).name)
    return real_open(path, mode, *a, **kw)


n8.open = open_fake
try:
    n8.main()
    checar(False, "n8.main: com conversa falhando deveria sair com erro")
except SystemExit as e:
    checar(e.code == 2, f"n8.main: thread que falhou deixa a rodada inválida (código {e.code})")
checar((tmp / "teste-n8n-resultado-INVALIDO.json").exists() and not (tmp / "teste-n8n-resultado.json").exists(), "n8.main: resultado gravado como INVALIDO")
dados = json.loads((tmp / "teste-n8n-resultado-INVALIDO.json").read_text(encoding="utf-8"))
checar(dados["valida"] is False and any("contagem incompleta" in e for e in dados["erros"]), "n8.main: aponta contagem incompleta e o motivo")
checar(n8.contar_esperado() == 56, f"n8: contagem esperada é {n8.contar_esperado()} casos (56; o C6 envia 3 mensagens num caso só)")
lim = [q for q in sqls2 if q.startswith("DELETE FROM pacientes")]
checar(len(lim) >= 3 and all("reservas_horario" in q for q in lim), f"n8.main: limpeza com reservas, no início e em duas passadas no fim ({len(lim)} limpezas)")

# rodada n8 completa e válida
(tmp / "teste-n8n-resultado-INVALIDO.json").unlink()
n8.rodar = lambda k, nome, msgs, saida: [saida.append({"conversa": nome, "ordem": i, "paciente": "x", "resposta": "ok"}) for i, _ in enumerate(msgs, 1)]
try:
    n8.main()
    checar((tmp / "teste-n8n-resultado.json").exists(), "n8.main: rodada completa grava o resultado válido")
except SystemExit as e:
    checar(False, f"n8.main: rodada completa não deveria falhar (código {e.code})")

print()
print("RESULTADO:", "TUDO CERTO" if not falhas else f"{len(falhas)} FALHA(S)")
sys.exit(1 if falhas else 0)
