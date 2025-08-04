This is a simple full-stack web application that simulates a **flight ticket booking system**. Built using Python Flask, HTML/CSS, and MySQL, users can input flight information and receive a **fake ticket**.

---

## About the Project

This project was created to practice full-stack web development skills and simulate a basic booking system. It's ideal for beginners learning how front-end forms connect to back-end logic and how databases handle user data.

---

## Features

-  Homepage with custom UI
-  Flight info form (name, destination, date, etc.)
-  Stores data in MySQL database
-  Generates a fake ticket after form submission
-  Styled with HTML and CSS

---

## Tech Stack

| Tech      | Role                   |
|-----------|------------------------|
| Flask     | Backend web framework  |
| MySQL     | Relational database    |
| HTML/CSS  | Frontend interface     |

---

##  How to Run This Project Locally

### Prerequisites

- Python 3 installed
- MySQL server running
- Git (optional but helpful)

### Setup Steps
Clone the repository:
   ```bash
   git clone https://github.com/Morenikeji-Olowo/Python-Flask-Flight-Booking-System

Install dependencies:

bash
Copy
Edit
pip install flask mysql-connector-python
Set up the database:

Open MySQL

Create a database (e.g., flight_system)

Import the included .sql file (if provided)

Update database config in app.py:

python
Copy
Edit
mydb = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",
    database="flight_system"
)
Run the Flask server:

bash
Copy
Edit
python app.py
Open the app in your browser:


=
