# achievements.py
# Module 5: XP & Achievements
# Gives the student XP points for completing tasks and doing well
# on tests, works out their level, and unlocks badges.

import storage
import student
import study_planner
import performance
from datetime import date

# how much xp you get for different things
XP_PER_TASK = 10
XP_PER_PASS = 15          # scored 50% or more on a test
XP_PER_DISTINCTION = 25   # scored 90% or more on a test
XP_PER_LEVEL = 100        # every 100 xp = 1 new level

BADGE_HEADERS = ["roll_no", "badge", "date_earned"]


def add_xp(roll_no, amount):
    # find the student and give them more xp, then work out new level
    profile = student.get_profile(roll_no)
    if profile is None:
        print("Error: student not found.")
        return None

    new_xp = int(profile["xp"]) + amount
    new_level = 1 + (new_xp // XP_PER_LEVEL)

    all_students = storage.read_csv(storage.STUDENT_FILE)
    for s in all_students:
        if s["roll_no"] == roll_no:
            s["xp"] = str(new_xp)
            s["level"] = str(new_level)

    storage.write_csv(storage.STUDENT_FILE, student.HEADERS, all_students)

    # after giving xp, check if any new badges were unlocked
    check_achievements(roll_no)

    return student.get_profile(roll_no)


def award_task_completion(roll_no):
    return add_xp(roll_no, XP_PER_TASK)


def award_test_result(roll_no, marks, max_marks):
    percent = (marks / max_marks) * 100

    if percent >= 90:
        return add_xp(roll_no, XP_PER_DISTINCTION)
    elif percent >= 50:
        return add_xp(roll_no, XP_PER_PASS)
    else:
        # no xp for failing, just return the profile as it is
        return student.get_profile(roll_no)


def already_has_badge(roll_no, badge_name):
    all_badges = storage.read_csv(storage.BADGE_FILE)
    for b in all_badges:
        if b["roll_no"] == roll_no and b["badge"] == badge_name:
            return True
    return False


def give_badge(roll_no, badge_name):
    new_badge = {
        "roll_no": roll_no,
        "badge": badge_name,
        "date_earned": date.today().strftime("%d-%m-%Y"),
    }
    storage.add_row(storage.BADGE_FILE, BADGE_HEADERS, new_badge)


def check_achievements(roll_no):
    # this function checks a few simple rules and gives badges if
    # the student has earned them and doesn't already have them
    newly_earned = []

    done_tasks = study_planner.list_tasks(roll_no, status_filter="done")
    average = performance.overall_average(roll_no)
    student_trend = performance.trend(roll_no)

    # Badge 1: completed at least 1 task
    if len(done_tasks) >= 1 and not already_has_badge(roll_no, "First Steps"):
        give_badge(roll_no, "First Steps")
        newly_earned.append("First Steps")

    # Badge 2: completed 10 or more tasks
    if len(done_tasks) >= 10 and not already_has_badge(roll_no, "Task Master"):
        give_badge(roll_no, "Task Master")
        newly_earned.append("Task Master")

    # Badge 3: overall average is 75% or higher
    if average >= 75 and not already_has_badge(roll_no, "Consistent Performer"):
        give_badge(roll_no, "Consistent Performer")
        newly_earned.append("Consistent Performer")

    # Badge 4: scores are improving over time
    if student_trend == "improving" and not already_has_badge(roll_no, "Rising Star"):
        give_badge(roll_no, "Rising Star")
        newly_earned.append("Rising Star")

    # Badge 5: overall average is 90% or higher
    if average >= 90 and not already_has_badge(roll_no, "Top Scorer"):
        give_badge(roll_no, "Top Scorer")
        newly_earned.append("Top Scorer")

    return newly_earned


def list_badges(roll_no):
    all_badges = storage.read_csv(storage.BADGE_FILE)
    my_badges = []
    for b in all_badges:
        if b["roll_no"] == roll_no:
            my_badges.append(b["badge"])
    return my_badges
