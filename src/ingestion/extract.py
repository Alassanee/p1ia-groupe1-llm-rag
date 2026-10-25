"""
Extraction du texte utile à partir du contenu brut récupéré par fetch.py.

- Contenu "live" HTML  : parsing BeautifulSoup, suppression des éléments de
                          navigation/structure (menus, footer, scripts...).
- Contenu "live" PDF    : extraction via pdfplumber.
- Contenu "cache"       : déjà du texte propre (document déjà collecté dans
                          data/corpus/, voir sources.py) — utilisé tel quel.
"""

import io

from bs4 import BeautifulSoup

# Balises et sélecteurs qui ne contiennent jamais de contenu utile pour ce corpus
NOISE_TAGS = ["nav", "header", "footer", "script", "style", "aside", "form", "svg"]
NOISE_CLASS_HINTS = [
    "menu", "navbar", "breadcrumb", "cookie", "newsletter", "share",
    "social", "sidebar", "related", "comments", "pub", "ad-", "advert",
]


def extract_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(NOISE_TAGS):
        tag.decompose()

    # On repère d'abord les éléments à retirer, PUIS on les supprime.
    # (Supprimer pendant l'itération fait tomber sur des éléments déjà
    #  détruits -> AttributeError: 'NoneType' object has no attribute 'get'.)
    noisy = []
    for el in soup.find_all(True):
        classes = " ".join(el.get("class", []) or []).lower()
        el_id = (el.get("id") or "").lower()
        if any(hint in classes or hint in el_id for hint in NOISE_CLASS_HINTS):
            noisy.append(el)
    for el in noisy:
        if not getattr(el, "decomposed", False):
            el.decompose()

    main = soup.find("article") or soup.find("main") or soup.body or soup
    text = main.get_text(separator="\n", strip=True)
    return text


def extract_pdf(pdf_bytes: bytes) -> str:
    import pdfplumber

    text_parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_text(fetch_result, source: dict) -> str:
    """Dispatch selon l'origine du contenu et le type de source déclaré."""
    if fetch_result.origin == "cache":
        # Le cache contient déjà du texte nettoyé (voir data/raw_cache/)
        return fetch_result.content

    if source["type"] == "pdf":
        return extract_pdf(fetch_result.content.encode("latin-1", errors="ignore"))

    return extract_html(fetch_result.content)
