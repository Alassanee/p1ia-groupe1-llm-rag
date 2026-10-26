"""
Réglages du RAG — périmètre de Fatima (qualité du retrieval).

C'est ici qu'on ajuste la recherche sans toucher à la logique du pipeline :
modèle d'embeddings, taille des chunks et nombre de passages récupérés.
⚠️ EMB_MODEL doit rester IDENTIQUE entre l'indexation et la recherche.
"""

# Chemins
CORPUS_DIR = "data/corpus"
PERSIST_DIR = "data/index/chroma"

# Embeddings (modèle multilingue gratuit, bon en français)
EMB_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Découpage des documents
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Recherche
TOP_K = 8              # nombre de passages renvoyés par question
FETCH_K = 25           # candidats examinés avant diversification (MMR)
SEARCH_TYPE = "mmr"    # "mmr" (diversifie, évite qu'un seul doc monopolise) ou "similarity"
