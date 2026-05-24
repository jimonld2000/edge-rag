import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set academic visualization standards
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.titlesize": 14,
    "font.family": "sans-serif"
})

# Define a professional, cohesive color palette
COLOR_NAIVE = "#a6c8e0"       # Soft Muted Blue
COLOR_HYDE = "#1f4e79"        # Deep Navy Blue
COLOR_CLOUD = "#d95f02"       # Sovereign Orange Reference Line
COLOR_ABSTAIN = "#2ca02c"     # Safe Green
COLOR_HALLUCINATE = "#d62728" # Alert Red

def generate_figure_2():
    """Generates an academically optimized Figure 2 with clean layer sorting and headroom."""
    models = ["Qwen 3.5\n(0.8B)", "Gemma 4\n(2B)", "Ministral 3\n(3B)", "Phi-4\n(14B)"]
    naive_accuracy = [1.1, 8.7, 7.6, 7.2]
    hyde_accuracy = [0.7, 19.6, 15.9, 23.2]
    cloud_upper_bound = 24.3

    x = np.arange(len(models))
    width = 0.35

    # Step 1: Increased figure height slightly for better vertical allocation
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    
    # Grid lines set to low zorder so they stay in the background
    ax.set_axisbelow(True)
    
    rects1 = ax.bar(x - width/2, naive_accuracy, width, label="Standard Naive RAG", 
                    color=COLOR_NAIVE, edgecolor="black", linewidth=0.8, zorder=3)
    rects2 = ax.bar(x + width/2, hyde_accuracy, width, label="Edge-HyDE (Ours)", 
                    color=COLOR_HYDE, edgecolor="black", linewidth=0.8, zorder=3)
    
    # Step 2: Draw the horizontal line *behind* the text labels but in front of grids
    ax.axhline(y=cloud_upper_bound, color=COLOR_CLOUD, linestyle="--", linewidth=1.5, 
               zorder=2, label=f"Cloud Upper Bound (Gemini 3.1 Flash Lite: {cloud_upper_bound}%)")

    # Labels and formatting
    ax.set_ylabel("Soft Classification Accuracy (%)", weight="bold", labelpad=10)
    ax.set_title("Figure 2: Relative Soft Accuracy Gains Across Local Scaling Tiers", weight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    
    # Step 3: Expanded Y-limit to 35% to clear space for the legend box
    ax.set_ylim(0, 35) 
    
    # Step 4: Refined legend placement with a clean boundary frame inside the new headroom
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=1.0, fontsize=10)

    # Step 5: Enhanced bar labels to prevent collision loops
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height}%",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  # Increased padding above the bar
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5, weight="bold", zorder=4)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig("figure_2_accuracy_gains.png", bbox_inches="tight")
    plt.close()

def generate_figure_3():
    """Generates an academically optimized Figure 3 with perfectly centered text labels."""
    # Data definitions based on empirical totals
    naive_data = [100.0, 0.0]  # 100% Hallucinations, 0% Safe Abstentions
    hyde_data = [82.1, 17.9]   # 82.1% Hallucinations, 17.9% Safe Abstentions
    
    labels = ["Hallucinations (False Positives)", "Safe Abstentions ('Unknown')"]
    colors = [COLOR_HALLUCINATE, COLOR_ABSTAIN]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.5), dpi=300)

    # Lambda function to suppress 0.0% labels to prevent messy layout collisions
    clean_pct = lambda p: f'{p:.1f}%' if p > 0 else ''

    # Donut chart 1: Naive RAG
    # Adjusted pctdistance to 0.78 to center text between inner radius (0.6) and outer radius (1.0)
    wedges1, texts1, autotexts1 = ax1.pie(
        naive_data, autopct=clean_pct, startangle=90, 
        colors=colors, pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor="black", linewidth=0.8)
    )
    ax1.set_title("Standard Naive RAG Failures", weight="bold", pad=12)

    # Donut chart 2: Edge-HyDE
    # Adjusted pctdistance to 0.78 here as well
    wedges2, texts2, autotexts2 = ax2.pie(
        hyde_data, autopct=clean_pct, startangle=90, 
        colors=colors, pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor="black", linewidth=0.8)
    )
    ax2.set_title("Proposed Edge-HyDE Failures", weight="bold", pad=12)

    # Clean up text properties explicitly to ensure crisp readability within the wedges
    for autotext in autotexts1 + autotexts2:
        autotext.set_color('white')
        autotext.set_weight('bold')
        autotext.set_fontsize(11) # Slightly enlarged for crisp visibility

    # Unified Legend and Subtitle configuration
    fig.legend(wedges2, labels, loc="lower center", ncol=2, frameon=True, edgecolor="#cccccc", fontsize=10)
    fig.suptitle("Figure 3: Behavioral Error Distribution and Safety Deficits under Failure Conditions", weight="bold", y=0.98)
    
    plt.tight_layout()
    # Adjust subplot vertical allocation to leave proper room for titles and legend
    fig.subplots_adjust(bottom=0.20, top=0.85, wspace=0.3)
    
    plt.savefig("figure_3_failure_modes.png", bbox_inches="tight")
    plt.close()

def generate_figure_4():
    """Generates Figure 4: Edge-HyDE Soft Accuracy Distribution Categorized by Parent MITRE Tactic."""
    # Placeholders reflecting performance trends from logs (Replace values directly from your aggregate CSV summary)
    tactics = [
        "Defense Evasion", 
        "Credential Access", 
        "Lateral Movement", 
        "Persistence", 
        "Execution", 
        "Privilege Escalation"
    ]
    # Example accuracy profile mapping performance peaks noted in text
    accuracies = [31.4, 26.8, 18.5, 14.2, 12.0, 9.5] 

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    
    bars = ax.barh(tactics, accuracies, color=COLOR_HYDE, edgecolor="black", linewidth=0.7, height=0.6)
    
    # Label modifications
    ax.invert_yaxis()  # Read top-to-bottom
    ax.set_xlabel("Soft Accuracy per Tactic Group (%)")
    ax.set_title("Figure 4: Edge-HyDE Soft Accuracy Distribution Categorized by Parent MITRE Tactic")
    ax.set_xlim(0, 40)

    # Add exact value readouts to the right of the bars
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f" {width}%",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha="left", va="center", fontsize=10, weight="bold")

    plt.tight_layout()
    plt.savefig("figure_4_tactic_breakdown.png", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    print("Generating Figure 2...")
    generate_figure_2()
    print("Generating Figure 3...")
    generate_figure_3()
    print("Generating Figure 4...")
    generate_figure_4()
    print("All figures successfully exported as high-DPI PNGs!")