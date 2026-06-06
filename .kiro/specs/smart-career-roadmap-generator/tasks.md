# Implementation Plan: Smart Career Roadmap Generator

## Overview

This plan implements a full-stack application using Next.js (React) for the frontend, Python/FastAPI for the backend API, and PostgreSQL for persistence. AI capabilities are accessed through a provider-agnostic abstraction layer. Implementation follows: infrastructure setup → AI provider abstraction → core domain services → progress tracking → frontend.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - [x] 1.1 Initialize project with Python/FastAPI backend and Next.js frontend
    - Create monorepo structure with `frontend/` and `backend/` directories
    - Set up Python project with `pyproject.toml` (or `requirements.txt`) using FastAPI, Uvicorn, SQLAlchemy, Pydantic, Alembic
    - Configure frontend with TypeScript, ESLint, and Prettier
    - Set up pytest and Hypothesis testing frameworks for the backend
    - Configure PostgreSQL connection using SQLAlchemy async (with asyncpg driver)
    - Set up virtual environment and dependency management (e.g., Poetry or pip-tools)
    - _Requirements: All_

  - [x] 1.2 Define Pydantic models, domain types, and enums
    - Create shared Pydantic models for `ProficiencyLevel`, `SkillGap`, `WeeklyPlan`, `InterviewQuestion`, etc.
    - Define all service Protocol interfaces as specified in the design document
    - Define error code constants and error response models
    - _Requirements: All_

  - [x] 1.3 Create database schema and migrations with SQLAlchemy + Alembic
    - Define all SQLAlchemy ORM models: User, Profile, Skill, TargetRole, SkillRequirement, SkillGapAnalysis, SkillGap, LearningRoadmap, RoadmapTopic, LearningResource, WeeklyPlan, WeeklyTask, ProjectSuggestion, InterviewSession, InterviewQuestion, AnswerSubmission
    - Set up foreign key relationships and constraints as per the ER diagram
    - Add data constraints (max lengths, value ranges, array count limits) using SQLAlchemy column constraints
    - Create initial Alembic migration
    - _Requirements: All_

  - [x] 1.4 Implement API layer with FastAPI router, authentication middleware, and Pydantic validation
    - Set up FastAPI application with APIRouter groups for each domain
    - Implement Pydantic request/response models for automatic input validation
    - Set up authentication dependency (JWT-based) using FastAPI `Depends`
    - Implement custom exception handlers for domain-specific errors
    - Configure CORS middleware for frontend communication
    - _Requirements: All_

- [ ] 2. Implement AI Provider Abstraction
  - [ ] 2.1 Implement AI Provider abstraction layer
    - Create provider Protocol with methods: analyze_resume, identify_role_skills, analyze_skill_gaps, generate_roadmap, generate_interview_questions, evaluate_interview_answer, suggest_projects
    - Implement at least one concrete provider (e.g., OpenAI using `openai` Python SDK)
    - Add retry logic (up to 3 retries with exponential backoff) using `tenacity` for transient failures
    - Handle timeouts (AI_TIMEOUT), unavailability (AI_UNAVAILABLE), and malformed responses (AI_RESPONSE_ERROR)
    - Use `httpx` or `aiohttp` for async HTTP calls to AI providers
    - _Requirements: 1.2, 2.2, 3.1, 4.1, 6.1, 6.5, 7.1_

