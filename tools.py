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
    out_dir = ensure_output_dir()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def write_csv(path: str, rows: List[List[Any]]) -> None:
    """
    Write rows to a CSV file.
    
    Args:
        path: File path where CSV will be written
        rows: List of rows, where each row is a list of values
    """
    out_dir = ensure_output_dir()
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
    out_dir = ensure_output_dir()
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

def ensure_output_dir() -> Path:
    Path("output").mkdir(parents=True, exist_ok=True)
    return Path("output")


def render_prd_md(prd: "PRD") -> str:
    """
    Render a Product Requirements Document (PRD) object into a formatted Markdown string.

    This function takes a PRD object and converts it into a well-structured Markdown document
    with sections for problem statement, target users, goals, non-goals, user stories,
    functional and non-functional requirements, risks, and open questions.

    Args:
        prd (PRD): A PRD object containing all the product requirements information.
            Expected attributes:
            - title (str): The title of the PRD
            - problem (str): Description of the problem being solved
            - target_users (list): List of target user descriptions
            - goals (list): List of project goals
            - non_goals (list): List of explicit non-goals
            - user_stories (list): List of user stories
            - functional_requirements (list): List of functional requirements
            - nonfunctional_requirements (list): List of non-functional requirements
            - risks (list): List of potential risks
            - open_questions (list): List of unresolved questions

    Returns:
        str: A formatted Markdown string representing the complete PRD document.
    """
    def bullets(items):
        """
        Convert a list of items into Markdown bullet points.
        
        Args:
            items: List of items to convert to bullet points
            
        Returns:
            str: Markdown formatted bullet list, or "- (none)" if list is empty
        """
        return "\n".join(f"- {x}" for x in items) if items else "- (none)"

    return f"""# {prd.title}

## Problem
{prd.problem}

## Target users
{bullets(prd.target_users)}

## Goals
{bullets(prd.goals)}

## Non-goals
{bullets(prd.non_goals)}

## User stories
{bullets(prd.user_stories)}

## Functional requirements
{bullets(prd.functional_requirements)}

## Non-functional requirements
{bullets(prd.nonfunctional_requirements)}

## Risks
{bullets(prd.risks)}

## Open questions
{bullets(prd.open_questions)}
"""
