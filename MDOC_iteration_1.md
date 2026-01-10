# Syllabus to Weekly Study Planner - Milestones (MVP)

## M1. Foundation and Offline Scaffolding
**Objective:** Establish project skeleton, offline-first data model, and core import plus initial 4-week plan generation.
**Estimate:** 7 days
**Deliverables:**
- Project scaffolding and build setup with offline-first capability
- Data model for syllabus, tasks, and progress stored in localStorage/IndexedDB
- Plain-text syllabus import pipeline with basic parsing
- Default 4-week plan generator and initial UI skeleton for weekly view

## M2. Plan Generation, Task Management, and Persistence
**Objective:** Implement task lifecycle, per-week progress tracking, and dynamic plan regeneration when weeks change.
**Estimate:** 12 days
**Deliverables:**
- CRUD for tasks with titles, due dates, and estimated effort
- Weekly progress indicators and per-week task views
- Regeneration on week count changes and autosave to browser storage
- Basic in-app validation and error handling

## M3. Export, Print, and Plan Sharing
**Objective:** Add export in JSON/Markdown, printable view, and ensure offline sharing capability.
**Estimate:** 8 days
**Deliverables:**
- Export to JSON and Markdown formats
- Printable view optimized for offline printing
- Local backup/restore capabilities for saved plans
- Option to reset data to initial state

## M4. UI Polish, Accessibility, and Onboarding
**Objective:** Refine UI for desktop/mobile, accessibility, keyboard navigation, and onboarding plus reset option.
**Estimate:** 6 days
**Deliverables:**
- Responsive weekly overview with clear task lists and progress bars
- Keyboard navigable UI with improved color contrast (WCAG AA baseline)
- Onboarding flow and contextual help
- Clear data reset option and final QA checks
