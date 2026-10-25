"""
Contrôle qualité rapide de data/chunks.json : longueurs, champs manquants,
répartition par démarche. Utile avant de transmettre les données à Fatima.

Usage :
    python -m src.ingestion.check
"""

import json
from collections import Counter
from pathlib import Path

CHUNKS_PATH = Path("data/chunks.json")


def main():
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))

    problemes = []
    longueurs = []
    par_demarche = Counter()

    for c in chunks:
        for champ in ("id", "texte", "source", "demarche", "position"):
            if champ not in c or c[champ] in (None, "", {}):
                problemes.append(f"{c.get('id', '?')} : champ manquant ou vide '{champ}'")

        if "source" in c:
            if not c["source"].get("url"):
                problemes.append(f"{c.get('id', '?')} : source.url vide")

        texte = c.get("texte", "")
        longueurs.append(len(texte))
        if len(texte) < 150:
            problemes.append(f"{c.get('id', '?')} : chunk anormalement court ({len(texte)} car.)")
        if len(texte) > 1500:
            problemes.append(f"{c.get('id', '?')} : chunk anormalement long ({len(texte)} car.)")

        par_demarche[c.get("demarche", "?")] += 1

    print(f"Total chunks : {len(chunks)}")
    print(f"Longueur min/moy/max : {min(longueurs)} / {sum(longueurs)//len(longueurs)} / {max(longueurs)} caractères")
    print()
    print("Répartition par démarche :")
    for demarche, n in sorted(par_demarche.items()):
        print(f"  - {demarche:<22} {n} chunk(s)")
    print()

    if problemes:
        print(f"{len(problemes)} point(s) à vérifier :")
        for p in problemes:
            print(f"  ⚠ {p}")
    else:
        print("✅ Aucun problème détecté : champs complets, longueurs dans la plage attendue.")


if __name__ == "__main__":
    main()
