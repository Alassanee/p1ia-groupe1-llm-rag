"""
Module Function Calling / Outils — Abdou Aziz.
Fournit des outils spécialisés pour les démarches administratives du Sénégal :
  1. Calculateur officiel des frais et timbres fiscaux (en FCFA).
  2. Estimateur des délais légaux et lieux de dépôt.
  3. Définition des schémas d'outils compatibles OpenAI / Groq / Gemini.
"""
from typing import Any, Dict, List, Optional

# Base de référence tarifaire officielle (Sénégal)
TARIFS_DEMARCHES = {
    "passeport": {
        "nom": "Passeport biométrique ordinaire",
        "timbre_fiscal_cfa": 20000,
        "delai_estime": "3 à 7 jours ouvrés (48h en procédure urgente)",
        "lieu_depot": "Direction de la Police des Étrangers et des Titres de Voyage (DPETV) ou commissariats agréés",
        "pieces_principales": ["CNI valide", "Extrait de naissance de moins de 3 mois", "Quittance de 20 000 FCFA", "Photos d'identité conformes"],
    },
    "cni": {
        "nom": "Carte Nationale d'Identité biométrique CEDEAO",
        "timbre_fiscal_cfa": 0,  # Gratuit à la première délivrance
        "frais_duplicata_cfa": 10000,
        "delai_estime": "2 à 4 semaines",
        "lieu_depot": "Commissariats de police, préfectures ou sous-préfectures",
        "pieces_principales": ["Extrait de naissance de moins de 3 mois", "Certificat de résidence"],
    },
    "casier_judiciaire": {
        "nom": "Extrait de Casier Judiciaire (Bulletin n°3)",
        "timbre_fiscal_cfa": 200,
        "delai_estime": "24 à 48 heures",
        "lieu_depot": "Greffe du Tribunal d'Instance du lieu de naissance",
        "pieces_principales": ["Copie de la CNI ou de l'acte de naissance", "Timbre fiscal de 200 FCFA"],
    },
    "certificat_residence": {
        "nom": "Certificat de résidence",
        "timbre_fiscal_cfa": 500,  # Timbre municipal usuel
        "delai_estime": "Immédiat à 24 heures",
        "lieu_depot": "Mairie ou commissariat / brigade de gendarmerie de domicile",
        "pieces_principales": ["CNI", "Facture Senelec / Sen'Eau ou quittance de loyer", "Attestation du chef de quartier"],
    },
    "certificat_nationalite": {
        "nom": "Certificat de Nationalité Sénégalaise",
        "timbre_fiscal_cfa": 2000,
        "delai_estime": "3 à 5 jours ouvrés",
        "lieu_depot": "Tribunal d'Instance",
        "pieces_principales": ["Extrait d'acte de naissance du demandeur", "Extrait d'acte de naissance du père ou de la mère attestant la nationalité"],
    },
    "permis_conduire": {
        "nom": "Permis de conduire",
        "timbre_fiscal_cfa": 10000,
        "delai_estime": "2 à 6 semaines",
        "lieu_depot": "Services régionaux des transports routiers",
        "pieces_principales": ["Certificat d'aptitude médicale", "CNI", "Attestation de réussite à l'examen", "Quittance de droit de timbre"],
    },
}


def calculer_frais_demarche(demarche: str, duplicata: bool = False, nombre_exemplaires: int = 1) -> Dict[str, Any]:
    """
    Calcule le montant total des frais et timbres fiscaux en Francs CFA pour une démarche donnée au Sénégal.
    """
    key = demarche.lower().strip()
    match = None
    for k in TARIFS_DEMARCHES:
        if k in key or key in k:
            match = TARIFS_DEMARCHES[k]
            break

    if not match:
        return {
            "trouve": False,
            "message": f"Démarche '{demarche}' non répertoriée dans le barème officiel.",
            "demarches_disponibles": list(TARIFS_DEMARCHES.keys()),
        }

    tarif_unitaire = match.get("frais_duplicata_cfa", match["timbre_fiscal_cfa"]) if duplicata else match["timbre_fiscal_cfa"]
    montant_total = tarif_unitaire * max(1, nombre_exemplaires)

    return {
        "trouve": True,
        "demarche": match["nom"],
        "est_duplicata": duplicata,
        "nombre_exemplaires": nombre_exemplaires,
        "tarif_unitaire_cfa": tarif_unitaire,
        "montant_total_cfa": montant_total,
        "delai_indicatif": match["delai_estime"],
        "lieu_depot": match["lieu_depot"],
    }


def verifier_pieces_requises(demarche: str) -> Dict[str, Any]:
    """
    Fournit la liste des pièces justificatives exigées pour une démarche administrative.
    """
    key = demarche.lower().strip()
    match = None
    for k in TARIFS_DEMARCHES:
        if k in key or key in k:
            match = TARIFS_DEMARCHES[k]
            break

    if not match:
        return {"trouve": False, "message": f"Démarche '{demarche}' non reconnue."}

    return {
        "trouve": True,
        "demarche": match["nom"],
        "pieces_requises": match["pieces_principales"],
        "lieu_depot": match["lieu_depot"],
    }


# Définition du schéma d'outils (Tools spec standard) pour intégration LLM Function Calling
TOOLS_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "calculer_frais_demarche",
            "description": "Calcule les frais officiels et timbres fiscaux en FCFA pour les démarches administratives au Sénégal (passeport, CNI, casier judiciaire, permis, certificat de résidence).",
            "parameters": {
                "type": "object",
                "properties": {
                    "demarche": {
                        "type": "string",
                        "description": "Le nom de la démarche (ex: 'passeport', 'cni', 'casier_judiciaire', 'certificat_residence', 'permis_conduire').",
                    },
                    "duplicata": {
                        "type": "boolean",
                        "description": "Indique s'il s'agit d'un duplicata ou remplacement suite à une perte/vol.",
                    },
                    "nombre_exemplaires": {
                        "type": "integer",
                        "description": "Nombre de copies demandées (par défaut 1).",
                    },
                },
                "required": ["demarche"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verifier_pieces_requises",
            "description": "Retourne les pièces justificatives obligatoires et le lieu de dépôt pour une démarche administrative sénégalaise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "demarche": {
                        "type": "string",
                        "description": "Le type de démarche demandée.",
                    }
                },
                "required": ["demarche"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "calculer_frais_demarche": calculer_frais_demarche,
    "verifier_pieces_requises": verifier_pieces_requises,
}


def execute_tool_call(func_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Exécute dynamiquement la fonction appelée par le LLM et renvoie le résultat JSON.
    """
    func = AVAILABLE_TOOLS.get(func_name)
    if not func:
        return {"erreur": f"Outil inconnu : '{func_name}'"}
    try:
        return func(**arguments)
    except Exception as e:
        return {"erreur": f"Échec d'exécution de l'outil {func_name} : {str(e)}"}
