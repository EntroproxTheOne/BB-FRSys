# Project: User Registration and Analytics System

## Project Description

This project is a web-based application that allows users to register for an account and log in to a dashboard. The system securely stores user credentials and tracks registration activity over time. The dashboard features a dynamically generated chart that visualizes the number of user registrations per day. The application is built using a Python Flask backend, a MySQL database, and a responsive frontend using HTML, CSS, and JavaScript.

## Major Technologies Used

### 1. Python (Backend)

The backend logic is written in Python using the Flask micro-framework. It handles HTTP requests, communicates with the database, and generates analytical charts.

* **Flask Framework**: Used `Flask` to create the web server, define routes (`@app.route`), and handle JSON requests/responses (`jsonify`).
* **Database Connection**: Used `mysql.connector` to establish connections and execute SQL queries.
* **Data Visualization**: Used `matplotlib.pyplot` with the 'Agg' backend to generate registration statistics charts on the server without a GUI.
* **File Handling**: Used `io.BytesIO` to save the generated plot into memory and serve it directly to the frontend using `send_file`.
* **Security**: Implemented basic password hashing using `hashlib.sha256` ensures passwords are not stored in plain text.

### 2. Database (MySQL)

MySQL is used as the relational database management system to store user data and login logs.

* **Table Creation**: Created tables for `users` (storing usernames and hashed passwords) and `logins` (tracking login timestamps).
* **Data Insertion**: Used `INSERT INTO` statements to add new users upon registration.
* **Data Retrieval**: Used `SELECT` statements with `WHERE` clauses to verify credentials during login.
* **Aggregations**: Used `COUNT(*)` and `GROUP BY DATE(created_at)` to calculate daily registration statistics for the dashboard graph.

### 3. JavaScript (Frontend Logic)

JavaScript is used to make the application interactive and handle communication with the backend without reloading the page (Single Page Application feel).

* **Asynchronous Fetch API**: Used `async/await` with `fetch()` to send POST requests for login and registration to the Python backend.
* **DOM Manipulation**: Used `document.getElementById()` and `classList` methods to toggle visibility of different views (Login, Register, Dashboard).
* **Event Listeners**: Added `addEventListener` to handle form submissions and button clicks.

### 4. CSS (Styling)

Cascading Style Sheets are used to style the user interface, implementing a dark, high-contrast neon theme.

* **CSS Variables**: Defined color variables in `:root` (e.g., `--primary: #39ff14`) for consistent theming.
* **Flexbox Layout**: Extensively used `display: flex`, `justify-content`, and `align-items` to center elements and create responsive layouts.
* **Animations**: Created `@keyframes` for fade-in effects when switching between views.

### 5. HTML (Structure)

HTML5 is used to structure the content of the web pages.

* **Semantic Elements**: Used tags like `<header>`, `<main>`, `<section>`, and `<nav>` for better document structure.
* **Forms**: Implemented input fields for username and password with appropriate types (`text`, `password`) and validation attributes (`required`).

### 6. Git (Version Control)

Git is used to track changes in the codebase during development.

* **Commit**: Used `git commit` to save snapshots of the project progress.
* **Add**: Used `git add` to stage files for commit.
