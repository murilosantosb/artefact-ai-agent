from langchain_core.tools import tool

from src.database.seed import get_connection
from src.rag.search import search_policies


@tool
def search_store_policies(question: str):
    """Search store policies for returns, exchanges, shipping,
    payment methods, opening hours and store information.
    """
    
    documents = search_policies(question)
    
    if not documents:
        return "No relevant policy information found."
    
    results = []
    
    for doc in documents:
        page = doc.metadata.get("page", "Unknown")
        
        results.append(
            f"Page {page}:\n{doc.page_content}"
        )
        
    return "\n\n".join(results)