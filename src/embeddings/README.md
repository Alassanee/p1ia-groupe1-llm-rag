# Module Embeddings & Base vectorielle — Fatima

**But :** chunks → vecteurs → index interrogeable.

**À exposer :** `search(question: str, k: int = 4) -> list[dict]`
chaque élément : `{ "texte": "...", "source": "...", "score": 0.0 }`

**Étapes :**
1. Charger `data/chunks.json`.
2. Encoder avec un modèle gratuit FR/multilingue (ex. `intfloat/multilingual-e5-small`).
3. Indexer dans FAISS **ou** ChromaDB.
4. Persister l'index (sauvegarde/chargement) → relançable.
5. Commande de build : `python -m src.embeddings.build_index`.

**Test :** `search("question test", k=4)` renvoie des passages pertinents avec leur source.
