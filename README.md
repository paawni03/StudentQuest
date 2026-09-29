# 🎓 StudentQuest

A gamified student productivity and performance tracker built in Python.
Students track their study tasks and test scores, earn **XP** and unlock
**achievement badges**, and get automatic performance analysis — turning
routine academic tracking into a game.

## Overview

StudentQuest was built as a "Build Your Own Project" submission. Rather
than a fixed brief, it applies core programming and software-engineering
concepts (modular design, data validation, persistent storage, automated
testing) to a real problem: helping students stay on top of their
coursework and see their own progress over time.

## Features

- 👤 **Student Profile** — create, view, and update a student's profile
  (roll number, name, class, section).
- 📚 **Study Planner** — add study tasks with a subject, description, and
  due date; mark tasks done or delete them; list pending/completed tasks.
- 📝 **Test & Marks Tracker** — record test scores per subject with full
  input validation (marks can't exceed max marks, dates must be valid).
- 📊 **Performance Analysis** — automatic overall average, per-subject
  averages, a trend indicator (improving / declining / stable), and a
  list of weak subjects (below 50%).
- 🏆 **XP & Achievements** — earn XP for completing tasks (+10) and for
  passing (+15) or excelling (+25) on tests; level up automatically;
  unlock badges such as *Task Master*, *Rising Star*, and *Top Scorer*.
- 💾 **Data Storage** — all data persists to CSV files in `data/`, so
  progress is saved between sessions.
- 📄 **Reports** — generate a formatted summary report on screen or save
  it to a text file.

## Technologies / Tools Used

- **Python 3** (standard library only — `csv`,  `datetime`,
  `unittest`, `os`) — no external dependencies required.
- **CSV** files for lightweight, human-readable persistent storage.
- **Custom Assertion Test Suite** using built-in `assert` checks for automated module testing.
- **Git / GitHub** for version control.

## Project Structure

```
StudentQuest/
├── main.py              # CLI entry point / menu
├── gui.py                 # Tkinter desktop GUI (same modules, graphical interface)
├── student.py            # Module 1: Student Profile
├── study_planner.py       # Module 2: Study Planner
├── test_tracker.py        # Module 3: Test & Marks Tracker
├── performance.py         # Module 4: Performance Analysis
├── achievements.py        # Module 5: XP & Achievements
├── reports.py             # Report generation (combines all modules)
├── validation.py          # Shared input validation helpers
├── storage.py             # Shared CSV persistence layer
├── data/                  # CSV data files (created automatically)
├── screenshots/            # Project screenshots
├── tests/
│   └── test_project.py    # Unit tests (23 tests)
├── README.md
└── statement.md
```

## Steps to Install & Run

1. Make sure Python 3.8+ is installed:
   ```bash
   python3 --version
   ```
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd StudentQuest
   ```
3. Run the application (no external packages needed):
   ```bash
   python3 main.py
   ```
4. Follow the on-screen menu. A typical first session:
   - Option `1` → create your student profile
   - Option `3` → add a study task
   - Option `6` → record a test score
   - Option `2` or `9` → view / save your summary report

   **Or run the graphical (Tkinter) version instead:**
   ```bash
   python3 gui.py
   ```
   Tkinter comes bundled with Python on Windows and Mac. On Linux you
   may need to install it first: `sudo apt install python3-tk`.
   Type a roll number at the top of the window and click "Load /
   Refresh", then use the tabs (Profile, Study Planner, Test Tracker,
   Performance, Achievements, Report) to work with that student.

## Instructions for Testing

Run the full automated test suite from the project root:

```bash
python tests/test_project.py
```

This runs 23 unit tests covering input validation, student profile
management, the study planner, the test tracker, performance
calculations, and the XP/achievements logic — each against an isolated
temporary data directory so your real data is never touched.

## Screenshots

Screenshots of the StudentQuest GUI, performance analysis,
achievement badges, generated report, and successful test execution
are included in the project documentation.

## Non-Functional Qualities

- **Validation / Security**: all user input is validated centrally in
  `validation.py` before it reaches storage.
- **Reliability**: every CLI action is wrapped in error handling so bad
  input shows a friendly message instead of crashing the app.
- **Maintainability**: each module has a single responsibility and talks
  to storage only through `storage.py`.
- **Resource efficiency**: lightweight CSV storage, no external
  dependencies or database server required.
