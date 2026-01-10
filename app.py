# app.py
from __future__ import annotations
import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import streamlit as st

from pipeline import run_pipeline

# Configure Streamlit page settings
st.set_page_config(page_title="Project Starter Agent", page_icon="✅", layout="wide")

# Display logo and title side by side
col1, col2 = st.columns([1, 8])
with col1:
    st.image("Project_Plan_App_Logo.png", width=120)
with col2:
    st.title("Project Starter Agent")
    st.caption("Turn an idea into a PRD, milestones, and an actionable task backlog.")

# Sidebar configuration section
with st.sidebar:
    st.header("Settings")
    # Slider to control how many revision attempts the pipeline will make
    max_attempts = st.slider("Max revision attempts", 1, 5, 3)
    st.divider()
    st.write("Tip: Keep v1 constraints short and concrete.")

# Main input: project idea text area
idea = st.text_area(
    "Project idea",
    height=160,
    placeholder="Example: A tool that helps students turn syllabi into weekly study plans...",
)

# Secondary input: constraints/preferences (multi-line)
constraints_text = st.text_area(
    "Constraints / preferences (one per line)",
    height=140,
    value="Solo developer\nMVP in 2 weeks\nDemoable locally\nNo external integrations in v1",
)

# Parse constraints into a list, filtering out empty lines
constraints = [c.strip() for c in constraints_text.splitlines() if c.strip()]

# Action buttons: Generate and Clear
col1, col2 = st.columns([1, 1])
generate = col1.button("Generate Project Plan", type="primary", use_container_width=True)
clear = col2.button("Clear", use_container_width=True)

# Clear button handler: reset session state and rerun
if clear:
    st.session_state.clear()
    st.rerun()

# Generate button handler: validate input and run the pipeline
if generate:
    if not idea.strip():
        st.error("Please enter a project idea.")
    else:
        # Run the pipeline with a status indicator
        with st.status("Running pipeline…", expanded=False) as status:
            result = run_pipeline(idea=idea, constraints=constraints, max_attempts=max_attempts)
            status.update(label="Done!", state="complete")

        # Store result in session state for persistence
        st.session_state["result"] = result

# Display results if they exist in session state
if "result" in st.session_state:
    result = st.session_state["result"]

    # Display execution time
    duration = result.get("duration_seconds", 0)
    minutes = int(duration // 60)
    seconds = duration % 60
    if minutes > 0:
        time_str = f"{minutes}m {seconds:.1f}s"
    else:
        time_str = f"{seconds:.1f}s"
    st.success(f"✅ Project plan generated in {time_str}")

    # Display validation issues if any remain
    issues = result["issues"]
    remaining = {k: v for k, v in issues.items() if v}
    if remaining:
        st.warning("Some validations still had issues (best-effort output).")
        st.json(remaining)

    # Download buttons for generated artifacts
    st.subheader("Downloads")
    d1, d2, d3 = st.columns(3)
    d1.download_button("Download PRD.md", result["prd_md"], file_name="PRD.md")
    d2.download_button("Download MILESTONES.md", result["milestones_md"], file_name="MILESTONES.md")
    d3.download_button("Download TASKS.csv", result["tasks_csv"], file_name="TASKS.csv")

    st.divider()

    # Add custom CSS for column divider
    st.markdown("""
        <style>
        [data-testid="column"]:first-child {
            border-right: 2px solid #e0e0e0;
            padding-right: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Two-column layout for PRD and Milestones previews
    left, right = st.columns(2)

    with left:
        st.subheader("PRD Preview")
        st.markdown(result["prd_md"])

    with right:
        st.subheader("Milestones Preview")
        st.markdown(result["milestones_md"])

    st.divider()
    
    # Tasks preview section with interactive dataframe
    st.subheader("Tasks Preview")
    
    # Convert tasks to a pandas-friendly format
    import pandas as pd
    tasks_data = []
    for task in result["tasks"].tasks:
        tasks_data.append({
            "Task ID": task.task_id,
            "Title": task.title,
            "Type": task.type,
            "Priority": task.priority,
            "Est. Hours": task.estimate_hours,
            "Dependencies": ", ".join(task.depends_on) if task.depends_on else "",
            "Acceptance Criteria": " | ".join(task.acceptance_criteria),
        })
    
    tasks_df = pd.DataFrame(tasks_data)
    
    # Display as interactive dataframe with horizontal scrolling enabled
    st.dataframe(
        tasks_df,
        hide_index=True,
        height=600,  # Set a fixed height to enable vertical scrolling
        width=2000,  # Set width larger than container to enable horizontal scrolling
        column_config={
            "Task ID": st.column_config.TextColumn("Task ID", width="small"),
            "Title": st.column_config.TextColumn("Title", width="medium"),
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "Est. Hours": st.column_config.NumberColumn("Est. Hours", width="small"),
            "Dependencies": st.column_config.TextColumn("Dependencies", width="medium"),
            "Acceptance Criteria": st.column_config.TextColumn("Acceptance Criteria", width="large"),
        }
    )
    
    # Debug expander with full structured data
    with st.expander("Show full structured JSON (debug)"):
        st.json({
            "goal": result["goal"].model_dump(),
            "prd": result["prd"].model_dump(),
            "milestones": result["milestones"].model_dump(),
            "tasks_sample": [t.model_dump() for t in result["tasks"].tasks[:5]],
        })
