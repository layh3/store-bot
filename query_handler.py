import openai
import json
import re
from vector_db import find_entry

# API key for OpenAI GPT-4 (left in for exam reviewer)
openai.api_key = "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"

def singularize(word):
    """Convert plural words to singular form."""
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
            return {"type": "error", "item": "unknown item", "department": "", "price_query": False}

        if query_type == "product":
            item_name = parsed_data.get("item", "").strip()
            department = parsed_data.get("department", "").strip()

            # Fallback: Infer department from a basic lookup
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
                "item": singularize(item_name) if item_name else "unknown item",
                "department": department,
                "price_query": parsed_data.get("price_query", False)
            }

        elif query_type == "info":
            topic = parsed_data.get("topic", "").strip()
            if not topic:
                topic = "general information"

            # Map possible variations of info topics
            topic_map = {
                "store hours": "Store Hours",
                "return policy": "Return Policy",
                "electronics": "Electronics",
                "grocery": "Grocery",
                "clothing": "Clothing"
            }
            matched_topic = topic_map.get(topic.lower(), topic)

            return {"type": "info", "item": matched_topic}

        return {"type": "error", "item": "unknown item", "department": "", "price_query": False}

    except json.JSONDecodeError:
        return {"type": "error", "item": "unknown item", "department": "", "price_query": False}

def process_customer_query(user_query):
    """
    Processes customer queries by interpreting them and retrieving relevant product or store information.
    """
    query_data = interpret_query(user_query)
    query_type = query_data.get("type")

    # Route query to the appropriate table
    if query_type == "product":
        result = find_entry(query_data["item"], "products")
    elif query_type == "info":
        result = find_entry(query_data["item"], "store_info")
    else:
        return "Sorry, I couldn't understand your request."

    # Generate a response based on the query type and database result
    if result:
        if query_type == "info":
            return result.get("content", "No information available.")
        else:
            response = (
                f"Department: {result['department']}\n"
                f"Item: {result['item']}\n"
                f"Available: {'Yes' if result['in_stock'] else 'No'}\n"
            )
            if query_data.get("price_query"):
                response += f"Price: ${result['price']}"
            return response

    return "Sorry, no information found."
