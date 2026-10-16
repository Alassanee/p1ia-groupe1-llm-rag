"""
Ingestion — Tayba.
Lit les documents de data/corpus/ (.txt ou .pdf), nettoie, découpe en chunks,
et écrit data/chunks.json au format : [{id, texte, source, position}].

Lancer depuis la racine du projet :
    python -m src.ingestion.run
"""
import glob
import json
import os
import re

CORPUS_DIR = "data/corpus"
OUT = "data/chunks.json"
CHUNK_SIZE = 800      # caractères par chunk (à ajuster)
OVERLAP = 150         # chevauchement entre chunks


def read_txt(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_pdf(path: str) -> str:
    from pypdf import PdfReader
    return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)


def clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    morceaux, start = [], 0
    while start < len(text):
        morceaux.append(text[start:start + size])
        start += size - overlap
    return [m for m in morceaux if m.strip()]


def main() -> None:
    files = sorted(glob.glob(f"{CORPUS_DIR}/*.txt") + glob.glob(f"{CORPUS_DIR}/*.pdf"))
    if not files:
        print(f"⚠️  Aucun document dans {CORPUS_DIR}/. Ajoute les fichiers du corpus (démarches admin).")
        return

    out, cid = [], 0
    for path in files:
        raw = read_pdf(path) if path.lower().endswith(".pdf") else read_txt(path)
        texte = clean(raw)
        source = os.path.basename(path)
        for pos, ch in enumerate(chunk(texte)):
            out.append({"id": f"c{cid}", "texte": ch, "source": source, "position": pos})
            cid += 1

    os.makedirs("data", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(out)} chunks écrits dans {OUT} (depuis {len(files)} fichier(s)).")


if __name__ == "__main__":
    main()
