# Syllabus to Weekly Planner

## Problem
Solo students and developers lack a lightweight tool to convert course syllabi into actionable weekly tasks with progress tracking. Current approaches are manual, error-prone, and hard to reuse across courses, making it difficult to stay organized across multiple classes.

## Target users
- College students juggling multiple courses who want to convert syllabi into weekly tasks and track progress

## Goals
- Convert syllabi into weekly tasks aligned with weeks and due dates
- Provide progress tracking for tasks and weeks
- Operate entirely client-side for quick MVP demos and offline capability
- Enable rapid setup: create the first weekly plan for a course in 15 minutes or less
- Support planning and tracking for at least 2 courses in the demo
- Allow simple export/import of plans for persistence, backup, or sharing

## Non-goals
- No authentication or real-time collaboration in v1
- No external integrations or server-side storage in v1
- No advanced calendar integrations or reminders in v1
- No automatic syllabus parsing from uploaded documents in v1; manual entry only
- No mobile app version in v1

## User stories
- As a student, I want to create a course entry with its name and syllabus structure so I can start planning weeks and tasks.
- As a student, I want to enter syllabus items (title, week number, due date, description) so I can map them to weekly tasks.
- As a student, I want the app to map syllabus items to calendar weeks so I can see a coherent weekly plan.
- As a student, I want to view a weekly plan that shows all tasks due in that week, so I can focus my work.
- As a student, I want to mark tasks as completed, so I can track my progress toward course goals.
- As a student, I want to store data locally in the browser, so I can reopen the plan later without a server.
- As a student, I want to export my plan to JSON or CSV, so I can back up or share it with others.
- As a student, I want to import a previously exported plan, so I can move between devices or restore a demo.

## Functional requirements
- FR1: The app runs entirely in the browser with client-side rendering and uses localStorage for persistence
- FR2: Users can create multiple courses, each with a name and optional start date or week mapping
- FR3: Users can add syllabus items by entering title, week number, due date, and description
- FR4: The system automatically maps syllabus items to their corresponding weeks and aggregates them into weekly plans
- FR5: A weekly planner view lists tasks by week and allows filtering by course
- FR6: Users can mark individual tasks as complete or incomplete and view completion progress per course
- FR7: Data is saved automatically to localStorage on changes and restored on page load
- FR8: Provide export functionality to JSON or CSV for all stored courses and plans
- FR9: Provide import functionality to load a previously exported JSON/CSV plan
- FR10: Support duplicating a course plan to quickly create a new course with the same structure

## Non-functional requirements
- NFR1: Performance: initial load and render of a course plan should complete within 2 seconds on modern desktop browsers
- NFR2: Reliability: data persists across reloads and browser sessions unless the user clears localStorage
- NFR3: Accessibility: keyboard navigable, screen-reader friendly, with clear focus indicators and aria labels
- NFR4: Compatibility: should work on major desktop browsers (Chrome, Firefox, Edge, Safari) and adapt to common screen sizes
- NFR5: Usability: intuitive, minimal UI with a simple workflow to create a course and its first weekly plan within minutes
- NFR6: Privacy: no data is transmitted to servers; all data remains in the local browser unless exported

## Risks
- R1: Low adoption due to perceived complexity of entering syllabi and planning manually
- R2: Data loss risk if users clear their browser storage or use a private/incognito window
- R3: Variability in syllabus formats may require additional UX hooks to map items accurately
- R4: Performance or UX issues with large syllabi or many courses in the MVP
- R5: No real-time collaboration may limit usefulness for group projects or shared courses

## Open questions
- Q1: How should breaks, holidays, or non-teaching weeks be represented in the weekly mapping?
- Q2: Should the tool support templates or import from common syllabus formats to reduce manual entry in v1?
- Q3: What export formats are preferred (JSON vs CSV) and should there be a dedicated import schema to handle updates to existing courses?
- Q4: How to handle multiple courses with overlapping weeks in the weekly view for clarity?
- Q5: Is there value in adding lightweight analytics (e.g., percent complete per week) without requiring authentication?
