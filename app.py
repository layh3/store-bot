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
    response = process_customer_query(user_query)

    if "Sorry" in response:
        st.error(response)  # Display error message for unhandled queries
    else:
        # Determine response type based on format
        if ":" in response:  # Structured product response
            response_lines = response.split("\n")
            formatted_response = "  \n".join(
                [f"**{line.split(':')[0].strip()}**: {line.split(':')[1].strip()}" for line in response_lines if ":" in line]
            )
            st.markdown(f"### Product Information  \n{formatted_response}")
        else:  # Single text response (store information)
            st.markdown(f"### Store Information  \n{response}")
