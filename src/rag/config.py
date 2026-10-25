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

# Recherche : nombre de passages renvoyés par question
TOP_K = 4
