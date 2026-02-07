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

    # Plotting - Light theme for white background
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    ax.bar(dates, counts, color='#1a5fb4', edgecolor='#ffc107')
    ax.set_xlabel('Date', color='#1a1a2e', fontweight='bold')
    ax.set_ylabel('New Registrations', color='#1a1a2e', fontweight='bold')
    ax.set_title('Daily User Registrations', color='#1a5fb4', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, color='#1a1a2e')
    plt.yticks(color='#1a1a2e')
    ax.grid(color='#dee2e6', linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor='#f8f9fa')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

# --- EVENT API ENDPOINTS ---

@app.route('/api/events')
def get_events():
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, 
               (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.id) as registration_count
        FROM events e
        ORDER BY e.event_date ASC
    """)
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert date objects to strings for JSON serialization
    for event in events:
        if event.get('event_date'):
            event['event_date'] = str(event['event_date'])
        if event.get('created_at'):
            event['created_at'] = str(event['created_at'])
    
    return jsonify({'success': True, 'events': events})

@app.route('/api/events/register', methods=['POST'])
def register_event():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    
    if not user_id or not event_id:
        return jsonify({'success': False, 'message': 'Missing user_id or event_id'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO event_registrations (user_id, event_id) VALUES (%s, %s)",
            (user_id, event_id)
        )
        conn.commit()
        return jsonify({'success': True, 'message': 'Registered successfully'})
    except mysql.connector.IntegrityError:
        return jsonify({'success': False, 'message': 'Already registered for this event'}), 409
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/events/unregister', methods=['POST'])
def unregister_event():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    
    if not user_id or not event_id:
        return jsonify({'success': False, 'message': 'Missing user_id or event_id'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM event_registrations WHERE user_id = %s AND event_id = %s",
            (user_id, event_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Unregistered successfully'})
        else:
            return jsonify({'success': False, 'message': 'Registration not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/<int:user_id>/registrations')
def get_user_registrations(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT event_id FROM event_registrations WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    event_ids = [r[0] for r in results]
    return jsonify({'success': True, 'event_ids': event_ids})

@app.route('/stats/event_registrations.png')
def event_registration_stats():
    conn = get_db_connection()
    if not conn:
        return "Database Error", 500
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.name, COUNT(er.id) as count 
        FROM events e 
        LEFT JOIN event_registrations er ON e.id = er.event_id 
        GROUP BY e.id, e.name 
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    event_names = [r[0] for r in results]
    counts = [r[1] for r in results]

    # Plotting - Light theme for white background
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Create gradient colors - Blue-Gold theme
    colors = ['#1a5fb4', '#3584e4', '#ffc107']
    bars = ax.barh(event_names, counts, color=colors[:len(event_names)], edgecolor='#1a5fb4', linewidth=2)
    
    # Add glow effect
    for bar in bars:
        bar.set_alpha(0.9)
    
    ax.set_xlabel('Number of Registrations', color='#1a1a2e', fontsize=12, fontweight='bold')
    ax.set_ylabel('Events', color='#1a1a2e', fontsize=12, fontweight='bold')
    ax.set_title('Event Registration Statistics', color='#1a5fb4', fontsize=16, fontweight='bold')
    ax.tick_params(colors='#1a1a2e')
    ax.grid(color='#dee2e6', linestyle='--', linewidth=0.5, axis='x')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#dee2e6')
    ax.spines['bottom'].set_color('#dee2e6')
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', color='#1a5fb4', fontweight='bold', fontsize=14)
    
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor='#f8f9fa', dpi=100)
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Ensure you have updated DB_CONFIG in app.py with your MySQL password.")
    app.run(debug=True, port=5000)
