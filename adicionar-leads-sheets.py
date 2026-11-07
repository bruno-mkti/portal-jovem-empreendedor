#!/usr/bin/env python3
"""Adiciona <script defer src="js/leads-sheets.js"> antes do </body>
nas páginas que têm o formulário #lead-form.

Uso:  python adicionar-leads-sheets.py CAMINHO_DA_PASTA
Pode rodar mais de uma vez: páginas que já têm o script são ignoradas.
"""
import sys
from pathlib import Path

TAG = '<script defer src="js/leads-sheets.js"></script>'

def main(pasta):
    for f in sorted(Path(pasta).rglob("*.html")):
        with open(f, encoding="utf-8", newline="") as fh:
            txt = fh.read()
        if 'id="lead-form"' not in txt:
            print(f"sem formulário, ignorado: {f.name}"); continue
        if "leads-sheets.js" in txt:
            print(f"já tem o script, ignorado: {f.name}"); continue
        pos = txt.lower().rfind("</body>")
        if pos == -1:
            print(f"sem </body>, ignorado: {f.name}"); continue
        nl = "\r\n" if "\r\n" in txt else "\n"
        txt = txt[:pos] + "    " + TAG + nl + txt[pos:]
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(txt)
        print(f"script adicionado: {f.name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python adicionar-leads-sheets.py portal-jovem-empreendedor")
    main(sys.argv[1])
