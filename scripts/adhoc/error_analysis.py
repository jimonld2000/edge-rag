import pandas as pd

def analyze_failures(csv_file):
    # Load data
    df = pd.read_csv(csv_file)
    print("=" * 50)
    print("     EDGE-RAG FAILURE MODE ANALYSIS")
    print("=" * 50)

    # 1. Analyze Edge-HyDE (C_HyDE)
    hyde_df = df[df['Mode'] == 'C_HyDE']
    hyde_failures = hyde_df[hyde_df['Strict_Match'] == False]
    total_hyde_failures = len(hyde_failures)

    safe_abstentions_hyde = hyde_failures[hyde_failures['Pred'].astype(str).str.lower() == 'unknown']
    hallucinations_hyde = hyde_failures[hyde_failures['Pred'].astype(str).str.lower() != 'unknown']

    print(f"\n[ Edge-HyDE ] Total Failures: {total_hyde_failures}")
    if total_hyde_failures > 0:
        pct_safe = (len(safe_abstentions_hyde)/total_hyde_failures) * 100
        pct_halluc = (len(hallucinations_hyde)/total_hyde_failures) * 100
        print(f"  -> Safe Abstentions ('Unknown'): {len(safe_abstentions_hyde)} ({pct_safe:.1f}%)")
        print(f"  -> Hallucinations (Wrong Class): {len(hallucinations_hyde)} ({pct_halluc:.1f}%)")

    # 2. Analyze Naive RAG (B_Naive) for baseline comparison
    naive_df = df[df['Mode'] == 'B_Naive']
    naive_failures = naive_df[naive_df['Strict_Match'] == False]
    total_naive_failures = len(naive_failures)

    safe_abstentions_naive = naive_failures[naive_failures['Pred'].astype(str).str.lower() == 'unknown']
    hallucinations_naive = naive_failures[naive_failures['Pred'].astype(str).str.lower() != 'unknown']

    print(f"\n[ Naive RAG ] Total Failures: {total_naive_failures}")
    if total_naive_failures > 0:
        pct_safe = (len(safe_abstentions_naive)/total_naive_failures) * 100
        pct_halluc = (len(hallucinations_naive)/total_naive_failures) * 100
        print(f"  -> Safe Abstentions ('Unknown'): {len(safe_abstentions_naive)} ({pct_safe:.1f}%)")
        print(f"  -> Hallucinations (Wrong Class): {len(hallucinations_naive)} ({pct_halluc:.1f}%)")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    analyze_failures("final_results_fixed.csv")