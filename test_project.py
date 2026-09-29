# tests/test_project.py
# Simple tests for my project. I'm using plain assert statements
# instead of a big testing framework, since that's what we learned
# in class. Run this file directly to see if everything passes:
#
#   python3 tests/test_project.py

import sys
import os

# this lets me import my files from the main project folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import storage
import validation
import student
import study_planner
import test_tracker
import performance
import achievements

tests_passed = 0
tests_failed = 0


def check(condition, test_name):
   # Helper function to track test pass/fail counts
    global tests_passed, tests_failed
    if condition:
        print("PASS - " + test_name)
        tests_passed = tests_passed + 1
    else:
        print("FAIL - " + test_name)
        tests_failed = tests_failed + 1


def use_test_files():
    # point all the storage file paths to a separate test folder
    # so my tests never touch the real student data
    storage.STUDENT_FILE = "data/test_student_data.csv"
    storage.TASK_FILE = "data/test_study_tasks.csv"
    storage.SCORE_FILE = "data/test_test_scores.csv"
    storage.BADGE_FILE = "data/test_achievements.csv"


def delete_test_files():
    for path in [storage.STUDENT_FILE, storage.TASK_FILE,
                 storage.SCORE_FILE, storage.BADGE_FILE]:
        if os.path.exists(path):
            os.remove(path)


# ---------- validation.py tests ----------

def test_validation():
    check(validation.check_roll_no("1") == True, "valid roll number accepted")
    check(validation.check_roll_no("ABC") == False, "invalid roll number rejected")
    check(validation.check_roll_no("0") == False, "zero roll number rejected")

    check(validation.check_class("10") == True, "valid class accepted")
    check(validation.check_class("13") == False, "class out of range rejected")

    check(validation.check_date("15-01-2026") == True, "valid date accepted")
    check(validation.check_date("2026-01-15") == False, "wrong date format rejected")

    check(validation.check_marks("40", "50") == True, "valid marks accepted")
    check(validation.check_marks("60", "50") == False, "marks over max rejected")


# ---------- student.py tests ----------

def test_student():
    delete_test_files()

    profile = student.create_profile("100", "Asha Rao", "10", "A")
    check(profile is not None, "student profile created")

    found = student.get_profile("100")
    check(found is not None and found["name"] == "Asha Rao", "get_profile finds the student")

    duplicate = student.create_profile("100", "Someone Else", "9", "B")
    check(duplicate is None, "duplicate roll number rejected")

    missing = student.get_profile("999")
    check(missing is None, "missing profile returns None")

    updated = student.update_profile("100", class_name="11")
    check(updated["class"] == "11", "profile class updated")


# ---------- study_planner.py tests ----------

def test_study_planner():
    delete_test_files()
    student.create_profile("200", "Kiran", "10", "A")

    task = study_planner.add_task("S200", "Maths", "Revise calculus", "01-02-2026")
    check(task is not None, "task added")

    tasks = study_planner.list_tasks("S200")
    check(len(tasks) == 1, "task shows up in list")

    study_planner.complete_task("S200", task["task_id"])
    done_tasks = study_planner.list_tasks("S200", status_filter="done")
    check(len(done_tasks) == 1, "task marked as done")

    study_planner.delete_task("S200", task["task_id"])
    remaining = study_planner.list_tasks("S200")
    check(len(remaining) == 0, "task deleted")


# ---------- test_tracker.py and performance.py tests ----------

def test_scores_and_performance():
    delete_test_files()
    student.create_profile("300", "Zara", "11", "B")

    test_tracker.add_score("S300", "Maths", "Unit Test 1", "40", "50", "10-01-2026")
    test_tracker.add_score("S300", "Maths", "Unit Test 2", "45", "50", "10-02-2026")

    average = performance.overall_average("S300")
    check(average == 85.0, "overall average is correct")

    test_tracker.add_score("S300", "History", "Quiz", "10", "50", "01-01-2026")
    weak = performance.weak_subjects("S300")
    check("History" in weak, "weak subject detected")


# ---------- achievements.py tests ----------

def test_achievements():
    delete_test_files()
    student.create_profile("400", "Dev", "12", "A")

    updated = achievements.award_task_completion("400")
    check(updated is not None and updated["xp"] == "10", "xp increases after completing a task")
    
    updated = achievements.award_test_result("400", 30, 50)
    check(updated is not None and updated["xp"] == "25", "xp increases after passing a test")
    
    badges = achievements.list_badges("400")
    check("First Steps" not in badges, "no First Steps badge yet (no task marked done)")


# ---------- run everything ----------

if __name__ == "__main__":
    use_test_files()

    test_validation()
    test_student()
    test_study_planner()
    test_scores_and_performance()
    test_achievements()

    delete_test_files()

    print("\n" + str(tests_passed) + " passed, " + str(tests_failed) + " failed")