- [ ] 3. Implement Profile Service and Resume Analyzer
  - [ ] 3.1 Implement Profile Service (create_profile, update_profile, get_profile, is_profile_complete)
    - Validate job title (1-100 chars), years of experience (0-50), skills (1-50 items, each name 1-60 chars) via Pydantic models
    - Return appropriate error codes for invalid input (`JOB_TITLE_TOO_LONG`, `INVALID_EXPERIENCE`, `INVALID_SKILL_COUNT`, `SKILL_NAME_TOO_LONG`)
    - Implement `is_profile_complete` returning true only when job title is non-empty AND at least one skill exists
    - _Requirements: 1.1, 1.7_

  - [ ]* 3.2 Write property tests for Profile Service
    - **Property 1: Profile Input Validation**
    - **Property 2: Profile Completeness Check**
    - Use Hypothesis strategies: `st.text()`, `st.integers()`, `st.lists(st.builds(Skill))`
    - **Validates: Requirements 1.1, 1.7**

  - [ ] 3.3 Implement Resume Analyzer Service (analyze_resume, validate_file_format, get_supported_formats)
    - Validate file format (PDF, DOCX, plain text) and size (≤ 5 MB)
    - Return `UNSUPPORTED_FORMAT` or `FILE_TOO_LARGE` errors for invalid files
    - Call AI provider to extract skills, job history, and years of experience
    - Return `EXTRACTION_FAILED` if AI extraction fails
    - Use `python-docx` for DOCX parsing, `PyPDF2`/`pdfplumber` for PDF parsing
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ]* 3.4 Write property test for File Upload Validation
    - **Property 3: File Upload Validation**
    - Use Hypothesis strategies: `st.binary()`, `st.sampled_from(mime_types)`
    - **Validates: Requirements 1.4, 1.5**

  - [ ] 3.5 Implement Profile API endpoints
    - POST `/api/profile` - create profile
    - PUT `/api/profile` - update profile
    - GET `/api/profile` - get current user's profile
    - POST `/api/profile/resume` - upload and analyze resume (using `UploadFile` from FastAPI)
    - Return extracted data for user confirmation before saving
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [ ] 4. Implement Target Role Service
  - [ ] 4.1 Implement Target Role Service (set_target_role, get_target_role_requirements, update_target_role_skills, is_role_recognized, set_custom_role)
    - Validate role title (1-100 chars)
    - For recognized roles, query AI provider to return at least 5 skills/competencies
    - Allow users to add/remove/modify skills in the target role requirements
    - For unrecognized roles, require at least 3 skills and a non-empty responsibilities description
    - Use user-provided info as target role requirements for unrecognized roles
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ]* 4.2 Write property tests for Target Role Service
    - **Property 4: Target Role Title Validation**
    - **Property 5: Recognized Role Skill Count**
    - **Property 6: Custom Role Validation**
    - Use Hypothesis strategies: `st.text()`, `st.lists(st.builds(SkillRequirement))`
    - **Validates: Requirements 2.1, 2.2, 2.4**

  - [ ] 4.3 Implement Target Role API endpoints
    - POST `/api/target-role` - set target role
    - GET `/api/target-role/requirements` - get role requirements
    - PUT `/api/target-role/skills` - update role skills
    - POST `/api/target-role/custom` - set custom role for unrecognized titles
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 5. Implement Skill Gap Analyzer Service
  - [ ] 5.1 Implement Skill Gap Analyzer Service (analyze_gaps)
    - Compare user's current skills against target role requirements
    - Categorize each gap as critical, important, or nice-to-have
    - Assign proficiency levels (beginner, intermediate, advanced) to existing skills relative to target
    - If all requirements met, suggest at least 3 advanced specialization areas
    - Check prerequisite: profile must be complete and target role must be selected
    - Raise `IncompleteProfileError` or `NoTargetRoleError` for missing prerequisites
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ]* 5.2 Write property tests for Skill Gap Analyzer
    - **Property 7: Skill Gap Analysis Completeness**
    - **Property 8: Skill Gap Grouping Correctness**
    - Use Hypothesis strategies: `st.lists(st.builds(Skill))`, `st.lists(st.builds(SkillRequirement))`
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

  - [ ] 5.3 Implement Skill Gap Analysis API endpoint
    - POST `/api/skill-gap/analyze` - run skill gap analysis
    - GET `/api/skill-gap/results` - get latest analysis results grouped by category
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 6. Checkpoint - Ensure all tests pass
  - Run `pytest` to ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement Roadmap Generator Service
  - [ ] 7.1 Implement Roadmap Generator Service (generate_roadmap, recalculate_timeline)
    - Order topics so prerequisites appear before dependent topics
    - Prioritize critical gaps over important over nice-to-have at the same dependency level
    - Estimate total duration: ceiling(total estimated hours / weekly study hours)
    - Default to 10 weekly study hours if user hasn't specified
    - Include at least 2 learning resources per topic (type from: course, book, tutorial, documentation)
    - Validate weekly study hours (1-40); reject invalid values with `INVALID_WEEKLY_HOURS`
    - Recalculate timeline proportionally when weekly hours change
    - Check prerequisite: gap analysis must exist; raise `NoGapAnalysisError` if missing
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 7.2 Write property tests for Roadmap Generator
    - **Property 9: Roadmap Prerequisite Ordering**
    - **Property 10: Roadmap Duration Calculation**
    - **Property 11: Roadmap Resource Minimum**
    - **Property 12: Weekly Study Hours Validation**
    - Use custom Hypothesis strategies for DAG generation
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**

  - [ ] 7.3 Implement Roadmap API endpoints
    - POST `/api/roadmap/generate` - generate learning roadmap
    - GET `/api/roadmap` - get current roadmap
    - PUT `/api/roadmap/hours` - update weekly study hours and recalculate
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [ ] 8. Implement Weekly Plan Service
  - [ ] 8.1 Implement Weekly Plan Service (generate_weekly_plans, mark_task_complete, advance_to_next_plan, adjust_for_delay)
    - Break roadmap into weekly plans with 3-7 tasks each
    - Ensure task hours sum ≤ user's weekly study hours
    - Each task has description, estimated hours, skill name, and completion criterion (observable outcome)
    - Mark tasks complete; when all tasks done, advance to next plan
    - Notify user when week ends with incomplete tasks and offer adjustment
    - When final plan completed, indicate roadmap finished and show skills acquired summary
    - Mark certain plans as practical milestones for project suggestions
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ]* 8.2 Write property tests for Weekly Plan Service
    - **Property 13: Weekly Plan Structural Validity**
    - **Property 14: Plan Advancement on Completion**
    - Use Hypothesis strategies: `st.builds(LearningRoadmap)`, custom plan strategies
    - **Validates: Requirements 5.1, 5.2, 5.4**

  - [ ] 8.3 Implement Weekly Plan API endpoints
    - GET `/api/weekly-plans` - get all plans for current roadmap
    - GET `/api/weekly-plans/current` - get current active plan
    - PUT `/api/weekly-plans/{plan_id}/tasks/{task_id}/complete` - mark task complete
    - POST `/api/weekly-plans/adjust` - adjust remaining plans for delay
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 9. Implement Interview Preparer Service
  - [ ] 9.1 Implement Interview Preparer Service (generate_questions, evaluate_answer)
    - Generate 5-20 questions relevant to the target role
    - Categorize questions: technical, behavioral, system-design
    - Include at least one question per applicable category
    - Assign difficulty based on user progress: <33% → beginner, 33-66% → intermediate, ≥66% → advanced
    - If target role doesn't involve system design, omit that category
    - Provide model answer and evaluation criteria for each question
    - Evaluate user answers by comparing against criteria, identifying strengths and areas for improvement
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

  - [ ]* 9.2 Write property tests for Interview Preparer
    - **Property 15: Interview Question Set Validity**
    - **Property 16: Interview Difficulty Matches Progress**
    - **Property 17: System Design Category Omission**
    - Use Hypothesis strategies: `st.builds(TargetRole)`, `st.integers(min_value=0, max_value=100)`
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.6**

  - [ ] 9.3 Implement Interview Preparer API endpoints
    - POST `/api/interview/generate` - generate mock interview questions
    - GET `/api/interview/sessions/{session_id}` - get interview session with questions
    - POST `/api/interview/questions/{question_id}/answer` - submit answer for evaluation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [ ] 10. Implement Project Suggester Service
  - [ ] 10.1 Implement Project Suggester Service (suggest_projects, mark_project_completed)
    - Suggest at least 2 projects when a practical milestone is completed
    - Each project includes: objectives, deliverables, technologies, estimated weeks (1-4), complexity
    - Align complexity with user skill level (beginner = single concept, advanced = multiple concepts)
    - Allow marking projects complete with outcome description (max 500 chars)
    - Allow user to dismiss all projects and proceed without completing one
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ]* 10.2 Write property tests for Project Suggester
    - **Property 18: Project Suggestion Validity**
    - **Property 19: Project Outcome Validation**
    - Use Hypothesis strategies: `st.builds(WeeklyPlan)`, `st.text(min_size=0, max_size=1000)`
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

  - [ ] 10.3 Implement Project Suggester API endpoints
    - GET `/api/projects/suggestions/{plan_id}` - get project suggestions for a milestone
    - PUT `/api/projects/{project_id}/complete` - mark project complete with outcome
    - PUT `/api/projects/{project_id}/dismiss` - dismiss a project suggestion
    - POST `/api/projects/skip/{plan_id}` - skip all projects for a milestone
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 11. Checkpoint - Ensure all tests pass
  - Run `pytest` to ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement Progress Tracking Service
  - [ ] 12.1 Implement Progress Tracking Service (get_overall_progress, update_skill_proficiency, get_timeline)
    - Calculate progress: floor(completed_plans / total_plans × 100) as integer 0-100
    - Update skill proficiency levels when a weekly plan is completed
    - Provide timeline showing each plan's status (completed, in-progress, upcoming)
    - Notify user when a skill gap milestone is fully achieved
    - Update progress and timeline when roadmap is recalculated due to hours change
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ]* 12.2 Write property tests for Progress Tracking
    - **Property 20: Progress Tracking Correctness**
    - **Property 21: Skill Proficiency Update on Plan Completion**
    - Use Hypothesis strategies: `st.integers(min_value=0)`, `st.builds(WeeklyPlan)`
    - **Validates: Requirements 8.1, 8.2, 8.4, 8.5**

  - [ ] 12.3 Implement Progress Tracking API endpoints and internal event bus
    - GET `/api/progress` - get overall progress summary
    - GET `/api/progress/timeline` - get visual timeline data
    - Set up internal event system (using Python signals/callbacks or a lightweight event bus library) to trigger proficiency updates and notifications on plan/task completion events
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 13. Backend checkpoint - Ensure all backend tests pass
  - Run `pytest` to ensure all backend tests pass, ask the user if questions arise.

