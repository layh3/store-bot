import lancedb
import pandas as pd
import spacy

# Load spaCy's medium-sized word embedding model for text processing
nlp = spacy.load("en_core_web_md")

# Sample product and general store information data
data = pd.DataFrame([
    # Product entries
    {"item": "iPhone 15", "department": "Electronics", "price": 999, "in_stock": True, "type": "product", "content": ""},
    {"item": "Samsung TV", "department": "Electronics", "price": 799, "in_stock": False, "type": "product", "content": ""},
    {"item": "Milk", "department": "Grocery", "price": 2.99, "in_stock": True, "type": "product", "content": ""},
    {"item": "Nike Shoes", "department": "Clothing", "price": 120, "in_stock": True, "type": "product", "content": ""},

    # General store information entries
    {"item": "Electronics", "department": "Electronics", "price": None, "in_stock": None, "type": "info",
     "content": "The Electronics department carries phones, TVs, and accessories."},
    {"item": "Grocery", "department": "Grocery", "price": None, "in_stock": None, "type": "info",
     "content": "The Grocery department offers fresh produce, dairy, and baked goods."},
    {"item": "Clothing", "department": "Clothing", "price": None, "in_stock": None, "type": "info",
     "content": "The Clothing department sells casual and formal attire, including shoes."},
    {"item": "Store Hours", "department": "General", "price": None, "in_stock": None, "type": "info",
     "content": "The store is open from 9 AM to 9 PM, Monday to Sunday."},
    {"item": "Return Policy", "department": "General", "price": None, "in_stock": None, "type": "info",
     "content": "Items can be returned within 30 days with a receipt."}
])

# Generate embeddings using both item name and content for better search accuracy
data["embedding"] = data.apply(
    lambda row: nlp(row["item"] + " " + row["content"]).vector.tolist(), axis=1
)

# Connect to LanceDB
db = lancedb.connect("store_db")

# Drop existing table if it exists to ensure fresh data
if "products" in db.table_names():
    db.drop_table("products")

# Create a new table with product and store information
table = db.create_table("products", data)

print("Database initialized successfully with product and store information.")
