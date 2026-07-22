import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Schema de todas las tablas relevantes
for tabla in ["usuarios", "voluntariados", "inscripciones", "participaciones", "programas", "programas_usuarios"]:
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{tabla}' ORDER BY ordinal_position")
    cols = cur.fetchall()
    print(f"\nTabla '{tabla}':")
    for c in cols:
        print(f"  {c[0]} ({c[1]})")

cur.close()
conn.close()
