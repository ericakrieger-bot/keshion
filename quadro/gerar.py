# Gera o plano de ação em Markdown e o quadro em HTML a partir de tarefas.json.
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
dados = json.loads((AQUI / "tarefas.json").read_text(encoding="utf-8"))
NUM = {t["id"]: i for i, t in enumerate(dados["tarefas"], 1)}
import re
def refs(x):
    return re.sub(r"\bt\d{2}\b", lambda m: f"tarefa {NUM[m.group(0)]}" if m.group(0) in NUM else m.group(0), x)
TIPO = {"tarefa": "", "decisao": "Decisão: ", "marco": "Marco: "}

m = []
s = dados["sprint"]
m.append("# Plano de ação: sprint de validação (28/10 a 18/12/2026)\n")
m.append(f"> **Objetivo:** {s['objetivo']}")
m.append(f"> **Prazo do piloto:** {s['marco']['texto']}\n")
m.append("## Papéis (proposta, confirmar na reunião de alinhamento)\n")
for p in dados["papeis"]:
    m.append(f"- **{p['quem']}:** {p['texto']}")
m.append("\n## Como trabalhamos\n")
for c in dados["contexto"]:
    m.append(f"- {c}")
m.append("\n## Metas do sprint (placar)\n")
m.append("| Indicador | Meta até 18/12 |\n|---|---|")
for g in dados["metas"]:
    m.append(f"| {g['rotulo']} | {g.get('texto', g['meta'])} |")
for sem in dados["semanas"]:
    m.append(f"\n---\n\n## {sem['titulo']} ({sem['datas']}): {sem['tema']}\n")
    ts = [t for t in dados["tarefas"] if t["semana"] == sem["id"]]
    m.append("| # | Tarefa | Responsável | Prazo | Feito |\n|---|---|---|---|---|")
    for t in ts:
        m.append(f"| {NUM[t["id"]]} | {TIPO[t['tipo']]}{t['titulo']} | {' + '.join(t['resp'])} | {t['prazo']} | [ ] |")
    for t in ts:
        m.append(f"\n### {NUM[t["id"]]}. {TIPO[t['tipo']]}{t['titulo']}\n")
        m.append(f"**Responsável:** {' + '.join(t['resp'])} · **Prazo:** {t['prazo']}\n")
        m.append(f"**Por quê:** {refs(t['porque'])}\n")
        m.append("**Como fazer:**\n")
        for i, p in enumerate(t["passos"], 1):
            m.append(f"{i}. {refs(p)}")
        m.append(f"\n**Entregável:** {refs(t['entrega'])}  ")
        m.append(f"**Pronto quando:** {refs(t['pronto'])}  ")
        m.append(f"**Ferramentas:** {refs(t['ferramentas'])}")
m.append("\n---\n\n## Rotina fixa durante o sprint\n")
m.append("| Quando | O quê | Quem |\n|---|---|---|")
for r in dados["rotina"]:
    m.append(f"| {r['quando']} | {r['oque']} | {r['quem']} |")
(AQUI.parent / "plano-de-acao.md").write_text("\n".join(m) + "\n", encoding="utf-8")

html = (AQUI / "quadro-modelo.html").read_text(encoding="utf-8")
js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
(AQUI / "quadro.html").write_text(html.replace("/*DADOS*/null", js), encoding="utf-8")
print("ok", len(dados["tarefas"]), "tarefas")
