import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# Try to import adjustText for better label placement in Fig 4
try:
    from adjustText import adjust_text
    ADJUST_TEXT_AVAILABLE = True
except ImportError:
    ADJUST_TEXT_AVAILABLE = False
    print("Note: 'adjustText' library not found. Figure 4 labels might overlap. "
          "Install with: pip install adjustText")

# -----------------------------
# 1. Setup & Styling
# -----------------------------
# Set academic aesthetic
sns.set_theme(style="ticks", context="paper", font_scale=1.4)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True # Helps with label clipping
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Define consistent colors for modes
COLORS = {"A_Baseline": "#E24A33", "B_Naive": "#348ABD", "C_HyDE": "#988ED5"}

def load_data(filename='final_results.csv'):
    try:
        df = pd.read_csv(filename)
        # Ensure 'Match' is boolean or 0/1 for calculation
        df['Match'] = df['Match'].astype(int) 
        
        # Standardize column names if needed
        df.rename(columns={'True_Label': 'True', 'Predicted_Label': 'Pred', 'Latency_Seconds': 'Time'}, 
                  inplace=True, errors='ignore')
        
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

# -----------------------------
# Figure 1: Accuracy Comparison (Bar Chart)
# -----------------------------
def plot_accuracy(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.barplot(
        data=df, 
        x='Mode', 
        y='Match', 
        hue='Mode',
        palette=COLORS, 
        legend=False,
        capsize=.1, 
        errorbar=('ci', 95),
        ax=ax
    )
    
    ax.set_title("Figure 1: Accuracy Comparison by Mode", fontweight='bold', pad=20)
    ax.set_ylabel("Accuracy (% Matches)", fontweight='bold')
    ax.set_xlabel("", fontweight='bold')
    ax.set_ylim(0, 1.05)
    
    # Format Y-axis as percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    fig.savefig('fig1_accuracy.png', dpi=300, bbox_inches='tight')
    print("Saved fig1_accuracy.png")
    plt.close(fig)

# -----------------------------
# Figure 2: The "Latency Tax" (Box Plot)
# -----------------------------
def plot_latency(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.boxplot(
        data=df, 
        x='Mode', 
        y='Time', 
        hue='Mode',
        palette=COLORS,
        legend=False,
        width=0.6,
        showfliers=False, # Hide outliers for cleaner academic look
        linewidth=1.5,
        ax=ax
    )
    
    ax.set_title("Figure 2: Latency Distribution (The Trade-off)", fontweight='bold', pad=20)
    ax.set_ylabel("Latency (Seconds)", fontweight='bold')
    ax.set_xlabel("", fontweight='bold')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    fig.savefig('fig2_latency.png', dpi=300, bbox_inches='tight')
    print("Saved fig2_latency.png")
    plt.close(fig)

# -----------------------------
# Figure 3: Confusion Matrix (HyDE Only) - IMPROVED
# -----------------------------
def plot_confusion_matrix(df):
    # 1. Filter for HyDE mode only
    hyde_df = df[df['Mode'] == 'C_HyDE'].copy()
    if hyde_df.empty:
        print("Warning: No data found for Mode 'C_HyDE'. Skipping Fig 3.")
        return

    # 2. Select Top 5 most common True Labels
    top_true_labels = hyde_df['True'].value_counts().nlargest(5).index
    filtered_df = hyde_df[hyde_df['True'].isin(top_true_labels)].copy()
    
    # 3. Select Top N most common Predicted Labels within this filtered set
    # This is key to reducing the number of columns and making the plot readable.
    TOP_N_PRED = 10 
    top_pred_labels = filtered_df['Pred'].value_counts().nlargest(TOP_N_PRED).index
    
    # Group any predicted labels not in the top N into "Other"
    filtered_df.loc[~filtered_df['Pred'].isin(top_pred_labels), 'Pred'] = 'Other'
    
    # 4. Create Confusion Matrix (Normalize by True Label)
    cm = pd.crosstab(filtered_df['True'], filtered_df['Pred'], normalize='index')
    
    # Reorder columns to put "Other" last if it exists
    pred_cols = [col for col in cm.columns if col != 'Other']
    if 'Other' in cm.columns:
        pred_cols.append('Other')
    cm = cm[pred_cols]

    # 5. Plot Heatmap
    # Increase figure size for better readability
    fig, ax = plt.subplots(figsize=(12, 8)) 
    
    sns.heatmap(
        cm, 
        annot=True, 
        fmt=".0%", # Show as percentage with no decimals for clearer view
        cmap="Blues", 
        linewidths=1,
        linecolor='white',
        cbar_kws={'label': 'Proportion Classified', 'shrink': .8},
        square=True, # Make cells square
        ax=ax,
        annot_kws={"size": 10} # Reduce annotation font size slightly
    )
    
    ax.set_title("Figure 3: HyDE Confusion Matrix\n(Top 5 True vs. Top 10 Predicted Categories)", 
                 fontweight='bold', pad=20)
    ax.set_ylabel("True Attack Category", fontweight='bold')
    ax.set_xlabel("Predicted Category", fontweight='bold')
    
    # Rotate x-labels for readability
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    
    fig.savefig('fig3_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("Saved fig3_confusion_matrix.png")
    plt.close(fig)

# -----------------------------
# Figure 4: Efficiency Scatter Plot (Pareto Frontier)
# -----------------------------
def plot_efficiency(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Aggregate data by Mode
    summary = df.groupby('Mode').agg({
        'Time': 'mean',
        'Match': 'mean'
    }).reset_index()
    
    # Plot Scatter
    sns.scatterplot(
        data=summary,
        x='Time',
        y='Match',
        hue='Mode',
        palette=COLORS,
        s=500, # Larger markers
        edgecolor='black',
        linewidth=2,
        alpha=0.9,
        zorder=10,
        ax=ax,
        legend=False # We will label points directly
    )
    
    # Add labels
    texts = []
    for i in range(summary.shape[0]):
        # Basic manual offset
        x_pos = summary.Time[i]
        y_pos = summary.Match[i] + 0.01
        
        text = ax.text(
            x_pos, 
            y_pos,
            summary.Mode[i], 
            horizontalalignment='center', 
            verticalalignment='bottom',
            size='x-large', 
            color=COLORS[summary.Mode[i]], # Color label to match marker
            weight='bold'
        )
        texts.append(text)

    # Use adjust_text if available to prevent overlaps
    if ADJUST_TEXT_AVAILABLE:
        adjust_text(texts, ax=ax, 
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5),
                    force_text=(0.1, 0.5)) # Adjust force parameters as needed

    ax.set_title("Figure 4: Efficiency Frontier (Accuracy vs. Latency)", fontweight='bold', pad=20)
    ax.set_ylabel("Accuracy (Mean Match Rate)", fontweight='bold', fontsize=12)
    ax.set_xlabel("Latency (Mean Seconds)", fontweight='bold', fontsize=12)
    
    # Set limits and grid
    ax.set_xlim(left=0)
    ax.set_ylim(0, 1.15) # More headroom for labels
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Format Y-axis as percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    fig.savefig('fig4_efficiency.png', dpi=300, bbox_inches='tight')
    print("Saved fig4_efficiency.png")
    plt.close(fig)

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    df = load_data()
    
    if df is not None:
        print("Data loaded. Generating improved plots...")
        # Check for required columns
        required_cols = ['Mode', 'True', 'Pred', 'Time', 'Match']
        if all(col in df.columns for col in required_cols):
            plot_accuracy(df)
            plot_latency(df)
            plot_confusion_matrix(df)
            plot_efficiency(df)
            print("\nAll plots generated successfully. Check the .png files.")
        else:
            print(f"Error: The CSV is missing one or more required columns: {required_cols}")
            print(f"Found columns: {list(df.columns)}")