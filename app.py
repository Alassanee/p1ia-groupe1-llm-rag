"""
Point d'entrée de l'assistant RAG — Groupe 1.
Responsable : Alassane (intégration).

Utilise le pipeline AVANCÉ (RAG + garde-fous + observabilité + outils).

Prérequis (voir README) :
    1. pip install -r requirements.txt
    2. .env avec GROQ_API_KEY
    3. python -m src.rag.build_index   # construit l'index Chroma
    4. python app.py
"""
from src.advanced.pipeline_advanced import answer_advanced


def main():
    print("=== Assistant RAG — Groupe 1 (démarches administratives) ===")
    print("Pose une question sur le corpus (ou 'quit' pour sortir).\n")

    while True:
        question = input("❓ Question : ").strip()
        if question.lower() in {"quit", "exit", "q", ""}:
            break

        result = answer_advanced(question)
        print("\n💬 Réponse :", result["reponse"])

        if result["passages"]:
            print("\n📎 Sources utilisées :")
            for p in result["passages"]:
                print(f"  - [{p['source']}] {p['texte'][:120]}...")

        obs = result["observabilite"]
        print(
            f"\n⏱️  {obs['latences_secondes']['totale']}s · "
            f"{obs['tokens']['total']} tokens · "
            f"~{obs['cout_estime_usd']:.6f} $"
        )
        if result["outils"]:
            print(f"🛠️  outil utilisé : {result['outils'][0]['outil']}")
        print()


if __name__ == "__main__":
    main()
