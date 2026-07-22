from app.config.db_config import conn

def get_inscripciones():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, u.nombre, v.titulo, i.fecha_inscripcion, i.tarea_asignada, i.estado
        FROM inscripciones i
        JOIN usuarios u ON i.usuario_id = u.id
        JOIN voluntariados v ON i.voluntariado_id = v.id
    """)
    res = cursor.fetchall()
    return [{"id": r[0], "usuario": r[1], "voluntariado": r[2], "fecha": str(r[3]), "tarea": r[4], "estado": r[5]} for r in res]

def asignar_tarea(inscripcion_id: int, tarea: str):
    cursor = conn.cursor()
    cursor.execute("UPDATE inscripciones SET tarea_asignada = %s WHERE id = %s", (tarea, inscripcion_id))
    conn.commit()
    return {"success": True}

def crear_inscripcion(data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inscripciones (usuario_id, voluntariado_id)
        VALUES (%s, %s)
        RETURNING id;
    """, (
        data["usuario_id"],
        data["voluntariado_id"]
    ))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return {"success": True, "id": new_id}

def confirmar_asistencia(inscripcion_id: int, horas: int = 4):
    cursor = conn.cursor()
    # Primero insertamos o actualizamos en participaciones
    cursor.execute("""
        INSERT INTO participaciones (inscripcion_id, asistio, horas_voluntariado)
        VALUES (%s, TRUE, %s)
        ON CONFLICT (inscripcion_id) DO UPDATE SET asistio = TRUE, horas_voluntariado = %s;
    """, (inscripcion_id, horas, horas))
    
    # Actualizamos el estado de la inscripción
    cursor.execute("UPDATE inscripciones SET estado = 'Completado' WHERE id = %s", (inscripcion_id,))
    
    conn.commit()
    return {"success": True, "message": "Asistencia confirmada"}