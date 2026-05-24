import pandas as pd

def fix_scoring(file_path):
    # 1. Load the CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return

    # 2. Define the Deprecation Map (MITRE v8/v9 -> v14)
    DEPRECATION_MAP = {
        'T1086': 'T1059.001',  # PowerShell -> Command and Scripting Interpreter: PowerShell
        'T1084': 'T1546.003',  # WMI Event Subscription -> Event Triggered Execution: WMI
        'T1117': 'T1218.010',  # Regsvr32 -> Signed Binary Proxy Execution: Regsvr32
        'T1085': 'T1218.011',  # Rundll32 -> Signed Binary Proxy Execution: Rundll32
        'T1064': 'T1059',      # Scripting -> Command and Scripting Interpreter
        'T1073': 'T1574.002',  # DLL Side-Loading -> Hijack Execution Flow: DLL Side-Loading
        'T1060': 'T1547.001',  # Registry Run Keys -> Boot or Logon Autostart Execution: Registry Run Keys
        'T1158': 'T1564.001',  # Hidden Files -> Hide Artifacts: Hidden Files and Directories
        'T1050': 'T1543.003',  # New Service -> Create or Modify System Process: Windows Service
        'T1035': 'T1569.002',  # Service Execution -> System Services: Service Execution
        'T1031': 'T1543.003',  # Modify Existing Service -> Create or Modify System Process: Windows Service
        'T1193': 'T1566.001',  # Spearphishing Attachment -> Phishing: Spearphishing Attachment
        'T1192': 'T1566.002'   # Spearphishing Link -> Phishing: Spearphishing Link
    }

    # 3. Apply Normalization
    # If the label exists in the map, replace it; otherwise, keep the original.
    df['True_Normalized'] = df['True'].map(DEPRECATION_MAP).fillna(df['True'])

    # 4. Calculate Old Accuracy (Strict Match)
    df['Strict_Match'] = df['True'] == df['Pred']
    old_accuracy = df['Strict_Match'].mean()

    # 5. Calculate New "Scientific" Accuracy (Parent Logic)
    def get_parent(label):
        # Handles NaNs and ensures string conversion
        if pd.isna(label): return "Unknown"
        return str(label).split('.')[0]

    # Extract parents from the Normalized Truth and the Prediction
    df['True_Parent'] = df['True_Normalized'].apply(get_parent)
    df['Pred_Parent'] = df['Pred'].apply(get_parent)

    # Check for matches on the Parent ID
    df['Soft_Match'] = df['True_Parent'] == df['Pred_Parent']
    new_accuracy = df['Soft_Match'].mean()

    # 6. Identify "Fixed" Rows
    # Rows where the original strict match failed, but the new logic succeeds
    fixed_rows = df[(~df['Strict_Match']) & (df['Soft_Match'])]

    # 7. Generate Report
    print("=" * 40)
    print("SCORING CORRECTION REPORT")
    print("=" * 40)
    print(f"Old Accuracy (Strict Match):       {old_accuracy:.2%}")
    print(f"New Accuracy (Normalized + Parent): {new_accuracy:.2%}")
    print("-" * 40)
    print(f"Total Rows Processed: {len(df)}")
    print(f"Rows 'Salvaged' (Fixed): {len(fixed_rows)}")
    print("-" * 40)

    # --- NEW: Save the results to a CSV ---
    output_filename = 'final_results_fixed.csv'
    df.to_csv(output_filename, index=False)
    print(f"\n[+] Saved normalized results to: {output_filename}")
    
    if not fixed_rows.empty:
        print("Sample of Fixed Rows (Original Mismatch -> New Match):")
        # Display key columns to verify the logic
        print(fixed_rows[['File', 'True', 'True_Normalized', 'Pred']].head(10).to_string(index=False))
        if len(fixed_rows) > 10:
            print(f"...and {len(fixed_rows) - 10} more.")
    else:
        print("No rows were fixed by this logic.")

if __name__ == "__main__":
    fix_scoring('final_results.csv')