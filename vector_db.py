import lancedb
import pandas as pd
import spacy
import numpy as np

# Load spaCy's medium-sized word embedding model for text processing
nlp = spacy.load("en_core_web_md")

# Connect to the LanceDB database
db = lancedb.connect("store_db")
table = db.open_table("products")

def find_product(query_text):
    """
    Uses vector similarity search to find the best-matching product or store information.

    Parameters:
        query_text (str): The search query (product name, department, or store info topic).

    Returns:
        dict: The most relevant match (product or store info), otherwise None.
    """
    if not query_text.strip():
        return None  # Return None for empty queries

    df = table.to_pandas()

    # Generate an embedding for the query using spaCy
    query_embedding = np.array(nlp(query_text).vector)

    # Compute cosine similarity between the query and stored embeddings
    df["similarity"] = df["embedding"].apply(
        lambda emb: np.dot(np.array(emb), query_embedding) / 
                    (np.linalg.norm(emb) * np.linalg.norm(query_embedding))
    )

    if df.empty:
        return None  # Return None if database is empty or retrieval fails

    # Retrieve the most similar match
    best_match = df.sort_values("similarity", ascending=False).iloc[0]

    # Ensure 'type' exists (either product or info)
    entry_type = best_match.get("type", "unknown")

    # Adjust similarity threshold for info queries
    similarity_threshold = 0.60 if entry_type == "info" else 0.75

    if best_match["similarity"] < similarity_threshold:
        return None  # No valid match found if similarity is too low

    return best_match.to_dict()

