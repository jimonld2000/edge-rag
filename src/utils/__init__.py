"""Utility functions shared across the EDGE-RAG system."""

from sentence_transformers import SentenceTransformer
from lxml import etree
import json
from pathlib import Path
from src.config import EMBEDDING_MODEL

_embedding_model = None

def get_embedding_model():
    """Lazily load and cache the embedding model."""
    global _embedding_model
    if _embedding_model is None:
        print(f"Initializing Embedding Model: {EMBEDDING_MODEL}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def clean_xml_to_string(xml_string):
    """
    Parses raw XML from event logs and converts to clean text representation.
    
    Transforms complex XML structure into Key: Value pairs, reducing token count
    and noise for LLM processing.
    
    Args:
        xml_string: Raw XML string from event log
        
    Returns:
        str: Cleaned text representation or error message
    """
    try:
        # Secure XML parser to prevent XXE (XML External Entity) attacks
        parser = etree.XMLParser(resolve_entities=False)
        if isinstance(xml_string, str):
            xml_string = xml_string.encode('utf-8')
        root = etree.fromstring(xml_string, parser=parser)
        lines = []
        
        for elem in root.iter():
            if elem.text and elem.text.strip():
                tag_name = etree.QName(elem).localname
                key = elem.get("Name") or tag_name
                value = elem.text.strip()
                lines.append(f"{key}: {value}")
                
        return "\n".join(lines)
    except Exception as e:
        return f"Error parsing XML: {str(e)}\nRaw Content: {xml_string[:500]}..."


def safe_json_parse(json_string):
    """
    Safely parse JSON with fallback for malformed responses.
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        dict: Parsed JSON or empty dict on failure
    """
    try:
        clean_text = json_string.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception:
        return {}


def extract_json_id(llm_response):
    """
    Extract MITRE ID from LLM response.
    
    Args:
        llm_response: LLM response potentially containing JSON
        
    Returns:
        str: Extracted ID or "ParseError"
    """
    data = safe_json_parse(llm_response)
    return data.get("id", "ParseError")