- [ ] 14. Implement Frontend
  - [ ] 14.1 Build Profile Creation and Resume Upload UI
    - Form for job title, years of experience, skills input
    - Resume upload with drag-and-drop, format validation feedback, and progress indicator
    - Display extracted resume data for user confirmation/editing
    - Show appropriate error messages for validation failures and extraction errors
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [ ] 14.2 Build Target Role Selection UI
    - Role title input with display of associated skills/competencies
    - Allow adding, removing, modifying skills in the requirements list
    - Handle unrecognized role flow: prompt for skills (min 3) and responsibilities
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 14.3 Build Skill Gap Analysis Results UI
    - Display gaps grouped by category (critical, important, nice-to-have)
    - Show skill name, category, and current proficiency for each gap
    - Handle case where all requirements are met (show specialization suggestions)
    - Show error guidance if prerequisites are missing
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ] 14.4 Build Learning Roadmap and Weekly Plans UI
    - Display ordered roadmap topics with resources
    - Weekly study hours input (1-40) with recalculation on change
    - Weekly plan view with tasks, completion criteria, and check-off functionality
    - Visual timeline showing plan statuses (completed, in-progress, upcoming)
    - Delay adjustment prompt and roadmap completion summary
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ] 14.5 Build Interview Prep and Project Suggestions UI
    - Interview question display with category and difficulty badges
    - Answer submission form with feedback display (strengths, areas for improvement)
    - Project suggestion cards with objectives, deliverables, technologies, and estimated time
    - Mark project complete with outcome text input (max 500 chars)
    - Dismiss/skip project options
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ] 14.6 Build Progress Dashboard UI
    - Overall progress percentage display
    - Visual timeline of weekly plans with status indicators
    - Skills acquired list and milestone notifications
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 15. Final checkpoint - Ensure all tests pass
  - Run `pytest` for backend and frontend test runner for frontend. Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document using Hypothesis
