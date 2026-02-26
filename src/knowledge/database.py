"""LanceDB database setup and management."""

import json
from pathlib import Path
import lancedb
from src.config import DB_PATH, KNOWLEDGE_FILE
from src.utils import get_embedding_model


def setup_database(knowledge_file=None, db_path=None):
    """
    Load MITRE knowledge, create embeddings, and store in LanceDB.
    
    Creates a vector database for semantic search over MITRE techniques.
    
    Args:
        knowledge_file: Path to MITRE knowledge JSON file
        db_path: Path to LanceDB directory
        
    Returns:
        LanceDB table object
        
    Raises:
        FileNotFoundError: If knowledge file not found
    """
    knowledge_file = knowledge_file or KNOWLEDGE_FILE
    db_path = db_path or DB_PATH
    
    print("--- Setting up Knowledge Base ---")
    
    # 1. Connect to LanceDB
    db = lancedb.connect(str(db_path))
    
    # 2. Load JSON
    if not Path(knowledge_file).exists():
        raise FileNotFoundError(
            f"Could not find {knowledge_file}. Run knowledge builder first."
        )
    
    with open(knowledge_file, 'r') as f:
        knowledge_data = json.load(f)
    
    print(f"Loaded {len(knowledge_data)} MITRE techniques.")

    # 3. Embed Data
    print("Generating embeddings (this may take a moment)...")
    model = get_embedding_model()
    
    table_data = []
    descriptions = [
        f"{item['id']} {item['name']}: {item['text']}" 
        for item in knowledge_data
    ]
    vectors = model.encode(descriptions, normalize_embeddings=True)
    
    for i, item in enumerate(knowledge_data):
        table_data.append({
            "vector": vectors[i],
            "id": item['id'],
            "name": item['name'],
            "text": descriptions[i]
        })
    
    # 4. Create/Overwrite Table
    tbl = db.create_table("mitre_context", data=table_data, mode="overwrite")
    print("Database 'mitre_context' created successfully.")
    return tbl


def get_database_table(db_path=None, create_if_missing=False):
    """
    Get or create LanceDB table.
    
    Args:
        db_path: Path to LanceDB directory
        create_if_missing: Whether to create database if not found
        
    Returns:
        LanceDB table object or None
    """
    db_path = db_path or DB_PATH
    
    try:
        db = lancedb.connect(str(db_path))
        table = db.open_table("mitre_context")
        return table
    except Exception as e:
        if create_if_missing:
            print(f"Database not found: {e}")
            print("Building database now...")
            return setup_database(db_path=db_path)
        else:
            raise
