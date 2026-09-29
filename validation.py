# validation.py
# Simple functions to check if the user typed something correct.
# Each function just returns True or False.
# I check inputs here so bad data never gets saved to the csv files.


def is_empty(text):
    # checks if a string is empty or just spaces
    if text is None:
        return True
    if text.strip() == "":
        return True
    return False


def check_roll_no(roll_no):
    if is_empty(roll_no):
        return False

    # roll number should be a positive number
    if not roll_no.strip().isdigit():
        return False

    if int(roll_no.strip()) <= 0:
        return False

    return True


def check_class(class_text):
    # class should be a whole number between 1 and 12
    if not class_text.strip().isdigit():
        return False

    class_number = int(class_text)

    if class_number < 1 or class_number > 12:
        return False

    return True


def check_date(date_text):
    # date should be in DD-MM-YYYY format
    parts = date_text.strip().split("-")

    if len(parts) != 3:
        return False

    if not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit():
        return False

    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])

    if day < 1 or day > 31:
        return False

    if month < 1 or month > 12:
        return False

    if year < 2000 or year > 2100:
        return False

    return True

def check_marks(marks_text, max_marks_text):
    # marks and max marks should be numbers, and marks should not be
    # more than max marks
    try:
        marks = float(marks_text)
        max_marks = float(max_marks_text)
    except ValueError:
        return False

    if max_marks <= 0:
        return False
    if marks < 0 or marks > max_marks:
        return False

    return True
