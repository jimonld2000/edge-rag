#!/usr/bin/env python3
"""
Setup LanceDB Vector Database

Initializes the LanceDB vector database with MITRE knowledge embeddings
for semantic search during analysis.
"""

from src.knowledge.database import setup_database
from src.config import DB_PATH, KNOWLEDGE_FILE

if __name__ == "__main__":
    print("Setting up LanceDB Vector Database...")
    table = setup_database(
        knowledge_file=str(KNOWLEDGE_FILE),
        db_path=str(DB_PATH)
    )
    print("✅ Database setup complete!")
