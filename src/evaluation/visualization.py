"""Visualization utilities for results analysis."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_accuracy_comparison(results_file, output_dir="results/visualizations"):
    """
    Create bar chart comparing accuracy across modes.
    
    Args:
        results_file: Path to results CSV
        output_dir: Directory to save plot
    """
    df = pd.read_csv(results_file)
    df = df.drop_duplicates(subset=['File', 'Mode'], keep='last')

    def get_parent_id(mitre_id):
        if pd.isna(mitre_id):
            return "Unknown"
        return str(mitre_id).split('.')[0]

    df['True_Parent'] = df['True'].apply(get_parent_id)
    df['Pred_Parent'] = df['Pred'].apply(get_parent_id)
    df['Match'] = df['True_Parent'] == df['Pred_Parent']

    summary = df.groupby('Mode')[['Match', 'Time']].mean().reset_index()
    summary['Accuracy'] = summary['Match'] * 100

    plt.figure(figsize=(10, 5))
    sns.set_style("whitegrid")

    ax = sns.barplot(
        x='Mode', y='Accuracy', data=summary, palette="viridis",
        order=['A_Baseline', 'B_Naive', 'C_HyDE']
    )

    for i, row in summary.iterrows():
        try:
            idx = ['A_Baseline', 'B_Naive', 'C_HyDE'].index(row['Mode'])
        except ValueError:
            continue
        ax.text(
            idx, row['Accuracy'] + 1, f"{row['Accuracy']:.1f}%",
            color='black', ha="center", fontweight='bold'
        )

    plt.title('Detection Accuracy by Method (Soft Match)', fontsize=14, fontweight='bold')
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Analysis Mode')
    plt.ylim(0, max(summary['Accuracy']) + 5)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "accuracy_comparison.png"
    
    plt.savefig(str(output_file), dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_file}")
    plt.close()


def plot_latency_comparison(results_file, output_dir="results/visualizations"):
    """
    Create bar chart comparing latency across modes.
    
    Args:
        results_file: Path to results CSV
        output_dir: Directory to save plot
    """
    df = pd.read_csv(results_file)
    df = df.drop_duplicates(subset=['File', 'Mode'], keep='last')

    summary = df.groupby('Mode')['Time'].mean().reset_index()
    summary = summary.sort_values('Time')

    plt.figure(figsize=(10, 5))
    sns.set_style("whitegrid")

    ax = sns.barplot(x='Mode', y='Time', data=summary, palette="rocket")

    for i, row in summary.iterrows():
        ax.text(
            i, row['Time'] + 0.1, f"{row['Time']:.2f}s",
            color='black', ha="center", fontweight='bold'
        )

    plt.title('Latency Comparison by Method', fontsize=14, fontweight='bold')
    plt.ylabel('Time (seconds)')
    plt.xlabel('Analysis Mode')
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "latency_comparison.png"
    
    plt.savefig(str(output_file), dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_file}")
    plt.close()


def plot_accuracy_vs_latency(results_file, output_dir="results/visualizations"):
    """
    Create scatter plot of accuracy vs latency tradeoff.
    
    Args:
        results_file: Path to results CSV
        output_dir: Directory to save plot
    """
    df = pd.read_csv(results_file)
    df = df.drop_duplicates(subset=['File', 'Mode'], keep='last')

    def get_parent_id(mitre_id):
        if pd.isna(mitre_id):
            return "Unknown"
        return str(mitre_id).split('.')[0]

    df['True_Parent'] = df['True'].apply(get_parent_id)
    df['Pred_Parent'] = df['Pred'].apply(get_parent_id)
    df['Match'] = df['True_Parent'] == df['Pred_Parent']

    summary = df.groupby('Mode').agg({
        'Match': 'mean',
        'Time': 'mean'
    }).reset_index()
    summary['Accuracy'] = summary['Match'] * 100

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    colors = {'A_Baseline': 'blue', 'B_Naive': 'green', 'C_HyDE': 'red'}
    for mode in summary['Mode']:
        data = summary[summary['Mode'] == mode]
        plt.scatter(
            data['Time'], data['Accuracy'], s=200, label=mode,
            color=colors.get(mode, 'gray'), alpha=0.7
        )
        plt.text(
            data['Time'].values[0], data['Accuracy'].values[0],
            f"  {mode}", ha='left', va='bottom', fontweight='bold'
        )

    plt.xlabel('Latency (seconds)', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.title('Accuracy vs Latency Tradeoff', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "accuracy_latency_tradeoff.png"
    
    plt.savefig(str(output_file), dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_file}")
    plt.close()
