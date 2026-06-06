# Requirements Document

## Introduction

The Smart Career Roadmap Generator is a platform that helps users identify the exact skills, knowledge, and experience they need to transition from their current role to a target role. The system analyzes the user's current profile (including resume and experience), compares it against target role requirements, and generates a personalized learning roadmap with weekly plans, project suggestions, and mock interview questions. AI is used for resume analysis, roadmap generation, and interview preparation.

## Glossary

- **Platform**: The Smart Career Roadmap Generator application
- **User**: A person using the Platform to plan their career progression
- **Profile**: A collection of information about the User including current role, years of experience, skills, and optionally a resume
- **Target_Role**: The desired career position the User wants to achieve
- **Skill_Gap_Analyzer**: The component that compares User skills against Target_Role requirements and identifies missing competencies
- **Roadmap_Generator**: The component that creates a structured learning path based on identified skill gaps
- **Weekly_Plan**: A time-bound set of learning activities and milestones for a single week
- **Learning_Roadmap**: An ordered sequence of Weekly_Plans forming a complete path from current skills to Target_Role readiness
- **Interview_Preparer**: The component that generates mock interview questions relevant to the Target_Role
- **Project_Suggester**: The component that recommends hands-on projects to build Target_Role competencies
- **Resume_Analyzer**: The AI component that extracts skills, experience, and competencies from an uploaded resume document
- **Skill**: A specific technical or soft competency (e.g., "distributed systems", "system design", "leadership")

## Requirements

### Requirement 1: User Profile Creation

**User Story:** As a User, I want to create my profile with current role information, so that the Platform can understand my starting point.

#### Acceptance Criteria

1. THE Platform SHALL allow the User to input their current job title (maximum 100 characters), years of experience (integer from 0 to 50), and known skills (between 1 and 50 skills, each skill name maximum 60 characters)
2. WHEN a User uploads a resume document, THE Resume_Analyzer SHALL extract skills, job history, and years of experience from the document
3. WHEN the Resume_Analyzer completes extraction, THE Platform SHALL present all extracted information (including partial or empty results) to the User for confirmation or editing before saving to the Profile
4. IF a resume document is in an unsupported format, THEN THE Platform SHALL inform the User of supported formats and request a new upload
5. THE Platform SHALL support resume uploads in PDF, DOCX, and plain text formats with a maximum file size of 5 MB
6. IF the Resume_Analyzer fails to extract information from a supported-format document, THEN THE Platform SHALL display an error message indicating extraction failure and allow the User to re-upload or enter profile information manually
7. THE Platform SHALL require the User to provide at least a current job title and one known skill before the Profile is considered complete

### Requirement 2: Target Role Selection

**User Story:** As a User, I want to specify my target role, so that the Platform can determine what I need to learn.

#### Acceptance Criteria

1. THE Platform SHALL allow the User to specify a Target_Role by entering a role title of 1 to 100 characters
2. WHEN a User specifies a Target_Role, THE Platform SHALL display at least 5 skills and competencies associated with that Target_Role
3. THE Platform SHALL allow the User to add, remove, or modify individual skills and competencies in the displayed Target_Role requirements to match a specific job description
4. IF a Target_Role is not recognized by the Platform, THEN THE Platform SHALL prompt the User to provide at least 3 skills and a brief description of the role's responsibilities before proceeding
5. WHEN a User provides skills and responsibilities for an unrecognized Target_Role, THE Platform SHALL use the user-provided information as the Target_Role requirements for subsequent skill gap analysis

### Requirement 3: Skill Gap Analysis

**User Story:** As a User, I want to see which skills I'm missing for my target role, so that I know exactly what to focus on.

#### Acceptance Criteria

1. WHEN a User has a completed Profile and a selected Target_Role, THE Skill_Gap_Analyzer SHALL compare the User's current skills against the Target_Role requirements and produce a list of missing or insufficient skills
2. THE Skill_Gap_Analyzer SHALL categorize each identified gap as critical, important, or nice-to-have based on the Target_Role requirements
3. THE Skill_Gap_Analyzer SHALL assign a proficiency level (beginner, intermediate, advanced) to each of the User's existing skills relative to the Target_Role expectations
4. WHEN the analysis is complete, THE Platform SHALL display the skill gaps grouped by category (critical, important, nice-to-have), showing for each gap the skill name, assigned category, and current proficiency level
5. IF the User's current skills already meet all Target_Role requirements, THEN THE Platform SHALL inform the User and suggest at least 3 advanced specialization areas related to the Target_Role
6. IF any prerequisite for skill gap analysis is missing (including but not limited to incomplete Profile or unselected Target_Role), THEN THE Platform SHALL display an error message indicating each missing prerequisite and guide the User to complete it

### Requirement 4: Learning Roadmap Generation

**User Story:** As a User, I want a structured learning path, so that I know the order in which to acquire missing skills.

#### Acceptance Criteria

