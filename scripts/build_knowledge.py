#!/usr/bin/env python3
"""
Build MITRE Knowledge Base

Downloads and processes MITRE Enterprise ATT&CK data into a structured
JSON knowledge base for use in the RAG pipeline.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge import build_knowledge_base
from src.config import KNOWLEDGE_FILE

if __name__ == "__main__":
    print("Building MITRE Knowledge Base...")
    build_knowledge_base(output_file=str(KNOWLEDGE_FILE))
