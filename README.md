# Assistant RAG sur corpus de documents — P1IA Groupe 1

Projet de certification IA (Orange Digital Center). Un assistant qui **répond à des questions sur un corpus de documents publics en français**, en citant les passages utilisés, puis **mesure la qualité** de ses réponses.

## 🎯 Fonctionnalités

**Socle (obligatoire)**
- Pipeline **RAG** : découpage → embeddings → base vectorielle → génération **avec citation des passages**.
- **Évaluation** : ~20 questions de référence + mesure (fidélité au corpus, pertinence du retrieval).

**Bonus (si le temps le permet)**
- Function calling · Observabilité (coût + latence) · Garde-fous (hors-sujet, injection, données perso).

## 📚 Corpus

**Démarches administratives du Sénégal** (CNI, passeport, état civil, casier judiciaire, certificat de résidence, permis…).
Sources **publiques** uniquement, citées dans le rapport : Guide des démarches (Senego), Annuaire des services publics, pages consulaires officielles. Aucune donnée personnelle ou confidentielle.

## 👥 Équipe & modules

| Membre | Module | Dossier |
|---|---|---|
| Alassane | Cœur RAG + intégration | `src/rag/`, `app.py` |
| Tayba | Ingestion du corpus | `src/ingestion/`, `data/` |
| Fatima | Embeddings + base vectorielle | `src/embeddings/` |
| Khadidiatou | Évaluation | `src/evaluation/`, `eval/` |
| Khadidiatou + Tayba | Rapport | `docs/` |
| Tayba | Bonus (si le temps le permet) | `src/advanced/` |

## 🚀 Installation & lancement (relançable)

```bash
# 1. Cloner
git clone https://github.com/Alassanee/p1ia-groupe1-llm-rag.git
cd p1ia-groupe1-llm-rag

# 2. Environnement
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

# 3. Clé API (ne jamais commiter .env)
cp .env.example .env             # puis coller sa clé Groq ou Gemini

# 4. Préparer le corpus (génère data/chunks.json)
python -m src.ingestion.run

# 5. Construire l'index vectoriel
python -m src.embeddings.build_index

# 6. Lancer l'assistant
python app.py
```

> ℹ️ Les commandes 4 et 5 dépendent des modules en cours de développement — voir le README de chaque dossier `src/`.

## 📂 Structure

```
├── app.py              # point d'entrée (Alassane)
├── src/
│   ├── ingestion/      # corpus → chunks (Tayba)
│   ├── embeddings/     # index + search() (Fatima)
│   ├── rag/            # answer() : retrieval + génération (Alassane)
│   ├── evaluation/     # métriques (Khadidiatou)
│   └── advanced/       # bonus (Tayba)
├── data/               # corpus + chunks.json
├── eval/               # questions.json + résultats
└── docs/               # rapport
```

## 🔗 Contrats d'interface entre modules

- **Ingestion** → produit `data/chunks.json` : `[{id, texte, source, position}]`
- **Embeddings** → expose `search(question, k) -> [{texte, source, score}]`
- **RAG** → expose `answer(question) -> {reponse, passages}`

## 🤝 Travailler en équipe

Voir **[GUIDE_GIT.md](GUIDE_GIT.md)** : clone, branches, commits, Pull Requests, zéro conflit.

## 📦 Livrables

- Ce dépôt (code + README relançable).
- `docs/rapport.*` : résultats d'évaluation, erreurs, améliorations.
- Démo ~5 min.

## ⏰ Deadline

**22 octobre 23h59** — dépôt `p1ia_groupe-1_llm-projet` sur Google Drive + lien WhatsApp.
