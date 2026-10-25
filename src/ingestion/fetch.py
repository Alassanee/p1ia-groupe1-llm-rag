"""
Récupération des documents sources.

Stratégie : on tente toujours un appel réseau réel en premier (c'est ce qui
permet de relancer le pipeline et d'obtenir des données à jour). Si le réseau
n'est pas joignable (environnement restreint, site temporairement hors
ligne, pas de connexion), on se replie automatiquement sur le fichier de
cache local déclaré dans sources.py — ce qui garantit que le pipeline reste
toujours exécutable de bout en bout, y compris hors ligne ou dans un
environnement d'évaluation sans accès internet.
"""

import logging
import time
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (projet-pedagogique-rag; +contact-groupe)"}
TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = 1.0  # secondes, politesse envers les serveurs

logger = logging.getLogger(__name__)


class FetchResult:
    """Résultat d'une récupération : le contenu brut, et sa provenance."""

    def __init__(self, content: str, origin: str):
        self.content = content   # texte (HTML si live, texte déjà extrait si cache)
        self.origin = origin     # "live" ou "cache"


def fetch_source(source: dict) -> FetchResult:
    """Récupère le contenu d'une source, en direct si possible, sinon via le cache."""
    url = source["url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        time.sleep(DELAY_BETWEEN_REQUESTS)
        logger.info("OK (live)   %s", url)
        return FetchResult(content=resp.text, origin="live")
    except Exception as exc:  # réseau indisponible, site en erreur, timeout...
        cache_path = Path(source["cache_file"])
        if not cache_path.exists():
            raise RuntimeError(
                f"Impossible de récupérer {url} ({exc}) et aucun cache "
                f"disponible à {cache_path}."
            ) from exc
        logger.warning("Repli cache pour %s (%s) — raison : %s", url, cache_path, exc)
        return FetchResult(content=cache_path.read_text(encoding="utf-8"), origin="cache")
