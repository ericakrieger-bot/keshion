import subprocess, shutil, os, pathlib
K = pathlib.Path(r"C:\Users\Erica Krieger-Akerma\Documents\Claude Code\keshion")
OUT = K/"comercial/sergio/materiais"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PRINT_CSS = """<style>
@page{size:A4 landscape;margin:10mm 11mm}
:root{color-scheme:light}
html,body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
nav,nav.toc,nav.sections,body::before{display:none!important}
.tbl,.chart,.road,.mapbox,.tablebox{overflow:visible!important}
table{font-size:11px!important}
tr,figure{break-inside:avoid}
.logo-dark{display:none!important}
h2,h3{break-after:avoid}
</style></head>"""
def pdf(src, dst):
    subprocess.run([CH,"--headless=new","--disable-gpu","--no-pdf-header-footer","--run-all-compositor-stages-before-draw","--virtual-time-budget=8000",
                    f"--print-to-pdf={dst}", pathlib.Path(src).as_uri()], check=True, capture_output=True, timeout=120)
def com_css(src, tmpname, dst):
    src = pathlib.Path(src); tmp = src.with_name(tmpname)
    html = src.read_text(encoding="utf-8")
    html = html.replace('data-theme="dark"','data-theme="light"').replace('src="logo-fundo-claro.svg"','src="../../branding/kit/logos/keshion-ai-fundo-claro.svg"')
    html = html.replace("</head>", PRINT_CSS, 1) if "</head>" in html else PRINT_CSS.replace("</head>","") + html
    tmp.write_text(html, encoding="utf-8")
    try: pdf(tmp, dst)
    finally: tmp.unlink()
com_css(K/"estrategia/canvas-page/startup-canvas.html", "_print-canvas.html", OUT/"01-startup-canvas-keshion.pdf")
shutil.copy(K/"comercial/piloto/keshion-piloto-clinicas-v2.pdf", OUT/"02-piloto-keshion-para-clinicas.pdf")
com_css(K/"pesquisa/concorrentes-odonto.html", "_print-conc.html", OUT/"03-concorrentes-odonto.pdf")
pdf(OUT/"fontes/04-mensagens-abordagem.html", OUT/"04-mensagens-de-convite-e-respostas.pdf")
pdf(OUT/"fontes/05-cliente-ideal-e-jornada.html", OUT/"05-cliente-ideal-e-jornada.pdf")
for f in sorted(OUT.glob("*.pdf")): print(f.name, f.stat().st_size//1024, "KB")
