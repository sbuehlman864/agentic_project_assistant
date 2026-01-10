# agentic_project_assistant

An intelligent CLI tool that helps you manage and complete projects through AI-powered assistance and automated workflows.

## Overview

This project implements an agentic architecture that autonomously helps manage projects by breaking down tasks, tracking progress, and facilitating completion. The system leverages AI agents to provide intelligent project assistance through a command-line interface.

## Features

- Automated project task decomposition
- Intelligent workflow management
- Progress tracking and reporting
- Agentic decision-making for project optimization
- Interactive CLI with multiple management commands
- Conversation history tracking
- Project state persistence

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentic_project_assistant

# Install dependencies
pip install -r requirements.txt
```

## Usage

The application provides a command-line interface with several commands to manage your projects:

### Starting the Assistant

```bash
python main.py
```

### Available Commands

- **`new`** - Start a new project conversation
- **`continue`** - Resume the most recent project conversation
- **`list`** - View all your project conversations with their IDs and summaries
- **`switch <conversation_id>`** - Switch to a specific conversation by ID
- **`exit`** - Save your work and exit the application

### Example Workflow

```bash
$ python main.py
> new
# Describe your project needs
> "I need to build a REST API for a todo application"

# The assistant will help break down tasks and guide you through implementation
> continue
# Resume your previous session

> list
# See all your projects
```

## What You Get

The agentic_project_assistant provides:

1. **Intelligent Project Planning**: AI agents analyze your requirements and create actionable task breakdowns
2. **Guided Execution**: Step-by-step assistance through project completion with contextual suggestions
3. **Conversation Persistence**: All project discussions are saved and can be resumed anytime
4. **Multi-Project Management**: Switch between different projects seamlessly
5. **Progress Tracking**: Keep track of where you are in each project conversation

## Agentic Workflow

The system uses an agentic workflow pattern where AI agents operate autonomously to achieve goals:

- **Planning**: Agents analyze project requirements and create actionable plans
- **Execution**: Agents perform tasks or delegate to specialized sub-agents
- **Reflection**: Agents evaluate outcomes and adapt strategies
- **Iteration**: Continuous improvement through feedback loops

### Workflow Example

```
User Request → Planning Agent → Task Decomposition
                                          ↓
                          Execution Agents (parallel)
                                 ↓    ↓    ↓
                          [Code] [Test] [Doc]
                                          ↓
                          Review Agent → Quality Check
                                          ↓
                          Integration → Final Output
```

This autonomous approach enables the system to handle complex projects with minimal human intervention while maintaining quality and adaptability.

## Configuration

The application stores conversation history in:
- `conversations/` - Individual conversation files
- `conversation_index.json` - Index of all conversations

## Purpose

The agentic_project_assistant aims to reduce manual overhead in project management by providing an AI-powered assistant that can understand project requirements, suggest action items, and help guide projects to completion through an intuitive command-line interface.
