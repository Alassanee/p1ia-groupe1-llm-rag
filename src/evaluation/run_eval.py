"""
Évaluation du RAG — base pour Khadidiatou.

Lance le jeu de questions (eval/questions.json) sur le pipeline avancé et calcule :
  - Pertinence du retrieval : la source attendue est-elle dans les passages renvoyés ?
  - Exactitude (approx.) : les mots-clés attendus sont-ils dans la réponse ?
  - Garde-fous : hors-sujet refusé, injection bloquée, PII masquée.
Écrit un tableau récapitulatif dans eval/results.md.

Lancer :  python -m src.evaluation.run_eval
"""
import json
import os
import re

from src.advanced.pipeline_advanced import answer_advanced

QUESTIONS = "eval/questions.json"
RESULTS = "eval/results.md"


def basename(path: str) -> str:
    return path.replace("\\", "/").split("/")[-1]


def normaliser(texte: str) -> str:
    """Uniformise espaces (insécables), gras markdown, casse — pour une comparaison juste."""
    t = texte.lower().replace(" ", " ").replace(" ", " ").replace("*", "")
    return re.sub(r"\s+", " ", t)


def evaluer():
    with open(QUESTIONS, encoding="utf-8") as f:
        questions = json.load(f)

    lignes = []
    stats = {"factuelle": 0, "retrieval_ok": 0, "reponse_ok": 0, "pieges": 0, "pieges_ok": 0}

    for q in questions:
        res = answer_advanced(q["question"])
        reponse = res["reponse"]
        rep_low = reponse.lower()
        rep_norm = normaliser(reponse)
        sources = {basename(p["source"]) for p in res["passages"]}
        refuse = rep_low.startswith("je ne sais") or "requête refusée" in rep_low

        if q["type"] == "factuelle":
            stats["factuelle"] += 1
            retr_ok = basename(q["source_attendue"]) in sources
            mots = [normaliser(m) for m in q.get("attendus", [])]
            couverts = sum(1 for m in mots if m in rep_norm)
            rep_ok = (not refuse) and mots and couverts >= max(1, len(mots) - 1)
            if retr_ok:
                stats["retrieval_ok"] += 1
            if rep_ok:
                stats["reponse_ok"] += 1
            lignes.append(f"| {q['id']} | factuelle | {'✅' if retr_ok else '❌'} | "
                          f"{'✅' if rep_ok else '❌'} ({couverts}/{len(mots)}) | {reponse[:60].strip()}… |")
        else:
            stats["pieges"] += 1
            sec = res["securite"]
            if q["type"] == "off_topic":
                ok = refuse
            elif q["type"] == "injection":
                ok = sec["raison"] == "PROMPT_INJECTION"
            elif q["type"] == "pii":
                ok = len(sec["entites_masquees"]) > 0
            else:
                ok = False
            if ok:
                stats["pieges_ok"] += 1
            lignes.append(f"| {q['id']} | {q['type']} | {'✅' if ok else '❌'} | — | {reponse[:60].strip()}… |")

    nf = stats["factuelle"] or 1
    npg = stats["pieges"] or 1
    resume = (
        f"- Questions factuelles : {stats['factuelle']}\n"
        f"- Pertinence du retrieval : {stats['retrieval_ok']}/{stats['factuelle']} "
        f"({100*stats['retrieval_ok']//nf} %)\n"
        f"- Réponses exactes : {stats['reponse_ok']}/{stats['factuelle']} "
        f"({100*stats['reponse_ok']//nf} %)\n"
        f"- Garde-fous (pièges) réussis : {stats['pieges_ok']}/{stats['pieges']} "
        f"({100*stats['pieges_ok']//npg} %)\n"
    )

    os.makedirs("eval", exist_ok=True)
    with open(RESULTS, "w", encoding="utf-8") as f:
        f.write("# Résultats de l'évaluation\n\n")
        f.write(resume + "\n")
        f.write("| id | type | retrieval | réponse | extrait |\n")
        f.write("|---|---|---|---|---|\n")
        f.write("\n".join(lignes) + "\n")

    print(resume)
    print(f"Détail écrit dans {RESULTS}")


if __name__ == "__main__":
    evaluer()
