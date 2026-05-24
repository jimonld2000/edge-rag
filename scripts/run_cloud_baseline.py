"""Run a Google Gemini baseline to establish an upper-bound for the paper."""

import os
import sys
import time
import pandas as pd
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import google.generativeai as genai

from src.config import EVTX_FOLDER, OUTPUT_FILE, GOLD_LABELS_FILE, LOG_TRUNCATION_LENGTH
from src.parsers import parse_evtx, get_evtx_files
from src.utils import safe_json_parse

import dotenv
dotenv.load_dotenv()

# Initialize Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=api_key)

def run_gemini_baseline():
    labels_df = pd.read_csv(GOLD_LABELS_FILE)
    truth_map = dict(zip(labels_df["Filename"], labels_df["True_ID"]))
    
    files = get_evtx_files(EVTX_FOLDER, recursive=True)
    valid_files = [f for f in files if f.name in truth_map]
    
    results_data = []
    
    # Using cloud-based Gemini model
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    
    print("Starting Google Gemini baseline...")
    
    for file_path in tqdm(valid_files, desc="Running Gemini Upper Bound"):
        log_content = parse_evtx(str(file_path))
        if not log_content: continue
        
        short_log = log_content[:LOG_TRUNCATION_LENGTH]
        true_label = str(truth_map.get(file_path.name, "Unknown")).strip()
        
        prompt = f"""
        You are an elite security expert. Match the provided Windows Event Log to the most accurate MITRE ATT&CK ID.
        Output ONLY a JSON object in this exact format:
        {{"id": "Txxxx"}}
        
        <log_data>
        {short_log}
        </log_data>
        """
        
        t0 = time.time()
        success = False
        retries = 3
        
        while retries > 0 and not success:
            try:
                # Force JSON output mode for perfect parsing
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                    )
                )
                result = safe_json_parse(response.text)
                pred_id = result.get('id', 'Unknown')
                success = True
            except Exception as e:
                if "429" in str(e): # Rate limit hit
                    print(f"\nRate limit hit! Sleeping for 15 seconds... ({retries} retries left)")
                    time.sleep(15)
                    retries -= 1
                else:
                    pred_id = "Error"
                    break
                    
        if not success:
            pred_id = "API_Failed"
            
        latency = time.time() - t0
        
        results_data.append({
            "File": file_path.name,
            "Mode": "E_Cloud_Upper_Bound", # Matches your analytics script
            "True": true_label,
            "Pred": pred_id,
            "Strict_Match": pred_id == true_label,
            "Time": latency
        })
        
        # Google's free tier allows 15 requests per minute. 
        # Sleeping for 4.1 seconds ensures we stay perfectly under the limit (approx 14.6 req/min).
        time.sleep(4.1)

    # Append to existing results
    df_new = pd.DataFrame(results_data)
    if os.path.exists(OUTPUT_FILE):
        df_old = pd.read_csv(OUTPUT_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    df_combined.to_csv(OUTPUT_FILE, index=False)
    print("Cloud baseline completed and appended to results!")

if __name__ == "__main__":
    run_gemini_baseline()