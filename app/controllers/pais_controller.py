from app.config.db_config import get_connection

def crear_pais(nombre: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO paises (nombre) VALUES (%s) RETURNING id, nombre, estado;",
        (nombre,)
    )
    
    nuevo_pais = cursor.fetchone()
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {
        "id": nuevo_pais[0],
        "nombre": nuevo_pais[1],
        "estado": nuevo_pais[2]
    }

def listar_paises():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, estado FROM paises;")
    paises = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return [
        {"id": p[0], "nombre": p[1], "estado": p[2]}
        for p in paises
    ]