1. WHEN a skill gap analysis is complete, THE Roadmap_Generator SHALL create a Learning_Roadmap with an ordered sequence of topics where prerequisite topics appear before topics that depend on them, and topics addressing critical skill gaps are prioritized over important and nice-to-have gaps
2. THE Roadmap_Generator SHALL estimate a total duration for the Learning_Roadmap in weeks, based on the number of skill gaps and their required proficiency level (beginner topics estimated shorter than advanced topics), assuming a default of 10 weekly study hours if the User has not specified availability
3. THE Roadmap_Generator SHALL include at least 2 recommended learning resources (from among courses, books, tutorials, or documentation) for each topic in the Learning_Roadmap
4. THE Platform SHALL allow the User to specify available weekly study hours between 1 and 40 hours to calibrate the Learning_Roadmap timeline
5. WHEN the User adjusts available weekly study hours, THE Roadmap_Generator SHALL recalculate the Learning_Roadmap timeline proportionally and display the updated total duration in weeks
6. IF the User enters weekly study hours outside the range of 1 to 40, THEN THE Platform SHALL display an error message indicating the valid range and, independently, retain the previously specified value if one exists

### Requirement 5: Weekly Plan Generation

**User Story:** As a User, I want weekly plans with specific tasks, so that I can make consistent progress toward my target role.

#### Acceptance Criteria

1. WHEN a Learning_Roadmap is generated, THE Platform SHALL break it down into Weekly_Plans, each containing 3 to 7 tasks, where each task includes a description, an estimated duration in hours, and the associated skill being developed, and the total estimated duration of tasks within a Weekly_Plan SHALL NOT exceed the User's declared available weekly study hours
2. THE Platform SHALL include a completion criterion for each task within a Weekly_Plan, stated as an observable outcome or deliverable that the User can verify as done or not done
3. THE Platform SHALL allow the User to mark tasks as complete within a Weekly_Plan
4. WHEN a User marks all tasks in a Weekly_Plan as complete, THE Platform SHALL advance the User to the next Weekly_Plan in the Learning_Roadmap sequence
5. WHEN a Weekly_Plan's assigned calendar week ends, THE Platform SHALL notify the User and offer to adjust the remaining Weekly_Plans to accommodate any delay, regardless of task completion status
6. WHEN a User marks all tasks in the final Weekly_Plan of the Learning_Roadmap as complete, THE Platform SHALL indicate that the Learning_Roadmap is finished and present a summary of all skills acquired

### Requirement 6: Mock Interview Questions

**User Story:** As a User, I want practice interview questions for my target role, so that I can prepare for real interviews.

#### Acceptance Criteria

1. WHEN a User requests interview preparation, THE Interview_Preparer SHALL generate between 5 and 20 mock interview questions relevant to the Target_Role's required skills and competencies
2. THE Interview_Preparer SHALL categorize questions by type: technical, behavioral, and system design, and SHALL include at least one question from each category applicable to the Target_Role
3. THE Interview_Preparer SHALL provide for each generated question a model answer and a list of evaluation criteria specifying the key points a complete answer should address
4. THE Interview_Preparer SHALL assign each question a difficulty level of beginner, intermediate, or advanced, matching the difficulty to the User's current progress through the Learning_Roadmap such that Users in the first third receive beginner questions, the middle third receive intermediate questions, and the final third receive advanced questions
5. WHEN a User submits a text answer to a mock question, THE Interview_Preparer SHALL provide feedback identifying specific strengths and specific areas for improvement by comparing the submitted answer against the question's evaluation criteria
6. IF the Target_Role does not typically involve system design responsibilities, THEN THE Interview_Preparer SHALL omit the system design category and distribute questions across the remaining applicable categories

### Requirement 7: Project Suggestions

**User Story:** As a User, I want project ideas relevant to my target role, so that I can build practical experience and a portfolio.

#### Acceptance Criteria

1. WHEN a User completes all tasks in a Weekly_Plan that is designated as a practical milestone in the Learning_Roadmap, THE Project_Suggester SHALL recommend at least 2 hands-on projects that exercise the skills learned in that milestone
2. THE Project_Suggester SHALL provide a project brief for each suggestion including objectives, expected deliverables, technologies to use, and an estimated completion time between 1 and 4 weeks
3. THE Project_Suggester SHALL align project complexity with the User's current skill level such that projects for beginner-level skills require application of a single concept and projects for advanced-level skills require integration of multiple concepts
4. THE Platform SHALL allow the User to mark projects as completed and record a text outcome description of up to 500 characters
5. THE Project_Suggester SHALL suggest at least two project options per milestone so the User can choose based on interest
6. IF a User dismisses all suggested projects for a milestone, THEN THE Platform SHALL allow the User to proceed to the next phase of the Learning_Roadmap without completing a project

### Requirement 8: Progress Tracking

**User Story:** As a User, I want to track my overall progress, so that I can stay motivated and see how far I've come.

#### Acceptance Criteria

1. THE Platform SHALL display an overall progress percentage calculated as the number of completed Weekly_Plans divided by the total number of Weekly_Plans in the Learning_Roadmap, displayed as an integer from 0 to 100
2. WHEN a User completes all tasks within a Weekly_Plan, THE Platform SHALL update the User's skill proficiency levels for skills associated with that Weekly_Plan to reflect their new proficiency (beginner, intermediate, or advanced)
3. WHEN a User completes all Weekly_Plans associated with a skill gap in the Learning_Roadmap, THE Platform SHALL notify the User within the application that the skill gap milestone has been achieved
4. THE Platform SHALL provide a visual timeline showing each Weekly_Plan in the Learning_Roadmap distinguished by status: completed, in-progress, or upcoming
5. WHEN the Learning_Roadmap is recalculated due to a change in weekly study hours, THE Platform SHALL update the progress percentage and timeline to reflect the revised total number of Weekly_Plans
