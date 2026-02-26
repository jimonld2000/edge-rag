"""Results analysis and visualization."""

import pandas as pd
import json
import os
from pathlib import Path


def get_parent_id(mitre_id):
    """Extract parent MITRE ID (e.g., T1059 from T1059.001)."""
    if pd.isna(mitre_id):
        return "Unknown"
    return str(mitre_id).split('.')[0]


def analyze_results(results_file):
    """
    Analyze benchmark results with detailed metrics.
    
    Args:
        results_file: Path to results CSV
        
    Returns:
        dict: Analysis results including accuracy metrics
    """
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found.")
        return None

    df = pd.read_csv(results_file)
    original_count = len(df)
    
    # De-duplicate, keeping most recent for each File+Mode
    df = df.drop_duplicates(subset=['File', 'Mode'], keep='last')
    removed = original_count - len(df)
    print(f"Loaded {len(df)} rows (Removed {removed} duplicates).")

    # Add matching logic
    df['True_Parent'] = df['True'].apply(get_parent_id)
    df['Pred_Parent'] = df['Pred'].apply(get_parent_id)
    df['Strict_Match'] = df['True'] == df['Pred']
    df['Soft_Match'] = df['True_Parent'] == df['Pred_Parent']

    # Calculate metrics by mode
    print("\n" + "="*50)
    print("       SCIENTIFIC BENCHMARK REPORT")
    print("="*50)
    
    modes = ['A_Baseline', 'B_Naive', 'C_HyDE']
    analysis = {}
    
    for mode in modes:
        if mode not in df['Mode'].values:
            continue
        
        subset = df[df['Mode'] == mode]
        strict_acc = subset['Strict_Match'].mean() * 100
        soft_acc = subset['Soft_Match'].mean() * 100
        avg_latency = subset['Time'].mean()
        
        analysis[mode] = {
            'strict_accuracy': strict_acc,
            'soft_accuracy': soft_acc,
            'avg_latency': avg_latency,
            'count': len(subset)
        }
        
        print(f"\nMODE: {mode}")
        print(f"  Strict Accuracy: {strict_acc:.1f}%")
        print(f"  Soft Accuracy:   {soft_acc:.1f}%  (Use this for paper)")
        print(f"  Avg Latency:     {avg_latency:.2f}s")

    # Find HyDE wins vs Naive
    if 'B_Naive' in df['Mode'].values and 'C_HyDE' in df['Mode'].values:
        pivot = df.pivot(index='File', columns='Mode', values='Soft_Match')
        
        if 'B_Naive' in pivot.columns and 'C_HyDE' in pivot.columns:
            hyde_wins = pivot[(pivot['B_Naive'] == False) & (pivot['C_HyDE'] == True)]
            
            print("\n" + "="*50)
            print(f"🏆 HyDE EXCLUSIVE WINS: {len(hyde_wins)} files")
            print("(Cases where Naive Failed BUT HyDE Succeeded)")
            print("-" * 50)
            
            analysis['hyde_exclusive_wins'] = len(hyde_wins)

    print("\n" + "="*50)
    
    return {'results': df, 'analysis': analysis}


def analyze_failures(results_file):
    """
    Analyze failure modes and safety metrics.
    
    Args:
        results_file: Path to results CSV
    """
    df = pd.read_csv(results_file)
    
    print("\n" + "="*50)
    print("     EDGE-RAG FAILURE MODE ANALYSIS")
    print("="*50)

    # Analyze each mode
    for mode in ['A_Baseline', 'B_Naive', 'C_HyDE']:
        mode_df = df[df['Mode'] == mode]
        failures = mode_df[mode_df['Strict_Match'] == False]
        total_failures = len(failures)

        if 'Pred' not in failures.columns:
            continue
            
        safe_abstentions = failures[
            failures['Pred'].astype(str).str.lower() == 'unknown'
        ]
        hallucinations = failures[
            failures['Pred'].astype(str).str.lower() != 'unknown'
        ]

        print(f"\n[ {mode} ] Total Failures: {total_failures}")
        if total_failures > 0:
            pct_safe = (len(safe_abstentions)/total_failures) * 100
            pct_halluc = (len(hallucinations)/total_failures) * 100
            print(f"  -> Safe Abstentions ('Unknown'): {len(safe_abstentions)} ({pct_safe:.1f}%)")
            print(f"  -> Hallucinations (Wrong Class): {len(hallucinations)} ({pct_halluc:.1f}%)")

    print("\n" + "="*50)


def validate_labels(labels_file, knowledge_file):
    """
    Validate ground truth labels against MITRE knowledge base.
    
    Args:
        labels_file: Path to gold labels CSV
        knowledge_file: Path to MITRE knowledge JSON
    """
    if not os.path.exists(knowledge_file) or not os.path.exists(labels_file):
        print("Skipping validation (files not found).")
        return

    print("\n" + "="*50)
    print("       LABEL VALIDATION CHECK")
    print("="*50)
    
    with open(knowledge_file, 'r') as f:
        valid_ids = set(item['id'] for item in json.load(f))
    
    labels_df = pd.read_csv(labels_file)
    
    print(f"Checking {len(labels_df)} labels against MITRE Knowledge Base...")
    errors = []
    
    for idx, row in labels_df.iterrows():
        tid = str(row['True_ID']).strip()
        if tid not in valid_ids and tid != "nan":
            if tid.split('.')[0] in valid_ids:
                continue
            errors.append(f"{row['Filename']}: '{tid}'")
    
    if errors:
        print(f"⚠️  FOUND {len(errors)} POTENTIALLY INVALID LABELS:")
        for e in errors[:5]:
            print(f"  - {e}")
        if len(errors) > 5:
            print(f"  ... and {len(errors)-5} more.")
    else:
        print("✅ All labels look like valid MITRE IDs.")
    
    print("="*50)
