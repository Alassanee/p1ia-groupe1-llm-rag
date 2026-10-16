"""
Recherche vectorielle — Fatima.
Expose la fonction du contrat d'interface :
    search(question, k) -> [{texte, source, score}]
"""
import functools
import json
import os

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
INDEX_DIR = "data/index"


@functools.lru_cache(maxsize=1)
def _load():
    emb = np.load(f"{INDEX_DIR}/embeddings.npy")
    with open(f"{INDEX_DIR}/meta.json", encoding="utf-8") as f:
        meta = json.load(f)
    model = SentenceTransformer(MODEL)
    return emb, meta, model


def search(question: str, k: int = 4) -> list[dict]:
    emb, meta, model = _load()
    # e5 attend le préfixe "query: " pour les questions.
    q = model.encode([f"query: {question}"], normalize_embeddings=True)[0]
    scores = emb @ q                       # produit scalaire = cosinus (vecteurs normalisés)
    top = np.argsort(scores)[::-1][:k]
    return [
        {"texte": meta[i]["texte"], "source": meta[i]["source"], "score": float(scores[i])}
        for i in top
    ]
