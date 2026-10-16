"""
Cœur RAG — Alassane.
Expose la fonction du contrat d'interface :
    answer(question) -> {reponse, passages}
Assemble : recherche des passages (Fatima) + génération (LLM).
"""
import os

from dotenv import load_dotenv

from src.embeddings.search import search

load_dotenv()

SYSTEM = (
    "Tu es un assistant qui répond UNIQUEMENT à partir des passages fournis. "
    "Si l'information ne s'y trouve pas, réponds exactement : "
    "« Je ne sais pas d'après le corpus. » Cite la source utilisée."
)
SEUIL_PERTINENCE = 0.80   # garde-fou minimal (à calibrer pendant l'éval)


def build_prompt(question: str, passages: list[dict]) -> str:
    contexte = "\n\n".join(f"[Source: {p['source']}]\n{p['texte']}" for p in passages)
    return f"{SYSTEM}\n\n### Passages\n{contexte}\n\n### Question\n{question}\n\n### Réponse :"


def call_llm(prompt: str) -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return "[LLM non configuré — ajoute GROQ_API_KEY dans .env pour activer la génération]"
    from groq import Groq
    client = Groq(api_key=key)
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return resp.choices[0].message.content.strip()


def answer(question: str, k: int = 4) -> dict:
    passages = search(question, k)
    # Garde-fou : si rien d'assez proche, on n'invente pas.
    if not passages or passages[0]["score"] < SEUIL_PERTINENCE:
        return {"reponse": "Je ne sais pas d'après le corpus.", "passages": passages}
    reponse = call_llm(build_prompt(question, passages))
    return {"reponse": reponse, "passages": passages}
