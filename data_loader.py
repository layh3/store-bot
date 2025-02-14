import lancedb
import pandas as pd
import spacy

# Load spaCy's medium-sized word embedding model
nlp = spacy.load("en_core_web_md")

# Product data
product_data = pd.DataFrame([
    # Electronics
    {"item": "iPhone 15", "department": "Electronics", "price": 999, "in_stock": True},
    {"item": "Samsung Galaxy S22", "department": "Electronics", "price": 899, "in_stock": True},
    {"item": "Sony 65-inch TV", "department": "Electronics", "price": 1199, "in_stock": False},
    {"item": "Apple AirPods Pro", "department": "Electronics", "price": 249, "in_stock": True},
    {"item": "Lenovo Laptop", "department": "Electronics", "price": 750, "in_stock": True},

    # Grocery
    {"item": "Milk", "department": "Grocery", "price": 2.99, "in_stock": True},
    {"item": "Eggs", "department": "Grocery", "price": 3.49, "in_stock": True},
    {"item": "Whole Wheat Bread", "department": "Grocery", "price": 2.49, "in_stock": False},
    {"item": "Bananas", "department": "Grocery", "price": 0.69, "in_stock": True},
    {"item": "Orange Juice (1L)", "department": "Grocery", "price": 4.99, "in_stock": True},

    # Clothing
    {"item": "Nike Running Shoes", "department": "Clothing", "price": 120, "in_stock": True},
    {"item": "Adidas Hoodie", "department": "Clothing", "price": 60, "in_stock": False},
    {"item": "Levi's Jeans", "department": "Clothing", "price": 80, "in_stock": True},
    {"item": "Under Armour T-Shirt", "department": "Clothing", "price": 35, "in_stock": True},
    {"item": "Winter Jacket", "department": "Clothing", "price": 150, "in_stock": False},

    # Home & Kitchen
    {"item": "Instant Pot 6L", "department": "Home & Kitchen", "price": 120, "in_stock": True},
    {"item": "Dyson V11 Vacuum", "department": "Home & Kitchen", "price": 599, "in_stock": False},
    {"item": "Non-stick Frying Pan", "department": "Home & Kitchen", "price": 35, "in_stock": True},
    {"item": "Electric Kettle", "department": "Home & Kitchen", "price": 40, "in_stock": True},
    {"item": "Blender", "department": "Home & Kitchen", "price": 65, "in_stock": False},

    # Toys & Games
    {"item": "LEGO City Set", "department": "Toys & Games", "price": 50, "in_stock": True},
    {"item": "Monopoly Board Game", "department": "Toys & Games", "price": 25, "in_stock": True},
    {"item": "Nintendo Switch", "department": "Toys & Games", "price": 299, "in_stock": False},
    {"item": "Puzzle", "department": "Toys & Games", "price": 20, "in_stock": True},
    {"item": "RC Car", "department": "Toys & Games", "price": 75, "in_stock": False},
])

# Add embeddings for product items
product_data["embedding"] = product_data["item"].apply(lambda x: nlp(x).vector.tolist())


# Store information data
info_data = pd.DataFrame([
    # General Store Info
    {"topic": "Store Hours", "content": "The store is open from 9 AM to 9 PM, Monday to Sunday."},
    {"topic": "Return Policy", "content": "Items can be returned within 30 days with a receipt."},
    {"topic": "Store Locations", "content": "We have stores located in Toronto, Vancouver, and Calgary."},
    {"topic": "Store Contact", "content": "You can reach us at 1-800-STORE-HELP or email contact@storebot.com."},
    {"topic": "Store Services", "content": "We offer delivery, curbside pickup, and gift wrapping services."},

    # Department Overviews
    {"topic": "Electronics", "content": "The Electronics department offers smartphones, TVs, laptops, and audio devices."},
    {"topic": "Grocery", "content": "The Grocery department provides fresh produce, dairy, baked goods, and beverages."},
    {"topic": "Clothing", "content": "The Clothing department has apparel for all ages, including footwear and accessories."},
    {"topic": "Home & Kitchen", "content": "The Home & Kitchen section features appliances, cookware, and cleaning supplies."},
    {"topic": "Toys & Games", "content": "The Toys & Games department includes educational toys, puzzles, and gaming consoles."},

    # Policies & Customer Guidance
    {"topic": "Shipping Policy", "content": "We offer standard, express, and next-day shipping options across Canada."},
    {"topic": "Refund Policy", "content": "Refunds are available within 30 days with a receipt. Some exclusions apply."},
    {"topic": "Warranty Policy", "content": "Most electronics come with a 1-year warranty. Extended warranties available."},
    {"topic": "Payment Methods", "content": "We accept Visa, MasterCard, AMEX, PayPal, and in-store payments."},
    {"topic": "Gift Cards", "content": "Gift cards are available in-store and online in various denominations."}
])


# Add embeddings for info topics
info_data["embedding"] = info_data["topic"].apply(lambda x: nlp(x).vector.tolist())

# Connect to LanceDB
db = lancedb.connect("store_db")

# Drop and recreate the products table
if "products" in db.table_names():
    db.drop_table("products")
db.create_table("products", product_data)

# Drop and recreate the store_info table
if "store_info" in db.table_names():
    db.drop_table("store_info")
db.create_table("store_info", info_data)

print("Database with product and store information initialized successfully!")

