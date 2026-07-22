from app.config.db_config import conn

def obtener_todos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rescate_animal")
    registros = cursor.fetchall()
    return [{"id": r[0], "tipo_animal": r[1], "condicion": r[2], "ubicacion": r[3], "estado": r[4]} for r in registros]

def obtener_por_id(id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rescate_animal WHERE id = %s", (id,))
    r = cursor.fetchone()
    if r:
        return {"id": r[0], "tipo_animal": r[1], "condicion": r[2], "ubicacion": r[3], "estado": r[4]}
    return None

def crear(data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rescate_animal (tipo_animal, condicion, ubicacion, estado)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (data.tipo_animal, data.condicion, data.ubicacion, data.estado))
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    return obtener_por_id(nuevo_id)

def actualizar(id: int, data):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rescate_animal 
        SET tipo_animal = %s, condicion = %s, ubicacion = %s, estado = %s
        WHERE id = %s
    """, (data.tipo_animal, data.condicion, data.ubicacion, data.estado, id))
    conn.commit()
    return obtener_por_id(id)

def eliminar(id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rescate_animal WHERE id = %s", (id,))
    conn.commit()
    return {"success": True, "message": "Registro eliminado exitosamente"}
