# Monta o SQL que prepara (ou atualiza) o banco de UMA clínica: tabelas + tabela config.
# Uso: python preparar_banco.py <slug>   (lê clientes/<slug>/clinica.json, instruções e base)
# Saída: gerados/<slug>/banco.sql (fora do Git). Rodar dentro do banco da clínica, como dono (não como <banco>_app):
#   docker compose exec -T postgres psql -U <dono> -d <banco> < banco.sql
# Pode rodar de novo quando mudar instruções, base ou config: guarda a versão anterior com data.
import json, pathlib, sys, datetime

PASTA = pathlib.Path(__file__).parent
RAIZ = PASTA.parent.parent
SLUG = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Uso: python preparar_banco.py <slug>")
DIR = RAIZ / "clientes" / SLUG
CLI = json.loads((DIR / "clinica.json").read_text(encoding="utf-8"))
assert CLI.get("slug") == SLUG, "slug do clinica.json diferente do nome da pasta"


def lit(texto):
    """Texto entre $tag$ ... $tag$. A tag não pode aparecer no texto nem se formar na emenda com o fechamento
    (texto terminado em '$k', por exemplo): o primeiro fechamento tem que ser o do fim (revisão Codex 17/11)."""
    n = 0
    while True:
        fecha = "$k" + str(n) + "$"
        if fecha not in texto and (texto + fecha).find(fecha) == len(texto):
            return fecha + texto + fecha
        n += 1


import re
if not re.fullmatch(r"[a-z][a-z0-9_]{2,62}", CLI["banco"]):
    sys.exit("banco precisa ter só letras minúsculas, números e _")
PERMITIDAS = {"aprovador", "local_avaliacao", "modelo", "modo_teste", "prefixo_teste", "numeros_keshion"}
valores = {k: str(v) for k, v in CLI["config_no_banco"].items() if not k.startswith("_")}
if set(valores) - PERMITIDAS:
    sys.exit("config_no_banco tem chaves desconhecidas: " + ", ".join(sorted(set(valores) - PERMITIDAS)))
for chave, campo in (("_instrucoes", "instrucoes"), ("_base", "base")):
    arq = DIR / CLI["arquivos"][campo]
    if not arq.exists():
        sys.exit("Falta " + str(arq))
    valores[chave] = arq.read_text(encoding="utf-8").strip()
# #reiniciar apaga a ficha sem cancelar a agenda: só existe na demo e na clínica de teste (decisão de 17/11).
SO_DEMO = {"clinica-demo", "clinica-teste"}
if SLUG not in SO_DEMO and valores.get("numeros_keshion", "").strip():
    sys.exit("numeros_keshion precisa ficar vazio em " + SLUG + ": #reiniciar só existe na demo")
for k, v in valores.items():
    if "PREENCHER" in v:
        sys.exit("config_no_banco." + k + " ainda está para preencher em clientes/" + SLUG + "/clinica.json")

hoje = datetime.date.today().strftime("%Y%m%d")
sql = ["-- Banco da clínica " + SLUG + " (" + CLI["banco"] + "). Gerado por preparar_banco.py em " + hoje + ".",
       "-- Rodar com: psql -v ON_ERROR_STOP=1 ... -d " + CLI["banco"] + " < banco.sql",
       "\\set ON_ERROR_STOP on",
       "BEGIN;",
       # Trava: aplicado no banco errado, para antes de escrever qualquer coisa (revisão Codex 17/11).
       "DO $trava$ BEGIN IF current_database() <> '" + CLI["banco"] + "' THEN RAISE EXCEPTION "
       "'Este SQL é da clínica " + SLUG + " (banco " + CLI["banco"] + "), não de %%', current_database(); END IF; END $trava$;".replace("%%", "%"),
       (PASTA / "schema-clara.sql").read_text(encoding="utf-8").strip(), ""]
for k, v in valores.items():
    if k in ("_instrucoes", "_base"):   # guarda a versão anterior, se for diferente
        sql.append("INSERT INTO config (chave, valor) SELECT '" + k + "_anterior_" + hoje + "', valor FROM config "
                   "WHERE chave = '" + k + "' AND valor <> " + lit(v) + " ON CONFLICT (chave) DO NOTHING;")
    sql.append("INSERT INTO config (chave, valor) VALUES ('" + k + "', " + lit(v) + ") "
               "ON CONFLICT (chave) DO UPDATE SET valor = EXCLUDED.valor;")
# Usuário do dia a dia (<banco>_app, o que o n8n usa): lê e grava linhas, não muda a estrutura e só lê a config.
# O dono (<banco>) fica só para instalar. Se o usuário _app ainda não existir, este bloco não faz nada.
APP = CLI["banco"] + "_app"
sql.append("DO $permissoes$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '" + APP + "') THEN\n"
           "  GRANT CONNECT ON DATABASE " + CLI["banco"] + " TO " + APP + ";\n"
           "  GRANT USAGE ON SCHEMA public TO " + APP + ";\n"
           "  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO " + APP + ";\n"
           "  REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON config FROM " + APP + ";\n"
           "  GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO " + APP + ";\n"
           "END IF; END $permissoes$;")
sql.append("COMMIT;")
saida = PASTA / "gerados" / SLUG
saida.mkdir(parents=True, exist_ok=True)
(saida / "banco.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
print(SLUG + "/banco.sql:", ", ".join(sorted(valores)))
