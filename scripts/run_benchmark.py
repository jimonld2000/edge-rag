#!/usr/bin/env python3
"""
Run Comprehensive Benchmark

Benchmarks all three analysis modes (Baseline, Naive RAG, HyDE) against
labeled EVTX files and generates performance metrics.
"""

from src.inference import BenchmarkRunner
from src.config import EVTX_FOLDER, OUTPUT_FILE, DB_PATH, GOLD_LABELS_FILE

if __name__ == "__main__":
    print("="*60)
    print("       EDGE-RAG BENCHMARK SUITE")
    print("="*60)
    
    runner = BenchmarkRunner(
        db_path=str(DB_PATH),
        labels_file=str(GOLD_LABELS_FILE)
    )
    
    print(f"\nStarting benchmark on {EVTX_FOLDER}...")
    results = runner.run_benchmark(
        evtx_folder=str(EVTX_FOLDER),
        output_file=OUTPUT_FILE
    )
    
    print(f"\n✅ Benchmark complete! Results saved to {OUTPUT_FILE}")
    print(f"   Total runs: {len(results)}")
