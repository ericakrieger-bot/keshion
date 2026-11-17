# Monta o SQL que prepara (ou atualiza) o banco de UMA clínica: tabelas + tabela config.
# Uso: python preparar_banco.py <slug>   (lê clientes/<slug>/clinica.json, instruções e base)
# Saída: gerados/<slug>/banco.sql (fora do Git). Rodar dentro do banco da clínica, como dono:
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
    """Texto entre $tag$ ... $tag$, com uma tag que não aparece no texto."""
    tag = "k"
    while ("$" + tag + "$") in texto:
        tag += "k"
    return "$" + tag + "$" + texto + "$" + tag + "$"


valores = {k: str(v) for k, v in CLI["config_no_banco"].items() if not k.startswith("_")}
for chave, campo in (("_instrucoes", "instrucoes"), ("_base", "base")):
    arq = DIR / CLI["arquivos"][campo]
    if not arq.exists():
        sys.exit("Falta " + str(arq))
    valores[chave] = arq.read_text(encoding="utf-8").strip()
for k, v in valores.items():
    if "PREENCHER" in v:
        sys.exit("config_no_banco." + k + " ainda está para preencher em clientes/" + SLUG + "/clinica.json")

hoje = datetime.date.today().strftime("%Y%m%d")
sql = ["-- Banco da clínica " + SLUG + " (" + CLI["banco"] + "). Gerado por preparar_banco.py em " + hoje + ".",
       "BEGIN;",
       (PASTA / "schema-clara.sql").read_text(encoding="utf-8").strip(), ""]
for k, v in valores.items():
    if k in ("_instrucoes", "_base"):   # guarda a versão anterior, se for diferente
        sql.append("INSERT INTO config (chave, valor) SELECT '" + k + "_anterior_" + hoje + "', valor FROM config "
                   "WHERE chave = '" + k + "' AND valor <> " + lit(v) + " ON CONFLICT (chave) DO NOTHING;")
    sql.append("INSERT INTO config (chave, valor) VALUES ('" + k + "', " + lit(v) + ") "
               "ON CONFLICT (chave) DO UPDATE SET valor = EXCLUDED.valor;")
sql.append("COMMIT;")
saida = PASTA / "gerados" / SLUG
saida.mkdir(parents=True, exist_ok=True)
(saida / "banco.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
print(SLUG + "/banco.sql:", ", ".join(sorted(valores)))
