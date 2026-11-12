# Compara o teste do n8n (teste-n8n-resultado.json) com o Haiku da rodada 2 do A/B.
# Uso: python comparar_n8n.py teste-n8n-resultado.json  -> gera relatorio-n8n.md
import json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
n8n = json.load(open(sys.argv[1], encoding="utf-8"))
ab = {(l["conversa"], l["ordem"]): l for l in json.load(open(AQUI / "resultado-20261111-2044.json", encoding="utf-8"))
      if l["modelo"] == "claude-haiku-5.5"}

linhas = ["# Passo 8 · Clara no n8n x Haiku da rodada 2 (Make/A/B)", "",
          "Teste rodado pelo fluxo inteiro do n8n (fila, ficha, Google Agenda real, ações), em modo teste.",
          "No A/B a data era fixa (11/11, 10h30) e a agenda inventada; aqui a data e a agenda são reais,",
          "então os horários oferecidos mudam. Compare tom, regras e ações.", ""]
atual = None
for r in n8n["respostas"]:
    if r["conversa"] != atual:
        atual = r["conversa"]
        linhas += ["", "## " + atual, ""]
    a = ab.get((r["conversa"], r["ordem"]), {})
    ficha = ", ".join(f"{k}: {r[k]}" for k in ("nome_ficha", "tratamento", "avaliacao") if r.get(k))
    linhas += [f"**{r['ordem']}. Paciente:** {r['paciente']}", "",
               f"- **n8n** ({r['segundos']} s): {r['resposta']}",
               f"- **A/B rodada 2:** {(a.get('resposta') or '').replace(chr(10), ' ')}  _(ação: {a.get('acao', '')})_",
               f"- Ficha depois: {ficha or '(vazia)'}", ""]
linhas += ["", "## Avisos que foram para o aprovador", ""]
for v in n8n["avisos"]:
    linhas += ["- " + v["texto"].replace("\n", " · "), ""]
saida = AQUI / "relatorio-n8n.md"
saida.write_text("\n".join(linhas), encoding="utf-8")
print("Relatório:", saida, "|", len(n8n["respostas"]), "respostas,", len(n8n["avisos"]), "avisos")
