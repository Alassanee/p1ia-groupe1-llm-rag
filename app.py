"""
Point d'entrée de l'assistant RAG — Groupe 1.
Responsable : Alassane (intégration).

Prérequis (voir README) :
    1. pip install -r requirements.txt
    2. .env avec GROQ_API_KEY
    3. python -m src.rag.build_index   # construit l'index Chroma
    4. python app.py
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
            print("\n📎 Sources utilisées :")
            for p in result["passages"]:
                print(f"  - [{p['source']}] {p['texte'][:120]}...")
        print()


if __name__ == "__main__":
    main()
