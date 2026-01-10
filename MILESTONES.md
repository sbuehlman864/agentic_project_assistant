# Milestones for Syllabus to Weekly Planner MVP

## M1. Foundation and data model
**Objective:** Establish the client-side app skeleton, core data models, and persistent storage to support multiple courses and manual syllabus entry.
**Estimate:** 5 days
**Deliverables:**
- Project scaffold and single-page app shell with modular structure
- Data models for Course and SyllabusItem defined in code
- LocalStorage persistence layer with save/load functionality
- Initial UI to create and list courses

## M2. Syllabus entry and week mapping
**Objective:** Enable course creation with syllabus items and map items to calendar weeks to form an initial weekly plan.
**Estimate:** 8 days
**Deliverables:**
- UI forms to add syllabus items (title, week number, due date, description)
- Logic to map syllabus items to weeks and generate weekly plan data
- Validation and error handling for required fields
- Automatic persistence of changes to localStorage

## M3. Weekly planner view and progress tracking
**Objective:** Provide a weekly view of tasks, allow completion tracking, and show progress per course.
**Estimate:** 7 days
**Deliverables:**
- Weekly planner UI displaying tasks grouped by week
- Task completion toggles and per-course progress calculation
- Filter by course to view a specific plan
- Auto-save of progress to localStorage

## M4. Export/Import and duplication features
**Objective:** Allow exporting and importing plans for backup/sharing, and duplicating courses to accelerate setup.
**Estimate:** 6 days
**Deliverables:**
- Export all courses/plans to JSON and CSV formats
- Import from JSON/CSV to restore or upgrade plans
- Duplicate course plan to quickly create a new course with the same structure

## M5. Polish, accessibility, and offline readiness
**Objective:** Improve accessibility, performance, and onboarding to ensure a smooth MVP experience.
**Estimate:** 5 days
**Deliverables:**
- Accessibility improvements: keyboard navigation and ARIA labeling
- Performance tuning to keep initial load fast (target under 2 seconds)
- Onboarding flow or sample demo data to enable quick-start planning
- UI polish and helpful microcopy to guide users
