# Rapport — Assistant RAG sur les démarches administratives du Sénégal

**Certification IA — Orange Digital Center · P1IA · Groupe 1**
**Membres :** Alassane (lead/intégration), Tayba (corpus), Fatima (retrieval), Khadidiatou (évaluation), Abdou Aziz (bonus)

---

## 1. Objectif

Construire un assistant capable de répondre à des questions sur un corpus de documents **publics en français**, en **citant les passages utilisés**, puis **mesurer la qualité** de ses réponses. Corpus choisi : les **démarches administratives du Sénégal** (CNI, passeport, état civil, casier judiciaire, certificat de résidence, permis).

## 2. Corpus

- **8 documents** texte, regroupés par démarche dans `data/corpus/`, découpés en **37 chunks** indexés.
- **Sources publiques** (citées, traçées dans `data/sources.json`) : guide des démarches et dossier passeport (Senego), fiche CNI (OSIRIS / Le Soleil), article e-Senegal (NDARINFO).
- Aucune donnée personnelle ni confidentielle.
- Point notable : sur le casier judiciaire, le corpus documente **deux procédures concurrentes** (dépôt physique au greffe *vs* plateforme e-Senegal en déploiement) — utile pour tester la nuance.

## 3. Architecture (pipeline RAG)

```
Corpus (.txt) → [DirectoryLoader] → [RecursiveCharacterTextSplitter 800/150]
   → [Embeddings multilingues] → [Chroma] → [Retriever top-k]
        ↓
  Question → [Garde-fous] → [Function calling éventuel] → [Prompt + LLM Groq] → Réponse + sources citées
```

Un seul flux : `answer_advanced()` enchaîne garde-fous → outils → RAG → observabilité.

## 4. Choix techniques (justifiés)

| Composant | Choix | Pourquoi |
|---|---|---|
| Framework | **LangChain** | standard, composable, gère loader/splitter/retriever/LLM |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` | gratuit, bon en français, léger (pas de préfixe à gérer) |
| Base vectorielle | **Chroma** (persistée) | simple, local, gratuit, relançable |
| Découpage | 800 car. / overlap 150 | compromis contexte / précision du passage |
| LLM | **Groq** `openai/gpt-oss-20b` | gratuit, rapide, bon en français |
| Garde-fous | règles + seuil + anonymisation PII | sécurité sans coût LLM supplémentaire |

> Aucun budget : API Groq gratuite + modèles ouverts locaux pour les embeddings.

## 5. Protocole d'évaluation

Jeu de **15 questions** (`eval/questions.json`) : **12 factuelles** (avec réponse de référence + source attendue) et **3 pièges** (hors-sujet, injection de prompt, données personnelles). Script : `python -m src.evaluation.run_eval`.

Métriques :
- **Pertinence du retrieval** : la source attendue figure-t-elle dans les passages renvoyés ? (objectif, automatique)
- **Exactitude** : la réponse contient-elle les informations clés attendues ? (vérif. par mots-clés + revue)
- **Garde-fous** : hors-sujet refusé, injection bloquée, PII masquée.

## 6. Résultats

| Métrique | Score |
|---|---|
| Pertinence du retrieval | **11 / 12 (91 %)** |
| Exactitude (mots-clés) | **10 / 12 (83 %)** |
| Garde-fous (pièges) | **3 / 3 (100 %)** |
| Latence typique | ~0,6 à 3 s / requête |
| Coût estimé | ~0,0001 à 0,0003 $ / requête |

Les 3 pièges sont correctement gérés : hors-sujet → « Je ne sais pas d'après le corpus », injection → requête bloquée, NIN → masqué avant traitement.

## 7. Analyse des échecs ⭐

Deux « échecs » seulement, et l'analyse est instructive :

1. **`passeport_docs` — vrai échec de retrieval.**
 Question : « Quels documents pour une première demande de passeport adulte ? » → le système répond « Je ne sais pas d'après le corpus ».
 **Cause :** le dossier passeport est long et génère beaucoup de chunks ; pour cette formulation, les passages « documents requis » d'autres démarches (CNI…) sont sémantiquement proches, et le bon chunk passeport n'est pas remonté dans le top-4. C'est une **confusion inter-documents** classique en RAG.
 **Pistes :** augmenter `k`, filtrer par démarche (métadonnée), ou affiner le découpage (Fatima, via `src/rag/config.py`).

2. **`passeport_prix` — faux échec (artefact de mesure).**
 La réponse est en réalité **correcte** (« 20000 FCFA », via l'outil fiscal), mais elle est comptée ❌ car l'outil écrit « 20000 » sans séparateur de milliers, alors que le mot-clé attendu est « 20 000 ».
 **Leçon :** notre métrique automatique par mots-clés est **sensible au formatage** (espaces insécables, séparateurs). Après revue manuelle, **11 réponses sur 12 sont réellement correctes**. Petite amélioration : formater les montants de l'outil avec séparateur.

**Ce que ça nous apprend :** la qualité dépend autant du **retrieval** (le bon passage doit remonter) que de la **mesure** (une métrique trop littérale sous-estime la performance). D'où l'importance de croiser métrique automatique et relecture.

## 8. Limites connues

- Corpus volontairement restreint (8 documents) → couverture partielle.
- Pas de filtrage par démarche au retrieval → risque de confusion inter-documents (cf. échec 1).
- Métrique d'exactitude approximative (mots-clés) → à compléter par une évaluation humaine ou RAGAS.
- Réponses dépendantes d'un modèle gratuit (variabilité possible).

## 9. Améliorations envisagées

- Ajouter un **filtre par métadonnée « démarche »** ou un reranking pour corriger l'échec de retrieval.
- Tester d'autres embeddings / tailles de chunk (via `src/rag/config.py`).
- Enrichir le corpus (couverture + coûts manquants).
- Évaluation avec **RAGAS** (faithfulness, context precision/recall) en complément.

## 10. Fonctionnalités avancées (bonus) — implémentées

- **Function calling :** outil « barème officiel » qui calcule frais/timbres et pièces par démarche (déclenché sur les questions de coût).
- **Observabilité :** latence, tokens, coût estimé par requête, journalisés dans `eval/traces.jsonl`.
- **Garde-fous :** blocage des injections de prompt, anonymisation des données personnelles (NIN, téléphone, email), refus hors-sujet.

## 11. Sources

Documents du corpus cités dans `data/sources.json` (Senego, OSIRIS/Le Soleil, NDARINFO). Bibliothèques : LangChain, sentence-transformers, Chroma, Groq.

## 12. Répartition du travail

| Membre | Contribution |
|---|---|
| Alassane | Cœur RAG LangChain, intégration, pipeline unifié |
| Tayba | Corpus (collecte, nettoyage) + provenance des sources |
| Fatima | Réglage du retrieval (embeddings, chunks, k) |
| Khadidiatou | Jeu d'évaluation, métriques, analyse des échecs |
| Abdou Aziz | Garde-fous, observabilité, function calling |

## 13. Démonstration (plan ~5 min)

1. Problème + corpus (30 s).
2. Questions en direct : une factuelle (réponse + sources), une de coût (outil), un piège injection (blocage) (2 min).
3. Résultats d'évaluation (1 min).
4. L'échec `passeport_docs` + les limites (1 min).
5. Observabilité (latence/coût) en direct (30 s).

---

*Évaluation réalisée le 2026-10-25 sur 15 questions. Reproductible via `python -m src.evaluation.run_eval` (voir `eval/results.md`).*
