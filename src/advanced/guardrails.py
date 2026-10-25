"""
Module Garde-fous (Guardrails) & Sécurité — Abdou Aziz.
Ce module implémente les contrôles de sécurité et de conformité :
  1. Détection des injections de prompt (Prompt Injection / Jailbreak).
  2. Détection et anonymisation des données personnelles sensibles (PII : NIN sénégalais, Téléphone, Email).
  3. Filtrage hors-sujet préventif adapté au domaine administratif sénégalais.
"""
import re
from typing import Dict, List, Tuple

# --- 1. MOTS-CLÉS & PATTERNS D'INJECTION DE PROMPT ---
INJECTION_PATTERNS = [
    r"(?i)ignore(s|z)?\s+(toutes\s+)?(les|tes|vos)?\s+instructions",
    r"(?i)oublie(s|z)?\s+(toutes\s+)?(les|tes|vos)?\s+instructions",
    r"(?i)disregard\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)system\s*prompt",
    r"(?i)prompt\s*syst[èe]me",
    r"(?i)r[ée]v[èe]le(-moi)?\s+(ton|le)\s+prompt",
    r"(?i)show\s+(me\s+)?(your\s+)?prompt",
    r"(?i)mode\s+d[ée]veloppeur",
    r"(?i)jailbreak",
    r"(?i)tu\s+es\s+d[ée]sormais",
    r"(?i)you\s+are\s+now",
    r"(?i)act\s+as\s+an\s+unrestricted",
]

# --- 2. EXPRESSIONS RÉGULIÈRES POUR LES DONNÉES PERSONNELLES (PII) ---
# Numéro d'Identification Nationale (NIN) au Sénégal : 13 à 14 chiffres (parfois groupés)
# Ex: 1 890 1995 01234 ou 1890199501234
NIN_PATTERN = r"\b[12]\s?\d{3}\s?\d{4}\s?\d{5}\b|\b\d{13,14}\b"

# Téléphone Sénégal (+221 ou 00221 suivi de 70, 75, 76, 77, 78 et 7 chiffres)
PHONE_SN_PATTERN = r"(?:\+221|00221)?\s?[7][05678]\s?\d{3}\s?\d{2}\s?\d{2}\b"

# Email standard
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def check_prompt_injection(question: str) -> Tuple[bool, str]:
    """
    Vérifie si la question contient une tentative d'injection de prompt.
    Retourne (is_safe, message_ou_alerte).
    """
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, question):
            return False, "Tentative d'injection de prompt détectée. Requête bloquée par sécurité."
    return True, ""


def anonymize_pii(text: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Détecte et anonymise les données sensibles (NIN sénégalais, téléphone, email).
    Retourne le texte assaini et la liste des entités masquées.
    """
    entities_found = []
    sanitized = text

    # Anonymiser les NIN
    def _mask_nin(match):
        val = match.group(0)
        entities_found.append({"type": "NIN_SENEGAL", "valeur": val})
        return "[NIN_MASQUÉ]"

    sanitized = re.sub(NIN_PATTERN, _mask_nin, sanitized)

    # Anonymiser les Téléphones
    def _mask_phone(match):
        val = match.group(0)
        entities_found.append({"type": "TELEPHONE_SN", "valeur": val})
        return "[TEL_MASQUÉ]"

    sanitized = re.sub(PHONE_SN_PATTERN, _mask_phone, sanitized)

    # Anonymiser les Emails
    def _mask_email(match):
        val = match.group(0)
        entities_found.append({"type": "EMAIL", "valeur": val})
        return "[EMAIL_MASQUÉ]"

    sanitized = re.sub(EMAIL_PATTERN, _mask_email, sanitized)

    return sanitized, entities_found


def validate_input(question: str) -> Dict[str, any]:
    """
    Exécute tous les garde-fous sur l'entrée utilisateur.
    Retourne un dictionnaire avec le statut, le texte assaini et les alertes.
    """
    is_safe, injection_msg = check_prompt_injection(question)
    if not is_safe:
        return {
            "autorise": False,
            "raison": "PROMPT_INJECTION",
            "message": "⚠️ Requête refusée : tentative de manipulation du système détectée.",
            "texte_assaini": question,
            "entites_masquees": [],
        }

    sanitized_text, masked_entities = anonymize_pii(question)

    return {
        "autorise": True,
        "raison": "OK",
        "message": "Requête validée.",
        "texte_assaini": sanitized_text,
        "entites_masquees": masked_entities,
    }
