# Rapport — Assistant RAG sur les démarches administratives du Sénégal

**Certification IA — Orange Digital Center · P1IA · Groupe 1**
**Membres :** Alassane, Tayba, Fatima, Khadidiatou, Abdou Aziz
**Date :** _(à compléter)_

> 📝 Modèle à remplir. Les `_(à compléter)_` sont des trous à combler. Gardez le rapport **court et lucide** : d'après les critères, **l'évaluation et l'analyse des échecs comptent plus que la performance brute**.

---

## 1. Contexte & objectif

Assistant qui répond à des questions sur un corpus de documents publics, en citant les passages utilisés, puis dont on mesure la qualité des réponses.

- **Problème traité :** _(à compléter — ex. aider à s'y retrouver dans les démarches administratives)_
- **Ce que fait l'assistant :** _(à compléter)_

## 2. Corpus

- **Thème :** démarches administratives du Sénégal (CNI, passeport, état civil, casier judiciaire…).
- **Sources (publiques, citées) :** _(à compléter — liste des URL/documents)_
- **Taille :** _(à compléter — nb de documents, nb de pages, nb de chunks)_
- **Caractère public confirmé :** oui — aucune donnée personnelle / confidentielle.
- **Prétraitement :** nettoyage _(à compléter)_, découpage en chunks de ~800 caractères (overlap 150).

## 3. Architecture du pipeline

```
Corpus → [Ingestion] → chunks.json → [Embeddings + index] → [Recherche top-k]
                                                                   ↓
                              Question ───────────────────→ [Prompt + LLM] → Réponse + passages cités
```

- **Étapes :** ingestion → embeddings/index → retrieval → génération avec citation.
- _(à compléter — insérer un schéma si possible)_

## 4. Choix techniques (justifiés)

| Composant | Choix retenu | Pourquoi | Alternatives écartées |
|---|---|---|---|
| Modèle d'embeddings | `intfloat/multilingual-e5-small` | gratuit, bon en français | _(à compléter)_ |
| Base vectorielle | _(à compléter : FAISS / Chroma / numpy)_ | _(à compléter)_ | _(à compléter)_ |
| LLM (génération) | _(à compléter : Groq Llama / Gemini)_ | gratuit, suffisant | _(à compléter)_ |
| Découpage (chunking) | 800 car. / overlap 150 | compromis contexte / précision | _(à compléter)_ |

## 5. Protocole d'évaluation

- **Jeu de test :** _(à compléter)_ questions avec réponses de référence (`eval/questions.json`).
- **Métriques :**
  - **Fidélité** (la réponse s'appuie-t-elle vraiment sur le corpus, sans invention ?) — méthode : _(à compléter : manuelle / RAGAS faithfulness)_
  - **Pertinence du retrieval** (les bons passages sont-ils retrouvés ?) — méthode : _(à compléter : context precision/recall)_
- **Procédure :** _(à compléter — comment les scores ont été attribués)_

## 6. Résultats

| Métrique | Score | Commentaire |
|---|---|---|
| Fidélité | _(à compléter)_ | _(à compléter)_ |
| Pertinence du retrieval | _(à compléter)_ | _(à compléter)_ |
| Taux de bonnes réponses | _(à compléter)_ | _(à compléter)_ |

_(à compléter — 2-3 phrases de synthèse)_

## 7. Analyse des échecs ⭐ (section la plus importante)

Pour chaque échec représentatif : la question, ce qui était attendu, ce qu'a produit le système, et **pourquoi** ça a raté.

| # | Question | Réponse attendue | Réponse obtenue | Cause probable | Catégorie |
|---|---|---|---|---|---|
| 1 | _(à compléter)_ | _(à compléter)_ | _(à compléter)_ | _(à compléter)_ | hallucination / mauvais passage / chunk coupé / hors-corpus |
| 2 | _(à compléter)_ | | | | |
| 3 | _(à compléter)_ | | | | |

**Ce que ces échecs nous apprennent :** _(à compléter — l'analyse lucide, c'est ce qui rapporte le plus de points)_

## 8. Limites connues

- _(à compléter — ex. corpus limité, pas de gestion des questions multi-documents, dépendance au modèle gratuit…)_

## 9. Ce qu'on changerait / pistes d'amélioration

- _(à compléter — ex. meilleur chunking, reranking, corpus plus large, modèle plus grand…)_

## 10. Fonctionnalités avancées (bonus)

- **Function calling :** _(à compléter ou « non traité »)_
- **Observabilité (coût + latence) :** _(à compléter ou « non traité »)_
- **Garde-fous :** hors-sujet géré via seuil de pertinence + réponse « je ne sais pas d'après le corpus » ; _(à compléter : injection de prompt / données perso)_

## 11. Sources & références

- _(à compléter — sources du corpus + bibliothèques/modèles utilisés)_

## 12. Répartition du travail

| Membre | Contribution |
|---|---|
| Alassane | Cœur RAG, intégration, coordination, démo |
| Tayba | Ingestion du corpus, rapport |
| Fatima | Embeddings & base vectorielle |
| Khadidiatou | Évaluation, rapport |
| Abdou Aziz | Fonctionnalités bonus |

## 13. Démonstration (plan ~5 min)

1. Le problème + le corpus (30 s)
2. Une question en direct → réponse + passages cités (1-2 min)
3. Résultats d'évaluation (1 min)
4. Un échec analysé + les limites (1-2 min)
