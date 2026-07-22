from app.config.db_config import get_connection


def crear_programa(nombre: str, descripcion: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO programas (nombre, descripcion)
        VALUES (%s, %s)
        RETURNING id, nombre, estado;
        """,
        (nombre, descripcion)
    )

    nuevo = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    if not nuevo:
        return {"id": None, "nombre": None, "estado": None}

    return {
        "id": nuevo[0],
        "nombre": nuevo[1],
        "estado": nuevo[2]
    }



def listar_programas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, estado FROM programas;")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "nombre": p[1],
            "estado": p[2]
        }
        for p in rows
    ]


def inscribir_usuario_programa(usuario_id: int, programa_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO programas_usuarios (usuario_id, programa_id)
            VALUES (%s, %s)
            ON CONFLICT (usuario_id, programa_id) DO NOTHING
            RETURNING id;
            """,
            (usuario_id, programa_id)
        )
        res = cursor.fetchone()
        conn.commit()
        return {"success": True, "message": "Inscrito exitosamente", "id": res[0] if res else None}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()
        conn.close()


def obtener_programas_usuario(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.id, p.nombre, p.descripcion 
        FROM programas p
        JOIN programas_usuarios pu ON p.id = pu.programa_id
        WHERE pu.usuario_id = %s AND pu.estado = TRUE;
        """,
        (usuario_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2]
        }
        for p in rows
    ]
