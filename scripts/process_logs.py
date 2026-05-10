#!/usr/bin/env python3
"""
Process and Analyze Event Logs

Interactively processes EVTX files using the HyDE analysis pipeline
and displays results dynamically.
"""

import random

from src.config import EVTX_FOLDER, DB_PATH, MAX_SAMPLE_FILES
from src.parsers import parse_evtx, get_evtx_files
from src.core import hyde_analysis
from src.knowledge.database import get_database_table

if __name__ == "__main__":
    print("="*60)
    print("       EDGE-RAG LOG ANALYSIS")
    print("="*60)
    
    # Load database
    print(f"\nLoading database from {DB_PATH}...")
    try:
        table = get_database_table(db_path=str(DB_PATH), create_if_missing=True)
    except Exception as e:
        print(f"Error loading database: {e}")
        exit(1)
    
    # Find EVTX files
    print(f"\nSearching for EVTX files in {EVTX_FOLDER}...")
    files = get_evtx_files(EVTX_FOLDER, recursive=True)
    
    if not files:
        print("No EVTX files found!")
        exit(1)
    
    # Sample files if too many
    if len(files) > MAX_SAMPLE_FILES:
        files = random.sample(files, MAX_SAMPLE_FILES)
        print(f"Sampled {MAX_SAMPLE_FILES} files from {len(get_evtx_files(EVTX_FOLDER))} total")
    else:
        print(f"Found {len(files)} files")
    
    print(f"\nProcessing {len(files)} log files...")
    print("-" * 60)
    
    results_summary = []
    
    for file_path in files:
        print(f"\n📄 Analyzing: {file_path.parent.name}/{file_path.name}")
        
        # Parse
        log_content = parse_evtx(str(file_path))
        if not log_content:
            print("  ❌ [SKIP] Could not parse file")
            continue
        
        # Analyze
        try:
            result = hyde_analysis(log_content, table)
            
            print(f"  ✅ MITRE ID:    {result.get('id', 'N/A')}")
            print(f"     Confidence: {result.get('confidence', 'N/A')}")
            reasoning = result.get('reasoning', 'N/A')
            print(f"     Reasoning:  {reasoning[:100]}...")
            print(f"     Time:       {result.get('total_time', 0):.2f}s")
            
            results_summary.append({
                "file": file_path.name,
                "category": file_path.parent.name,
                "id": result.get('id'),
                "confidence": result.get('confidence'),
                "time": result.get('total_time', 0)
            })
        except Exception as e:
            print(f"  ❌ [ERROR] {e}")
    
    # Summary Report
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    print(f"{'FILE':<35} | {'CATEGORY':<15} | {'ID':<10} | {'CONF':<10} | {'TIME'}")
    print("-"*80)
    
    for r in results_summary:
        print(
            f"{r['file'][:35]:<35} | {r['category']:<15} | "
            f"{r['id']:<10} | {r['confidence']:<10} | {r['time']:.2f}s"
        )
    
    print("="*60)
    print(f"✅ Analysis complete! Processed {len(results_summary)} files")
