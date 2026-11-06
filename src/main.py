from src.agent.graph import agent


def main():
    print("=== Emporio da Musica AI Assistant ===")
    print("Type 'exit' to quit.\n")
    
    config = {
        "configurable": {
            "thread_id": "customer-session-1"
        }
    }
    
    while True:
        user_message = input("You: ").strip()
        
        if user_message.lower() in ("exit", "quit", "sair"):
            print("Goodbye!")
            break
        
        if not user_message:
            continue
        
        try:
            result = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": user_message}
                    ]
                },
                config=config
            )

            response = result["messages"][-1].content 
            
            print(f"\nAssistant: {response}\n")
            
        except Exception as error:
            print(f"\nError: {error}\n")

if __name__ == "__main__":
    main()