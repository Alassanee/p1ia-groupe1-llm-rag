# Module RAG (LangChain) — Alassane

Cœur du projet : indexation du corpus + réponse aux questions avec citations.

## Fichiers
- `config.py` — **réglages du retriever (périmètre de Fatima)** : modèle d'embeddings, taille des chunks, nombre de passages `k`.
- `build_index.py` — charge `data/corpus/**/*.txt`, découpe (`RecursiveCharacterTextSplitter`), encode et construit l'index **Chroma** (`data/index/chroma`).
- `pipeline.py` — `answer(question)` : recherche Chroma + génération **Groq** + citation des sources.

## Utilisation
```bash
python -m src.rag.build_index   # (ré)indexe le corpus
python app.py                   # pose des questions
```

## Contrat d'interface
`answer(question) -> {"reponse": str, "passages": [{"texte", "source"}, ...]}`
