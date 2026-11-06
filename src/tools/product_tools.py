
from langchain_core.tools import tool

from src.database.db import get_connection


@tool
def search_products(
    query: str = "",
    max_price: float = 0,
) -> str:
    """Search available musical instruments by product name or category.

    Examples: 'violão', 'guitarra', 'Yamaha'.
    Use max_price=0 when there is no price limit.
    """
    sql = """
        SELECT p.name, c.name, p.price_brl, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.status = 'active'
          AND p.stock_quantity > 0
          AND (
              LOWER(p.name) LIKE LOWER(?)
              OR LOWER(c.name) LIKE LOWER(?)
          )
          AND (? = 0 OR p.price_brl <= ?)
        ORDER BY p.price_brl ASC
        LIMIT 10
    """

    search = query.strip().lower()

    aliases = {
        "violão": "violões",
        "guitarra": "guitarras",
        "baixo": "baixos",
        "bateria": "baterias",
        "teclado": "teclados",
    }

    search = aliases.get(search, search)
    pattern = f"%{search}%"

    with get_connection() as conn:
        products = conn.execute(
            sql,
            (pattern, pattern, max_price, max_price),
        ).fetchall()

    if not products:
        return "No matching products found."

    return "\n".join(
        f"{name} | Category: {category} | "
        f"Price: R$ {price:.2f} | Stock: {stock}"
        for name, category, price, stock in products
    )
