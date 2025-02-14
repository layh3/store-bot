import pytest
from vector_db import find_entry

# --- Product Search Tests ---

def test_find_existing_product():
    result = find_entry("iPhone 15", "products")
    assert result is not None
    assert result["item"].lower() == "iphone 15"


def test_find_non_existing_product():
    result = find_entry("PlayStation 5", "products")
    assert result is None


def test_find_similar_product():
    result = find_entry("milks", "products")
    assert result is not None
    assert "milk" in result["item"].lower()


def test_find_partial_product_name():
    result = find_entry("iPhon", "products")
    assert result is not None
    assert "iphone" in result["item"].lower()

# --- Store Information Tests ---

def test_find_store_hours():
    result = find_entry("store hours", "store_info")
    assert result is not None
    assert result["topic"] == "Store Hours"
    assert "open" in result["content"].lower()


def test_find_return_policy():
    result = find_entry("return policy", "store_info")
    assert result is not None
    assert result["topic"] == "Return Policy"
    assert "return" in result["content"].lower()


def test_find_department_info():
    result = find_entry("electronics", "store_info")
    assert result is not None
    assert result["topic"] == "Electronics"
    assert "phones" in result["content"].lower()


# --- Edge Cases ---

def test_find_empty_string():
    result = find_entry("", "products")
    assert result is None


def test_find_gibberish():
    result = find_entry("!@#$%^&*()", "products")
    assert result is None


def test_find_info_partial():
    result = find_entry("return", "store_info")
    assert result is not None
    assert "return" in result["content"].lower()


def test_find_low_similarity_product():
    result = find_entry("zyxwvutsrq", "products")
    assert result is None


def test_find_low_similarity_info():
    result = find_entry("abcdxyz", "store_info")
    assert result is None

