#!/usr/bin/env python3
"""Insere o Google Tag Manager em todos os .html de uma pasta.

Uso:  python adicionar-gtm.py CAMINHO_DA_PASTA
Pode rodar mais de uma vez: arquivos que já têm o GTM são ignorados.
"""
import re, sys
from pathlib import Path

GTM_ID = "GTM-KPX8THWP"

HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','%s');</script>
<!-- End Google Tag Manager -->""" % GTM_ID

BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->""" % GTM_ID

def main(pasta):
    for f in sorted(Path(pasta).rglob("*.html")):
        with open(f, encoding="utf-8", newline="") as fh:   # newline="" preserva CRLF/LF
            txt = fh.read()
        if GTM_ID in txt:
            print(f"já tem GTM, ignorado: {f.name}"); continue
        nl = "\r\n" if "\r\n" in txt else "\n"
        h = re.search(r"<head[^>]*>", txt, re.I)
        b = re.search(r"<body[^>]*>", txt, re.I)
        if not (h and b):
            print(f"sem <head>/<body>, ignorado: {f.name}"); continue
        # insere o body primeiro (posição mais adiante) para não deslocar o índice do head
        txt = txt[:b.end()] + nl + BODY.replace("\n", nl) + txt[b.end():]
        txt = txt[:h.end()] + nl + HEAD.replace("\n", nl) + txt[h.end():]
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(txt)
        print(f"GTM adicionado: {f.name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python adicionar-gtm.py CAMINHO_DA_PASTA")
    main(sys.argv[1])
