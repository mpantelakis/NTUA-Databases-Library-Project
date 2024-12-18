# **DBMS Semester Project - Spring 2023**

This project involves creating a system to store and manage all the necessary information for operating a **School Library** in a network of **Public Schools**. The system includes both **front-end** and **back-end** components. It was co-developed with [Enrica-Iliana Maggiori](https://github.com/ilianamaggiori).

---

## **Installation Instructions**

### **Step 1: Clone the Repository**
Download the project repository using the following command:
```bash
git clone <repository-url>

```
### Step 2: Install the Database and Import Dummy Data

- Install a **SQL server** (e.g., MySQL Server) and a **DBMS tool** (e.g., MySQL Workbench).
- Create a connection to the SQL server.
- Run the following SQL scripts in order, located in the SQL code folder:
    - semester_project_DDL.sql
    - triggers_events_DML.sql
    - semester_project_inserts_DML.sql

These scripts will create the necessary database structure, triggers, events, and populate the database with dummy data.

### Step 3: Launch the Application
1. Install the required libraries by running:
```bash
pip install -r requirements.txt
```
2. Run the application:
  - Use the command:
```bash
python3 run.py
```
Alternatively, use an IDE (e.g., Visual Studio Code) and run the run.py file.

3. Update the MySQL server credentials:
  - Open the __init__.py file in the library folder.
  - Replace the placeholder username and password with your MySQL server credentials.
  - Open a browser and navigate to:
    ```arduino
    http://localhost:3000
    ```
You should see the home page of the application.

### Features
- Comprehensive management of school library operations.
- Database design optimized for public school networks.
- User-friendly front-end and robust back-end.

### Technologies Used
- **Back-end:** MySQL, Python (Flask)
- **Front-end:** HTML, CSS
- **Database Management Tools:** MySQL Workbench, MySQL Server

