import mysql.connector
from app import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Update Sports Fiesta to TSPARK
cursor.execute("UPDATE events SET name='TSPARK', image_url='/static/images/Picture1.jpg' WHERE name='Sports Fiesta'")
print(f"Updated Sports Fiesta -> TSPARK: {cursor.rowcount} rows")

# Update ZEPHYR image
cursor.execute("UPDATE events SET image_url='/static/images/Picture2.png' WHERE name='ZEPHYR 2025'")
print(f"Updated ZEPHYR 2025 image: {cursor.rowcount} rows")

# Update SOJOURN image
cursor.execute("UPDATE events SET image_url='/static/images/Picture3.jpg' WHERE name='SOJOURN'")
print(f"Updated SOJOURN image: {cursor.rowcount} rows")

conn.commit()
cursor.close()
conn.close()
print("All events updated successfully!")
