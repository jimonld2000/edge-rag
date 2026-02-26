"""Benchmarking and evaluation framework."""

import time
import pandas as pd
import re
from pathlib import Path
from tqdm import tqdm
import lancedb

from src.config import (
    DB_PATH, GOLD_LABELS_FILE, OUTPUT_FILE, EVTX_FOLDER
)
from src.parsers import parse_evtx, get_evtx_files
from src.core import baseline_analysis, naive_rag_analysis, hyde_analysis
from src.knowledge.database import get_database_table


def extract_ground_truth(file_path):
    """
    Extract MITRE T-Code from filename or parent folder.
    
    Args:
        file_path: Path to EVTX file
        
    Returns:
        str: MITRE ID or category fallback
    """
    filename = Path(file_path).name
    match = re.search(r'(T\d{4}(?:\.\d{3})?)', filename)
    
    if match:
        return match.group(1)
    
    parent = Path(file_path).parent.name
    return f"Category: {parent}"


class BenchmarkRunner:
    """Runner for benchmarking analysis modes."""
    
    def __init__(self, db_path=None, labels_file=None):
        """
        Initialize benchmark runner.
        
        Args:
            db_path: Path to LanceDB database
            labels_file: Path to gold labels CSV
        """
        self.db_path = db_path or DB_PATH
        self.labels_file = labels_file or GOLD_LABELS_FILE
        self.table = get_database_table(db_path=self.db_path, create_if_missing=True)
        self.truth_map = self._load_truth_map()
    
    def _load_truth_map(self):
        """Load ground truth labels from CSV."""
        truth_map = {}
        try:
            labels_df = pd.read_csv(self.labels_file)
            truth_map = dict(zip(labels_df["Filename"], labels_df["True_ID"]))
            print(f"Loaded {len(truth_map)} ground truth labels.")
        except FileNotFoundError:
            print(f"Warning: {self.labels_file} not found.")
        return truth_map
    
    def run_benchmark(self, evtx_folder=None, output_file=None):
        """
        Run full benchmark across all analysis modes.
        
        Args:
            evtx_folder: Path to EVTX files
            output_file: CSV file to save results
        """
        evtx_folder = evtx_folder or EVTX_FOLDER
        output_file = output_file or OUTPUT_FILE
        
        files = get_evtx_files(evtx_folder, recursive=True)
        valid_files = [
            f for f in files 
            if f.name in self.truth_map and pd.notna(self.truth_map[f.name])
        ]
        
        print(f"Found {len(files)} total files, benchmarking {len(valid_files)} labeled files.")
        
        results_data = []
        
        for file_path in tqdm(valid_files, desc="Benchmarking"):
            log_content = parse_evtx(str(file_path))
            if not log_content:
                continue

            filename = file_path.name
            true_label = str(self.truth_map.get(filename, "Unknown")).strip()

            # Run all modes
            result_a = baseline_analysis(log_content, self.table)
            result_b = naive_rag_analysis(log_content, self.table)
            result_c = hyde_analysis(log_content, self.table)

            # Record Results
            results_data.append({
                "File": filename,
                "Mode": "A_Baseline",
                "True": true_label,
                "Pred": result_a.get('id', 'Unknown'),
                "Strict_Match": result_a.get('id') == true_label,
                "Time": result_a.get('total_time', 0)
            })
            results_data.append({
                "File": filename,
                "Mode": "B_Naive",
                "True": true_label,
                "Pred": result_b.get('id', 'Unknown'),
                "Strict_Match": result_b.get('id') == true_label,
                "Time": result_b.get('total_time', 0)
            })
            results_data.append({
                "File": filename,
                "Mode": "C_HyDE",
                "True": true_label,
                "Pred": result_c.get('id', 'Unknown'),
                "Strict_Match": result_c.get('id') == true_label,
                "Time": result_c.get('total_time', 0)
            })

        # Save results
        df_results = pd.DataFrame(results_data)
        df_results.to_csv(output_file, index=False)
        print(f"Benchmark saved to {output_file}")
        
        return df_results
