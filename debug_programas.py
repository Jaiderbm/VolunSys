from app.config.db_config import get_connection

conn = get_connection()
cur = conn.cursor()

print("=== programas_usuarios (all rows) ===")
cur.execute("SELECT * FROM programas_usuarios LIMIT 20")
rows = cur.fetchall()
for r in rows:
    print(r)

print("\n=== programas (all rows) ===")
cur.execute("SELECT * FROM programas LIMIT 20")
rows = cur.fetchall()
for r in rows:
    print(r)

cur.close()
conn.close()
