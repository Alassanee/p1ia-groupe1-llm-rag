"""
Construction de l'index vectoriel (LangChain + Chroma) — Alassane.

Charge le corpus local (data/corpus/**/*.txt), le découpe, l'encode et
persiste l'index dans data/index/chroma.

Lancer depuis la racine :
    python -m src.rag.build_index
"""
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src.rag.config import CORPUS_DIR, PERSIST_DIR, EMB_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


def main() -> None:
    loader = DirectoryLoader(
        CORPUS_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs = loader.load()
    if not docs:
        print(f"⚠️ Aucun document .txt dans {CORPUS_DIR}/ — ajoute le corpus d'abord.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMB_MODEL)
    Chroma.from_documents(chunks, embeddings, persist_directory=PERSIST_DIR)
    print(f"✅ {len(docs)} document(s) → {len(chunks)} chunks indexés dans {PERSIST_DIR}")


if __name__ == "__main__":
    main()
