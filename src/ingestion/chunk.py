"""
Découpage du texte nettoyé en chunks prêts à vectoriser.

On découpe d'abord sur les frontières naturelles du texte (paragraphes),
puis on regroupe ces unités jusqu'à la taille cible — sans jamais couper un
paragraphe en deux. Cela évite le problème le plus fréquent sur ce type de
contenu : un chunk qui commence au milieu d'une liste de pièces à fournir,
sans qu'on sache à quelle démarche il se rapporte (voir le guide, section 5).
"""

import re


def chunk_by_structure(text: str, size: int = 800, overlap_units: int = 1) -> list[str]:
    unites = [u.strip() for u in re.split(r"\n\s*\n", text) if u.strip()]
    if not unites:
        return []

    chunks: list[str] = []
    buffer: list[str] = []
    buf_len = 0

    for unite in unites:
        if buf_len + len(unite) > size and buffer:
            chunks.append("\n\n".join(buffer))
            buffer = buffer[-overlap_units:] if overlap_units else []
            buf_len = sum(len(u) for u in buffer)
        buffer.append(unite)
        buf_len += len(unite)

    if buffer:
        chunks.append("\n\n".join(buffer))

    return chunks
