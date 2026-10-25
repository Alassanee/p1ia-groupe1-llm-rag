# Assistant RAG — Démarches administratives du Sénégal

**P1IA · Groupe 1 — Certification IA (Orange Digital Center)**

Un assistant qui répond à des questions sur un corpus de documents publics (démarches administratives sénégalaises) en **citant ses sources**, construit avec **LangChain**, puis évalué.

## 🧱 Stack

| Étape | Techno |
|---|---|
| Chargement du corpus | LangChain `DirectoryLoader` (`data/corpus/**/*.txt`) |
| Découpage | `RecursiveCharacterTextSplitter` (800 / overlap 150) |
| Embeddings | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Base vectorielle | **Chroma** (persistée dans `data/index/chroma`) |
| Génération (LLM) | **Groq** `openai/gpt-oss-20b` (gratuit) |
| Évaluation | jeu de questions + métriques (fidélité, pertinence) |

## 🚀 Installation & lancement

```bash
git clone https://github.com/Alassanee/p1ia-groupe1-llm-rag.git
cd p1ia-groupe1-llm-rag

python3 -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # puis colle ta clé GROQ_API_KEY

python -m src.rag.build_index   # construit l'index vectoriel à partir du corpus
python app.py                   # pose tes questions
```

> Obtenir une clé Groq gratuite : https://console.groq.com

## 📂 Structure

```
├── app.py                  # point d'entrée (CLI)
├── data/
│   ├── corpus/             # corpus .txt par démarche (cni, passeport, …)
│   └── sources.json        # bibliographie des sources
├── src/
│   ├── rag/                # cœur RAG (LangChain)
│   │   ├── config.py       #   réglages retriever (Fatima)
│   │   ├── build_index.py  #   indexation Chroma
│   │   └── pipeline.py     #   answer() : retrieval + génération + citations
│   ├── ingestion/          # constitution / provenance du corpus (Tayba)
│   ├── evaluation/         # jeu de test + métriques (Khadidiatou)
│   └── advanced/           # bonus : garde-fous, observabilité, outils (Abdou)
├── eval/                   # questions.json + résultats
├── docs/                   # rapport + sources
└── requirements.txt
```

## 👥 Rôles

| Membre | Rôle | Où |
|---|---|---|
| **Alassane** | Cœur RAG + intégration | `src/rag/` (build_index, pipeline), `app.py` |
| **Fatima** | Qualité du retrieval (modèle, chunks, `k`) | `src/rag/config.py` |
| **Tayba** | Corpus + provenance | `data/corpus/`, `src/ingestion/` |
| **Khadidiatou** | Évaluation | `src/evaluation/`, `eval/` |
| **Abdou Aziz** | Bonus (garde-fous, observabilité, function calling) | `src/advanced/` |
| **Khadidiatou + Tayba** | Rapport | `docs/` |

## 📦 Livrables
- Ce dépôt (code + README relançable)
- `docs/rapport.md` : résultats d'évaluation, erreurs, améliorations
- Démo ~5 min

## 🤝 Travail d'équipe
Workflow Git (branches, PR, zéro conflit) : voir **[GUIDE_GIT.md](GUIDE_GIT.md)**.
