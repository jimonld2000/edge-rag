import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df = pd.read_csv("final_results.csv")

# Clean Data (Drop Duplicates/NaNs)
df = df.drop_duplicates(subset=['File', 'Mode'], keep='last')

# Calculate Metrics
def get_parent_id(mitre_id):
    if pd.isna(mitre_id): return "Unknown"
    return str(mitre_id).split('.')[0]

df['True_Parent'] = df['True'].apply(get_parent_id)
df['Pred_Parent'] = df['Pred'].apply(get_parent_id)
df['Match'] = df['True_Parent'] == df['Pred_Parent']

# Aggregate
summary = df.groupby('Mode')[['Match', 'Time']].mean().reset_index()
summary['Accuracy'] = summary['Match'] * 100

# Plotting
plt.figure(figsize=(10, 5))
sns.set_style("whitegrid")

# Create Bar Chart
ax = sns.barplot(x='Mode', y='Accuracy', data=summary, palette="viridis", order=['A_Baseline', 'B_Naive', 'C_HyDE'])

# Add Labels
for i, row in summary.iterrows():
    # Find the correct location based on order
    idx = ['A_Baseline', 'B_Naive', 'C_HyDE'].index(row['Mode'])
    ax.text(idx, row['Accuracy'] + 1, f"{row['Accuracy']:.1f}%", color='black', ha="center", fontweight='bold')

plt.title('Detection Accuracy by Method (Soft Match)', fontsize=14, fontweight='bold')
plt.ylabel('Accuracy (%)')
plt.xlabel('Analysis Mode')
plt.ylim(0, 35)  # Set limit slightly higher than max accuracy
plt.savefig("accuracy_chart.png", dpi=300)
print("Chart saved to accuracy_chart.png")