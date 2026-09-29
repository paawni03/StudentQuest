# student.py
# Module 1: Student Profile
# Functions to create, view and update a student's profile.

import storage
import validation

# these are the column names in student_data.csv
HEADERS = ["roll_no", "name", "class", "section", "xp", "level"]

def create_profile(roll_no, name, class_name, section):    # first check everything is valid before saving
    if not validation.check_roll_no(roll_no):
        print("Error: roll number must be a positive number.")
        return None

    if validation.is_empty(name):
        print("Error: name cannot be empty.")
        return None

    if validation.is_empty(class_name):
        print("Error: class cannot be empty.")
        return None

    if not validation.check_class(class_name):
        print("Error: class must be a number between 1 and 12.")
        return None

    if validation.is_empty(section):
        print("Error: section cannot be empty.")
        return None

    # check that this roll number is not already used
    all_students = storage.read_csv(storage.STUDENT_FILE)
    for s in all_students:
        if s["roll_no"] == roll_no:
            print("Error: a profile with this roll number already exists.")
            return None

    # everything looks good, so build the new profile and save it
    new_profile = {
        "roll_no": roll_no,
        "name": name,
        "class": class_name,
        "section": section,
        "xp": "0",
        "level": "1",
}

    storage.add_row(storage.STUDENT_FILE, HEADERS, new_profile)
    return new_profile


def get_profile(roll_no):
    all_students = storage.read_csv(storage.STUDENT_FILE)
    for s in all_students:
        if s["roll_no"] == roll_no:
            return s
    # not found
    return None


def update_profile(roll_no, name=None, class_name=None, section=None):
    all_students = storage.read_csv(storage.STUDENT_FILE)
    found_student = None
        
    for s in all_students:
        if s["roll_no"] == roll_no:
            if name:
                 s["name"] = name

            if class_name:
                if validation.check_class(class_name):
                    s["class"] = class_name
                else:
                    print("Error: class must be a number between 1 and 12.")
            if section:
                s["section"] = section
            found_student = s
            break
    if found_student is None:
            print("Error: no profile found for this roll number.")
            return None
            
    storage.write_csv(storage.STUDENT_FILE, HEADERS, all_students)
    return found_student


def list_profiles():
    return storage.read_csv(storage.STUDENT_FILE)
