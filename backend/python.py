from database import get_db

conn = get_db()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO auctions (id, commit_deadline, reveal_deadline, status)
VALUES (1, '2026-12-31T23:59:59', '2026-12-31T23:59:59', 'active')
""")

conn.commit()
conn.close()