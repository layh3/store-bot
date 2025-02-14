import lancedb
import pandas as pd
import spacy
import re
import numpy as np

# Load spaCy's medium-sized word embedding model
nlp = spacy.load("en_core_web_md")

# Connect to LanceDB
db = lancedb.connect("store_db")

def singularize(word):
    """Converts plural words to singular form using basic regex rules."""
    return re.sub(r's$', '', word, flags=re.IGNORECASE)


def find_entry(query_text, table_name):
    """
    Uses vector similarity search to find the best match in the specified table.

    Parameters:
        query_text (str): The search query (product name or info topic).
        table_name (str): The name of the table to search ('products' or 'store_info').

    Returns:
        dict: The best matching result or None if no match found.
    """
    # Preprocess the query: lowercase and singularize
    cleaned_query = singularize(query_text.lower()).strip()

    if not cleaned_query:
        return None

    # Open the correct table
    table = db.open_table(table_name)
    df = table.search().limit(1000).to_pandas()


    if df.empty:
        return None

    # Generate the query embedding
    query_embedding = np.array(nlp(cleaned_query).vector)

    # Calculate cosine similarity
    df["similarity"] = df["embedding"].apply(
        lambda emb: np.dot(np.array(emb), query_embedding) / 
                    (np.linalg.norm(emb) * np.linalg.norm(query_embedding))
    )

    # Access the top 5 matches (could be usedto provide additional products in the future)
    top_matches = df.sort_values("similarity", ascending=False).head(5)

    # Get the best match
    best_match = top_matches.iloc[0]

    # Adjust threshold based on table type and query length
    similarity_threshold = 0.55 if table_name == "store_info" else 0.75

    # Filter out potential false positives
    if best_match["similarity"] < similarity_threshold:
        print(f"No valid match found for '{query_text}' (Best similarity: {best_match['similarity']:.2f})")
        return None

    # Ensure the match shares a keyword with the query
    if not any(word in best_match.get("item", best_match.get("topic", "")).lower() for word in cleaned_query):
        print(f"Potential false positive: '{best_match.get('item', best_match.get('topic', ''))}' doesn't match '{cleaned_query}'")
        return None

    return best_match.to_dict()
