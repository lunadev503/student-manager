import sqlite3
import tkinter as tk
from tkinter import messagebox


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

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM student_id WHERE id = ?",
            (student_id,)
        )

        self.conn.commit()

    def close(self):
        self.conn.close()


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

    def delete_student(self, student_id):
        self.db.delete_student(student_id)

    def close(self):
        self.db.close()


# ======================
# GUI
# ======================

class GUI:
    def __init__(self):
        self.manager = StudentManager()

        self.window = tk.Tk()
        self.window.title("Luna Student Manager")
        self.window.geometry("700x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # INPUT FRAME
        input_frame = tk.Frame(self.window, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        # NAME
        self.name_label = tk.Label(
            input_frame,
            text="Name:"
        )
        self.name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.name_entry = tk.Entry(
            input_frame,
            width=30
        )
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # AGE
        self.age_label = tk.Label(
            input_frame,
            text="Age:"
        )
        self.age_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.age_entry = tk.Entry(
            input_frame,
            width=30
        )
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        # BUTTONS FRAME
        button_frame = tk.Frame(self.window, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        self.add_button = tk.Button(
            button_frame,
            text="Add Student",
            command=self.add_student,
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.view_button = tk.Button(
            button_frame,
            text="View Students",
            command=self.view_students,
            bg="#2196F3",
            fg="white",
            padx=10
        )
        self.view_button.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(
            button_frame,
            text="Search By Name",
            command=self.search_by_name,
            bg="#FF9800",
            fg="white",
            padx=10
        )
        self.search_button.grid(row=0, column=2, padx=5)

        self.count_button = tk.Button(
            button_frame,
            text="Count Users",
            command=self.count_users,
            bg="#9C27B0",
            fg="white",
            padx=10
        )
        self.count_button.grid(row=0, column=3, padx=5)

        self.delete_button = tk.Button(
            button_frame,
            text="Delete Student",
            command=self.delete_student,
            bg="#F44336",
            fg="white",
            padx=10
        )
        self.delete_button.grid(row=0, column=4, padx=5)

        # STATUS
        self.status = tk.Label(
            self.window,
            text="",
            fg="blue"
        )
        self.status.pack()

        # RESULTS
        self.result_box = tk.Listbox(
            self.window,
            width=85,
            height=18
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
            self.status.config(text="❌ Fill all fields", fg="red")
            return

        try:
            age_int = int(age)
            if age_int < 0 or age_int > 120:
                self.status.config(text="❌ Age must be between 0 and 120", fg="red")
                return
        except ValueError:
            self.status.config(text="❌ Age must be a number", fg="red")
            return

        self.manager.add_student(name, age_int)

        self.status.config(text=f"✅ Added {name} (Age: {age_int})", fg="green")

        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def view_students(self):
        self.result_box.delete(0, tk.END)

        students = self.manager.view_students()

        if not students:
            self.result_box.insert(tk.END, "No students found")
            return

        self.result_box.insert(tk.END, "ID | Name | Age")
        self.result_box.insert(tk.END, "-" * 80)

        for student_id, name, age in students:
            self.result_box.insert(
                tk.END,
                f"{student_id:3} | {name:20} | {age}"
            )

    def search_by_name(self):
        self.result_box.delete(0, tk.END)

        name = self.name_entry.get()

        if not name:
            self.status.config(text="❌ Enter a name to search", fg="red")
            return

        results = self.manager.search_by_name(name)

        if not results:
            self.result_box.insert(tk.END, f"No students found with name: {name}")
            return

        self.result_box.insert(tk.END, "ID | Name | Age")
        self.result_box.insert(tk.END, "-" * 80)

        for student_id, name_result, age in results:
            self.result_box.insert(
                tk.END,
                f"{student_id:3} | {name_result:20} | {age}"
            )

    def count_users(self):
        total = self.manager.count_users()
        self.status.config(text=f"📊 Total Users: {total}", fg="blue")

    def delete_student(self):
        self.result_box.delete(0, tk.END)

        try:
            student_id = int(self.name_entry.get())
        except ValueError:
            self.status.config(text="❌ Enter a valid student ID to delete", fg="red")
            return

        self.manager.delete_student(student_id)
        self.status.config(text=f"✅ Deleted student with ID: {student_id}", fg="green")
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

    def on_closing(self):
        self.manager.close()
        self.window.destroy()


# ======================
# START APP
# ======================

if __name__ == "__main__":
    GUI()
