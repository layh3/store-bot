import pytest
from query_handler import interpret_query

# --- Product Inquiry Tests ---

def test_interpret_query_basic():
    """Test if a basic product inquiry correctly extracts item and department."""
    query = "Do you have iPhones?"
    result = interpret_query(query)

    # Validate product name and department
    assert result["item"].lower() == "iphone"  # Should be singularized automatically
    assert result.get("department", "") in ["Electronics", ""]  # Department inference optional
    assert result["price_query"] is False  # Default to False for non-price queries


def test_interpret_query_price_request():
    """Test if price-related queries are correctly identified."""
    query = "How much is a Samsung TV?"
    result = interpret_query(query)

    assert "tv" in result["item"].lower()  # Recognize 'Samsung TV'
    assert result.get("department", "") in ["Electronics", ""]  # Electronics department expected
    assert result["price_query"] is True  # Detects price query correctly


def test_interpret_query_unknown():
    """Test how the system handles vague or unclear product inquiries."""
    query = "Do you have anything good?"
    result = interpret_query(query)

    assert result["item"] == "unknown item"  # Should default to 'unknown item'
    assert result.get("department", "") == ""  # No department detected
    assert result["price_query"] is False  # Should default to False


# --- Store Information Tests ---

def test_interpret_query_store_hours():
    """Test if store-related queries are recognized."""
    query = "What are the store hours?"
    result = interpret_query(query)

    assert result["type"] == "info"  # Ensure it's classified as store information
    assert result["item"] == "Store Hours"  # Matches the exact database entry


def test_interpret_query_return_policy():
    """Test if return policy questions are correctly classified."""
    query = "What is your return policy?"
    result = interpret_query(query)

    assert result["type"] == "info"  # Ensure it's classified as store info
    assert result["item"] == "Return Policy"  # Confirm correct topic mapping


# --- Non-Store Query Tests ---

def test_interpret_non_store_query():
    """Test how the system handles non-store-related queries."""
    query = "Tell me a joke."
    result = interpret_query(query)

    # Ensure it recognizes the query as unrelated
    assert result["type"] == "error"
    assert result["item"] == "unknown item"
    assert result.get("department", "") == ""
    assert result["price_query"] is False


def test_interpret_query_gibberish():
    """Handle cases where the query is nonsense."""
    query = "asdkjhasd87y9832"
    result = interpret_query(query)

    # Should treat gibberish like a non-store query
    assert result["type"] == "error"
    assert result["item"] == "unknown item"
    assert result.get("department", "") == ""
    assert result["price_query"] is False


# --- Edge Cases ---

def test_interpret_query_empty():
    """Test with an empty query."""
    query = ""
    result = interpret_query(query)

    assert result["type"] == "error"
    assert result["item"] == "unknown item"
    assert result.get("department", "") == ""
    assert result["price_query"] is False


def test_interpret_query_edge_plural():
    """Test product with irregular plural form."""
    query = "Do you sell shoes?"
    result = interpret_query(query)

    assert result["item"].lower() == "shoe" or result["item"].lower() == "shoes"
    assert result.get("department", "") in ["Clothing", ""]


def test_interpret_query_mixed_case():
    """Test queries with mixed casing."""
    query = "Do you have a SaMsUnG TV?"
    result = interpret_query(query)

    assert "samsung" in result["item"].lower()
    assert result.get("department", "") in ["Electronics", ""]


def test_interpret_query_price_with_weird_spacing():
    """Test query with unusual spacing."""
    query = "   How   much   is a Samsung   TV?   "
    result = interpret_query(query)

    assert "tv" in result["item"].lower()
    assert result["price_query"] is True
    assert result.get("department", "") in ["Electronics", ""]


def test_interpret_query_partial_product_name():
    """Test query with partial product name."""
    query = "Do you have iPhon?"
    result = interpret_query(query)

    assert "iphone" in result["item"].lower()
    assert result.get("department", "") in ["Electronics", ""]


def test_interpret_query_store_info_partial():
    """Test query with partial store info term."""
    query = "When do you open?"
    result = interpret_query(query)

    assert result["type"] == "info"
    assert result["item"] == "Store Hours"

