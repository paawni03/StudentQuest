# test_tracker.py
# Module 3: Test & Marks Tracker
# Functions to add and view test scores for a student.

import storage
import validation

HEADERS = ["score_id", "roll_no", "subject", "test_name", "marks", "max_marks", "date"]


def add_score(roll_no, subject, test_name, marks, max_marks, date):
    if validation.is_empty(subject):
        print("Error: subject cannot be empty.")
        return None

    if validation.is_empty(test_name):
        print("Error: test name cannot be empty.")
        return None

    if not validation.check_marks(marks, max_marks):
        print("Error: marks must be a number and cannot be more than max marks.")
        return None

    if not validation.check_date(date):
        print("Error: date must be in DD-MM-YYYY format.")
        return None

    all_scores = storage.read_csv(storage.SCORE_FILE)
    new_id = len(all_scores) + 1

    new_score = {
        "score_id": str(new_id),
        "roll_no": roll_no,
        "subject": subject,
        "test_name": test_name,
        "marks": marks,
        "max_marks": max_marks,
        "date": date,
    }

    storage.add_row(storage.SCORE_FILE, HEADERS, new_score)
    return new_score


def list_scores(roll_no, subject=None):
    all_scores = storage.read_csv(storage.SCORE_FILE)
    my_scores = []

    for s in all_scores:
        if s["roll_no"] == roll_no:
            if subject is None or s["subject"].lower() == subject.lower():
                my_scores.append(s)

    my_scores.sort(key=lambda s: s["date"])
    return my_scores


def subjects_for(roll_no):
    # returns a list of all the different subjects this student has
    # taken tests in (no duplicates)
    all_scores = storage.read_csv(storage.SCORE_FILE)
    subject_list = []

    for s in all_scores:
        if s["roll_no"] == roll_no:
            if s["subject"] not in subject_list:
                subject_list.append(s["subject"])

    subject_list.sort()
    return subject_list
