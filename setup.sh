#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_md

echo "Setup complete!"
