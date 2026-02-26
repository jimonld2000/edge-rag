"""Core RAG analysis pipeline implementations."""

import json
import time
import ollama
from src.config import OLLAMA_MODEL, LOG_TRUNCATION_LENGTH, MAX_RETRIEVAL_RESULTS
from src.utils import get_embedding_model, safe_json_parse


def hyde_analysis(log_text, table):
    """
    HyDE (Hypothetical Document Embeddings) Analysis Pipeline.
    
    Three-step process:
    1. Transform Log -> Search Query (Concept Translation via LLM)
    2. Retrieve Context using Concept
    3. Final Reasoning with retrieved context
    
    Args:
        log_text: Event log text to analyze
        table: LanceDB table for retrieval
        
    Returns:
        dict: Analysis result with id, confidence, and reasoning
    """
    print("  -> Starting HyDE Analysis Pipeline...")
    
    # --- STEP 1: Query Transformation ---
    t0 = time.time()
    
    search_prompt = f"""
    You are a security expert. Briefly summarize the suspicious behavior in this log. 
    Focus on the attack technique (e.g., "persistence via registry", "UAC bypass", "credential dumping").
    Do not mention specific IDs. Keep it under 20 words.
    
    Log:
    {log_text[:LOG_TRUNCATION_LENGTH]}
    """
    
    query_response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{'role': 'user', 'content': search_prompt}]
    )
    search_query = query_response['message']['content'].strip()
    
    t1 = time.time()
    print(f"     [1] Query Gen:   {t1-t0:.2f}s | Concept: \"{search_query}\"")

    # --- STEP 2: Retrieval ---
    t2 = time.time()
    
    model = get_embedding_model()
    query_vector = model.encode(search_query, normalize_embeddings=True)
    
    results = table.search(query_vector).limit(MAX_RETRIEVAL_RESULTS).to_list()
    context_str = "\n".join([
        f"- {r['id']} {r['name']}: {r['text'][:200]}..." 
        for r in results
    ])
    
    t3 = time.time()
    retrieved_ids = [r['id'] for r in results]
    print(f"     [2] Retrieval:   {t3-t2:.2f}s | Found: {retrieved_ids}")

    # --- STEP 3: Final Reasoning ---
    t4 = time.time()
    
    final_prompt = f"""
    You are a security analyst. Match the Log to the best MITRE technique from the Context.
    
    [LOG DATA]
    {log_text[:2000]}
    
    [SEARCH CONCEPT USED]
    {search_query}
    
    [RETRIEVED CONTEXT]
    {context_str}
    
    Which MITRE ID matches best? 
    If the context contains a UAC Bypass or Elevation technique (like T1548), prioritize it.
    If none match, say "Unknown".
    
    Output JSON: {{"id": "Txxxx", "confidence": "High/Medium/Low", "reasoning": "explanation"}}
    """
    
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{'role': 'user', 'content': final_prompt}],
        format='json'
    )
    
    t5 = time.time()
    print(f"     [3] Reasoning:   {t5-t4:.2f}s")
    
    result = safe_json_parse(response['message']['content'])
    result['total_time'] = t5 - t0
    
    return result


def baseline_analysis(log_text, table):
    """
    Baseline Vector-Only Analysis.
    
    Raw Log -> Embed -> Search -> Top 1 Result ID.
    No LLM reasoning - fast but less sophisticated.
    
    Args:
        log_text: Event log text to analyze
        table: LanceDB table for retrieval
        
    Returns:
        dict: Result with id and time
    """
    t0 = time.time()
    model = get_embedding_model()
    query_vector = model.encode(log_text, normalize_embeddings=True)
    results = table.search(query_vector).limit(1).to_list()
    
    predicted_id = results[0]['id'] if results else "Unknown"
    latency = time.time() - t0
    
    return {
        'id': predicted_id,
        'confidence': 'N/A',
        'reasoning': 'Vector baseline - no reasoning',
        'total_time': latency
    }


def naive_rag_analysis(log_text, table):
    """
    Naive RAG Analysis.
    
    Log -> Embed -> Retrieve Context -> LLM Reasoning
    Simpler reasoning without hypothesis generation.
    
    Args:
        log_text: Event log text to analyze
        table: LanceDB table for retrieval
        
    Returns:
        dict: Result with id, confidence, and time
    """
    t0 = time.time()
    
    short_log = log_text[:LOG_TRUNCATION_LENGTH]
    
    model = get_embedding_model()
    query_vector = model.encode(short_log, normalize_embeddings=True)
    results = table.search(query_vector).limit(MAX_RETRIEVAL_RESULTS).to_list()
    context_str = "\n".join([
        f"- ID: {r['id']}, Desc: {r['text'][:150]}" 
        for r in results
    ])
    
    prompt = f"""
    Match this Log to a MITRE ID from the Context.
    
    Log: {short_log}
    
    Context:
    {context_str}
    
    Output JSON: {{"id": "Txxxx", "confidence": "High/Medium/Low"}}
    """
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        result = safe_json_parse(response['message']['content'])
        result['reasoning'] = 'Naive RAG - direct LLM matching'
        result['total_time'] = time.time() - t0
        return result
    except Exception as e:
        return {
            'id': 'Error',
            'confidence': 'N/A',
            'reasoning': str(e),
            'total_time': time.time() - t0
        }
