"""
Évaluation — Khadidiatou.
Lance les questions de référence (eval/questions.json) sur le pipeline et affiche
réponse de référence vs réponse du RAG + sources retrouvées.
À enrichir : métriques (fidélité, pertinence du retrieval), export, analyse des échecs.

Lancer depuis la racine :
    python -m src.evaluation.run_eval
"""
import json

from src.rag.pipeline import answer

QUESTIONS = "eval/questions.json"


def main() -> None:
    with open(QUESTIONS, encoding="utf-8") as f:
        questions = json.load(f)

    for item in questions:
        res = answer(item["question"])
        sources = ", ".join(sorted({p["source"] for p in res["passages"]}))
        print("Q   :", item["question"])
        print("Réf :", item.get("reponse_reference", ""))
        print("RAG :", res["reponse"])
        print("Sources retrouvées :", sources)
        print("-" * 70)

    # TODO (Khadidiatou) : calculer fidélité + pertinence du retrieval,
    # exporter un tableau, et rédiger l'analyse des échecs.


if __name__ == "__main__":
    main()
