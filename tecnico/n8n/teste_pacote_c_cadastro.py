# Teste local (sem servidor, sem custo) do C7 (19/11): cadastro de clínica REAL com numeros_keshion vazio.
# Monta uma cópia temporária da pasta (clínica fictícia "clinica-real-teste", com segredo falso), roda gerar_fluxos.py e
# preparar_banco.py e confere: vazio passa; número preenchido fora da demo e do teste é recusado; PREENCHER é recusado.
# Uso (dentro de tecnico/n8n):  python teste_pacote_c_cadastro.py [caminho/de/outro/gerar_fluxos.py]
# (o argumento serve para ver o "antes", com o gerador antigo)
import json, os, pathlib, shutil, subprocess, sys, tempfile

AQUI = pathlib.Path(__file__).parent
RAIZ = AQUI.parent.parent
GERADOR = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "gerar_fluxos.py"
SLUG = "clinica-real-teste"
resultados = []


def confere(desc, ok, info=""):
    resultados.append(ok)
    print(("OK      " if ok else "FALHOU  ") + desc + ("" if ok else "  " + info))


def rodar(raiz, script, *args):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(raiz / "tecnico" / "n8n" / script), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    r.saida = (r.stdout or "") + (r.stderr or "")
    return r


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    (tmp / "tecnico" / "n8n").mkdir(parents=True)
    shutil.copy(GERADOR, tmp / "tecnico" / "n8n" / "gerar_fluxos.py")
    shutil.copy(AQUI / "preparar_banco.py", tmp / "tecnico" / "n8n" / "preparar_banco.py")
    shutil.copy(AQUI / "alerta-keshion.json", tmp / "tecnico" / "n8n" / "alerta-keshion.json")
    shutil.copy(AQUI / "schema-clara.sql", tmp / "tecnico" / "n8n" / "schema-clara.sql")
    (tmp / "tecnico" / "n8n" / "segredos.local.json").write_text(json.dumps({SLUG: {"webhook_path": "caminho-falso-so-para-teste"}}), encoding="utf-8")
    pasta = tmp / "clientes" / SLUG
    pasta.mkdir(parents=True)
    (pasta / "instrucoes.md").write_text("Instruções de teste.", encoding="utf-8")
    (pasta / "base.md").write_text("Base de teste.", encoding="utf-8")
    cli = json.loads((RAIZ / "clientes" / "clinica-teste" / "clinica.json").read_text(encoding="utf-8"))
    cli.pop("compartilha_para_teste", None)
    cli.update({"slug": SLUG, "banco": "clinica_real_teste", "nome_clinica": "Clínica real de teste", "nome_assistente": "Ana",
                "arquivos": {"instrucoes": "instrucoes.md", "base": "base.md"}})
    cli["fluxos"] = {"id_atendimento": "RealAtendimento1", "id_envio": "RealEnvio0000001"}
    cli["config_no_banco"]["numeros_keshion"] = ""        # como manda o roteiro de clínica nova
    cli["config_no_banco"]["modo_teste"] = "1"
    arq = pasta / "clinica.json"

    def gravar():
        arq.write_text(json.dumps(cli, ensure_ascii=False, indent=2), encoding="utf-8")

    gravar()
    r = rodar(tmp, "gerar_fluxos.py", SLUG)
    confere("C7 gerar_fluxos aceita numeros_keshion vazio em clínica real", r.returncode == 0, r.saida.strip()[-200:])
    gerados = tmp / "tecnico" / "n8n" / "gerados" / SLUG
    confere("C7 gerou envio.json e atendimento.json", (gerados / "envio.json").exists() and (gerados / "atendimento.json").exists())
    r = rodar(tmp, "preparar_banco.py", SLUG)
    confere("C7 preparar_banco aceita numeros_keshion vazio em clínica real", r.returncode == 0, r.saida.strip()[-200:])
    sql = gerados / "banco.sql"
    confere("C7 gerou banco.sql da clínica real", sql.exists() and "clinica_real_teste" in sql.read_text(encoding="utf-8"))

    cli["config_no_banco"]["numeros_keshion"] = "972584285541"
    gravar()
    r = rodar(tmp, "preparar_banco.py", SLUG)
    confere("C7 preparar_banco RECUSA número preenchido fora da demo e do teste", r.returncode != 0 and "numeros_keshion" in r.saida, r.saida.strip()[-200:])

    cli["config_no_banco"]["numeros_keshion"] = "PREENCHER"
    gravar()
    r = rodar(tmp, "gerar_fluxos.py", SLUG)
    confere("C7 gerar_fluxos recusa PREENCHER em numeros_keshion", r.returncode != 0 and "numeros_keshion" in r.saida, r.saida.strip()[-200:])

    cli["config_no_banco"]["numeros_keshion"] = ""
    cli["config_no_banco"]["aprovador"] = ""
    gravar()
    r = rodar(tmp, "gerar_fluxos.py", SLUG)
    confere("C7 outros campos vazios (aprovador) continuam recusados", r.returncode != 0 and "aprovador" in r.saida, r.saida.strip()[-200:])

ok = sum(resultados)
print(str(ok) + " de " + str(len(resultados)) + " testes do cadastro (C7) certos" + ("" if ok == len(resultados) else ", " + str(len(resultados) - ok) + " falharam"))
sys.exit(0 if ok == len(resultados) else 1)
