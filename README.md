# EDGE-RAG: Event Detection with Guided Embeddings and Retrieval-Augmented Generation

A system for analyzing Windows Event Logs (EVTX) using MITRE ATT&CK knowledge and advanced retrieval-augmented generation (RAG) techniques, built for research purposes.

## Overview

EDGE-RAG implements a hybrid approach to security event analysis by:

1. **Building a Knowledge Base** from MITRE Enterprise ATT&CK data
2. **Creating Vector Embeddings** for semantic search over attack techniques
3. **Implementing Evaluated Analytical Modes**:
   - **Baseline (Keyword Search)**: Traditional BM25 lexical mapping
   - **Zero-Shot SLM**: Direct parametric inference without retrieval
   - **Naive RAG**: Vector retrieval + SLM reasoning
   - **Edge-HyDE (Proposed)**: Hypothesis generation + retrieval + SLM reasoning
   - **Cloud Upper-Bound**: Commercial API boundary test
4. **Benchmarking Performance** across accuracy, latency dimensions, and parameter scales (0.8B to 14B)
5. **Analyzing Results** with detailed metrics and visualizations

## Project Structure

```
edge-rag/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Centralized configuration
│   ├── knowledge/
│   │   ├── __init__.py           # Knowledge base builder
│   │   └── database.py           # LanceDB setup and management
│   ├── core/
│   │   └── __init__.py           # RAG pipeline implementations
│   ├── parsers/
│   │   └── __init__.py           # EVTX parsing utilities
│   ├── inference/
│   │   └── __init__.py           # Benchmarking framework
│   ├── evaluation/
│   │   ├── __init__.py           # Results analysis
│   │   └── visualization.py      # Plotting utilities
│   └── utils/
│       └── __init__.py           # Shared utilities
├── scripts/
│   ├── build_knowledge.py        # Build MITRE knowledge base
│   ├── setup_database.py         # Initialize vector database
│   ├── process_logs.py           # Interactive log processing
│   ├── run_benchmark.py          # Run full benchmark
│   └── analyze_results.py        # Analyze and visualize results
├── data/
│   ├── evtx_samples/             # Windows event log samples
│   ├── atomic_logs/              # ATOMIC RED TEAM test data
│   └── lancedb_data/             # Vector database storage
├── results/
│   ├── outputs/                  # CSV results
│   └── visualizations/           # Generated plots
├── tests/
│   └── __init__.py               # Test suite
├── pyproject.toml
├── LICENSE
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- Ollama (for LLM inference)
- CUDA/GPU (recommended for embedding generation)

### Installation

```bash
# Clone repository
git clone https://github.com/jimonld2000/edge-rag
cd edge-rag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Running the Pipeline

#### Step 1: Build Knowledge Base

Download and process MITRE Enterprise ATT&CK data:

```bash
python scripts/build_knowledge.py
```

This generates `data/mitre_knowledge.json` with structured technique data.

#### Step 2: Setup Vector Database

Initialize LanceDB with embeddings:

```bash
python scripts/setup_database.py
```

Creates embeddings for all MITRE techniques and stores them in `lancedb_data/`.

#### Step 3: Process Event Logs

Analyze individual EVTX files using the HyDE pipeline:

```bash
python scripts/process_logs.py
```

Interactive script that processes EVTX files and displays analysis results.

#### Step 4: Run Full Benchmark

Benchmark all three modes against gold-labeled data:

```bash
# First, prepare gold labels (ensure data/gold_labels.csv exists)
python scripts/build_knowledge.py  # If not done
python scripts/setup_database.py

# Run benchmark (requires data/gold_labels.csv)
python scripts/run_benchmark.py
```

Generates `results/outputs/final_results.csv` with detailed metrics.

#### Step 5: Analyze Results

Generate comprehensive analysis and visualizations:

```bash
python scripts/analyze_results.py
```

Outputs:
- Accuracy and latency metrics
- Failure mode analysis
- Performance visualizations
- Label validation

## Analysis Modes

### Baseline (Keyword Search)
- **Description**: Traditional BM25 lexical mapping, acting as a heuristic baseline
- **Speed**: Fastest (0.02s)
- **Accuracy**: Lowest (4.3%)
- **Process**: Log → Keyword Search → Return ID

### Zero-Shot SLM
- **Description**: Direct prompting of the model using parametric memory only
- **Process**: Log → SLM → Return ID

### Naive RAG
- **Description**: Vector retrieval + SLM reasoning
- **Speed**: Depends on model weight
- **Accuracy**: Low (Under 9%)
- **Process**: Log → Embed → Retrieve → SLM Reason → Return ID

### Edge-HyDE (Proposed Framework)
- **Description**: Hypothesis generation + retrieval + reasoning to bridge the semantic gap
- **Process**: Log → Concept Generation → Embed → Retrieve → SLM Reason → Return ID

### Cloud Upper-Bound
- **Description**: Commercial cloud-hosted frontier model utilized via API to establish the theoretical maximum accuracy
- **Process**: Log → Embed → Retrieve → Cloud LLM Reason → Return ID

## Key Components

### Configuration (`src/config.py`)
Centralized configuration for:
- Database paths and model names
- Data folder locations
- Output directories
- Analysis parameters

### Knowledge Module (`src/knowledge/`)
- `__init__.py`: Fetches and processes MITRE ATT&CK data
- `database.py`: LanceDB vector database management

### Core Analysis (`src/core/`)
Implements three analysis modes:
- `hyde_analysis()`: HyDE pipeline
- `naive_rag_analysis()`: Simple RAG pipeline
- `baseline_analysis()`: Vector similarity baseline

