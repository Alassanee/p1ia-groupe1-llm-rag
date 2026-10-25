"""
Nettoyage du texte extrait : suppression des lignes de bruit résiduelles,
normalisation des espaces, sans toucher à la ponctuation ni aux accents
français.
"""

import re

# Lignes de bruit fréquentes, propres à chaque site (voir guide section 4 :
# un filtre par source est plus précis qu'un filtre générique global).
NOISE_LINES_BY_DOMAIN = {
    "senego.com": [
        "Contact", "Se connecter", "Soutenir Senego", "Mon compte",
        "Déconnexion", "Rechercher", "Politique", "Société", "Justice",
        "International", "Afrique", "Économie", "Célébrités", "Buzz",
        "Sports", "Vidéos", "Services", "Météo", "Accueil",
        "Plan du site", "Mentions légales", "CGU", "Confidentialité",
        "Nous suivre", "A propos", "Qui sommes-nous",
    ],
    "osiris.sn": [
        "Rechercher :", "Show navigation", "Hide navigation", "OSIRIS",
        "Accueil", "Fil d'actu", "Liens intéressants", "Navigation par mots clés",
    ],
    "ndarinfo.com": [
        "Accueil", "Newsletter", "Inscription", "Réseau Social", "Forum",
        "Agenda", "Boutique", "Vidéo", "Rechercher", "Accès membres",
    ],
}

GENERIC_NOISE_SUBSTRINGS = [
    "cookie", "s'abonner", "partager sur", "articles similaires",
    "© République du Sénégal", "tous droits réservés",
]


def _domain_of(source: dict) -> str:
    url = source.get("url", "")
    for domain in NOISE_LINES_BY_DOMAIN:
        if domain in url:
            return domain
    return ""


def clean_text(text: str, source: dict | None = None) -> str:
    """Nettoie le texte tout en PRÉSERVANT les coupures de paragraphe
    (lignes vides) : chunk.py s'appuie sur ces coupures pour découper sans
    jamais casser une liste ou une phrase en deux. On ne filtre donc le
    bruit qu'à l'intérieur de chaque paragraphe, sans aplatir le document
    entier en un bloc de lignes consécutives.
    """
    domain = _domain_of(source) if source else ""
    noise_lines = set(NOISE_LINES_BY_DOMAIN.get(domain, []))

    paragraphes_bruts = re.split(r"\n\s*\n", text)
    paragraphes_propres = []

    for paragraphe in paragraphes_bruts:
        lignes_gardees = []
        for line in paragraphe.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped in noise_lines:
                continue
            if any(sub.lower() in stripped.lower() for sub in GENERIC_NOISE_SUBSTRINGS):
                continue
            lignes_gardees.append(stripped)
        if lignes_gardees:
            paragraphes_propres.append("\n".join(lignes_gardees))

    cleaned = "\n\n".join(paragraphes_propres)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return cleaned.strip()
