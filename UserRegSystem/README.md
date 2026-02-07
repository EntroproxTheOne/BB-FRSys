# TCETReg - Event Registration System

A modern web application for event registration and user analytics, built with Flask, MySQL, and Python Matplotlib.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Installation and Setup](#installation-and-setup)
8. [Usage Guide](#usage-guide)
9. [Screenshots](#screenshots)

---

## Overview

TCETReg is a full-stack web application that enables users to:

- Register and login to the platform
- Browse and register for live events
- View real-time registration statistics through dynamic charts

The application features a clean, modern UI with a Blue-Gold-White color scheme and responsive design.

---

## Features

### User Authentication

- **User Registration**: New users can create accounts with username and password
- **User Login**: Secure login with password hashing (SHA-256)
- **Session Management**: Persistent login sessions using localStorage
- **Logout**: Clean session termination

### Event Management

- **Live Events Display**: Three dynamic event cards with hover animations
- **Event Registration**: Logged-in users can register for events
- **Toggle Registration**: Users can unregister from events
- **Registration Counter**: Real-time display of registration counts per event

### Data Visualization (Matplotlib)

- **Event Registration Statistics**: Horizontal bar chart showing registrations per event
- **Daily User Registrations**: Bar chart showing user signups over time
- **Dynamic Refresh**: Charts update on button click
- **Light Theme**: Charts styled to match the website's color scheme

### UI/UX Features

- **Dynamic Event Cards**: Perspective transforms with skew effects
- **Hover Animations**: Cards enlarge and glow on hover
- **Gradient Text**: "Live Events" header with blue-gold gradient
- **Toast Notifications**: User feedback for all actions
- **Responsive Design**: Mobile-friendly layout

---

## Technologies Used

### Backend

| Technology | Purpose |
|------------|---------|
| **Python 3** | Backend programming language |
| **Flask** | Web framework for routing and API |
| **MySQL** | Relational database for data storage |
| **mysql-connector-python** | Database connectivity |
| **Matplotlib** | Chart generation for statistics |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure and semantics |
| **CSS3** | Styling with custom properties (variables) |
| **JavaScript (ES6)** | Client-side interactivity and API calls |
| **Google Fonts** | Inter and Outfit font families |

### Database

| Technology | Purpose |
|------------|---------|
| **MySQL** | Data persistence |
| **SQL** | Database schema and queries |

---

## Project Structure

```
UserRegSystem/
├── app.py                 # Main Flask application
├── init_db.py             # Database initialization script
├── database_setup.sql     # SQL schema definitions
├── requirements.txt       # Python dependencies
├── static/
│   ├── index.html         # Main HTML page
│   ├── style.css          # All CSS styles
│   ├── script.js          # JavaScript logic
│   └── images/            # Event images
│       ├── Picture1.jpg   # TSPARK event image
│       ├── Picture2.png   # ZEPHYR 2025 event image
│       └── Picture3.jpg   # SOJOURN event image
└── images/                # Source images folder
```

---

## Database Schema

### Tables

#### users

| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| username | VARCHAR(50) | Unique username |
| password_hash | VARCHAR(255) | SHA-256 hashed password |
| created_at | TIMESTAMP | Registration timestamp |

#### logins

| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| user_id | INT (FK) | Reference to users.id |
| login_time | TIMESTAMP | Login timestamp |

#### events

| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| name | VARCHAR(100) | Event name |
| description | TEXT | Event description |
| image_url | VARCHAR(255) | Path to event image |
| event_date | DATE | Event date |
| created_at | TIMESTAMP | Creation timestamp |

#### event_registrations

| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| user_id | INT (FK) | Reference to users.id |
| event_id | INT (FK) | Reference to events.id |
| registered_at | TIMESTAMP | Registration timestamp |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/register` | Register new user | `{username, password}` |
| POST | `/login` | User login | `{username, password}` |

### Events

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/events` | Get all events with counts | - |
| POST | `/api/events/register` | Register for event | `{user_id, event_id}` |
| POST | `/api/events/unregister` | Unregister from event | `{user_id, event_id}` |
| GET | `/api/user/<id>/registrations` | Get user's registrations | - |

### Statistics (Matplotlib Charts)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/registrations.png` | Daily user registration chart |
| GET | `/stats/event_registrations.png` | Event registration statistics |

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MySQL Server (running on port 6767)
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements include:

- Flask
- mysql-connector-python
- matplotlib

### Step 2: Configure Database

Edit `app.py` and update the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 6767,          # Your MySQL port
    'user': 'root',
    'password': 'your_password',
    'database': 'user_reg_db',
}
```

### Step 3: Initialize Database

```bash
python init_db.py
```

This creates all tables and seeds 3 sample events.

### Step 4: Run the Application

```bash
python app.py
```

The server starts at `http://localhost:5000`

---

## Usage Guide

### Home Page

1. Open `http://localhost:5000` in your browser
2. View the three live events: ZEPHYR 2025, SOJOURN, and TSPARK
3. Hover over event cards to see animation effects
4. Scroll down to view registration statistics

### Registration and Login

1. Click "Register" in the navigation
2. Enter a username and password
3. After registration, login with your credentials
4. You'll be redirected to the home page

### Event Registration

1. Login to your account
2. Click "Register" on any event card
3. The button changes to "Registered" with a checkmark
4. Click again to unregister
5. Registration counts update in real-time

### Viewing Statistics

1. Scroll to the "Registration Statistics" section
2. View the bar chart showing registrations per event
3. Click "Refresh Stats" to update the chart

---

## Color Scheme

| Element | Color | Hex Code |
|---------|-------|----------|
| Background | White | #ffffff |
| Cards | Light Gray | #f8f9fa |
| Primary (Blue) | Royal Blue | #1a5fb4 |
| Secondary (Gold) | Gold Yellow | #ffc107 |
| Text | Dark | #1a1a2e |
| Muted Text | Gray | #6c757d |

---

## Sample Events

| Event | Description | Date |
|-------|-------------|------|
| ZEPHYR 2025 | Tech fest with coding competitions and hackathons | March 15, 2025 |
| SOJOURN | Cultural extravaganza with music and dance | April 20, 2025 |
| TSPARK | Inter-college sports championship | May 10, 2025 |

---

## Key Code Syntax Examples

### Python (Flask Route)

```python
@app.route('/api/events')
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return jsonify({'success': True, 'events': events})
```

### JavaScript (Fetch API)

```javascript
async function loadEvents() {
    const response = await fetch('/api/events');
    const data = await response.json();
    if (data.success) {
        renderEvents(data.events);
    }
}
```

### SQL (Table Creation)

```sql
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    event_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CSS (Custom Properties)

```css
:root {
    --bg-color: #ffffff;
    --primary: #1a5fb4;
    --secondary: #ffc107;
    --text-main: #1a1a2e;
}
```

---

## Security Notes

- Passwords are hashed using SHA-256 (for demonstration)
- For production, use bcrypt or Argon2
- Session management uses client-side localStorage
- API endpoints validate required parameters

---

## Credits

Developed as part of IP 2026 Project at TCET.
