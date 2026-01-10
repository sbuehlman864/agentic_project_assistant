# Syllabus to Weekly Study Planner

## Problem
Many college syllabi are inconsistent in format and terminology, making it hard for students to translate requirements into actionable weekly tasks. Existing tools require manual planning, are often online-only, and do not meet the MVP constraint of being a demoable, offline-first local web app for a solo developer.

## Target users
- Undergraduate college students
- Students juggling multiple courses
- Self-motivated learners who prefer structured plans

## Goals
- Convert syllabus content into a structured weekly study plan with tasks, due dates, and estimated effort.
- Operate offline-first with data stored locally in the browser (no server required).
- Provide a clear weekly overview and progress tracking for adherence.
- Enable quick MVP generation (default 4 weeks) with the ability to adjust weeks and re-generate.
- Support local export/print options for offline use and sharing.

## Non-goals
- Real-time collaboration or multi-user features
- Cloud sync or LMS integrations in v1
- Advanced analytics or learning insights beyond basic completion metrics
- Complex PDF/image syllabus parsing or OCR in v1
- Mobile app native experiences or push notifications

## User stories
- As a student, I want to paste or paste/upload a syllabus text and have the app create a structured plan, so I don't have to manually interpret the syllabus.
- As a student, I want the app to distribute tasks across weeks by default (4 weeks) with due dates, so I have a ready plan.
- As a student, I want to see a weekly overview with tasks, due dates, and estimated hours, so I can plan my study time.
- As a student, I want to mark tasks as completed and see progress, so I can stay motivated.
- As a student, I want to adjust the number of weeks and re-generate the plan, so I can tailor to my schedule.
- As a student, I want to customize tasks by editing titles, due dates, and estimated effort, so the plan matches my needs.
- As a student, I want to save plans locally and reopen them later without internet, so I can continue offline.
- As a student, I want to export the plan as JSON/Markdown/printable view, so I can share or print.
- As a student, I want a simple, clean UI that works on desktop and mobile, so I can use it anywhere.

## Functional requirements
- Import: Support copy-paste or file upload of plain-text syllabus; parse into a structured syllabus object.
- Plan generation: Generate a weekly plan by distributing syllabus items across weeks (default 4 weeks); allow user to set number of weeks and regenerate.
- Task management: Create, edit, and delete tasks; mark tasks as completed; track per-week and overall progress.
- Editing capabilities: Allow editing of task titles, due dates, and estimated effort; adjust week allocations manually if needed.
- Local storage: Persist syllabus, tasks, and progress to browser storage (localStorage or IndexedDB) with autosave.
- Export/print: Provide options to export the plan as JSON, Markdown, or a printable view; support offline viewing.
- UI/UX: Present a weekly view with clear task lists, progress indicators, and responsive design for desktop and mobile.
- Reset: Provide a clear data reset option to start over from the initial state.

## Non-functional requirements
- Offline-first: All data remains stored and operable entirely in the browser with no server interactions.
- Performance: Generate a 4-week plan from typical syllabi within 2 seconds on standard hardware; scale gracefully with up to ~100 tasks.
- Accessibility: Keyboard navigable, proper semantic structure, and adequate color contrast to meet WCAG 2.1 AA baseline.
- Cross-browser compatibility: Works on modern Chrome, Firefox, Safari, and Edge without relying on vendor-specific APIs.
- Security and privacy: No data is sent to external services; user data is stored locally and never transmitted by default.
- Usability: Minimal onboarding, clear success metrics, and intuitive controls to reduce setup time.

## Risks
- Ambiguity in syllabus formatting may lead to incorrect automatic task extraction or misalignment of weeks.
- LocalStorage quota limits or browser storage clears can result in data loss for users with large syllabi.
- Performance degradation with unusually long or complex syllabi or very large task sets.
- Users may expect features (e.g., calendar integrations) that are outside v1 scope, causing misaligned expectations.
- If parsing relies on heuristic text extraction, edge cases could require manual correction, affecting MVP appeal.

## Open questions
- What is the minimum viable default parsing rule set for common syllabus formats, and should we define a supported template to reduce ambiguity?
- How should we handle estimation of effort for tasks when the syllabus does not specify hours per week?
- Should the app automatically accommodate holidays or term breaks when distributing tasks across weeks?
- Is there value in supporting additional import formats (e.g., CSV or Markdown syllabus templates) in v1 or should we limit to plain text?
- What is the preferred export format for sharing with others (JSON, Markdown, or printable PDF) given MVP constraints?
