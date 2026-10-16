"""
Embeddings & index — Fatima.
Lit data/chunks.json, encode les textes, sauvegarde l'index dans data/index/.

Lancer depuis la racine :
    python -m src.embeddings.build_index
"""
import json
import os

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
CHUNKS = "data/chunks.json"
INDEX_DIR = "data/index"


def main() -> None:
    with open(CHUNKS, encoding="utf-8") as f:
        chunks = json.load(f)

    model = SentenceTransformer(MODEL)
    # NB : les modèles e5 attendent le préfixe "passage: " pour les documents.
    textes = [f"passage: {c['texte']}" for c in chunks]
    emb = model.encode(textes, normalize_embeddings=True, show_progress_bar=True)

    os.makedirs(INDEX_DIR, exist_ok=True)
    np.save(f"{INDEX_DIR}/embeddings.npy", emb)
    with open(f"{INDEX_DIR}/meta.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)
    print(f"✅ Index construit : {len(chunks)} vecteurs — modèle {MODEL}.")


if __name__ == "__main__":
    main()
