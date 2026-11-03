from database.db import get_connection

def main():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT name, price_brl, stock_quantity
            FROM products
            WHERE price_brl <= 1000
                AND stock_quantity > 0
                AND status = 'active'
               ORDER BY price_brl ASC    
    """)
    products = cursor.fetchall()

    for name, price, stock in products:
        print(f"{name} - R$ {price:.2f} - Estoque: {stock}")

if __name__ == "__main__":
    main()