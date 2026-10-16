# Module Évaluation — Khadidiatou ⭐

**But :** mesurer la qualité (c'est ce qui rapporte le plus de points).

**À produire :**
- `eval/questions.json` = `[{ "question", "reponse_reference", "source_attendue" }]` (~20 entrées)
- `eval/results.*` = tableau de métriques
- La section « résultats & limites » du rapport (`docs/`)

**Mesures :**
- **Fidélité** : la réponse s'appuie-t-elle vraiment sur le corpus (sans invention) ?
- **Pertinence du retrieval** : les bons passages sont-ils retrouvés ?

**Méthode :** grille manuelle et/ou **RAGAS** (faithfulness, context precision/recall).

**⭐ Le plus important :** l'**analyse des échecs** (où/pourquoi ça rate) — rédigée, lucide.
