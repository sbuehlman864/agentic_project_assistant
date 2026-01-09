"""
Test script for tools.py functions
"""
import os
from pathlib import Path
from tools import write_markdown, write_csv, append_jsonl_log, render_prd

def test_write_markdown():
    print("Testing write_markdown...")
    test_path = "output/test_markdown.md"
    test_content = "# Test Document\n\nThis is a test markdown file.\n\n## Section 1\nSome content here."
    
    write_markdown(test_path, test_content)
    
    # Verify the file was created
    if os.path.exists(test_path):
        with open(test_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Markdown file created successfully!")
        print(f"   Location: {test_path}")
        print(f"   Content preview: {content[:50]}...")
    else:
        print("❌ Failed to create markdown file")
    print()


def test_write_csv():
    print("Testing write_csv...")
    test_path = "output/test_data.csv"
    test_rows = [
        ["Name", "Age", "City"],
        ["Alice", 25, "New York"],
        ["Bob", 30, "San Francisco"],
        ["Charlie", 35, "Boston"]
    ]
    
    write_csv(test_path, test_rows)
    
    # Verify the file was created
    if os.path.exists(test_path):
        with open(test_path, 'r') as f:
            content = f.read()
        print(f"✅ CSV file created successfully!")
        print(f"   Location: {test_path}")
        print(f"   Content:\n{content}")
    else:
        print("❌ Failed to create CSV file")
    print()


def test_append_jsonl_log():
    print("Testing append_jsonl_log...")
    test_path = "output/test_events.jsonl"
    
    # Remove old test file if it exists
    if os.path.exists(test_path):
        os.remove(test_path)
    
    # Add multiple events
    events = [
        {"timestamp": "2026-01-09T10:00:00", "action": "user_login", "user": "alice", "status": "success"},
        {"timestamp": "2026-01-09T10:05:00", "action": "file_upload", "user": "alice", "filename": "data.csv"},
        {"timestamp": "2026-01-09T10:10:00", "action": "task_complete", "user": "alice", "task_id": 123}
    ]
    
    for event in events:
        append_jsonl_log(event, test_path)
    
    # Verify the file was created
    if os.path.exists(test_path):
        with open(test_path, 'r') as f:
            lines = f.readlines()
        print(f"✅ JSONL log file created successfully!")
        print(f"   Location: {test_path}")
        print(f"   Number of events: {len(lines)}")
        print(f"   Content:")
        for i, line in enumerate(lines, 1):
            print(f"      Event {i}: {line.strip()}")
    else:
        print("❌ Failed to create JSONL log file")
    print()


def test_render_prd():
    print("Testing render_prd...")
    
    test_prd = {
        "title": "Mobile Weather App",
        "overview": "A simple weather app for iOS and Android that provides accurate forecasts.",
        "objectives": [
            "Provide accurate weather forecasts",
            "Support multiple cities",
            "Show 7-day forecast",
            "Display current conditions"
        ],
        "requirements": [
            "Must fetch data from weather API",
            "Must display temperature in Celsius and Fahrenheit",
            "Must cache data for offline use",
            "Must support iOS 14+ and Android 10+"
        ],
        "constraints": [
            "Budget: $50,000",
            "Timeline: 3 months",
            "Team size: 4 developers",
            "Must use React Native"
        ]
    }
    
    rendered = render_prd(test_prd)
    
    print(f"✅ PRD rendered successfully!")
    print(f"   Length: {len(rendered)} characters")
    print(f"   Rendered markdown:\n")
    print("=" * 60)
    print(rendered)
    print("=" * 60)
    
    # Also save it to a file to verify it looks good
    output_path = "output/test_prd.md"
    write_markdown(output_path, rendered)
    print(f"\n   Also saved to: {output_path}")
    print()


def main():
    print("=" * 60)
    print("Testing tools.py functions")
    print("=" * 60)
    print()
    
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    # Run all tests
    test_write_markdown()
    test_write_csv()
    test_append_jsonl_log()
    test_render_prd()
    
    print("=" * 60)
    print("All tests completed! Check the output/ directory for files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
