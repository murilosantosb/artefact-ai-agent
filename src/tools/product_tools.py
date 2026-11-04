from langchain_core.tools import tool
from database.db import get_connection

@tool
def search_products(
    name: str = "",
    category: str = "",
    max_price: float = 0
) -> str:
    """Search available musical instruments by name, category or maximum price.

    Use empty strings to ignore name/category filters.
    Use max_price=0 to ignore the price filter.
    """
    
    query = """
     SELECT p.name, c.name, p.price_brl, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.status = 'active'
          AND p.stock_quantity > 0
          AND LOWER(p.name) LIKE LOWER(?)
          AND LOWER(c.name) LIKE LOWER(?)
          AND (? = 0 OR p.price_brl <= ?)
        ORDER BY p.price_brl ASC
        LIMIT 10   
    """
    
    with get_connection() as conn:
        products = conn.execute(
            query,
             (f"%{name}%", f"%{category}%", max_price, max_price),
        ).fetchall()
        
    if not products:
        return "No matching products found."
    
    return "\n".join(
        f"{product_name} | Category: {product_category} | "
        f"Price: R$ {price:.2f} | Stock: {stock}"
        for product_name, product_category, price, stock in products
    )