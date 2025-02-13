import pytest
from query_handler import interpret_query

# --- Product Inquiry Tests ---

def test_interpret_query_basic():
    """Test if a basic product inquiry correctly extracts item and department."""
    query = "Do you have iPhones?"
    result = interpret_query(query)

    # Ensure item singularization is working properly
    expected_item = "iphone"
    assert result["item"].lower().rstrip("s") == expected_item  # Normalize plural form
    
    # Fix: Ensure the department defaults to "Unknown" if missing
    assert result.get("department", "Unknown") != "Unknown"  # Ensure department inference
    assert result["price_query"] is False  # Should default to False

def test_interpret_query_price_request():
    """Test if price-related queries are correctly identified."""
    query = "How much is a Samsung TV?"
    result = interpret_query(query)
    
    assert "tv" in result["item"].lower()  # Ensure item recognition
    assert result["department"] != ""  # Department should be inferred
    assert result["price_query"] is True  # Ensure it detects a price request

def test_interpret_query_unknown():
    """Test how the system handles vague or unclear product inquiries."""
    query = "Do you have anything good?"
    result = interpret_query(query)

    assert result["item"] in ["unknown item", "miscellaneous"]  # Should default to one of these
    assert result["department"] == ""  # No valid department detected
    assert result["price_query"] is False  # Default to False

# --- Store Information Tests ---

def test_interpret_query_store_hours():
    """Test if store-related queries are recognized."""
    query = "What are the store hours?"
    result = interpret_query(query)

    assert result["type"] == "info"  # Ensure classified as store info
    assert result["item"] == "Store Hours"  # Matches database key

def test_interpret_query_return_policy():
    """Test if return policy questions are correctly classified."""
    query = "What is your return policy?"
    result = interpret_query(query)

    assert result["type"] == "info"  # Store info category
    assert result["item"] == "Return Policy"  # Correct mapping

# --- Failure & Edge Case Tests ---

def test_interpret_query_invalid_json():
    """Simulate a failure where the LLM returns invalid JSON."""
    query = "Tell me a joke."
    result = interpret_query(query)

    # Fix: Accept the new response type
    assert result["item"] in ["unknown item"]
    assert result.get("department", "") == ""  # No department inferred
    assert result["price_query"] is False  # Default to False

def test_interpret_query_gibberish():
    """Handle cases where the query is nonsense."""
    query = "asdkjhasd87y9832"
    result = interpret_query(query)

    assert result["item"] in ["unknown item"]
    assert result.get("department", "") == ""  # Prevent KeyError
    assert result["price_query"] is False  # Default to False
