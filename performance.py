# performance.py
# Module 4: Performance Analysis
# Takes the raw test scores and turns them into percentages,
# averages, and a simple trend (improving / declining / stable).

import test_tracker


def get_percentage(score):
    # turns a score dictionary like {"marks": "40", "max_marks": "50"}
    # into a percentage number like 80.0
    marks = float(score["marks"])
    max_marks = float(score["max_marks"])
    percent = (marks / max_marks) * 100
    return percent


def overall_average(roll_no):
    scores = test_tracker.list_scores(roll_no)

    if len(scores) == 0:
        return 0.0

    total = 0
    for s in scores:
        total = total + get_percentage(s)

    average = total / len(scores)
    return round(average, 2)


def subject_averages(roll_no):
    scores = test_tracker.list_scores(roll_no)

    # group percentages by subject using a dictionary
    subject_totals = {}

    for s in scores:
        subject = s["subject"]
        percent = get_percentage(s)

        if subject not in subject_totals:
            subject_totals[subject] = []

        subject_totals[subject].append(percent)

    # now calculate the average for each subject
    averages = {}
    for subject in subject_totals:
        percent_list = subject_totals[subject]
        avg = sum(percent_list) / len(percent_list)
        averages[subject] = round(avg, 2)

    return averages


def weak_subjects(roll_no, threshold=50.0):
    averages = subject_averages(roll_no)
    weak_list = []

    for subject in averages:
        if averages[subject] < threshold:
            weak_list.append(subject)

    weak_list.sort()
    return weak_list


def trend(roll_no):
    # compares the average of the older half of tests to the newer half
    # to see if the student is doing better or worse over time
    scores = test_tracker.list_scores(roll_no)

    if len(scores) < 2:
        return "not enough data"

    middle = len(scores) // 2
    older_half = scores[:middle]
    newer_half = scores[middle:]

    older_total = 0
    for s in older_half:
        older_total = older_total + get_percentage(s)
    older_avg = older_total / len(older_half)

    newer_total = 0
    for s in newer_half:
        newer_total = newer_total + get_percentage(s)
    newer_avg = newer_total / len(newer_half)

    difference = newer_avg - older_avg

    if difference > 2:
        return "improving"
    elif difference < -2:
        return "declining"
    else:
        return "stable"
