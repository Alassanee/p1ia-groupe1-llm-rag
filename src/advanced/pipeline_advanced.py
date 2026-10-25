"""
Pipeline RAG Avancé — Abdou Aziz.
Intègre le cœur RAG (Alassane) avec les 3 fonctionnalités bonus :
  1. Garde-fous préventifs (anti-injection, anonymisation PII des NIN/téléphones/emails).
  2. Observabilité complète (latence, tokens, coût estimé, audit JSONL).
  3. Function calling / Outils fiscaux pour les démarches sénégalaises.
"""
import time
from typing import Any, Dict

from src.advanced.guardrails import validate_input
from src.advanced.observability import QueryTrace
from src.advanced.tools import AVAILABLE_TOOLS, execute_tool_call
from src.rag.pipeline import SEUIL_PERTINENCE, build_prompt, call_llm
from src.embeddings.search import search


def answer_advanced(question: str, k: int = 4) -> Dict[str, Any]:
    """
    Point d'entrée du pipeline enrichi.
    Garantit la sécurité, la traçabilité et le support d'outils.
    """
    trace = QueryTrace(question)

    # 1. ÉTAPE GARDE-FOUS (Sécurité & Anonymisation)
    guard_result = validate_input(question)
    if not guard_result["autorise"]:
        trace.record_guardrail("PROMPT_INJECTION_BLOQUÉE")
        trace_data = trace.finish()
        return {
            "reponse": guard_result["message"],
            "passages": [],
            "securite": guard_result,
            "observabilite": trace_data,
            "outils": [],
        }

    question_assainie = guard_result["texte_assaini"]
    if guard_result["entites_masquees"]:
        trace.record_guardrail(f"PII_ANONYMISÉE ({len(guard_result['entites_masquees'])} entité(s))")

    # 2. ÉTAPE OUTILS / FUNCTION CALLING (Détection de besoin de calcul/barème)
    outils_executes = []
    q_lower = question_assainie.lower()
    if any(mot in q_lower for mot in ["coût", "cout", "combien", "prix", "frais", "timbre", "tarif"]):
        for demarche_key in ["passeport", "cni", "casier_judiciaire", "certificat_residence", "permis_conduire", "certificat_nationalite"]:
            if demarche_key.replace("_", " ") in q_lower or demarche_key in q_lower:
                duplicata = "perte" in q_lower or "duplicata" in q_lower or "renouvellement" in q_lower
                tool_res = execute_tool_call("calculer_frais_demarche", {"demarche": demarche_key, "duplicata": duplicata})
                outils_executes.append({"outil": "calculer_frais_demarche", "resultat": tool_res})
                trace.record_guardrail(f"TOOL_CALL:calculer_frais_demarche({demarche_key})")
                break

    # 3. ÉTAPE RETRIEVAL (Recherche sémantique vectorielle)
    t_retrieval_start = time.perf_counter()
    passages = []
    try:
        passages = search(question_assainie, k=k)
    except Exception as e:
        # Cas où l'index n'est pas encore généré
        passages = []
    duree_retrieval = time.perf_counter() - t_retrieval_start
    trace.record_retrieval(duree_retrieval, len(passages))

    # 4. ÉTAPE GÉNÉRATION & VÉRIFICATION SEUIL
    t_llm_start = time.perf_counter()
    if not passages or passages[0]["score"] < SEUIL_PERTINENCE:
        # Si un outil a trouvé les tarifs officiels, on l'utilise pour compléter la réponse
        if outils_executes:
            outil = outils_executes[0]["resultat"]
            reponse = (
                f"D'après le barème officiel des démarches au Sénégal :\n"
                f"- Démarche : {outil['demarche']}\n"
                f"- Frais / Timbre fiscal : {outil['montant_total_cfa']} FCFA\n"
                f"- Lieu de dépôt : {outil['lieu_depot']}\n"
                f"- Délai estimé : {outil['delai_indicatif']}"
            )
        else:
            reponse = "Je ne sais pas d'après le corpus."
        duree_llm = time.perf_counter() - t_llm_start
        trace.record_llm(duree_llm, model_name="local-rule", prompt_text="", response_text=reponse)
    else:
        prompt = build_prompt(question_assainie, passages)
        # Si un outil a été exécuté, on enrichit le prompt
        if outils_executes:
            prompt += f"\n\n[Données officielles outil fiscal]: {outils_executes[0]['resultat']}"
        reponse = call_llm(prompt)
        duree_llm = time.perf_counter() - t_llm_start
        trace.record_llm(duree_llm, model_name="llama-3.1-8b-instant", prompt_text=prompt, response_text=reponse)

    trace_data = trace.finish()

    return {
        "reponse": reponse,
        "passages": passages,
        "securite": guard_result,
        "observabilite": trace_data,
        "outils": outils_executes,
    }
