"""Gera site/design-v1-visualizar.html a partir de site/design-v1.html.

Troca os arquivos ligados (CSS da marca, fontes, logos, foto) por versões embutidas,
para o HTML abrir sozinho com duplo clique. Rodar na pasta do projeto:
    python site/gerar-visualizar.py
"""
import base64
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def dados(caminho, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode((RAIZ / caminho).read_bytes()).decode())


html = (RAIZ / "site/design-v1.html").read_text(encoding="utf-8")
css = (RAIZ / "branding/kit/digital/keshion.css").read_text(encoding="utf-8")
# Fontes: o arquivo fica leve (cabe no painel do app) usando as mesmas fontes pelo Google Fonts.
# As fontes oficiais ficam em branding/kit/fontes/ e entram no site de verdade.
css = re.sub(r"@font-face\s*\{[^}]*\}", "", css, flags=re.S)
fontes = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@700&family=Inter:wght@400;500;600&display=swap">'
html = html.replace('<link rel="stylesheet" href="../branding/kit/digital/keshion.css">', fontes + "<style>" + css + "</style>")

for logo in ["logos/keshion-ai-fundo-claro.svg", "logos/simbolo.svg"]:
    html = html.replace("../branding/kit/" + logo, dados("branding/kit/" + logo, "image/svg+xml"))

# qualquer imagem em site/img/ referenciada como img/arquivo.jpg
for img in re.findall(r"img/[\w.-]+\.jpg", html):
    html = html.replace(img, dados("site/" + img, "image/jpeg"))

(RAIZ / "site/design-v1-visualizar.html").write_text(html, encoding="utf-8")
print("ok:", len(html), "bytes")
