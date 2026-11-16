# Compara duas rodadas do teste das 56 mensagens no n8n (antes e depois de mudar as instruções).
# Uso: python comparar_antes_depois.py antes.json depois.json saida.md
import json, re, sys
from pathlib import Path

antes = json.load(open(sys.argv[1], encoding="utf-8"))["respostas"]
depois_tudo = json.load(open(sys.argv[2], encoding="utf-8"))
depois = depois_tudo["respostas"]
A = {(r["conversa"], r["ordem"]): r for r in antes}

VICIOS = {
    "aqui na clínica": r"aqui na cl[ií]nica",
    "ressalva de preço": r"valor exato a Dra\. Suzana define",
    "abre com Entendo": r"^Entendo",
    "elogio (Ótima escolha / Que bom que)": r"[ÓO]tima escolha|Que (bom|ótimo) que",
    "emoji": r"[\U0001F300-\U0001FAFF✨]",
    "mais de 1 exclamação": None,
    "frase de enchimento": r"Lá você encontra|é só me perguntar|Se tiver (alguma )?d[úu]vida",
    "travessão": r"—",
}

def conta(rs):
    c = {k: 0 for k in VICIOS}
    for r in rs:
        t = r["resposta"] or ""
        for k, rx in VICIOS.items():
            if rx is None:
                c[k] += t.count("!") > 1
            else:
                c[k] += bool(re.search(rx, t, re.M))
    return c

ca, cd = conta(antes), conta(depois)
L = ["# Clara: instruções antigas x novas (teste das 56 mensagens no n8n)", "",
     "Antes: rodada de 12/11/2026. Depois: instruções com as 8 mudanças de tom e a regra de nome completo e telefone ao marcar.", "",
     "## Quantas respostas tinham cada hábito", "", "| Hábito | Antes | Depois |", "|---|---|---|"]
L += [f"| {k} | {ca[k]} | {cd[k]} |" for k in VICIOS]
L += ["", f"Respostas: antes {len(antes)}, depois {len(depois)}. Sem resposta depois: "
      f"{sum(1 for r in depois if r['resposta'].startswith('(SEM RESPOSTA'))}.", ""]
atual = None
for r in depois:
    if r["conversa"] != atual:
        atual = r["conversa"]; L += ["", "## " + atual, ""]
    a = A.get((r["conversa"], r["ordem"]), {})
    ficha = ", ".join(f"{k}: {r[k]}" for k in ("nome_ficha", "tratamento", "avaliacao") if r.get(k))
    L += [f"**{r['ordem']}. Paciente:** {r['paciente']}", "",
          f"- **Antes:** {a.get('resposta', '')}",
          f"- **Depois:** {r['resposta']}",
          f"- Ficha depois: {ficha or '(vazia)'}", ""]
L += ["", "## Avisos para o aprovador (depois)", ""] + ["- " + v["texto"].replace("\n", " · ") for v in depois_tudo["avisos"]]
Path(sys.argv[3]).write_text("\n".join(L), encoding="utf-8")
print("hábitos antes:", ca); print("hábitos depois:", cd)
