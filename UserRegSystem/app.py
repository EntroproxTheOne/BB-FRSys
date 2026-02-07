from flask import Flask, request, jsonify, send_file
import mysql.connector
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server
import matplotlib.pyplot as plt
import io
import hashlib

app = Flask(__name__, static_folder='static', static_url_path='')

# --- DATABASE CONFIG ---
# UPDATE THESE VALUES TO MATCH YOUR LOCAL MYSQL SETUP
DB_CONFIG = {
    'host': 'localhost',
    'port': 6767,  # User specified port
    'user': 'root',
    'password': 'root', # User confirmed password
    'database': 'user_reg_db',
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    # Simple hash (for demonstration - use bcrypt/argon2 in production)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        return jsonify({'success': True, 'message': 'User registered successfully'})
    except mysql.connector.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'}), 409
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500

    cursor = conn.cursor(dictionary=True)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT id FROM users WHERE username = %s AND password_hash = %s", (username, password_hash))
    user = cursor.fetchone()

    if user:
        # Log the login
        cursor.execute("INSERT INTO logins (user_id) VALUES (%s)", (user['id'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Login successful', 'user_id': user['id']})
    else:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/stats/registrations.png')
def registration_stats():
    conn = get_db_connection()
    if not conn:
        return "Database Error", 500
    
    cursor = conn.cursor()
    # Get registrations by date
    cursor.execute("SELECT DATE(created_at) as date, COUNT(*) as count FROM users GROUP BY DATE(created_at) ORDER BY date ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    dates = [str(r[0]) for r in results]
    counts = [r[1] for r in results]

    # Plotting
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.bar(dates, counts, color='#39ff14', edgecolor='black')
    plt.xlabel('Date', color='white')
    plt.ylabel('New Registrations', color='white')
    plt.title('Daily User Registrations', color='#39ff14', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    plt.grid(color='#333', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True)
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Ensure you have updated DB_CONFIG in app.py with your MySQL password.")
    app.run(debug=True, port=5000)
