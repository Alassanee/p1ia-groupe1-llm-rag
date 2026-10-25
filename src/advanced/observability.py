"""
Module Observabilité & Métriques — Abdou Aziz.
Mesure et journalise les indicateurs clés de chaque requête :
  1. Latence détaillée (recherche vectorielle, appel LLM, temps total).
  2. Consommation de tokens (prompt, réponse, total).
  3. Estimation du coût financier en dollars (USD) selon le modèle.
  4. Journalisation persistante dans 'eval/traces.jsonl' avec récapitulatif statistique.
"""
import json
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

LOG_FILE = "eval/traces.jsonl"

# Tarification indicative pour 1 000 000 de tokens (1M)
PRICING_PER_1M = {
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "default": {"input": 0.10, "output": 0.20},
}


def estimate_tokens(text: str) -> int:
    """
    Estimation rapide du nombre de tokens (règle empirique ~4 caractères / token pour le français).
    """
    if not text:
        return 0
    return max(1, int(len(text) / 3.8))


def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calcule le coût estimé en dollars (USD).
    """
    pricing = PRICING_PER_1M.get(model_name, PRICING_PER_1M["default"])
    cost_in = (input_tokens / 1_000_000) * pricing["input"]
    cost_out = (output_tokens / 1_000_000) * pricing["output"]
    return cost_in + cost_out


class QueryTrace:
    """
    Trace le cycle de vie d'une requête RAG.
    """

    def __init__(self, question: str):
        self.question = question
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.t_start = time.perf_counter()
        self.latence_retrieval_sec: float = 0.0
        self.latence_llm_sec: float = 0.0
        self.latence_totale_sec: float = 0.0
        self.model: str = "non-specifie"
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.total_tokens: int = 0
        self.cout_estime_usd: float = 0.0
        self.nb_passages: int = 0
        self.garde_fous_declenches: list[str] = []

    def record_retrieval(self, duration_sec: float, nb_passages: int):
        self.latence_retrieval_sec = round(duration_sec, 4)
        self.nb_passages = nb_passages

    def record_llm(
        self,
        duration_sec: float,
        model_name: str,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        prompt_text: str = "",
        response_text: str = "",
    ):
        self.latence_llm_sec = round(duration_sec, 4)
        self.model = model_name
        self.input_tokens = input_tokens if input_tokens is not None else estimate_tokens(prompt_text)
        self.output_tokens = output_tokens if output_tokens is not None else estimate_tokens(response_text)
        self.total_tokens = self.input_tokens + self.output_tokens
        self.cout_estime_usd = round(calculate_cost(self.model, self.input_tokens, self.output_tokens), 6)

    def record_guardrail(self, rule_name: str):
        self.garde_fous_declenches.append(rule_name)

    def finish(self, log_path: str = LOG_FILE) -> Dict[str, Any]:
        self.latence_totale_sec = round(time.perf_counter() - self.t_start, 4)
        data = {
            "timestamp": self.timestamp,
            "question": self.question,
            "model": self.model,
            "latences_secondes": {
                "retrieval": self.latence_retrieval_sec,
                "llm": self.latence_llm_sec,
                "totale": self.latence_totale_sec,
            },
            "tokens": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "total": self.total_tokens,
            },
            "cout_estime_usd": self.cout_estime_usd,
            "nb_passages_retrouves": self.nb_passages,
            "garde_fous": self.garde_fous_declenches,
        }

        # Sauvegarde en JSON Lines
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

        return data


def get_traces_summary(log_path: str = LOG_FILE) -> Dict[str, Any]:
    """
    Génère un résumé statistique des traces enregistrées pour le rapport.
    """
    if not os.path.exists(log_path):
        return {"total_requetes": 0, "message": "Aucune trace enregistrée."}

    total_requetes = 0
    total_tokens = 0
    total_cost = 0.0
    latences_totales = []
    latences_llm = []
    latences_retrieval = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            total_requetes += 1
            total_tokens += entry.get("tokens", {}).get("total", 0)
            total_cost += entry.get("cout_estime_usd", 0.0)
            lat = entry.get("latences_secondes", {})
            latences_totales.append(lat.get("totale", 0.0))
            latences_llm.append(lat.get("llm", 0.0))
            latences_retrieval.append(lat.get("retrieval", 0.0))

    if total_requetes == 0:
        return {"total_requetes": 0}

    return {
        "total_requetes": total_requetes,
        "total_tokens_consommes": total_tokens,
        "cout_cumule_usd": round(total_cost, 6),
        "latence_moyenne_sec": round(sum(latences_totales) / total_requetes, 3),
        "latence_llm_moyenne_sec": round(sum(latences_llm) / total_requetes, 3),
        "latence_retrieval_moyenne_sec": round(sum(latences_retrieval) / total_requetes, 3),
    }
