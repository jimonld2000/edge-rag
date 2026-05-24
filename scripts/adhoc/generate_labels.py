import pandas as pd
from pathlib import Path

EVTX_FOLDER = "data/evtx_samples"

def main():
    files = list(Path(EVTX_FOLDER).rglob("*.evtx"))
    
    data = []
    for f in files:
        data.append({
            "Filename": f.name,
            "Folder": f.parent.name,
            "True_ID": "" # <--- You will fill this in manually!
        })
    
    df = pd.DataFrame(data)
    df.to_csv("gold_labels.csv", index=False)
    print(f"Generated gold_labels.csv with {len(files)} files. Go fill in the 'True_ID' column!")

if __name__ == "__main__":
    main()