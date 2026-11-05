from src.tools.product_tools import search_products
from src.tools.order_tools import get_order_status
from src.tools.policy_tools import search_store_policies

def main():
    print("\n=== PRODUCT SEARCH ===")
    
    result = search_products.invoke({
        "name": "",
        "category": "Violões",
        "max_price": 1000,
    })
    
    print(result)
    
    print("\n=== ORDER ===")
    
    # Teste errado para verifica se a tool está sendo executada corretamente
    result = get_order_status.invoke({
        "order_id": 4,
        "email": "errado@exemplo.com"
    })
    
    print(result)
    
    print("\n=== POLICY SEARCH ===")
    
    result = search_store_policies.invoke({
        "question": "Qual é a política de devolução para compras online?"
    })
    
    print(result)
    
if __name__ == "__main__":
    main()