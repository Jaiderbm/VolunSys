from app.config.db_config import conn

def get_voluntariados():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, v.titulo, v.descripcion, v.fecha, v.hora, v.cupos, v.proyecto_id, p.programa_id, v.ciudad_id, v.tipo_voluntariado_id
        FROM voluntariados v
        LEFT JOIN proyectos p ON v.proyecto_id = p.id
    """)
    res = cursor.fetchall()
    return [{
        "id": r[0], "titulo": r[1], "descripcion": r[2], 
        "fecha": str(r[3]), "hora": str(r[4]), 
        "cupos": r[5], "proyecto_id": r[6],
        "programa_id": r[7], "ciudad_id": r[8],
        "tipo_voluntariado_id": r[9]
    } for r in res]

def crear_voluntariado(data: dict):
    cursor = conn.cursor()
    
    # 1. Resolve proyecto_id from programa_id or proyecto_id
    programa_id = data.get("programa_id") or data.get("proyecto_id")
    proyecto_id = None
    if programa_id:
        try:
            programa_id = int(programa_id)
        except (ValueError, TypeError):
            pass
            
    if programa_id:
        cursor.execute("SELECT id FROM proyectos WHERE programa_id = %s LIMIT 1;", (programa_id,))
        row = cursor.fetchone()
        if row:
            proyecto_id = row[0]
        else:
            # Create project if it doesn't exist for this program
            cursor.execute("SELECT nombre, descripcion FROM programas WHERE id = %s;", (programa_id,))
            prog_row = cursor.fetchone()
            if prog_row:
                prog_nombre, prog_desc = prog_row
                cursor.execute("""
                    INSERT INTO proyectos (nombre, programa_id, descripcion)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                """, (f"Proyecto - {prog_nombre}", programa_id, prog_desc))
                proyecto_id = cursor.fetchone()[0]
                
    if not proyecto_id:
        # Fallback to any project to satisfy NOT NULL constraint
        cursor.execute("SELECT id FROM proyectos LIMIT 1;")
        row = cursor.fetchone()
        if row:
            proyecto_id = row[0]

    # 2. Get ciudad_id (if passed)
    ciudad_id = data.get("ciudad_id")
    if ciudad_id:
        try:
            ciudad_id = int(ciudad_id)
        except (ValueError, TypeError):
            ciudad_id = None

    # 3. Get tipo_voluntariado_id
    tipo_voluntariado_id = data.get("tipo_voluntariado_id")
    if tipo_voluntariado_id:
        try:
            tipo_voluntariado_id = int(tipo_voluntariado_id)
        except (ValueError, TypeError):
            tipo_voluntariado_id = 1
    else:
        tipo_voluntariado_id = 1 # Default to 1 (Presencial)

    try:
        cursor.execute("""
            INSERT INTO voluntariados (titulo, descripcion, fecha, hora, cupos, proyecto_id, tipo_voluntariado_id, ciudad_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, titulo;
        """, (
            data.get("titulo"),
            data.get("descripcion"),
            data.get("fecha"),
            data.get("hora"),
            data.get("cupos", 10),
            proyecto_id,
            tipo_voluntariado_id,
            ciudad_id
        ))
        row = cursor.fetchone()
        conn.commit()
        return {"success": True, "id": row[0], "titulo": row[1]}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}

def eliminar_voluntariado(id: int):
    cursor = conn.cursor()
    try:
        # 1. Eliminar participaciones relacionadas (vía inscripciones)
        cursor.execute("""
            DELETE FROM participaciones 
            WHERE inscripcion_id IN (SELECT id FROM inscripciones WHERE voluntariado_id = %s);
        """, (id,))
        # 2. Eliminar inscripciones del voluntariado
        cursor.execute("DELETE FROM inscripciones WHERE voluntariado_id = %s;", (id,))
        # 3. Eliminar voluntariado
        cursor.execute("DELETE FROM voluntariados WHERE id = %s;", (id,))
        conn.commit()
        return {"success": True}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()