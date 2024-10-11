from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import threading
import time

# Create the database connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_username',  # Change this
        password='your_password',  # Change this
        database='todo_list'
    )

# Validate date format
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")  # Change format as necessary
        return True
    except ValueError:
        return False


# Function to set a reminder
def set_reminder(task_name, estimated_time, reminder_time):
    total_time_in_minutes = estimated_time * 60  # Convert estimated time to minutes
    reminder_time_in_minutes = reminder_time * 60  # Convert reminder time to minutes
    
    # Notify user when there's 1 hour and 2 hours left
    for i in range(reminder_time_in_minutes, total_time_in_minutes, 60):  # Check every hour
        time.sleep(60)  # Sleep for one minute before checking again
        
        time_left = (total_time_in_minutes - i) / 60  # Calculate remaining time in hours
        if time_left in [1, 2]:  # Notify when 1 or 2 hours are left
            messagebox.showinfo("Reminder", f"Reminder: {time_left} hour(s) remaining for task: {task_name}.")
    
    # Final notification when the task is due
    time.sleep((total_time_in_minutes - reminder_time_in_minutes) * 60)  # Wait until task is due
    messagebox.showinfo("Reminder", f"Reminder: {task_name} is due!")


# Function to add a task
def add_task():
    task_name = AddTask.get()
    due_date = AddDate.get()
    priority_level = AddPrio.get()
    estimated_time = EstimatedTime.get()  # Get estimated time in hours
    reminder_time = ReminderTime.get()  # Get reminder time in hours
    sub_task = SubTask.get()
    description = DescOfTask.get()
    notes = NotesOfTask.get()

    # Mandatory field checks
    if not task_name or not due_date or not priority_level or not estimated_time or not reminder_time or not sub_task or not description or not notes:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    if not priority_level.isdigit() or not estimated_time.isdigit() or not reminder_time.isdigit():
        messagebox.showerror("Error", "Priority Level, Estimated Time, and Reminder Time must be numbers!")
        return

    if not validate_date(due_date):
        messagebox.showerror("Error", "Due Date must be in the format YYYY-MM-DD!")
        return

    estimated_time = int(estimated_time)
    reminder_time = int(reminder_time)

    if reminder_time >= estimated_time:
        messagebox.showerror("Error", "Reminder Time must be less than Estimated Time!")
        return

    # Clear fields after validation
    AddTask.delete(0, END)
    AddDate.delete(0, END)
    AddPrio.delete(0, END)
    EstimatedTime.delete(0, END)
    ReminderTime.delete(0, END)
    SubTask.delete(0, END)
    DescOfTask.delete(0, END)
    NotesOfTask.delete(0, END)

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO tasks (task_name, due_date, priority_level, estimated_time, sub_task, description, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (task_name, due_date, priority_level, estimated_time, sub_task, description, notes))
        conn.commit()
        messagebox.showinfo("Success", "Task added successfully!")

        # Calculate reminder time in minutes
        reminder_time_in_minutes = (estimated_time - reminder_time) * 60
        threading.Thread(target=set_reminder, args=(task_name, reminder_time_in_minutes)).start()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to remove a task
def remove_task():
    task_name = AddTask.get()
    if not task_name:
        messagebox.showerror("Error", "Please enter a Task Name to remove!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_name = %s", (task_name,))
        conn.commit()
        messagebox.showinfo("Success", "Task removed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to see all tasks
def see_all_tasks():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        task_list = "\n".join([f"{task[1]} - Due: {task[2]} - Priority: {task[3]}" for task in tasks])
        messagebox.showinfo("All Tasks", task_list if task_list else "No tasks available.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to sort tasks (by priority)
def sort_tasks():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY priority_level")
        tasks = cursor.fetchall()
        task_list = "\n".join([f"{task[1]} - Due: {task[2]} - Priority: {task[3]}" for task in tasks])
        messagebox.showinfo("Sorted Tasks", task_list if task_list else "No tasks available.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to update a task
def update_task():
    task_name = AddTask.get()
    new_due_date = AddDate.get()

    if not task_name:
        messagebox.showerror("Error", "Please enter a Task Name to update!")
        return
    if not new_due_date:
        messagebox.showerror("Error", "New Due Date cannot be empty!")
        return
    if not validate_date(new_due_date):
        messagebox.showerror("Error", "New Due Date must be in the format YYYY-MM-DD!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET due_date = %s WHERE task_name = %s", (new_due_date, task_name))
        conn.commit()
        messagebox.showinfo("Success", "Task updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to track progress (count tasks)
def track_progress():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        messagebox.showinfo("Task Progress", f"You have {count} task(s) in total.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to search for a task
def search_task():
    task_name = AddTask.get()
    if not task_name:
        messagebox.showerror("Error", "Please enter a Task Name to search!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE task_name = %s", (task_name,))
        task = cursor.fetchone()
        if task:
            messagebox.showinfo("Task Found", f"Task: {task[1]}\nDue: {task[2]}\nPriority: {task[3]}\nSub-task: {task[4]}\nDescription: {task[5]}\nEstimated Time: {task[6]}\nNotes: {task[7]}")
        else:
            messagebox.showinfo("Task Not Found", "No task found with that name.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# GUI Setup
root = Tk()
root.title("To Do List")
root.geometry("800x400+50+50")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

Label(root, text="To DO List", font=('Comic Sans MS', 15, 'bold'), bg='#f0f0f0').place(x=350, y=10)

# Entry fields
labels = ["Task Name", "Due Date (YYYY-MM-DD)", "Priority Level", "Estimated Time (in hours)", "Reminder Time (in hours)", "Sub Task", "Description", "Add Notes"]
entries = []
for i, label in enumerate(labels):
    Label(root, text=label, font=('Comic Sans MS', 9, 'bold')).place(x=70 if i < 4 else 420, y=50 + (i % 4) * 70)
    entry = Entry(root, font=('Comic Sans MS', 9, 'bold'), bg='#f0f0f0')
    entry.place(x=170 if i < 4 else 520, y=80 + (i % 4) * 70)
    entries.append(entry)

AddTask, AddDate, AddPrio, EstimatedTime, ReminderTime, SubTask, DescOfTask, NotesOfTask = entries

# Buttons
Button(root, text="Add", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=add_task).place(x=50, y=340)
Button(root, text="Remove", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=remove_task).place(x=120, y=340)
Button(root, text="See All Tasks", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=see_all_tasks).place(x=210, y=340)
Button(root, text="Sort Tasks", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=sort_tasks).place(x=330, y=340)
Button(root, text="Update Tasks", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=update_task).place(x=430, y=340)
Button(root, text="Track Progress", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=track_progress).place(x=550, y=340)
Button(root, text="Search Task", font=('Comic Sans MS', 9, 'bold'), bg="#f0f0f0", command=search_task).place(x=680, y=340)

root.mainloop()
