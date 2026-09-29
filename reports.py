# reports.py
# Generates structured text performance summaries for students
# and exports them as plain text report files.

import os
import student
import study_planner
import performance
import achievements

REPORTS_FOLDER = "data/reports"


def build_report(roll_no):
    profile = student.get_profile(roll_no)
    if profile is None:
        return "Error: no profile found for this roll number."

    pending = study_planner.pending_count(roll_no)
    done_tasks = len(study_planner.list_tasks(roll_no, status_filter="done"))
    average = performance.overall_average(roll_no)
    subject_avgs = performance.subject_averages(roll_no)
    weak = performance.weak_subjects(roll_no)
    student_trend = performance.trend(roll_no)
    badges = achievements.list_badges(roll_no)

    # I'm building the report text line by line using a list, then
    # joining it all together at the end
    lines = []
    lines.append("=" * 50)
    lines.append("STUDENT QUEST - PERFORMANCE REPORT")
    lines.append("=" * 50)
    lines.append("Name       : " + profile["name"])
    lines.append("Roll No    : " + profile["roll_no"])
    lines.append("Class      : " + profile["class"] + " - Section " + profile["section"])
    lines.append("XP / Level : " + profile["xp"] + " XP - Level " + profile["level"])
    lines.append("-" * 50)
    lines.append("Study Tasks: " + str(done_tasks) + " completed, " + str(pending) + " pending")
    lines.append("Overall Avg: " + str(average) + "%")
    lines.append("Trend      : " + student_trend)
    lines.append("Subject Averages:")

    if len(subject_avgs) == 0:
        lines.append("  (no test scores recorded yet)")
    else:
        for subject in subject_avgs:
            lines.append("  - " + subject + ": " + str(subject_avgs[subject]) + "%")

    if len(weak) == 0:
        lines.append("Weak Subjects (below 50%): none")
    else:
        lines.append("Weak Subjects (below 50%): " + ", ".join(weak))

    if len(badges) == 0:
        lines.append("Badges Earned: none yet")
    else:
        lines.append("Badges Earned: " + ", ".join(badges))

    lines.append("=" * 50)

    # join all the lines with a newline character between them
    report_text = "\n".join(lines)
    return report_text


def save_report(roll_no):
    report_text = build_report(roll_no)

    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    file_path = REPORTS_FOLDER + "/" + roll_no + "_report.txt"

    file = open(file_path, "w")
    file.write(report_text)
    file.close()

    return file_path
