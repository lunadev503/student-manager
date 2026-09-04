import sqlite3
import tkinter as tk


# ======================
# Student
# ======================

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# ======================
# Database
# ======================

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("student_manager.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_id(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
        """)

        self.conn.commit()

    def add_student(self, student):
        self.cursor.execute(
            "INSERT INTO student_id(name, age) VALUES(?, ?)",
            (student.name, student.age)
        )

        self.conn.commit()

    def view_students(self):
        self.cursor.execute(
            "SELECT * FROM student_id"
        )

        return self.cursor.fetchall()

    def search_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM student_id WHERE name = ?",
            (name,)
        )

        return self.cursor.fetchall()

    def count_users(self):
        self.cursor.execute(
            "SELECT COUNT(*) FROM student_id"
        )

        return self.cursor.fetchone()[0]


# ======================
# Student Manager
# ======================

class StudentManager:
    def __init__(self):
        self.db = Database()

    def add_student(self, name, age):
        student = Student(name, age)
        self.db.add_student(student)

    def view_students(self):
        return self.db.view_students()

    def search_by_name(self, name):
        return self.db.search_by_name(name)

    def count_users(self):
        return self.db.count_users()


# ======================
# GUI
# ======================

class GUI:
    def __init__(self):
        self.manager = StudentManager()

        self.window = tk.Tk()
        self.window.title("Luna Student Manager")
        self.window.geometry("600x500")

        # NAME
        self.name_label = tk.Label(
            self.window,
            text="Name"
        )

        self.name_label.pack()

        self.name_entry = tk.Entry(
            self.window
        )

        self.name_entry.pack()

        # AGE
        self.age_label = tk.Label(
            self.window,
            text="Age"
        )

        self.age_label.pack()

        self.age_entry = tk.Entry(
            self.window
        )

        self.age_entry.pack()

        # BUTTONS

        self.add_button = tk.Button(
            self.window,
            text="Add Student",
            command=self.add_student
        )

        self.add_button.pack(pady=5)

        self.view_button = tk.Button(
            self.window,
            text="View Students",
            command=self.view_students
        )

        self.view_button.pack(pady=5)

        self.search_button = tk.Button(
            self.window,
            text="Search By Name",
            command=self.search_by_name
        )

        self.search_button.pack(pady=5)

        self.count_button = tk.Button(
            self.window,
            text="Count Users",
            command=self.count_users
        )

        self.count_button.pack(pady=5)

        # STATUS

        self.status = tk.Label(
            self.window,
            text=""
        )

        self.status.pack()

        # RESULTS

        self.result_box = tk.Listbox(
            self.window,
            width=70,
            height=15
        )

        self.result_box.pack(pady=10)

        self.window.mainloop()

    # ======================
    # GUI METHODS
    # ======================

    def add_student(self):

        name = self.name_entry.get()
        age = self.age_entry.get()

        if not name or not age:
            self.status.config(
                text="Fill all fields"
            )

            return

        self.manager.add_student(
            name,
            int(age)
        )

        self.status.config(
            text=f"Added {name}"
        )

        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def view_students(self):

        self.result_box.delete(
            0,
            tk.END
        )

        students = self.manager.view_students()

        for student in students:
            self.result_box.insert(
                tk.END,
                student
            )

    def search_by_name(self):

        self.result_box.delete(
            0,
            tk.END
        )

        name = self.name_entry.get()

        results = self.manager.search_by_name(
            name
        )

        for student in results:
            self.result_box.insert(
                tk.END,
                student
            )

    def count_users(self):

        total = self.manager.count_users()

        self.status.config(
            text=f"Total Users: {total}"
        )


# ======================
# START APP
# ======================

GUI()