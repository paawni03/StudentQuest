# storage.py
# Storage helper module for Reading and Writing CSV data files
# Uses DictReader and DictWriter to handle data as Python dictionaries.
import csv
import os

# file paths - all my data will be saved inside the data folder
STUDENT_FILE = "data/student_data.csv"
TASK_FILE = "data/study_tasks.csv"
SCORE_FILE = "data/test_scores.csv"
BADGE_FILE = "data/achievements.csv"


def read_csv(filename):
    # this function reads a csv file and gives back a list of
    # dictionaries (one dictionary per row)
    rows = []

    # if the file does not exist yet, just return empty list
    if not os.path.exists(filename):
        return rows

    file = open(filename, "r", newline="")
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)
    file.close()

    return rows


def write_csv(filename, headers, rows):
    # this function completely overwrites the csv file with new data
    # used when we need to update an existing row (like marking a task done)

    # make sure the data folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    file = open(filename, "w", newline="")
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    file.close()


def add_row(filename, headers, row):
    # this function just adds ONE new row at the end of the file
    # used when we are adding something new (like a new task)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    file_already_exists = os.path.exists(filename)

    file = open(filename, "a", newline="")
    writer = csv.DictWriter(file, fieldnames=headers)

    # only write the header line if the file is brand new
    if not file_already_exists:
        writer.writeheader()

    writer.writerow(row)
    file.close()
