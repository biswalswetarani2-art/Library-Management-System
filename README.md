📚 Library Management System (LMS)
A lightweight, web-based Library Management System built with Python (Flask), HTML/CSS, and SQLite. This application helps librarians manage book inventories and track issued/returned books through a clean dashboard interface.

🚀 Features
Dashboard: Real-time statistics (Total Books, Active Issues) and recent transaction history.

Book Management: Add new books with details (Title, Author, Category, Quantity).

Issue/Return System:

Issue books to students (auto-decrements stock).

Return books (auto-increments stock and updates status).

Database: Uses SQLite (built-in) for zero-configuration data storage.

Responsive UI: Clean, sidebar-based layout using custom CSS.

🛠️ Prerequisites
Before running the project, ensure you have Python installed. You will also need the Flask framework.

Bash

pip install flask
📂 Project Structure
Ensure your folders are organized exactly like this:

Plaintext

library_system/
│
├── app.py                # Main application entry point (Backend logic)
├── README.md             # Project documentation
│
├── static/
│   └── style.css         # Styling for the dashboard
│
└── templates/
    ├── base.html         # Master layout with Sidebar navigation
    ├── dashboard.html    # Home page with stats
    ├── books.html        # Page to Add and View books
    └── issue.html        # Page to Issue or Return books
⚙️ Installation & Setup
Clone or Download this repository to your local machine.

Navigate to the project folder in your terminal:

Bash

cd library_system
Run the Application:

Bash

python app.py
Note: The first time you run this, it will automatically create the library.db database file.

Access the Dashboard: Open your web browser and go to: http://127.0.0.1:5000/

📖 How to Use
Dashboard: Check the overview of your library stats.

Manage Books: Click the tab to add new books. Enter the Title, Author, Category, and Quantity.

Issue Book:

Go to "Issue / Return".

Enter the Book ID (found in the "Manage Books" list) and the Student Name.

Click "Issue Book".

Return Book:

Find the Transaction ID in the "Currently Issued Books" table.

Enter that ID in the "Return a Book" section.

Click "Return Book".

🛡️ Future Improvements
Add User Authentication (Login/Signup for Librarian).

Add a Search Bar for books and students.

Add "Due Dates" and fine calculation logic.
