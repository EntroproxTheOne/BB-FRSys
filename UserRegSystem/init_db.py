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
        cursor.close()
        conn.close()
        print("Database initialization complete!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("\nNOTE: Please make sure you have updated the 'password' in app.py to match your local MySQL setup.")

if __name__ == "__main__":
    init_db()
