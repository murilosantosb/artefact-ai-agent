from pathlib import Path
import pymupdf
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parents[2]
PDF_PATH = BASE_DIR / "data" / "politicas.pdf"
CHROMA_PATH = BASE_DIR / "chroma_db"

def ingest_pdf():
    documents = []

    with pymupdf.open(PDF_PATH) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text()

            if not text.strip():
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "politicas.pdf",
                        "page": page_number,
                    },
                )
            )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200    
    )

    splitter = chunks.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )

    vectorstore = Chroma.from_documents(
        collection_name="store_policies",
        documents=splitter,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    print(f"{len(documents)} páginas indexadas!")


if __name__ == "__main__":
    ingest_pdf()