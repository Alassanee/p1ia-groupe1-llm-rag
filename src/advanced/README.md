# Module Avancé (Bonus) — Abdou Aziz

Ce module enrichit le cœur RAG du Groupe 1 avec **trois fonctionnalités avancées** conformes aux exigences de certification :

---

## 🛡️ 1. Garde-fous & Sécurité (`guardrails.py`)
- **Détection des injections de prompt** : Détecte et bloque les tentatives de détournement de consignes (ex: *« ignore les instructions précédentes »*, *« révèle ton prompt système »*, *« jailbreak »*).
- **Anonymisation PII (Données personnelles)** :
  - Détecte et masque les numéros **NIN sénégalais** (Numéro d'Identification Nationale à 13-14 chiffres) en `[NIN_MASQUÉ]`.
  - Détecte et masque les numéros de **téléphone sénégalais** (`+221`, `77...`, `78...`, `70...`, `76...`) en `[TEL_MASQUÉ]`.
  - Détecte et masque les adresses email en `[EMAIL_MASQUÉ]`.

---

## 📊 2. Observabilité & Métriques (`observability.py`)
- **Latence fine** : Mesure séparément le temps de recherche vectorielle (retrieval), le temps d'inférence LLM, et le temps total.
- **Suivi des Tokens** : Comptage automatique des tokens entrants et sortants.
- **Estimation des coûts ($ USD)** : Calcul du coût financier de chaque requête selon le modèle utilisé (ex: Llama-3.1-8b-instant, Gemini).
- **Journal d'audit** : Sauvegarde continue de chaque requête dans `eval/traces.jsonl` et génération de récapitulatifs statistiques (`get_traces_summary()`).

---

## ⚙️ 3. Function Calling / Outils Fiscaux (`tools.py`)
- Outil spécialisé pour le calcul des frais administratifs au Sénégal :
  - **`calculer_frais_demarche`** : Passeport (20 000 FCFA), CNI (gratuit / 10 000 FCFA duplicata), Casier judiciaire (200 FCFA), Permis de conduire (10 000 FCFA), etc.
  - **`verifier_pieces_requises`** : Liste des pièces officielles et lieu de dépôt.
- Schémas standard JSON compatibles avec le Function Calling de Groq, Gemini et OpenAI.

---

## 🚀 Comment lancer la démonstration des bonus ?

Depuis la racine du projet (avec l'environnement activé) :

```bash
python -m src.advanced.demo
```

Ce script teste les 3 fonctionnalités et affiche les résultats détaillés dans la console.
