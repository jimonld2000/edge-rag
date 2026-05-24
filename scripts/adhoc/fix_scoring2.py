import pandas as pd
import requests
from pathlib import Path

# Important: Point this to your gold_labels.csv file!
GOLD_LABELS_FILE = Path("./gold_labels.csv") 

def build_navigator_revocation_map():
    """
    Mirrors the ATT&CK Navigator's logic.
    Pulls the official STIX feed and resolves revoked_by_ref pointers.
    """
    print("Downloading official MITRE Enterprise STIX database...")
    url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        stix_data = response.json()
    except Exception as e:
        print(f"Failed to download STIX data: {e}")
        return {}

    # Step 1: Map STIX IDs to T-Codes (e.g., 'attack-pattern--xyz' -> 'T1183')
    id_to_tcode = {}
    for obj in stix_data.get('objects', []):
        if obj.get('type') == 'attack-pattern':
            for ref in obj.get('external_references', []):
                if ref.get('source_name') == 'mitre-attack':
                    id_to_tcode[obj['id']] = ref['external_id']

    # Step 2: Find 'revoked-by' STIX Relationship Objects (SROs)
    revocation_map = {}
    for obj in stix_data.get('objects', []):
        if obj.get('type') == 'relationship' and obj.get('relationship_type') == 'revoked-by':
            old_stix_id = obj.get('source_ref')
            new_stix_id = obj.get('target_ref')
            
            # Translate the STIX IDs back into human-readable T-Codes
            if old_stix_id in id_to_tcode and new_stix_id in id_to_tcode:
                old_tcode = id_to_tcode[old_stix_id]
                new_tcode = id_to_tcode[new_stix_id]
                revocation_map[old_tcode] = new_tcode
                
    return revocation_map

def fix_gold_labels():
    # Make sure the path is correct based on where you run the script from
    gold_labels_file = GOLD_LABELS_FILE
    if not gold_labels_file.exists():
        # Fallback if running directly in the scripts folder
        alt_path = Path("../data/gold_labels.csv")
        if alt_path.exists():
            gold_labels_file = alt_path
        else:
            print(f"Could not find gold_labels.csv at {gold_labels_file} or {alt_path}")
            return

    df = pd.read_csv(gold_labels_file)
    revocation_map = build_navigator_revocation_map()
    
    print("\n--- ATT&CK Navigator Legacy Remapping ---")
    fixed_count = 0
    
    def remap_tcode(tcode):
        nonlocal fixed_count
        clean_tcode = str(tcode).strip()
        if clean_tcode in revocation_map:
            new_tcode = revocation_map[clean_tcode]
            print(f"Remapping deprecated {clean_tcode} -> {new_tcode}")
            fixed_count += 1
            return new_tcode
        return clean_tcode

    # Apply the remap to the 'True_ID' column (ensure this matches your CSV column name)
    # Note: Depending on your CSV structure, this might be named 'True_ID' or 'True'
    target_column = 'True_ID' if 'True_ID' in df.columns else 'True'
    
    if target_column in df.columns:
        df[target_column] = df[target_column].apply(remap_tcode)
        # Save the fixed labels back to the CSV
        df.to_csv(GOLD_LABELS_FILE, index=False)
        print(f"\nSuccessfully remapped {fixed_count} legacy labels using official STIX pointers.")
    else:
        print(f"Error: Could not find '{target_column}' column in {GOLD_LABELS_FILE}")

if __name__ == "__main__":
    fix_gold_labels()