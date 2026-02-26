"""Event log parsing utilities for EVTX files."""

from pathlib import Path
from Evtx.Evtx import Evtx
from src.utils import clean_xml_to_string


def parse_evtx(file_path):
    """
    Parse binary EVTX file and extract the most recent event.
    
    Reads Windows Event Log files and extracts the latest event record,
    converting XML to clean text format.
    
    Args:
        file_path: Path to .evtx file
        
    Returns:
        str: Cleaned event log text or None on failure
    """
    print(f"Reading: {file_path}")
    
    try:
        with Evtx(file_path) as log:
            last_record = None
            for record in log.records():
                last_record = record
            
            if last_record:
                return clean_xml_to_string(last_record.xml())
            else:
                return None
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return None


def get_evtx_files(evtx_folder, recursive=True, limit=None):
    """
    Find EVTX files in a directory.
    
    Args:
        evtx_folder: Path to search
        recursive: Whether to search subdirectories
        limit: Maximum number of files to return
        
    Returns:
        list: List of Path objects pointing to EVTX files
    """
    folder_path = Path(evtx_folder)
    
    if recursive:
        files = list(folder_path.rglob("*.evtx"))
    else:
        files = list(folder_path.glob("*.evtx"))
    
    if limit:
        files = files[:limit]
    
    return files
