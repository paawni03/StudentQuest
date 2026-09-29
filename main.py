# main.py
# This is the file you run to start the program.
# It just shows a menu in a loop and calls the right function
# depending on what number the user types.

import student
import study_planner
import test_tracker
import performance
import achievements
import reports


def show_menu():
    print("\n========================================")
    print("STUDENT QUEST - Main Menu")
    print("========================================")
    print("1. Create student profile")
    print("2. View profile and summary report")
    print("3. Add study task")
    print("4. List study tasks")
    print("5. Mark task as done")
    print("6. Add test score")
    print("7. View performance analysis")
    print("8. View XP and achievements")
    print("9. Save report to file")
    print("0. Exit")


def option_create_profile():
    roll_no = input("Roll number: ")
    name = input("Name: ")
    class_name = input("Class (1-12): ")
    section = input("Section: ")

    profile = student.create_profile(roll_no, name, class_name, section)
    if profile is not None:
        print("\nProfile created for " + profile["name"] + " (" + profile["roll_no"] + ")")


def option_view_profile():
    roll_no = input("Roll number: ")
    profile = student.get_profile(roll_no)

    if profile is None:
        print("Error: no profile found for that roll number.")
        return

    print("\n" + reports.build_report(roll_no))


def option_add_task():
    roll_no = input("Roll number: ")

    # make sure this student actually exists first
    if student.get_profile(roll_no) is None:
        print("Error: no profile found for that roll number.")
        return

    subject = input("Subject: ")
    description = input("Task description: ")
    due_date = input("Due date (DD-MM-YYYY): ")

    task = study_planner.add_task(roll_no, subject, description, due_date)
    if task is not None:
        print("\nTask #" + task["task_id"] + " added.")


def option_list_tasks():
    roll_no = input("Roll number: ")
    tasks = study_planner.list_tasks(roll_no)

    if len(tasks) == 0:
        print("\nNo tasks found.")
        return

    print()
    for t in tasks:
        print("[" + t["task_id"] + "] (" + t["status"] + ") " + t["subject"]
              + " - " + t["description"] + " due " + t["due_date"])


def option_complete_task():
    roll_no = input("Roll number: ")
    task_id = input("Task ID to mark done: ")

    result = study_planner.complete_task(roll_no, task_id)
    if result is not None:
        updated = achievements.award_task_completion(roll_no)
        print("\nTask #" + task_id + " completed. XP is now " + updated["xp"]
              + " (Level " + updated["level"] + ")")


def option_add_score():
    roll_no = input("Roll number: ")

    if student.get_profile(roll_no) is None:
        print("Error: no profile found for that roll number.")
        return

    subject = input("Subject: ")
    test_name = input("Test name: ")
    marks = input("Marks obtained: ")
    max_marks = input("Max marks: ")
    date_taken = input("Date (DD-MM-YYYY): ")

    score = test_tracker.add_score(roll_no, subject, test_name, marks, max_marks, date_taken)
    if score is not None:
        updated = achievements.award_test_result(roll_no, float(marks), float(max_marks))
        print("\nScore recorded. XP is now " + updated["xp"] + " (Level " + updated["level"] + ")")


def option_performance():
    roll_no = input("Roll number: ")

    if student.get_profile(roll_no) is None:
        print("Error: no profile found for that roll number.")
        return

    print("\nOverall average: " + str(performance.overall_average(roll_no)) + "%")
    print("Trend: " + performance.trend(roll_no))

    print("Subject averages:")
    subject_avgs = performance.subject_averages(roll_no)
    for subject in subject_avgs:
        print("  - " + subject + ": " + str(subject_avgs[subject]) + "%")

    weak = performance.weak_subjects(roll_no)
    if len(weak) == 0:
        print("Weak subjects: none")
    else:
        print("Weak subjects: " + ", ".join(weak))


def option_achievements():
    roll_no = input("Roll number: ")
    profile = student.get_profile(roll_no)

    if profile is None:
        print("Error: no profile found for that roll number.")
        return

    badges = achievements.list_badges(roll_no)
    print("\n" + profile["name"] + " - " + profile["xp"] + " XP, Level " + profile["level"])

    if len(badges) == 0:
        print("Badges: none yet")
    else:
        print("Badges: " + ", ".join(badges))


def option_save_report():
    roll_no = input("Roll number: ")

    if student.get_profile(roll_no) is None:
        print("Error: no profile found for that roll number.")
        return

    file_path = reports.save_report(roll_no)
    print("\nReport saved to " + file_path)


def main():
    print("Welcome to StudentQuest!")

    while True:
        show_menu()
        choice = input("\nChoose an option: ")

        if choice == "1":
            option_create_profile()
        elif choice == "2":
            option_view_profile()
        elif choice == "3":
            option_add_task()
        elif choice == "4":
            option_list_tasks()
        elif choice == "5":
            option_complete_task()
        elif choice == "6":
            option_add_score()
        elif choice == "7":
            option_performance()
        elif choice == "8":
            option_achievements()
        elif choice == "9":
            option_save_report()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

        input("\nPress Enter to continue...")


# this makes sure main() only runs when we run this file directly
if __name__ == "__main__":
    main()
