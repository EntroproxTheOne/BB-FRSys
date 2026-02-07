import mysql.connector
from app import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Fix image paths - remove /static prefix since Flask serves static files from /
cursor.execute("UPDATE events SET image_url='/images/Picture1.jpg' WHERE name='TSPARK'")
print(f"Fixed TSPARK image: {cursor.rowcount} rows")

cursor.execute("UPDATE events SET image_url='/images/Picture2.png' WHERE name='ZEPHYR 2025'")
print(f"Fixed ZEPHYR 2025 image: {cursor.rowcount} rows")

cursor.execute("UPDATE events SET image_url='/images/Picture3.jpg' WHERE name='SOJOURN'")
print(f"Fixed SOJOURN image: {cursor.rowcount} rows")

conn.commit()
cursor.close()
conn.close()
print("All image paths fixed!")
