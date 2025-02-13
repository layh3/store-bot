import pytest
from vector_db import find_product

# --- Product Search Tests ---

def test_find_existing_product():
    """Test retrieving a product that exists in the database."""
    result = find_product("iPhone 15")
    assert result is not None
    assert result["item"] == "iPhone 15"

def test_find_non_existing_product():
    """Test searching for a product that does not exist in the database."""
    result = find_product("PlayStation 5")
    assert result is None  # Should return None for products not in DB

def test_find_similar_product():
    """Test searching for a product with slight variations in the query."""
    result = find_product("milk")
    assert result is not None
    assert "milk" in result["item"].lower()  # Should match "Milk"

# --- Store Information Tests ---

def test_find_store_hours():
    """Test retrieving store hours from the database."""
    result = find_product("store hours")
    assert result is not None
    assert result["item"] == "Store Hours"
    assert "open" in result["content"].lower()  # Ensuring content describes store hours

def test_find_return_policy():
    """Test retrieving the store return policy."""
    result = find_product("return policy")
    assert result is not None
    assert result["item"] == "Return Policy"
    assert "return" in result["content"].lower()  # Ensuring relevant content is returned

# --- Failure & Edge Case Tests ---

def test_find_nonexistent_product():
    """Test searching for a completely fictional product."""
    result = find_product("Flying Car")
    assert result is None  # Should return None for a non-existent product

def test_find_empty_string():
    """Test handling of an empty string query."""
    result = find_product("")
    assert result is None  # Should return None for an empty query

def test_find_gibberish():
    """Test handling of random gibberish input."""
    result = find_product("!@#$%^&*()")
    assert result is None  # Should return None for a meaningless query
