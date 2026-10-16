# 🧭 GUIDE GIT DE L'ÉQUIPE — Projet LLM/RAG (Groupe 1)

> Objectif : que **5 personnes** travaillent **en même temps** sur le même projet **sans casser le code des autres** et **sans conflits**.
> Règle d'or : **1 personne = 1 dossier = 1 branche.** On ne pousse JAMAIS directement sur `main`.

---

## 0. À faire UNE SEULE FOIS (au tout début)

### a) Installer Git
- **Windows** : télécharger sur https://git-scm.com → installer.
- **Mac** : déjà installé (sinon `brew install git`).
- Vérifier : `git --version`

### b) Configurer son identité (ton nom + email GitHub)
```bash
git config --global user.name "Ton Prénom Nom"
git config --global user.email "ton-email-github@exemple.com"
```

### c) Cloner le dépôt (récupérer le projet sur ta machine)
```bash
git clone https://github.com/<ORG-OU-ALASSANE>/<NOM-DU-REPO>.git
cd <NOM-DU-REPO>
```

### d) Créer son environnement Python
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

### e) Mettre sa clé API dans `.env` (⚠️ JAMAIS commiter la clé)
```bash
cp .env.example .env
# puis ouvrir .env et coller sa clé (Groq / Gemini)
```
Le fichier `.env` est déjà dans `.gitignore` : il ne partira jamais sur GitHub. ✅

---

## 1. Qui touche à quoi (zéro conflit)

| Membre | SON dossier (il n'édite QUE ça) |
|---|---|
| Abdou Aziz | `data/` + `src/ingestion/` |
| Fatima | `src/embeddings/` |
| Alassane | `src/rag/` + `app.py` |
| Khadidiatou | `src/evaluation/` + `eval/` |
| Tayba | `src/advanced/` |

👉 Tant que **chacun reste dans son dossier**, Git n'a **aucune raison** de créer un conflit.
⚠️ Fichiers **partagés** (`README.md`, `requirements.txt`) : prévenir l'équipe sur WhatsApp **avant** d'y toucher.

---

## 2. Le cycle de travail quotidien (à répéter chaque jour)

### Étape 1 — Se mettre à jour AVANT de commencer
```bash
git checkout main
git pull origin main
```

### Étape 2 — Créer/retrouver SA branche
Nom de branche = `feat/<prenom>-<theme>`. Exemples :
- `feat/abdou-ingestion`
- `feat/fatima-embeddings`
- `feat/khadidiatou-evaluation`
- `feat/tayba-garde-fous`

Première fois (créer la branche) :
```bash
git checkout -b feat/abdou-ingestion
```
Les jours suivants (revenir dessus) :
```bash
git checkout feat/abdou-ingestion
git merge main      # récupérer le travail des autres déjà fusionné
```

### Étape 3 — Travailler, puis enregistrer (commit)
```bash
git add .
git commit -m "ingestion: découpage des documents en chunks"
```
> Fais des **petits commits** fréquents avec un message clair.

### Étape 4 — Envoyer sa branche sur GitHub (push)
```bash
git push origin feat/abdou-ingestion
```

### Étape 5 — Ouvrir une Pull Request (PR)
1. Va sur le repo GitHub → bouton **« Compare & pull request »**.
2. Base = `main`, Compare = ta branche.
3. Décris ce que tu as fait → **Create pull request**.
4. Préviens **Alassane** (lead) : il relit et **fusionne** dans `main`.

> ✅ C'est Alassane qui fusionne les PR dans `main`. Ça garde `main` toujours propre et fonctionnel.

---

## 3. Résoudre un conflit (si ça arrive quand même)

Un conflit = deux personnes ont modifié **les mêmes lignes**. Git l'indique ainsi :
```
<<<<<<< HEAD
ton code
=======
le code de l'autre
>>>>>>> main
```
1. Ouvre le fichier, **garde la bonne version** (ou combine les deux), supprime les lignes `<<<<<<<`, `=======`, `>>>>>>>`.
2. Puis :
```bash
git add .
git commit -m "fix: résolution du conflit"
git push
```
👉 En cas de doute : **ne devine pas**, appelle Alassane / l'équipe.

---

## 4. Tester le projet (avant chaque PR et avant le rendu)

Depuis la racine, environnement activé :
```bash
python app.py
```
- Pose une question → tu dois obtenir une **réponse + les passages cités**.
- Si une étape plante, c'est souvent une clé `.env` manquante ou un `pip install` oublié.

---

## 5. Les 7 règles d'or de l'équipe

1. **Jamais** de `git push` direct sur `main` → toujours par **Pull Request**.
2. **`git pull` AVANT** de commencer à coder (chaque jour).
3. **1 personne = 1 dossier = 1 branche.**
4. **Petits commits** avec messages clairs.
5. **Jamais** de clé API / `.env` / gros fichiers d'index dans Git.
6. Prévenir sur WhatsApp **avant** de toucher un fichier partagé.
7. Un **daily de 10 min** : qui a fait quoi, qui est bloqué.

---

## Antisèche (à garder sous les yeux)

```bash
git checkout main && git pull origin main   # se mettre à jour
git checkout -b feat/prenom-theme            # créer sa branche
# ... je code dans MON dossier ...
git add . && git commit -m "message clair"   # enregistrer
git push origin feat/prenom-theme            # envoyer
# puis Pull Request sur GitHub + prévenir Alassane
```
