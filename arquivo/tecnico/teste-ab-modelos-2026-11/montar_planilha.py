# Monta as linhas da aba "Teste A/B" a partir do último resultado, escondendo qual
# modelo escreveu cada coluna. O gabarito (letra = modelo) fica em gabarito.json.
import json
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
arquivo = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(AQUI.glob("resultado-*.json"))[-1]
dados = json.loads(arquivo.read_text(encoding="utf-8"))

modelos = sorted({d["modelo"] for d in dados})
letras = ["A", "B", "C", "D", "E", "F"][: len(modelos)]
embaralhados = modelos[:]
random.shuffle(embaralhados)
gabarito = dict(zip(letras, embaralhados))
nome_gabarito = sys.argv[2] if len(sys.argv) > 2 else "gabarito.json"
(AQUI / nome_gabarito).write_text(json.dumps(gabarito, ensure_ascii=False, indent=1), encoding="utf-8")

por_chave = {(d["modelo"], d["conversa"], d["ordem"]): d for d in dados}
base = [d for d in dados if d["modelo"] == modelos[0]]
linhas = [["Conversa", "Nº", "Paciente"] + [f"Resposta {l}" for l in letras] + ["Melhor (Erica)", "Observações da Erica", "Escolha do Claude", "Observações do Claude"]]
for d in base:
    linha = [d["conversa"], d["ordem"], d["paciente"]]
    for l in letras:
        r = por_chave.get((gabarito[l], d["conversa"], d["ordem"]), {})
        texto = r.get("resposta", "")
        if r.get("acao") and r["acao"] != "responder":
            texto += f"\n[ação: {r['acao']}]"
        if r.get("obs"):
            texto += f"\n[{r['obs']}]"
        linha.append(texto)
    linha += ["", "", "", ""]
    linhas.append(linha)

(AQUI / "linhas-planilha.json").write_text(json.dumps(linhas, ensure_ascii=False), encoding="utf-8")
print(f"{len(linhas) - 1} linhas prontas a partir de {arquivo.name}")
