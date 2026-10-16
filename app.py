"""
Point d'entrée de l'assistant RAG — Groupe 1.
Responsable : Alassane (intégration).

Prérequis (voir README) :
    1. python -m src.ingestion.run        # corpus -> data/chunks.json
    2. python -m src.embeddings.build_index   # -> data/index/
    3. python app.py
"""
from src.rag.pipeline import answer


def main():
    print("=== Assistant RAG — Groupe 1 (démarches administratives) ===")
    print("Pose une question sur le corpus (ou 'quit' pour sortir).\n")

    while True:
        question = input("❓ Question : ").strip()
        if question.lower() in {"quit", "exit", "q", ""}:
            break

        result = answer(question)
        print("\n💬 Réponse :", result["reponse"])
        if result["passages"]:
            print("\n📎 Passages utilisés :")
            for p in result["passages"]:
                print(f"  - [{p['source']}] (score {p['score']:.2f}) {p['texte'][:120]}...")
        print()


if __name__ == "__main__":
    main()
