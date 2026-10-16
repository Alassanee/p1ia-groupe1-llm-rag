# Sources du corpus — Démarches administratives du Sénégal

> Pour **Tayba** (ingestion). Toutes ces sources sont **publiques**. Priorité aux **sites officiels (`.gouv.sn`)**.
> ⚠️ Les sources se **contredisent parfois** (tarifs, délais, pièces exigées). C'est **normal et utile** : ça nourrit l'analyse des échecs. Règle : privilégier l'officiel, **noter la source et la date de consultation** pour chaque document, et ne pas mélanger deux sources contradictoires dans un même chunk sans le préciser.

## 1. Portails officiels (sources principales)

| Portail | Ce qu'on y trouve | URL |
|---|---|---|
| Sénégal Services | Portail officiel des démarches (état civil, passeport, CNI, élections…) | https://senegalservices.sn/ |
| Ministère de l'Intérieur | Services aux usagers (passeport, etc.) | https://interieur.gouv.sn/services/services-aux-usagers |
| e-Sénégal | e-administration (casier judiciaire, certificat de nationalité…) | https://e-senegal.sn/ |

## 2. Pages par démarche (à collecter)

| Démarche | Source officielle | URL |
|---|---|---|
| Carte nationale d'identité (CNI) | Sénégal Services — Nationalité & identité | https://bo.senegalservices.sn/demarches/papiers/nationalite-et-identite |
| Passeport (numérisé) | Sénégal Services | https://senegalservices.sn/demarche/demander-un-passeport-numerise |
| Passeport ordinaire | Ministère de l'Intérieur | https://interieur.gouv.sn/services/services-aux-usagers/passeport-ordinaire |
| Passeport (diaspora, 1ʳᵉ demande) | Consulat du Sénégal à Paris | https://consulsen-paris.gouv.sn/demande-de-passeport/ |
| État civil / extrait de naissance | Sénégal Services (thème État-civil) | https://senegalservices.sn/ |
| Casier judiciaire (bulletin n°3) | Ministère de la Justice *(à vérifier)* | https://casierjudiciaire.justice.gouv.sn/ |
| Certificat de résidence | Délivré en commissariat / gendarmerie — *pas de page en ligne dédiée confirmée* | — |

## 3. Source complémentaire (non officielle, mais publique et riche)

Utile pour le volume de texte en FAQ, **à recouper avec l'officiel** :

| Source | Nature | URL |
|---|---|---|
| Guide des démarches — Senego | Guide tiers (FAQ) | https://senego.com/services/guide-demarches |
| Dossier passeport 2026 — Senego | Article détaillé | https://senego.com/dossier/passeport-senegal |

## 4. Conseils de collecte (Tayba)

1. Vise **20-50 pages** au total (assez pour ~20 questions, pas trop pour rester gratuit/rapide).
2. Pour chaque page : copier le **texte** dans un `.txt` (ou enregistrer le **PDF**) dans `data/corpus/`, nommé clairement (ex. `passeport_interieur.txt`).
3. Garder une **trace de la source + date** (ce fichier sert de référence ; cite-les dans le rapport).
4. **Corpus public uniquement** — aucune donnée personnelle.
5. Supprimer les menus/pieds de page lors du nettoyage (le script `src/ingestion/run.py` fait déjà un premier nettoyage).
6. Quand le corpus est prêt : `python -m src.ingestion.run` puis prévenir Fatima.
