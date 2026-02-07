import mysql.connector
from app import DB_CONFIG

def init_db():
    print("Attempting to connect to MySQL to create database and tables...")
    
    # Connect to MySQL server (without selecting DB first to create it)
    try:
        # Create a copy of config without the database name to connect to server
        server_config = DB_CONFIG.copy()
        db_name = server_config.pop('database')
        
        conn = mysql.connector.connect(**server_config)
        cursor = conn.cursor()
        
        print(f"Connected to MySQL. Creating database '{db_name}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.close()
        
        # Now connect to the database to create tables
        print(f"Connecting to database '{db_name}'...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Read SQL file
        with open('database_setup.sql', 'r') as f:
            sql_script = f.read()
            
        # Execute SQL script (split by commands)
        commands = sql_script.split(';')
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Specific command failed (might be okay if 'IF NOT EXISTS'): {err}")

        conn.commit()
        
        # Seed sample events if they don't exist
        print("Seeding sample events...")
        sample_events = [
            ("ZEPHYR 2025", "The ultimate tech fest featuring coding competitions, hackathons, and innovation showcases. Join us for 3 days of tech excellence!", "/images/Picture2.png", "2025-03-15"),
            ("SOJOURN", "Annual cultural extravaganza with music, dance, and theatrical performances. Experience the magic of art and culture!", "/images/Picture3.jpg", "2025-04-20"),
            ("TSPARK", "Inter-college sports championship featuring cricket, football, basketball, and more. Show your athletic prowess!", "/images/Picture1.jpg", "2025-05-10")
        ]
        
        for event in sample_events:
            try:
                cursor.execute(
                    "INSERT INTO events (name, description, image_url, event_date) VALUES (%s, %s, %s, %s)",
                    event
                )
            except mysql.connector.IntegrityError:
                pass  # Event already exists
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialization complete!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("\nNOTE: Please make sure you have updated the 'password' in app.py to match your local MySQL setup.")

if __name__ == "__main__":
    init_db()
