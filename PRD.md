# Syllabus-to-Weekly Plan Builder for College Students

## Problem
College students receive syllabi that describe courses, deadlines, and milestones but struggle to transform them into actionable, weekly study plans. Current solutions are often generic planning tools or require backend services; there is a need for a lightweight, offline-capable MVP that translates syllabus structure into a weekly plan and tracks progress without external dependencies.

## Target users
- College students (undergraduate) who want to translate syllabi into weekly tasks
- Students who struggle with time management and consistent planning
- Individuals seeking a lightweight, offline-capable planning tool aligned with course requirements

## Goals
- Provide a solo-developed web app that converts class syllabi into structured weekly study plans and tracks progress
- Operate offline with client-side persistence (localStorage) and no backend for MVP
- Auto-generate a weekly plan from common syllabus structures (weeks, modules, assignments, exam dates)
- Support manual adjustments: add/edit/delete tasks, reweight tasks, and set milestones
- Offer a simple, printable/text-exportable view of the weekly plan for sharing or offline use
- Deliver a demoable, local MVP in 2 weeks

## Non-goals
- Backend/server infrastructure or cloud storage
- Real-time collaboration or multi-user accounts
- Calendar integrations (Google Calendar, Outlook) in v1
- Advanced AI-powered syllabus parsing beyond basic pattern recognition
- Support for complex multi-course dashboards in MVP
- Automatic import of PDFs or images without user action

## User stories
- As a student, I want to paste or upload my syllabus and have the app extract weeks, modules, assignments, and exam dates into a weekly plan, so I don’t have to manually re-create the structure.
- As a student, I want to view a weekly plan that groups tasks by week and highlights upcoming milestones, so I can focus on what’s due this week.
- As a student, I want to add, edit, delete, and re-order tasks within each week, so I can tailor the plan to my actual study flow.
- As a student, I want to mark tasks as complete and see a progress indicator (per week and overall), so I stay motivated and aware of progress.
- As a student, I want my plan to be saved locally in the browser so I can reopen it offline and continue planning after closing the tab.
- As a student, I want to reset or delete my data easily if I want to start over with a new syllabus.
- As a student, I want to export the current plan as a simple text/JSON format for printing or sharing with peers, so I can reference it outside the app.
- As a student, I want to create a plan manually from scratch when no syllabus is provided, so I still have a usable workflow.

## Functional requirements
- Ingest syllabus content via paste or file upload and parse common structures (weeks, modules, assignments, exam dates) into a structured weekly plan
- Automatically generate a weekly plan view from the parsed syllabus data, with sections for each week and associated milestones
- Provide task management within each week: create, edit, delete, and reorder tasks; assign due dates and milestones
- Allow marking tasks as complete and compute per-week and overall completion rates
- Persist all user data locally using browser localStorage with automatic load on app start and data recovery on refresh
- Ensure offline-first operation: all features function without internet connectivity
- Offer data export options (JSON or plain text) and an import option to restore from a previously exported file
- Provide accessible keyboard navigation and study-friendly UI with clear affordances

## Non-functional requirements
- Performance: generating a weekly plan from a typical syllabus should complete within 2 seconds on modern devices
- Reliability: data stored in localStorage should survive page reloads and browser restarts until the user clears it
- Security/Privacy: no network calls or data sharing by default; all data remains on the user’s device
- Compatibility: works on major modern browsers (Chrome, Firefox, Edge, Safari) with responsive UI for desktop and tablets
- Usability: intuitive onboarding and minimal steps to go from syllabus input to a usable weekly plan
- Accessibility: comply with basic WCAG 2.1 AA guidelines for keyboard navigation and screen reader compatibility

## Risks
- Syllabus parsing may be brittle due to diverse formatting; heavy reliance on pattern matching could yield incomplete plans
- Two-week MVP scope may be tight for implementing robust parsing and a polished UI
- Single-developer constraint increases risk of feature creep or delays; prioritization is critical
- Data loss risk if users clear localStorage or switch browsers; need clear UX for backups/export
- Limited offline testing on all devices could surface edge-case UI issues

## Open questions
- What level of parsing fidelity should we target for syllabi (basic pattern recognition vs. robust extraction)?
- Should the MVP support multiple syllabi/projects within one app instance, or focus on a single syllabus per plan?
- What export formats are most valuable: JSON for re-import, or printable plain text for sharing?
- Is basic template support desired (e.g., semester templates) to speed up plan creation for new courses?
- Will there be a need for reminder or notification features (e.g., due date reminders) in MVP or later release?
- How should we handle inconsistent or missing dates (e.g., no explicit exam date) in the syllabus?
