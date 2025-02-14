import streamlit as st
from query_handler import process_customer_query

# Set up Streamlit app title
st.title("Store Assistant Chatbot")

# Create a form to allow submission with the Enter key
with st.form("query_form"):
    user_query = st.text_input("Ask about the store:")
    submitted = st.form_submit_button("Submit")

# Process query when the user submits the form
if submitted and user_query:
    # Process the customer query
    response = process_customer_query(user_query)

    # Check if the response is empty or None
    if not response or response.strip() == "":
        st.error("Sorry, no response was generated. Please try again.")
    elif "Sorry" in response:
        # Display error messages directly
        st.error(response)
    else:
        # Display structured responses
        response_lines = response.strip().split("\n")

        # Check if we received multiple lines (likely product information)
        if len(response_lines) > 1:
            st.markdown("### Product Information")
            for line in response_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    st.markdown(f"**{key.strip()}**: {value.strip()}")
        else:
            # Single-line response for store info
            st.markdown(f"### Store Information\n{response}")
