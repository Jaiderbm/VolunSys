from app.config.db_config import conn

def obtener_todos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM limpieza_playas")
    registros = cursor.fetchall()
    return [{"id": r[0], "nombre_playa": r[1], "ubicacion": r[2], "cantidad_basura_estimada_kg": r[3], "estado": r[4]} for r in registros]

def obtener_por_id(id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM limpieza_playas WHERE id = %s", (id,))
    r = cursor.fetchone()
    if r:
        return {"id": r[0], "nombre_playa": r[1], "ubicacion": r[2], "cantidad_basura_estimada_kg": r[3], "estado": r[4]}
    return None

def crear(data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO limpieza_playas (nombre_playa, ubicacion, cantidad_basura_estimada_kg, estado)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (data.nombre_playa, data.ubicacion, data.cantidad_basura_estimada_kg, data.estado))
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    return obtener_por_id(nuevo_id)

def actualizar(id: int, data):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE limpieza_playas 
        SET nombre_playa = %s, ubicacion = %s, cantidad_basura_estimada_kg = %s, estado = %s
        WHERE id = %s
    """, (data.nombre_playa, data.ubicacion, data.cantidad_basura_estimada_kg, data.estado, id))
    conn.commit()
    return obtener_por_id(id)

def eliminar(id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM limpieza_playas WHERE id = %s", (id,))
    conn.commit()
    return {"success": True, "message": "Registro eliminado exitosamente"}
