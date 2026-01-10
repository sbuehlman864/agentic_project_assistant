# Syllabus-to-Weekly Plan Planner

## Problem
Students struggle to convert course syllabi into actionable weekly study plans. They need a lightweight, MVP-grade web app that can accept syllabus text, produce per-course weekly plans aligned to their available study hours, and track progress locally without external integrations.

## Target users
- College students (undergraduates) seeking structured study plans
- Students juggling multiple courses who need a weekly roadmap

## Goals
- Convert syllabus text into weekly, course-specific study plans
- Allow users to define weekly availability per course and generate feasible plans
- Provide a simple, browsable view of weekly tasks per course across the semester
- Track progress locally (task completion) and display completion metrics
- Deliver a demoable MVP within 2 weeks that runs entirely in the browser
- Avoid any external integrations or server dependencies in v1
- Persist user data locally (in-browser) between sessions

## Non-goals
- Calendar integrations (Google/ICS) or external syncing
- Server-side hosting or multi-user authentication
- Advanced analytics or predictive scheduling beyond simple hour-based allocation
- LMS integrations, assignment submission tracking, or grade calculations
- Mobile app edition or iOS/Android-native features

## User stories
- As a student, I want to paste a syllabus text for a course so the app can extract topics and create a plan scaffold.
- As a student, I want to add multiple courses with names and their total weeks, so I can plan across a semester.
- As a student, I want to specify my weekly study hours per course, so tasks are allocated to realistic time blocks.
- As a student, I want the app to generate a week-by-week plan for each course based on topics and available hours.
- As a student, I want to view a dashboard that shows weekly tasks for each course in a single glance.
- As a student, I want to mark tasks as completed and see progress percentages to stay motivated.
- As a student, I want to edit or reallocate tasks when my schedule changes, without losing data.
- As a student, I want to export or print my current weekly plan for offline reference.
- As a student, I want my data saved locally so it persists across browser sessions.

## Functional requirements
- Allow per-course setup: course name, number of weeks, and optional syllabus text input
- Accept syllabus text input for each course and perform lightweight parsing to extract topics or modules
- Provide a planning engine that assigns topics to weeks based on user-entered weekly hours and a simple rule set
- Offer an editable weekly view where users can adjust tasks, estimated hours, and week assignment
- Provide progress tracking: mark tasks complete, calculate completion rate per course and overall
- Implement local data persistence using browser storage (localStorage or equivalent) with data schema for courses, weeks, tasks, and progress
- Present an overview dashboard and per-course weekly breakdown views in a responsive UI
- Support data export (JSON or printable text) and data import for restoration
- Operate entirely client-side with no external network requests or integrations

## Non-functional requirements
- Performance: initial plan generation should complete within a few seconds on a modern browser
- Reliability: works offline and persists data across sessions without server interaction
- Usability: simple, clean UI with intuitive onboarding and minimal learning curve
- Accessibility: keyboard-navigable controls and proper ARIA labels; color contrasts for readability
- Compatibility: supported in major desktop browsers (Chrome, Firefox, Safari, Edge) with responsive layout
- Security/Privacy: no data leaves the user’s device; clearly communicate local storage usage

## Risks
- Syllabus parsing accuracy: heterogeneity of syllabus formats may hinder automatic topic extraction
- Scope creep: risk of adding features beyond MVP (calendar sync, LMS integration)
- Performance with large syllabi or long-term plans could degrade if not optimized
- User adoption: students may prefer existing tools or require a more guided experience
- Data loss risk if localStorage capacity is exceeded or users clear data unintentionally

## Open questions
- What is the minimum viable syllabus parsing approach (manual mapping vs. auto-extraction) and how will users correct parsing errors?
- How many weeks should the MVP assume by default, and how should it handle non-standard semester lengths (14 vs 15 weeks)?
- What rules will the planning engine use to allocate topics to weeks (e.g., even distribution, priority-based, or time-block based)?
- Should the export format include a human-readable printable view, or only machine-friendly JSON, or both?
- How will the UI scale when handling 2-4 courses simultaneously, and is a per-course toggle preferred for initial MVP?
- What accessibility and localization considerations should be included from the start (labels, date formats, etc.)?
