from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "chroma_db"

def search_policies(question: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    vectorstore = Chroma(
        collection_name="store_policies",
        embedding_function=embeddings,
        persist_directory=(CHROMA_PATH)
    )
    
    results = vectorstore.similarity_search(
        query=question,
        k=5
    )
    
    return results

if __name__ == "__main__":
    question = "Quais são as regras de trocas e devoluções?"
    
    results = search_policies(question)
    
    for doc in results:
        print(f"\nPágina: {doc.metadata['page']}")
        print(doc.page_content)