- Unit tests validate specific examples and edge cases using pytest
- The AI provider abstraction (task 2) is implemented early since all domain services depend on it
- The internal event bus decouples progress tracking from plan/task completion logic
- Key Python backend packages: FastAPI, Uvicorn, SQLAlchemy (async), Alembic, Pydantic, Hypothesis, pytest, tenacity, httpx, python-jose (JWT), passlib (password hashing)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["1.4", "2.1"] },
    { "id": 3, "tasks": ["3.1", "4.1"] },
    { "id": 4, "tasks": ["3.2", "3.3", "4.2", "5.1"] },
    { "id": 5, "tasks": ["3.4", "3.5", "4.3", "5.2", "5.3"] },
    { "id": 6, "tasks": ["7.1"] },
    { "id": 7, "tasks": ["7.2", "7.3", "8.1"] },
    { "id": 8, "tasks": ["8.2", "8.3", "9.1", "10.1"] },
    { "id": 9, "tasks": ["9.2", "9.3", "10.2", "10.3"] },
    { "id": 10, "tasks": ["12.1"] },
    { "id": 11, "tasks": ["12.2", "12.3"] },
    { "id": 12, "tasks": ["14.1", "14.2", "14.3"] },
    { "id": 13, "tasks": ["14.4", "14.5", "14.6"] }
  ]
}
```
