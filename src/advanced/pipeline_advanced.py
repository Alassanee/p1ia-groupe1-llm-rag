"""
Pipeline RAG Avancé — Abdou Aziz (intégré au cœur LangChain d'Alassane).

Enveloppe le `answer()` du RAG (src/rag/pipeline.py) avec les 3 bonus :
  1. Garde-fous préventifs (anti-injection + anonymisation PII avant traitement).
  2. Function calling / outils fiscaux (barème officiel des démarches).
  3. Observabilité (latence, tokens, coût estimé, audit JSONL).
"""
import time
from typing import Any, Dict

from src.advanced.guardrails import validate_input
from src.advanced.observability import QueryTrace
from src.advanced.tools import execute_tool_call
from src.rag.pipeline import answer, LLM_MODEL

FEE_KEYWORDS = ["coût", "cout", "combien", "prix", "frais", "timbre", "tarif"]
DEMARCHES = [
    "passeport", "cni", "casier_judiciaire",
    "certificat_residence", "permis_conduire", "certificat_nationalite",
]


def answer_advanced(question: str, k: int = 4) -> Dict[str, Any]:
    """Point d'entrée enrichi : sécurité + outils + RAG + observabilité."""
    trace = QueryTrace(question)

    # 1. GARDE-FOUS (sécurité & anonymisation) — AVANT tout traitement
    guard = validate_input(question)
    if not guard["autorise"]:
        trace.record_guardrail("PROMPT_INJECTION_BLOQUEE")
        return {
            "reponse": guard["message"],
            "passages": [],
            "securite": guard,
            "observabilite": trace.finish(),
            "outils": [],
        }

    question_assainie = guard["texte_assaini"]
    if guard["entites_masquees"]:
        trace.record_guardrail(f"PII_ANONYMISEE ({len(guard['entites_masquees'])} entite(s))")

    # 2. FUNCTION CALLING (barème fiscal si la question porte sur un coût)
    outils_executes = []
    q_lower = question_assainie.lower()
    if any(mot in q_lower for mot in FEE_KEYWORDS):
        for demarche_key in DEMARCHES:
            if demarche_key in q_lower or demarche_key.replace("_", " ") in q_lower:
                duplicata = any(w in q_lower for w in ["perte", "duplicata", "renouvellement"])
                tool_res = execute_tool_call(
                    "calculer_frais_demarche", {"demarche": demarche_key, "duplicata": duplicata}
                )
                outils_executes.append({"outil": "calculer_frais_demarche", "resultat": tool_res})
                trace.record_guardrail(f"TOOL_CALL:calculer_frais_demarche({demarche_key})")
                break

    # 3. RAG (retrieval + génération via LangChain)
    t0 = time.perf_counter()
    rag = answer(question_assainie, k=k)
    duree = time.perf_counter() - t0
    reponse = rag["reponse"]
    passages = rag["passages"]

    # 4. Complément outil : si le corpus ne sait pas mais l'outil a la réponse officielle
    if outils_executes and (not passages or reponse.strip().lower().startswith("je ne sais pas")):
        outil = outils_executes[0]["resultat"]
        if outil.get("trouve"):
            reponse = (
                "D'après le barème officiel des démarches au Sénégal :\n"
                f"- Démarche : {outil['demarche']}\n"
                f"- Frais / timbre fiscal : {outil['montant_total_cfa']} FCFA\n"
                f"- Lieu de dépôt : {outil['lieu_depot']}\n"
                f"- Délai estimé : {outil['delai_indicatif']}"
            )

    # 5. OBSERVABILITÉ
    trace.record_retrieval(0.0, len(passages))  # retrieval+génération mesurés ensemble ci-dessous
    prompt_text = question_assainie + "\n" + "\n".join(p.get("texte", "") for p in passages)
    trace.record_llm(duree, model_name=LLM_MODEL, prompt_text=prompt_text, response_text=reponse)

    return {
        "reponse": reponse,
        "passages": passages,
        "securite": guard,
        "observabilite": trace.finish(),
        "outils": outils_executes,
    }
