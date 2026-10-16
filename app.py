"""
Point d'entrée de l'assistant RAG — Groupe 1.
Responsable : Alassane (intégration).

Ce fichier assemble les modules de l'équipe. Les imports marqués TODO
seront activés au fur et à mesure que chaque module est prêt.
"""

# from src.rag.pipeline import answer   # TODO: activer quand src/rag est prêt


def main():
    print("=== Assistant RAG — Groupe 1 ===")
    print("Pose une question sur le corpus (ou 'quit' pour sortir).\n")

    while True:
        question = input("❓ Question : ").strip()
        if question.lower() in {"quit", "exit", "q", ""}:
            break

        # TODO (intégration) : brancher le vrai pipeline
        # result = answer(question)
        # print("\n💬 Réponse :", result["reponse"])
        # print("\n📎 Passages cités :")
        # for p in result["passages"]:
        #     print(f"  - [{p['source']}] {p['texte'][:120]}...")

        print("\n[squelette] Le pipeline n'est pas encore branché.\n")


if __name__ == "__main__":
    main()
