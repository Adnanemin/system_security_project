from database import get_db

conn = get_db()
cursor = conn.cursor()

cursor.execute("SELECT * FROM auctions")
print(cursor.fetchall())