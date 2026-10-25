# Ingestion & préparation du corpus — Démarches administratives du Sénégal

Module d'ingestion pour le projet **LLM & Écosystème**. Collecte, nettoie et
découpe en chunks le corpus public sur les démarches administratives
sénégalaises (CNI, passeport, état civil, casier judiciaire, certificat de
résidence, permis de conduire), prêt à être vectorisé par la suite du
pipeline RAG.

## Installation

```bash
pip install -r requirements.txt
```

## Lancer le pipeline

```bash
python -m src.ingestion.run
```

Produit :
- `data/chunks.json` — les chunks prêts à vectoriser (livrable principal)
- `data/sources.json` — la bibliographie des sources utilisées (traçabilité)

Puis, pour vérifier la qualité des chunks produits :

```bash
python -m src.ingestion.check
```

## Comment ça marche

```
src/ingestion/
├── sources.py   # liste des sources à ingérer (URL, démarche, date, cache de secours)
├── fetch.py     # récupération : tente le réseau en direct, replie sur le cache si indisponible
├── extract.py   # extraction du texte (BeautifulSoup pour le HTML, pdfplumber pour le PDF)
├── clean.py     # nettoyage (suppression du bruit propre à chaque site, préserve les paragraphes)
├── chunk.py     # découpage par structure (paragraphes), ~500-1000 caractères, chevauchement
├── check.py     # contrôle qualité du chunks.json produit
└── run.py       # orchestration de bout en bout
```

**Important — fonctionnement en réseau restreint.** Chaque source déclarée
dans `sources.py` a un `cache_file` associé dans `data/corpus/`. Le
pipeline tente toujours une requête réseau réelle en premier ; s'il échoue
(pas d'accès internet, site temporairement indisponible), il se replie
automatiquement sur ce fichier de cache. Cela garantit que `python -m
src.ingestion.run` fonctionne de façon reproductible dans n'importe quel
environnement, y compris sans accès internet (c'est d'ailleurs ce qui s'est
produit lors de l'exécution de référence, effectuée dans un environnement
réseau restreint — voir `origine_donnees` dans `data/sources.json`, qui vaut
`"cache"` pour cette exécution). **Avec un accès internet normal, relancer le
script récupère les pages en direct et met à jour les chunks avec le contenu
le plus récent.**

## Sources utilisées

| Démarche | Sources | Remarque |
|---|---|---|
| CNI | Senego (guide général), OSIRIS (pièces à fournir, 2016) | OSIRIS est une source plus ancienne, gardée pour croiser l'info |
| Passeport | Senego (dossier dédié, mis à jour mai 2026) | Source la plus détaillée (prix, délais par zone) |
| État civil | Senego (guide général) | Naissance, mariage, décès |
| Casier judiciaire | Senego (guide général), NDARINFO (migration e-Senegal, mars 2026) | Démarche en transition numérique — voir limites ci-dessous |
| Certificat de résidence | Senego (guide général) | Procédure simple, une seule source suffisante |
| Permis de conduire | Senego (guide général) | Couvre aussi le certificat d'immatriculation |

Le détail complet (URL, date de consultation, nombre de chunks produits par
source) est dans `data/sources.json`, généré automatiquement à chaque
exécution.

## Limites connues

- **Casier judiciaire et certificat de nationalité sont en cours de
  migration** vers la plateforme e-Senegal (lancée en mars 2026, déploiement
  progressif par juridiction). Les chunks de ce corpus mentionnent les deux
  procédures (guichet physique historique et nouvelle plateforme) ; un
  assistant basé sur ce corpus doit idéalement signaler cette transition
  plutôt que de trancher silencieusement.
- **Certificat de résidence et permis de conduire ne reposent que sur une
  seule source** (Senego). Les autres démarches ont été croisées avec une
  seconde source ; faute de temps, cela n'a pas été fait pour ces deux
  démarches — un axe d'amélioration si le projet est poursuivi.
- **Les pages consulaires** (démarches depuis l'étranger) n'ont pas été
  incluses dans cette version du corpus, qui se concentre sur les démarches
  effectuées au Sénégal.
- Le découpage par paragraphe (plutôt que par nombre fixe de caractères)
  produit des chunks de taille variable (391 à 1076 caractères dans
  l'exécution de référence) : légèrement en dehors de la fourchette
  indicative de 500-1000 caractères dans certains cas, mais volontairement
  pour ne jamais couper une liste de pièces à fournir en deux (voir
  `chunk.py`).

## Format d'un chunk

```json
{
  "id": "cni_0002",
  "texte": "CNI — La Carte Nationale d'Identité biométrique CEDEAO est...",
  "source": {
    "nom": "Senego — Guide des démarches administratives",
    "url": "https://senego.com/services/guide-demarches",
    "date_consultation": "2026-10-23"
  },
  "demarche": "cni",
  "position": 2
}
```

## Pour ajouter une source

Ajouter une entrée dans `SOURCES` (`src/ingestion/sources.py`) avec son
`url`, sa `demarche`, et — recommandé — un `cache_file` de secours dans
`data/corpus/<demarche>/`, puis relancer `python -m src.ingestion.run`.
