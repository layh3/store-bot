# Store Assistant (AI-Powered)

## Important: API Key Setup for Exam Review

This project requires an OpenAI API key to function. Since GitHub blocks secret keys from being pushed, you must manually add the key in query_handler.py.

Locate the query_handler.py file.
Find this line near the top:
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

Replace "YOUR_OPENAI_API_KEY_HERE" with the provided API key:
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

Save the file and run the chatbot as usual.

## Overview

This AI-powered store assistant is designed to help customers find products, check availability, and retrieve pricing information using GPT-4 and LanceDB. The chatbot processes customer queries, determines the correct department, and provides relevant responses based on the store's inventory.

## Features

-   Uses GPT-4 to extract product-related queries and interpret customer intent
-   Stores product data in LanceDB with vector embeddings for efficient retrieval
-   Supports semantic search to match user queries with the best available products
-   Runs as a web-based chatbot powered by Streamlit

## Installation

### Clone the Repository

git clone https://github.com/yourusername/store-bot.git
cd store-bot

### Install Dependencies

#### For Windows (PowerShell)

Run the setup script:

setup.bat

Or, manually install:

pip install -r requirements.txt
python -m spacy download en_core_web_md

#### For Mac/Linux

Run the setup script:

chmod +x setup.sh # (Only needed once)
./setup.sh

Or, manually install:

pip install -r requirements.txt
python -m spacy download en_core_web_md

## Running the Application

### Initialize the Database

Before running the assistant, initialize the database:

python data_loader.py

Expected Output:

Database with embeddings initialized!

### Start the Chatbot

To launch the chatbot, run:

streamlit run app.py

This will open the chatbot interface in your default web browser, where users can interact with the assistant in a conversational manner.

## Running Unit Tests

To verify everything works correctly, run:

python -m pytest tests/

Expected Output:

============================= test session starts =============================
collected 11 items

tests/test_query_handler.py .....
tests/test_vector_db.py ......

============================= 100% PASSED ====================================

## Troubleshooting

#### If python data_loader.py Fails

Ensure spacy is installed and the model is downloaded:

python -m spacy download en_core_web_md

#### If pytest Fails

Ensure all dependencies are installed:

pip install -r requirements.txt

Check if tests/**init**.py exists:

touch tests/**init**.py
