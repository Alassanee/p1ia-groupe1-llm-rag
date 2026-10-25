"""
Déclaration des sources à ingérer pour le corpus
« Démarches administratives du Sénégal ».

Chaque source est un dictionnaire :
- demarche          : identifiant court de la démarche (dossier dans data/)
- nom                : nom affiché de la source (pour la citation)
- url                : URL publique d'origine
- type               : "html" ou "pdf"
- date_consultation  : date à laquelle la page a été relevée pour ce corpus
- cache_file         : fichier texte de secours utilisé si le site n'est pas
                        joignable (réseau restreint, site hors ligne, etc.)
                        Permet de relancer le pipeline de façon reproductible
                        même sans accès internet au moment de l'exécution.

Pour ajouter une nouvelle source : ajouter une entrée à SOURCES, et
éventuellement un fichier de cache correspondant dans data/corpus/.
"""

SOURCES = [
    # ---------------------------------------------------------------- CNI
    {
        "demarche": "cni",
        "nom": "Senego — Guide des démarches administratives",
        "url": "https://senego.com/services/guide-demarches",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/cni/senego_guide_cni.txt",
    },
    {
        "demarche": "cni",
        "nom": "OSIRIS — Carte nationale d'identité : les pièces à fournir",
        "url": "https://osiris.sn/Carte-nationale-d-identite-Les.html",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/cni/osiris_cni_pieces.txt",
    },
    # ----------------------------------------------------------- PASSEPORT
    {
        "demarche": "passeport",
        "nom": "Senego — Dossier Passeport sénégalais 2026",
        "url": "https://senego.com/dossier/passeport-senegal",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/passeport/senego_dossier_passeport.txt",
    },
    # ---------------------------------------------------------- ETAT CIVIL
    {
        "demarche": "etat_civil",
        "nom": "Senego — Guide des démarches administratives",
        "url": "https://senego.com/services/guide-demarches",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/etat_civil/senego_guide_etat_civil.txt",
    },
    # ---------------------------------------------------- CASIER JUDICIAIRE
    {
        "demarche": "casier_judiciaire",
        "nom": "Senego — Guide des démarches administratives",
        "url": "https://senego.com/services/guide-demarches",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/casier_judiciaire/senego_guide_casier_judiciaire.txt",
    },
    {
        "demarche": "casier_judiciaire",
        "nom": "NDARINFO — Casier judiciaire et nationalité en ligne (e-Senegal)",
        "url": "https://www.ndarinfo.com/Casier-judiciaire-et-nationalite-en-ligne-Ce-qu-il-faut-savoir-sur-e-Senegal_a43636.html",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/casier_judiciaire/ndarinfo_e_senegal.txt",
    },
    # ----------------------------------------------- CERTIFICAT DE RESIDENCE
    {
        "demarche": "certificat_residence",
        "nom": "Senego — Guide des démarches administratives",
        "url": "https://senego.com/services/guide-demarches",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/certificat_residence/senego_guide_certificat_residence.txt",
    },
    # ------------------------------------------------------------- PERMIS
    {
        "demarche": "permis",
        "nom": "Senego — Guide des démarches administratives",
        "url": "https://senego.com/services/guide-demarches",
        "type": "html",
        "date_consultation": "2026-10-23",
        "cache_file": "data/corpus/permis/senego_guide_permis.txt",
    },
]
