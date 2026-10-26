"""
Cœur RAG (LangChain) — Alassane.

Retrieval (Chroma) + génération (Groq) + citation des sources.
Interface (contrat d'équipe) :
    answer(question) -> {"reponse": str, "passages": [{"texte", "source"}, ...]}

Prérequis : avoir lancé `python -m src.rag.build_index` au moins une fois.
"""
import functools
import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

from src.rag.config import PERSIST_DIR, EMB_MODEL, TOP_K, FETCH_K, SEARCH_TYPE

LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")

SYSTEM = (
    "Tu es un assistant qui répond aux questions sur les démarches administratives "
    "du Sénégal UNIQUEMENT à partir des passages fournis. Si l'information ne s'y "
    "trouve pas, réponds exactement : « Je ne sais pas d'après le corpus. » "
    "Indique la ou les sources utilisées."
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "Passages :\n{context}\n\nQuestion : {question}"),
])


@functools.lru_cache(maxsize=1)
def _store() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=EMB_MODEL)
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


@functools.lru_cache(maxsize=1)
def _llm() -> ChatGroq:
    return ChatGroq(model=LLM_MODEL, temperature=0.1)


def answer(question: str, k: int = TOP_K) -> dict:
    retriever = _store().as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={"k": k, "fetch_k": FETCH_K},
    )
    docs = retriever.invoke(question)
    if not docs:
        return {"reponse": "Je ne sais pas d'après le corpus.", "passages": []}

    context = "\n\n".join(
        f"[Source: {d.metadata.get('source', '?')}]\n{d.page_content}" for d in docs
    )
    reponse = (PROMPT | _llm()).invoke({"context": context, "question": question}).content

    passages = [
        {"texte": d.page_content, "source": d.metadata.get("source", "?")} for d in docs
    ]
    return {"reponse": reponse, "passages": passages}
