from query_handler import process_customer_query

# Display a welcome message
print("Welcome to the Store Assistant! Type 'exit' to quit.")

# Main loop for handling customer interactions
while True:
    user_query = input("\nCustomer: ")

    # Exit condition
    if user_query.lower() == "exit":
        print("Goodbye!")
        break

    # Process the query and return a response
    response = process_customer_query(user_query)

    # Determine output formatting
    if ":" in response:
        print("\nAssistant (Product Info):\n" + response)
    else:
        print("\nAssistant (Store Info):\n" + response)
