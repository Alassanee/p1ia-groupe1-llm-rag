# Module Ingestion — Tayba _(repris d'Abdou Aziz)_

**But :** corpus public FR → texte nettoyé → **chunks**.

**📂 Corpus choisi : Démarches administratives du Sénégal** (CNI, passeport, état civil, casier judiciaire, certificat de résidence, permis…). Sources publiques : Guide des démarches (Senego), Annuaire des services publics, pages consulaires.

**À produire :** `data/chunks.json` = `[{ "id": "...", "texte": "...", "source": "...", "position": 0 }]`

**Étapes :**
1. Collecter les documents publics FR (PDF/HTML/txt) dans `data/corpus/`.
2. Nettoyer (entêtes, pieds de page, caractères parasites).
3. Découper en chunks (~500-1000 caractères, overlap ~100-200).
4. Garder `source` + `position` pour permettre la citation.
5. Exposer une commande : `python -m src.ingestion.run`.

**Règle :** corpus **public** uniquement, sources **citées**.
