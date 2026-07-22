from app.config.db_config import conn

def obtener_todos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cuidado_adultos_mayores")
    registros = cursor.fetchall()
    return [{"id": r[0], "nombre_adulto": r[1], "edad": r[2], "condicion_medica": r[3], "ubicacion": r[4], "estado": r[5]} for r in registros]

def obtener_por_id(id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cuidado_adultos_mayores WHERE id = %s", (id,))
    r = cursor.fetchone()
    if r:
        return {"id": r[0], "nombre_adulto": r[1], "edad": r[2], "condicion_medica": r[3], "ubicacion": r[4], "estado": r[5]}
    return None

def crear(data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cuidado_adultos_mayores (nombre_adulto, edad, condicion_medica, ubicacion, estado)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """, (data.nombre_adulto, data.edad, data.condicion_medica, data.ubicacion, data.estado))
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    return obtener_por_id(nuevo_id)

def actualizar(id: int, data):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cuidado_adultos_mayores 
        SET nombre_adulto = %s, edad = %s, condicion_medica = %s, ubicacion = %s, estado = %s
        WHERE id = %s
    """, (data.nombre_adulto, data.edad, data.condicion_medica, data.ubicacion, data.estado, id))
    conn.commit()
    return obtener_por_id(id)

def eliminar(id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cuidado_adultos_mayores WHERE id = %s", (id,))
    conn.commit()
    return {"success": True, "message": "Registro eliminado exitosamente"}
