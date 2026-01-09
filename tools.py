import csv
import json
from pathlib import Path
from typing import List, Dict, Any

def write_markdown(path: str, text: str) -> None:
    """
    Write text content to a markdown file.
    
    Args:
        path: File path where markdown will be written
        text: Markdown content to write
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def write_csv(path: str, rows: List[List[Any]]) -> None:
    """
    Write rows to a CSV file.
    
    Args:
        path: File path where CSV will be written
        rows: List of rows, where each row is a list of values
    """
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def append_jsonl_log(event: Dict[str, Any], log_path: str = "events.jsonl") -> None:
    """
    Append an event as a JSON line to a log file.
    
    Args:
        event: Dictionary containing event data
        log_path: Path to the JSONL log file (default: "events.jsonl")
    """
    
    with open(log_path, 'a') as f:
        f.write(f'{json.dumps(event)}\n')


def render_prd(prd_obj: Dict[str, Any]) -> str:
    """
    Render a PRD (Product Requirements Document) object as a markdown string.
    
    Args:
        prd_obj: Dictionary containing PRD data with keys like 'title', 'overview', 
                'objectives', 'requirements', 'constraints', etc.
    
    Returns:
        Formatted markdown string
    """
    # Add title and overview
    result = f"# {prd_obj['title']}\n\n"
    result += f"## Overview\n{prd_obj['overview']}\n\n"
    
    # Helper pattern for list sections
    for section_name in ['objectives', 'requirements', 'constraints']:
        result += f"## {section_name.capitalize()}\n"
        for item in prd_obj[section_name]:
            result += f"- {item}\n"
        result += "\n"
    
    return result

