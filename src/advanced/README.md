# Module Bonus — Tayba

⚠️ **Priorité basse** : à faire seulement quand le socle (RAG + éval) tourne — et surtout **après avoir livré l'ingestion du corpus** (ta tâche prioritaire, `src/ingestion/`). En attendant, tu peux aussi aider Khadidiatou sur les questions d'évaluation.

**Trois fonctionnalités « pour aller plus loin » (au moins une, idéalement les trois) :**

1. **Function calling** : le modèle déclenche ≥1 fonction (calcul, recherche structurée, date…). Montrer un exemple.
2. **Observabilité** : tracer chaque requête avec **coût (tokens) + latence** (logging simple ou Langfuse gratuit) → petit récap.
3. **Garde-fou** : gérer ≥1 cas à risque — hors-sujet (refus poli), injection de prompt (détection), données perso (masquage). Documenter le cas traité.

**Livrable :** code dans `src/advanced/` + démonstration + notes pour le rapport.
