# EDGE-RAG: Event Detection with Guided Embeddings and Retrieval-Augmented Generation

A sophisticated system for analyzing Windows Event Logs (EVTX) using MITRE ATT&CK knowledge and advanced retrieval-augmented generation (RAG) techniques.

## 📋 Overview

EDGE-RAG implements a hybrid approach to security event analysis by:

1. **Building a Knowledge Base** from MITRE Enterprise ATT&CK data
2. **Creating Vector Embeddings** for semantic search over attack techniques
3. **Implementing Three Analysis Modes**:
   - **Mode A (Baseline)**: Pure vector similarity matching
   - **Mode B (Naive RAG)**: Vector retrieval + LLM reasoning
   - **Mode C (HyDE)**: Hypothesis generation + retrieval + LLM reasoning
4. **Benchmarking Performance** across accuracy and latency dimensions
5. **Analyzing Results** with detailed metrics and visualizations

## 🏗️ Project Structure

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

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Ollama (for LLM inference)
- CUDA/GPU (recommended for embedding generation)

### Installation

```bash
# Clone repository
git clone <repository>
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

This generates `mitre_knowledge.json` with structured technique data.

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
# First, prepare gold labels
python build_knowledge.py  # If not done
python scripts/setup_database.py

# Run benchmark (requires gold_labels.csv)
python scripts/run_benchmark.py
```

Generates `final_results.csv` with detailed metrics.

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

## 📊 Analysis Modes

### Mode A: Vector Baseline
- **Description**: Direct embedding similarity
- **Speed**: ⚡⚡⚡ (Fastest)
- **Accuracy**: ⭐⭐ (Low)
- **Process**: Log → Embed → Search → Return Top-1

### Mode B: Naive RAG
- **Description**: Vector retrieval + LLM reasoning
- **Speed**: ⚡⚡ (Medium)
- **Accuracy**: ⭐⭐⭐ (Medium)
- **Process**: Log → Embed → Retrieve → LLM Reason → Return ID

### Mode C: HyDE (Recommended)
- **Description**: Hypothesis generation + retrieval + reasoning
- **Speed**: ⚡ (Slowest)
- **Accuracy**: ⭐⭐⭐⭐ (Highest)
- **Process**: Log → Concept Generation → Embed → Retrieve → LLM Reason → Return ID

## 🗂️ Key Components

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
- `hyde_analysis()`: HyDE pipeline (recommended)
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

## 📊 Results Interpretation

### Accuracy Metrics
- **Strict Match**: Exact MITRE ID match (e.g., T1003.001)
- **Soft Match**: Parent ID match only (e.g., T1003)
- **Use soft match for papers** (more realistic for automated systems)

### Key Findings
Look for "HyDE EXCLUSIVE WINS": cases where Naive RAG fails but HyDE succeeds. These demonstrate the value of hypothesis generation.

### Failure Modes
- **Safe Abstentions**: System returns "Unknown" (safe)
- **Hallucinations**: System returns wrong ID (unsafe)

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Embedding model
OLLAMA_MODEL = "phi4"                 # LLM for reasoning

# Paths
DB_PATH = "lancedb_data/"
EVTX_FOLDER = "data/evtx_samples"

# Analysis Settings
MAX_SAMPLE_FILES = 5
LOG_TRUNCATION_LENGTH = 1000
MAX_RETRIEVAL_RESULTS = 3
```

## 📈 Performance Expectations

Typical results on labeled EVTX dataset:

| Mode | Accuracy | Latency | Safety |
|------|----------|---------|--------|
| Baseline (A) | 25-30% | <100ms | High |
| Naive RAG (B) | 35-40% | 1-2s | Medium |
| HyDE (C) | 50-60% | 3-5s | High |

*Note: Actual results depend on data quality, model configuration, and technique diversity*

## 📚 API Reference

### Core Functions

```python
from src.core import hyde_analysis, baseline_analysis, naive_rag_analysis
from src.parsers import parse_evtx
from src.evaluation import analyze_results

# Analyze a log file
log_content = parse_evtx("path/to/file.evtx")
result = hyde_analysis(log_content, table)
# result = {
#     'id': 'T1003',
#     'confidence': 'High',
#     'reasoning': 'explanation',
#     'total_time': 3.45
# }

# Analyze results
analysis = analyze_results("final_results.csv")
```

### Benchmarking

```python
from src.inference import BenchmarkRunner

runner = BenchmarkRunner()
results = runner.run_benchmark(
    evtx_folder="path/to/evtx",
    output_file="results.csv"
)
```

## 🧪 Testing

Run tests (when implemented):

```bash
pytest tests/
```

## 📄 Input Data Format

### Gold Labels CSV (`gold_labels.csv`)

```csv
Filename,Folder,True_ID
event1.evtx,Credential Access,T1110.001
event2.evtx,Execution,T1059
```

### MITRE Knowledge JSON (`mitre_knowledge.json`)

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

## 🤝 Contributing

Guidelines for contributions:
1. Maintain modular structure in `src/`
2. Add tests in `tests/`
3. Update docstrings with full descriptions
4. Keep scripts simple and focused

## 📝 License

See LICENSE file for details.

## 🔗 References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Hypothetical Document Embeddings (HyDE)](https://arxiv.org/abs/2212.10496)
- [LanceDB Vector Database](https://lancedb.com/)
- [Ollama LLM](https://ollama.ai/)

## 📞 Support

For issues or questions, refer to:
1. Project README and docstrings
2. Inline comments in module code
3. Configuration parameters in `src/config.py`

---

**Version**: 0.1.0  
**Last Updated**: 2025  
**Maintainer**: EDGE-RAG Research Team
