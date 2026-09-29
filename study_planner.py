# study_planner.py
# Module 2: Study Planner
# Functions to add, list, complete and delete study tasks.

import storage
import validation
from datetime import datetime

HEADERS = ["task_id", "roll_no", "subject", "description", "due_date", "status"]


def add_task(roll_no, subject, description, due_date):
    if validation.is_empty(subject):
        print("Error: subject cannot be empty.")
        return None

    if validation.is_empty(description):
        print("Error: description cannot be empty.")
        return None

    if not validation.check_date(due_date):
        print("Error: due date must be in DD-MM-YYYY format.")
        return None

    # work out the next task id by counting existing tasks + 1
    all_tasks = storage.read_csv(storage.TASK_FILE)
    new_id = len(all_tasks) + 1

    new_task = {
        "task_id": str(new_id),
        "roll_no": roll_no,
        "subject": subject,
        "description": description,
        "due_date": due_date,
        "status": "pending",
    }

    storage.add_row(storage.TASK_FILE, HEADERS, new_task)
    return new_task


def list_tasks(roll_no, status_filter=None):
    all_tasks = storage.read_csv(storage.TASK_FILE)
    my_tasks = []

    for t in all_tasks:
        if t["roll_no"] == roll_no:
            if status_filter is None or t["status"] == status_filter:
                my_tasks.append(t)

    # sort by due date, earliest first
    my_tasks.sort(key=lambda t: datetime.strptime(t["due_date"], "%d-%m-%Y"))
    return my_tasks


def complete_task(roll_no, task_id):
    all_tasks = storage.read_csv(storage.TASK_FILE)
    found_task = None

    for t in all_tasks:
        if t["roll_no"] == roll_no and t["task_id"] == str(task_id):
            t["status"] = "done"
            found_task = t

    if found_task is None:
        print("Error: could not find that task.")
        return None

    storage.write_csv(storage.TASK_FILE, HEADERS, all_tasks)
    return found_task


def delete_task(roll_no, task_id):
    all_tasks = storage.read_csv(storage.TASK_FILE)
    new_task_list = []
    task_was_found = False

    for t in all_tasks:
        if t["roll_no"] == roll_no and t["task_id"] == str(task_id):
            task_was_found = True
            # don't add it to the new list -> this deletes it
        else:
            new_task_list.append(t)

    if not task_was_found:
        print("Error: could not find that task.")
        return False

    storage.write_csv(storage.TASK_FILE, HEADERS, new_task_list)
    return True


def pending_count(roll_no):
    return len(list_tasks(roll_no, status_filter="pending"))
