# Problem Statement

Students juggling coursework, tests, and assignments often lose track of
what they need to study, how they are performing across subjects, and
whether their effort is actually paying off. Existing to-do apps track
tasks but rarely connect that effort to academic outcomes, and plain
gradebooks show marks without any motivation layer. There is a gap for a
simple, self-contained tool that combines task planning, score tracking,
and performance feedback with positive reinforcement.

**StudentQuest** addresses this by giving each student one place to plan
study tasks, log test scores, see clear performance analysis, and earn
XP and badges for consistent effort — turning academic tracking into a
lightweight game that encourages regular use.

## Scope of the Project

In scope:

- Single-user-per-profile, multi-profile application with both console and graphical interfaces (supports many students, one at a
time, identified by roll number)
- Local persistent storage using CSV files — no server or internet
  connection required.
- Five core functional modules: Student Profile, Study Planner, Test &
  Marks Tracker, Performance Analysis, and XP & Achievements.
- Automated unit tests for the core business logic.

Out of scope (possible future enhancements, not built here):

- Multi-device sync or cloud storage.
- Multi-user authentication / login system.
- Notifications or reminders for upcoming due dates.

## Target Users

- School and college students who want a lightweight, private way to
  plan their studies and track their own performance.
- Self-learners who want gamified motivation to stay consistent with
  study habits.
- Anyone evaluating the project academically as a demonstration of
  modular Python design, data validation, persistent storage, and
  automated testing.

## High-Level Features

1. **Student Profile** — create and maintain a profile per student(roll number, name, class, section, XP, level).
2. **Study Planner** — add, list, complete, and delete study tasks tied
   to a subject and due date.
3. **Test & Marks Tracker** — log test scores per subject with
   validation against a maximum mark.
4. **Performance Analysis** — compute overall and per-subject averages,
   flag weak subjects, and report an improving/declining/stable trend.
5. **XP & Achievements** — award XP for completed tasks and test
   results, auto-calculate level, and unlock badges based on milestones.
6. **Reports** — generate and optionally save a full text summary
   combining data from every module.
7. **Graphical User Interface** — provide a Tkinter-based desktop interface with tabs for Profile, Study Planner, Test Tracker Performance, Achievements, and Reports.