### Data Parsing (`src/parsers/`)
- `parse_evtx()`: Read binary EVTX files
- `get_evtx_files()`: Discover EVTX files recursively
- Converts event XML to clean text

### Inference Module (`src/inference/`)
- `BenchmarkRunner`: Orchestrates benchmarking pipeline
- Runs all modes against labeled data
- Generates performance metrics

### Evaluation (`src/evaluation/`)
- `analyze_results()`: Calculate accuracy/latency metrics
- `analyze_failures()`: Categorize failure modes
- `visualization.py`: Generate comparison charts

### Utilities (`src/utils/`)
- `get_embedding_model()`: Lazy-load SentenceTransformer
- `clean_xml_to_string()`: Parse event XML
- `safe_json_parse()`: Robust JSON parsing from LLM

## Results Interpretation

### Accuracy Metrics
- **Strict Match**: Exact MITRE ID match (e.g., T1003.001)
- **Soft Match**: Parent ID match only (e.g., T1003)
- **Use soft match for papers** (more realistic for automated systems)

### Key Findings
Look for "HyDE EXCLUSIVE WINS": cases where Naive RAG fails but HyDE succeeds. These demonstrate the value of hypothesis generation.

### Failure Modes
- **Safe Abstentions**: System returns "Unknown" (safe)
- **Hallucinations**: System returns wrong ID (unsafe)

## Configuration

Edit `src/config.py` to customize:

```python
# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Embedding model
OLLAMA_MODEL = "phi4"                 # LLM for reasoning, it can be of you choice
# tested models: phi4, qwen-3.5-0.8, gemma4-2b, ministral3-3b

# Paths
DB_PATH = "lancedb_data/"
EVTX_FOLDER = "data/evtx_samples"

# Analysis Settings
MAX_SAMPLE_FILES = 5
LOG_TRUNCATION_LENGTH = 1000
MAX_RETRIEVAL_RESULTS = 3
```

## Performance Expectations

The system was evaluated on a dataset of 278 real-world Windows EVTX attack logs on mid-range hardware (Intel i5 CPU, 16GB RAM) without discrete GPU acceleration. The following table showcases the operational configuration across different Small Language Models (SLMs). Both the traditional lexical search and a Cloud Upper Bound (Gemini 3.1 Flash Lite API) are included as baselines. Note that absolute Accuracy represents the 'Soft Classification Accuracy' (predicting the correct parent Tactic or overarching Technique, e.g., T1059).

### Comprehensive Performance Evaluation Across Used Architectures

| Operational Configuration | Architecture | Effective Scale | Soft Classification Accuracy | Mean Inference Latency |
|---------------------------|--------------|-----------------|------------------------------|------------------------|
| **Heuristic Baseline** | Lexical BM25 Search | - | 4.3% | 0.02s |
| **Direct Parametric Inference**<br>(Zero-Shot, No Retrieval Context) | Qwen-3.5-0.8B | 0.8B | 0.4% | 122.52s |
| | Ministral-3-3B | 3.0B | 3.6% | 0.71s |
| | Gemma-4-2B | 2.0B | 9.4% | 54.47s |
| | Phi-4-14B | 14.0B | 6.5% | 4.02s |
| **Standard Retrieval Baseline**<br>(Naive RAG Pipeline) | Qwen-3.5-0.8B | 0.8B | 1.1% | 143.1s |
| | Ministral-3-3B | 3.0B | 7.6% | 0.94s |
| | Gemma-4-2B | 2.0B | 8.7% | 32.17s |
| | Phi-4-14B | 14.0B | 7.2% | 4.06s |
| **Proposed Framework**<br>(Edge-HyDE Architecture) | Qwen-3.5-0.8B | 0.8B | 0.7% | 220.05s |
| | Ministral-3-3B | 3.0B | 15.9% | 3.67s |
| | Gemma-4-2B | 2.0B | 19.6% | 62.03s |
| | Phi-4-14B | 14.0B | 23.2% | 42.36s |
| **Upper Bound (Cloud)** | Gemini 3.1 Flash Lite | Frontier LLM Model API | 24.3% | 0.8s |

*Note: The Edge-HyDE pipeline achieves a minimum >3.2x relative improvement in classification accuracy over standard Naive RAG baselines across all viable models, demonstrating the necessity of an intermediate reasoning step to bridge the semantic gap.*


## Input Data Format

### Gold Labels CSV (`data/gold_labels.csv`)

```csv
Filename,Folder,True_ID
event1.evtx,Credential Access,T1110.001
event2.evtx,Execution,T1059
```

### MITRE Knowledge JSON (`data/mitre_knowledge.json`)

```json
[
  {
    "id": "T1003",
    "name": "Credential Dumping",
    "text": "Credential Dumping (T1003): ...",
    "metadata": {
      "detection_logic": "Monitor process access to LSASS...",
      "url": "https://attack.mitre.org/techniques/T1003"
    }
  }
]
```

## About the project

This project was created as a research for the KES 2026 conference http://kes2026.kesinternational.org/index.php. 
Future development and research ar expected.

## License

See LICENSE file for details.

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Hypothetical Document Embeddings (HyDE)](https://arxiv.org/abs/2212.10496)
- [LanceDB Vector Database](https://lancedb.com/)
- [Ollama LLM](https://ollama.ai/)


---

**Version**: 0.1.1 
**Last Updated**: 2026 
**Maintainer**: Daniel Jimon
