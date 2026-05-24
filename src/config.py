"""
Configuration settings for EDGE-RAG system.
Centralized configuration management for database, models, and data paths.
"""

from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Database Configuration
DB_PATH = PROJECT_ROOT / "lancedb_data"
KNOWLEDGE_FILE = PROJECT_ROOT / "data" / "mitre_knowledge.json"

# Data Paths
EVTX_FOLDER = PROJECT_ROOT / "data" / "evtx_samples"
GOLD_LABELS_FILE = PROJECT_ROOT / "data" / "gold_labels.csv"

# Output Paths
RESULTS_OUTPUT_DIR = PROJECT_ROOT / "results" / "outputs"
VISUALIZATIONS_DIR = PROJECT_ROOT / "results" / "visualizations"

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
#OLLAMA_MODEL = "gemma4:e2b"
# OLLAMA_MODEL = "phi4"
OLLAMA_MODEL = "qwen3.5:0.8b"
#OLLAMA_MODEL = "ministral-3:3b"

# Benchmark Configuration
OUTPUT_FILE = RESULTS_OUTPUT_DIR / "final_results.csv"
FIXED_OUTPUT_FILE = RESULTS_OUTPUT_DIR / "final_results_fixed.csv"

# Analysis Configuration
ENABLE_VERBOSE = True
LOG_TRUNCATION_LENGTH = 1000
MAX_RETRIEVAL_RESULTS = 3
MAX_SAMPLE_FILES = 5

# Ensure output directories exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)
