# gui.py
# Graphical interface for StudentQuest using Tkinter.
# The GUI uses the same modules as the console version.

import tkinter as tk
from tkinter import ttk, messagebox

import student
import study_planner
import test_tracker
import performance
import achievements
import reports


class StudentQuestApp:
       # Main class for the StudentQuest GUI.
    def __init__(self, window):
        self.window = window
        self.window.title("Student Quest")
        self.window.geometry("650x600")

        # this variable holds the roll number that is currently loaded.
        # every tab uses this same roll number
        self.roll_no_var = tk.StringVar()

        self.build_top_bar()
        self.build_tabs()

    # ---------------------------------------------------------
    # TOP BAR - where you type the roll number for the student
    # you want to work with
    # ---------------------------------------------------------

    def build_top_bar(self):
        top_frame = tk.Frame(self.window, pady=8)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Roll Number:").pack(side="left", padx=5)
        tk.Entry(top_frame, textvariable=self.roll_no_var, width=15).pack(side="left")

        tk.Button(top_frame, text="Load / Refresh", command=self.load_student).pack(side="left", padx=5)

        self.status_label = tk.Label(top_frame, text="No student loaded", fg="blue")
        self.status_label.pack(side="left", padx=10)

    def load_student(self):
        # this looks up the roll number typed at the top and shows the
        # student's name, level and xp if it finds them
        roll_no = self.roll_no_var.get().strip()
        if roll_no == "":
            messagebox.showerror("Error", "Please type a roll number first.")
            return

        profile = student.get_profile(roll_no)
        if profile is None:
            self.status_label.config(text="No profile found for " + roll_no, fg="red")
        else:
            self.status_label.config(
                text=profile["name"] + " - Level " + profile["level"] + " (" + profile["xp"] + " XP)",
                fg="green"
            )
            self.refresh_tasks()
            self.refresh_scores()

    def get_roll_no(self):
        # small helper so every tab can grab the roll number the same way
        roll_no = self.roll_no_var.get().strip()
        if roll_no == "":
            messagebox.showerror("Error", "Please type a roll number at the top first.")
            return None
        return roll_no

    # ---------------------------------------------------------
    # TABS - I used a Notebook widget which just means tabs you
    # can click between, like tabs in a web browser
    # ---------------------------------------------------------

    def build_tabs(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.build_profile_tab(notebook)
        self.build_planner_tab(notebook)
        self.build_tracker_tab(notebook)
        self.build_performance_tab(notebook)
        self.build_achievements_tab(notebook)
        self.build_report_tab(notebook)

    # ----- Tab 1: Profile -----

    def build_profile_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Profile")

        tk.Label(tab, text="Create a new student profile", font=("Arial", 11, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10)

        tk.Label(tab, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(tab, width=25)
        self.name_entry.grid(row=1, column=1, pady=5)

        tk.Label(tab, text="Class (1-12):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.class_entry = tk.Entry(tab, width=25)
        self.class_entry.grid(row=2, column=1, pady=5)

        tk.Label(tab, text="Section:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.section_entry = tk.Entry(tab, width=25)
        self.section_entry.grid(row=3, column=1, pady=5)

        tk.Button(tab, text="Create Profile", command=self.create_profile_clicked).grid(
            row=4, column=0, columnspan=2, pady=10)

        tk.Label(tab, text="(Roll number is taken from the top of the window)",
                 fg="gray").grid(row=5, column=0, columnspan=2)

    def create_profile_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        name = self.name_entry.get().strip()
        class_name = self.class_entry.get().strip()
        section = self.section_entry.get().strip()

        profile = student.create_profile(roll_no, name, class_name, section)
        if profile is None:
            messagebox.showerror(
                "Error",
                "Could not create profile.\n\n"
                "Check that:\n"
                "- roll number is a positive number\n"
                "- name, class and section are filled in\n"
                "- class is a number between 1 and 12\n"
                "- this roll number is not already used"
            )
            return

        messagebox.showinfo("Success", "Profile created for " + profile["name"])
        self.load_student()

    # ----- Tab 2: Study Planner -----

    def build_planner_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Study Planner")

        form = tk.Frame(tab)
        form.pack(pady=10)

        tk.Label(form, text="Subject:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.task_subject_entry = tk.Entry(form, width=25)
        self.task_subject_entry.grid(row=0, column=1, pady=3)

        tk.Label(form, text="Description:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.task_desc_entry = tk.Entry(form, width=25)
        self.task_desc_entry.grid(row=1, column=1, pady=3)

        tk.Label(form, text="Due Date (DD-MM-YYYY):").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.task_date_entry = tk.Entry(form, width=25)
        self.task_date_entry.grid(row=2, column=1, pady=3)

        tk.Button(form, text="Add Task", command=self.add_task_clicked).grid(
            row=3, column=0, columnspan=2, pady=8)

        self.task_listbox = tk.Listbox(tab, width=75, height=10)
        self.task_listbox.pack(pady=5)

        button_row = tk.Frame(tab)
        button_row.pack()
        tk.Button(button_row, text="Refresh List", command=self.refresh_tasks).pack(side="left", padx=5)
        tk.Button(button_row, text="Mark Selected Done", command=self.complete_task_clicked).pack(side="left", padx=5)
        tk.Button(button_row, text="Delete Selected", command=self.delete_task_clicked).pack(side="left", padx=5)

    def add_task_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        subject = self.task_subject_entry.get().strip()
        description = self.task_desc_entry.get().strip()
        due_date = self.task_date_entry.get().strip()

        task = study_planner.add_task(roll_no, subject, description, due_date)
        if task is None:
            messagebox.showerror(
                "Error",
                "Could not add task.\nMake sure subject and description are filled in, "
                "and the date is in DD-MM-YYYY format."
            )
            return

        # clear the boxes so it's ready for the next task
        self.task_subject_entry.delete(0, tk.END)
        self.task_desc_entry.delete(0, tk.END)
        self.task_date_entry.delete(0, tk.END)
        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        roll_no = self.roll_no_var.get().strip()
        if roll_no == "":
            return

        tasks = study_planner.list_tasks(roll_no)
        for t in tasks:
            line = "[" + t["task_id"] + "] (" + t["status"] + ") " + t["subject"] + \
                   " - " + t["description"] + " due " + t["due_date"]
            self.task_listbox.insert(tk.END, line)

    def get_selected_task_id(self):
        # Get the task ID from the selected list item.
        selection = self.task_listbox.curselection()
        if len(selection) == 0:
            messagebox.showerror("Error", "Please select a task from the list first.")
            return None

        line = self.task_listbox.get(selection[0])
        task_id = line.split("]")[0].replace("[", "")
        return task_id

    def complete_task_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        task_id = self.get_selected_task_id()
        if task_id is None:
            return

        result = study_planner.complete_task(roll_no, task_id)
        if result is not None:
            updated = achievements.award_task_completion(roll_no)
            messagebox.showinfo(
                "Task Completed",
                "Nice work! XP is now " + updated["xp"] + " (Level " + updated["level"] + ")"
            )
            self.refresh_tasks()
            self.load_student()

    def delete_task_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        task_id = self.get_selected_task_id()
        if task_id is None:
            return

        study_planner.delete_task(roll_no, task_id)
        self.refresh_tasks()

    # ----- Tab 3: Test Tracker -----

    def build_tracker_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Test Tracker")

        form = tk.Frame(tab)
        form.pack(pady=10)

        tk.Label(form, text="Subject:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.score_subject_entry = tk.Entry(form, width=25)
        self.score_subject_entry.grid(row=0, column=1, pady=3)

        tk.Label(form, text="Test Name:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.score_test_name_entry = tk.Entry(form, width=25)
        self.score_test_name_entry.grid(row=1, column=1, pady=3)

        tk.Label(form, text="Marks Obtained:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.score_marks_entry = tk.Entry(form, width=25)
        self.score_marks_entry.grid(row=2, column=1, pady=3)

        tk.Label(form, text="Max Marks:").grid(row=3, column=0, sticky="e", padx=5, pady=3)
        self.score_max_marks_entry = tk.Entry(form, width=25)
        self.score_max_marks_entry.grid(row=3, column=1, pady=3)

        tk.Label(form, text="Date (DD-MM-YYYY):").grid(row=4, column=0, sticky="e", padx=5, pady=3)
        self.score_date_entry = tk.Entry(form, width=25)
        self.score_date_entry.grid(row=4, column=1, pady=3)

        tk.Button(form, text="Add Score", command=self.add_score_clicked).grid(
            row=5, column=0, columnspan=2, pady=8)

        self.score_listbox = tk.Listbox(tab, width=75, height=8)
        self.score_listbox.pack(pady=5)

        tk.Button(tab, text="Refresh List", command=self.refresh_scores).pack(pady=5)

    def add_score_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        subject = self.score_subject_entry.get().strip()
        test_name = self.score_test_name_entry.get().strip()
        marks = self.score_marks_entry.get().strip()
        max_marks = self.score_max_marks_entry.get().strip()
        date_taken = self.score_date_entry.get().strip()

        score = test_tracker.add_score(roll_no, subject, test_name, marks, max_marks, date_taken)
        if score is None:
            messagebox.showerror(
                "Error",
                "Could not add score.\nCheck all fields are filled in, marks are not more "
                "than max marks, and the date is in DD-MM-YYYY format."
            )
            return

        updated = achievements.award_test_result(roll_no, float(marks), float(max_marks))
        messagebox.showinfo(
            "Score Added",
            "Score recorded! XP is now " + updated["xp"] + " (Level " + updated["level"] + ")"
        )

        self.score_subject_entry.delete(0, tk.END)
        self.score_test_name_entry.delete(0, tk.END)
        self.score_marks_entry.delete(0, tk.END)
        self.score_max_marks_entry.delete(0, tk.END)
        self.score_date_entry.delete(0, tk.END)

        self.refresh_scores()
        self.load_student()

    def refresh_scores(self):
        self.score_listbox.delete(0, tk.END)
        roll_no = self.roll_no_var.get().strip()
        if roll_no == "":
            return

        scores = test_tracker.list_scores(roll_no)
        for s in scores:
            line = s["date"] + " | " + s["subject"] + " | " + s["test_name"] + " | " + \
                   s["marks"] + "/" + s["max_marks"]
            self.score_listbox.insert(tk.END, line)

    # ----- Tab 4: Performance -----

    def build_performance_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Performance")

        tk.Button(tab, text="Show Performance", command=self.show_performance).pack(pady=10)

        self.performance_text = tk.Text(tab, width=75, height=20)
        self.performance_text.pack(pady=5)

    def show_performance(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        profile = student.get_profile(roll_no)
        if profile is None:
            messagebox.showerror("Error", "No profile found for that roll number.")
            return

        average = performance.overall_average(roll_no)
        trend = performance.trend(roll_no)
        subject_avgs = performance.subject_averages(roll_no)
        weak = performance.weak_subjects(roll_no)

        lines = []
        lines.append("Overall average: " + str(average) + "%")
        lines.append("Trend: " + trend)
        lines.append("")
        lines.append("Subject averages:")
        if len(subject_avgs) == 0:
            lines.append("  (no test scores recorded yet)")
        else:
            for subject in subject_avgs:
                lines.append("  - " + subject + ": " + str(subject_avgs[subject]) + "%")
        lines.append("")
        if len(weak) == 0:
            lines.append("Weak subjects: none")
        else:
            lines.append("Weak subjects: " + ", ".join(weak))

        self.performance_text.delete("1.0", tk.END)
        self.performance_text.insert(tk.END, "\n".join(lines))

    # ----- Tab 5: Achievements -----

    def build_achievements_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Achievements")

        tk.Button(tab, text="Show XP and Badges", command=self.show_achievements).pack(pady=10)

        self.achievements_text = tk.Text(tab, width=75, height=20)
        self.achievements_text.pack(pady=5)

    def show_achievements(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        profile = student.get_profile(roll_no)
        if profile is None:
            messagebox.showerror("Error", "No profile found for that roll number.")
            return

        badges = achievements.list_badges(roll_no)

        lines = []
        lines.append(profile["name"] + " - " + profile["xp"] + " XP, Level " + profile["level"])
        lines.append("")
        lines.append("Badges earned:")
        if len(badges) == 0:
            lines.append("  none yet")
        else:
            for b in badges:
                lines.append("  - " + b)

        self.achievements_text.delete("1.0", tk.END)
        self.achievements_text.insert(tk.END, "\n".join(lines))

    # ----- Tab 6: Report -----

    def build_report_tab(self, notebook):
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Report")

        button_row = tk.Frame(tab)
        button_row.pack(pady=10)
        tk.Button(button_row, text="Generate Report", command=self.show_report).pack(side="left", padx=5)
        tk.Button(button_row, text="Save Report to File", command=self.save_report_clicked).pack(side="left", padx=5)

        self.report_text = tk.Text(tab, width=75, height=20)
        self.report_text.pack(pady=5)

    def show_report(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        profile = student.get_profile(roll_no)
        if profile is None:
            messagebox.showerror("Error", "No profile found for that roll number.")
            return

        report = reports.build_report(roll_no)
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, report)

    def save_report_clicked(self):
        roll_no = self.get_roll_no()
        if roll_no is None:
            return

        profile = student.get_profile(roll_no)
        if profile is None:
            messagebox.showerror("Error", "No profile found for that roll number.")
            return

        file_path = reports.save_report(roll_no)
        messagebox.showinfo("Saved", "Report saved to " + file_path)


# this makes sure the window only opens when we run this file directly
# (not when gui.py is imported by something else)
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentQuestApp(root)
    root.mainloop()
