from langchain_core.tools import tool
from database.db import get_connection

@tool
def get_order_status(order_id: int, email: str) -> str:
    """Get an order's status using its ID and customer email.

    Ask for both fields before using this tool.
    Never return information for an unmatched order.
    """
    
    query = """
        SELECT o.order_id, o.status,
               o.estimated_delivery, o.tracking_code
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
          AND LOWER(c.email) = LOWER(?)
    """
    
    with get_connection() as conn:
        order = conn.execute(
            query,
            (order_id, email.strip())
        ).fetchone()
    
    if order is None:
        return "Order not found or customer information does not match."
    
    order_number, status, delivery, tracking = order
    
    return (
        f"Order: {order_number}\n"
        f"Status: {status}\n"
        f"Estimated delivery: {delivery or 'Not available'}\n"
        f"Tracking: {tracking or 'Not available'}"
    )