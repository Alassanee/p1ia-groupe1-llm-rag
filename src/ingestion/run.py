"""
Orchestration du pipeline d'ingestion :
    fetch -> extract -> clean -> chunk -> export (data/chunks.json)

Usage :
    python -m src.ingestion.run

Produit :
    data/chunks.json   — les chunks prêts à vectoriser (format attendu par Fatima)
    data/sources.json  — la bibliographie des sources utilisées (traçabilité)
"""

import json
import logging
from collections import defaultdict
from pathlib import Path

from .sources import SOURCES
from .fetch import fetch_source
from .extract import extract_text
from .clean import clean_text
from .chunk import chunk_by_structure

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_CHUNKS = Path("data/chunks.json")
OUTPUT_SOURCES = Path("data/sources.json")

CHUNK_SIZE = 800
CHUNK_OVERLAP_UNITS = 1  # nombre de paragraphes de chevauchement entre deux chunks


def main():
    all_chunks = []
    sources_meta = []
    chunk_counter = defaultdict(int)
    stats = defaultdict(lambda: {"sources": 0, "chunks": 0, "live": 0, "cache": 0})

    for source in SOURCES:
        logger.info("Traitement : [%s] %s", source["demarche"], source["nom"])

        result = fetch_source(source)
        raw_text = extract_text(result, source)
        text = clean_text(raw_text, source)

        if not text:
            logger.warning("Aucun texte exploitable pour %s — source ignorée.", source["url"])
            continue

        # Préfixe de contexte : aide le retrieval à bien situer le chunk
        # même si le nom de la démarche n'apparaît pas dans le passage lui-même.
        demarche_label = source["demarche"].replace("_", " ").upper()
        pieces = chunk_by_structure(text, size=CHUNK_SIZE, overlap_units=CHUNK_OVERLAP_UNITS)

        demarche = source["demarche"]
        for piece in pieces:
            chunk_counter[demarche] += 1
            chunk_id = f"{demarche}_{chunk_counter[demarche]:04d}"
            texte_final = f"{demarche_label} — {piece}"
            all_chunks.append({
                "id": chunk_id,
                "texte": texte_final,
                "source": {
                    "nom": source["nom"],
                    "url": source["url"],
                    "date_consultation": source["date_consultation"],
                },
                "demarche": demarche,
                "position": chunk_counter[demarche],
            })

        stats[demarche]["sources"] += 1
        stats[demarche]["chunks"] += len(pieces)
        stats[demarche][result.origin] += 1

        sources_meta.append({
            "nom": source["nom"],
            "url": source["url"],
            "demarche": demarche,
            "date_consultation": source["date_consultation"],
            "origine_donnees": result.origin,  # "live" ou "cache"
            "nb_chunks_produits": len(pieces),
        })

    OUTPUT_CHUNKS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CHUNKS, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_SOURCES, "w", encoding="utf-8") as f:
        json.dump(sources_meta, f, ensure_ascii=False, indent=2)

    logger.info("—" * 60)
    logger.info("%d chunks exportés dans %s", len(all_chunks), OUTPUT_CHUNKS)
    logger.info("%d sources listées dans %s", len(sources_meta), OUTPUT_SOURCES)
    logger.info("—" * 60)
    for demarche, s in sorted(stats.items()):
        logger.info(
            "  %-22s %2d source(s)  %3d chunk(s)  (live=%d, cache=%d)",
            demarche, s["sources"], s["chunks"], s["live"], s["cache"],
        )


if __name__ == "__main__":
    main()
