import openai
import json
import re
from vector_db import find_product

# API key for OpenAI GPT-4 (left in for exam reviewer)
openai.api_key = "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"

def singularize(word):
    """Converts plural words to singular form using basic regex rules."""
    return re.sub(r's$', '', word, flags=re.IGNORECASE)

def interpret_query(user_query):
    """
    Uses GPT-4 to interpret the query and classify it as a product inquiry or store info request.
    """
    system_prompt = """You are an AI assistant for a general store.

    You must interpret customer queries and classify them into one of the following categories:

    1. **Product Inquiry**: 
       Extract the product name, department, and whether the user is asking about price.

    2. **Store Information**: 
       Extract the main topic (e.g., 'store hours', 'return policy', or 'electronics').

    3. **Non-Store Query**: 
       If the query is unrelated to the store (like a joke request), categorize it as `"non_store_query": true`.

    **Example JSON Outputs:**

    Product inquiry:
    {"item": "iPhone", "department": "Electronics", "price_query": true, "query_type": "product"}

    Store info inquiry:
    {"topic": "store hours", "query_type": "info"}

    Non-store query:
    {"query_type": "non_store_query"}

    Only return valid JSON. No extra text.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )

        parsed_data = json.loads(response["choices"][0]["message"]["content"].strip())

        query_type = parsed_data.get("query_type")

        if query_type == "non_store_query":
            return {
                "type": "error",
                "item": "unknown item",
                "department": "",
                "price_query": False
            }

        if query_type == "product":
            item_name = parsed_data.get("item", "").strip()
            department = parsed_data.get("department", "").strip()

            # Fallback: If the department is missing, infer it from a lookup table
            department_lookup = {
                "iphone": "Electronics",
                "tv": "Electronics",
                "samsung tv": "Electronics",
                "milk": "Grocery",
                "shoes": "Clothing"
            }

            if not department and item_name.lower() in department_lookup:
                department = department_lookup[item_name.lower()]

            return {
                "type": "product",
                "item": item_name if item_name else "unknown item",
                "department": department if department else "",  # Fix: Default to empty string, not "Unknown"
                "price_query": parsed_data.get("price_query", False)
            }

        elif query_type == "info":
            topic = parsed_data.get("topic", "").strip()
            if not topic:
                topic = "general information"

            topic_map = {
                "store hours": "Store Hours",
                "return policy": "Return Policy",
                "electronics": "Electronics",
                "grocery": "Grocery",
                "clothing": "Clothing"
            }
            matched_topic = topic_map.get(topic.lower(), topic)

            return {
                "type": "info",
                "item": matched_topic,
                "price_query": False
            }

        return {"type": "error", "item": "unknown item", "department": "", "price_query": False}

    except json.JSONDecodeError:
        return {"type": "error", "item": "unknown item", "department": "", "price_query": False}

def process_customer_query(user_query):
    """
    Processes customer queries by interpreting them and retrieving relevant product or store information.
    """
    query_data = interpret_query(user_query)

    if query_data.get("type") == "error":
        return "I'm sorry, there was an issue understanding your request."

    query_target = query_data.get("item") or query_data.get("topic")

    if not query_target:
        return "Sorry, I couldn't understand your request."

    # Search for the matching product or store information
    result = find_product(query_target)

    if not result:
        return "Sorry, I couldn't find any relevant information."

    # Handle store information queries
    if result.get("type") == "info":
        return result.get("content", "Sorry, I don't have information on that topic.")

    # Handle product queries
    response = (
        f"Department: {result['department']}\n"
        f"Item: {result['item']}\n"
        f"Available: {'Yes' if result['in_stock'] else 'No'}\n"
    )
    if query_data.get("price_query"):
        response += f"Price: ${result['price']}"
    return response


if __name__ == "__main__":
    user_query = input("Ask about a product or store info: ")
    print(process_customer_query(user_query))
