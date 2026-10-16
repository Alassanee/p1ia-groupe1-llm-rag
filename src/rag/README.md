# Module RAG (cœur) — Alassane

**But :** assembler retrieval + génération.

**À exposer :** `answer(question: str) -> dict`
retour : `{ "reponse": "...", "passages": [ {"texte","source","score"}, ... ] }`

**Étapes :**
1. `passages = search(question, k)` (module embeddings de Fatima).
2. Construire le prompt : consignes + passages + question.
3. Appeler le LLM (Groq/Gemini via `.env`).
4. Retourner la réponse **et** les passages cités.
5. Brancher le tout dans `app.py`.

**Garde-fou minimal :** si aucun passage pertinent, répondre « je ne sais pas d'après le corpus ».
