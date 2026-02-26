"""MITRE Knowledge Base builder - fetches and processes MITRE ATT&CK data."""

import requests
import json
import re
from pathlib import Path
from tqdm import tqdm

MITRE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"


def clean_text(text):
    """Remove markdown links and extra whitespace.
    
    Args:
        text: Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text.strip()


def fetch_mitre_data():
    """
    Download latest MITRE Enterprise ATT&CK data.
    
    Returns:
        dict: STIX object collection
    """
    print(f"📥 Downloading MITRE Enterprise ATT&CK data from {MITRE_URL}...")
    response = requests.get(MITRE_URL)
    response.raise_for_status()
    return response.json()


def parse_mitre_data(stix_data):
    """
    Parse MITRE STIX data into technique entries.
    
    Extracts active techniques (non-deprecated/revoked) and structures them
    for RAG embedding.
    
    Args:
        stix_data: STIX collection dictionary
        
    Returns:
        list: List of technique dictionaries
    """
    techniques = []
    objects = stix_data.get("objects", [])
    
    print("⚙️  Parsing Techniques...")
    for obj in tqdm(objects):
        # Filter for active techniques
        if (obj.get("type") == "attack-pattern" and 
            not obj.get("revoked", False) and 
            not obj.get("x_mitre_deprecated", False)):
            
            # Extract ID (e.g., T1059)
            technique_id = "UNKNOWN"
            for ref in obj.get("external_references", []):
                if ref.get("source_name") == "mitre-attack":
                    technique_id = ref.get("external_id")
                    break
            
            # Extract Content
            name = obj.get("name", "Unknown")
            description = clean_text(obj.get("description", ""))
            detection = clean_text(obj.get("x_mitre_detection", ""))
            
            # Structure for RAG
            technique_entry = {
                "id": technique_id,
                "name": name,
                "text": f"{name} ({technique_id}): {description}",
                "metadata": {
                    "detection_logic": detection,
                    "url": f"https://attack.mitre.org/techniques/{technique_id}"
                }
            }
            techniques.append(technique_entry)
            
    return techniques


def build_knowledge_base(output_file="mitre_knowledge.json"):
    """
    Build complete MITRE knowledge base.
    
    Fetches latest MITRE data and saves knowledge base to file.
    
    Args:
        output_file: Path to save knowledge base JSON
    """
    data = fetch_mitre_data()
    knowledge_base = parse_mitre_data(data)
    
    print(f"💾 Saving {len(knowledge_base)} techniques to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=2)
    print("✅ Done.")
    
    return knowledge_base
