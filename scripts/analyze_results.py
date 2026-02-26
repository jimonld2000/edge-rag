#!/usr/bin/env python3
"""
Analyze Benchmark Results

Processes benchmark results and generates detailed analysis including
accuracy metrics, failure modes, and performance comparison.
"""

from src.evaluation import analyze_results, analyze_failures, validate_labels
from src.evaluation.visualization import (
    plot_accuracy_comparison,
    plot_latency_comparison,
    plot_accuracy_vs_latency
)
from src.config import OUTPUT_FILE, KNOWLEDGE_FILE, GOLD_LABELS_FILE

if __name__ == "__main__":
    print("="*60)
    print("       EDGE-RAG RESULTS ANALYSIS")
    print("="*60)
    
    # Run analysis
    print(f"\nAnalyzing results from {OUTPUT_FILE}...")
    analysis = analyze_results(OUTPUT_FILE)
    
    # Analyze failure modes
    print("\nAnalyzing failure modes...")
    analyze_failures(OUTPUT_FILE)
    
    # Validate labels
    print("\nValidating labels...")
    validate_labels(str(GOLD_LABELS_FILE), str(KNOWLEDGE_FILE))
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    try:
        plot_accuracy_comparison(OUTPUT_FILE)
        plot_latency_comparison(OUTPUT_FILE)
        plot_accuracy_vs_latency(OUTPUT_FILE)
        print("✅ All visualizations generated!")
    except Exception as e:
        print(f"⚠️  Visualization error: {e}")
    
    print("\n" + "="*60)
    print("Analysis complete!")
