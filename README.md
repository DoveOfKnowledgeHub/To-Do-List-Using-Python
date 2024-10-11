# To-Do-List-Using-Python-And-MySQL 


This To-Do List application is designed to help users efficiently manage their tasks through a user-friendly interface built with Tkinter. Users can add, update, remove, and view tasks, each accompanied by important details such as due dates, priority levels, and descriptions. The application integrates with a MySQL database for persistent storage, allowing for seamless retrieval and management of tasks. Additionally, it features a reminder system that notifies users as deadlines approach, ensuring timely completion. With the ability to track progress and sort tasks by priority, this application provides a comprehensive solution for effective task management.

 Before running the application, ensure that all necessary modules are installed as outlined in the requirements.txt file.

 To set up the project, follow these essential steps:

1. Create a database named "todo_list".
2. Within this database, establish a table called "tasks".

use this code to create the table under the "todo_list" database

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    due_date DATE NOT NULL,
    priority_level INT NOT NULL,
    estimated_time INT NOT NULL,
    sub_task VARCHAR(255),
    description TEXT,
    notes TEXT  
);

# OUPUT

![Screenshot 2024-10-11 150844](https://github.com/user-attachments/assets/b58e073b-0d4e-42a6-991e-15549d5d5922)
