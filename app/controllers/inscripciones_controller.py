from app.config.db_config import get_connection


def crear_inscripcion(usuario_id: int, proyecto_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inscripciones (usuario_id, proyecto_id)
        VALUES (%s, %s)
        RETURNING id, usuario_id, proyecto_id, estado;
        """,
        (usuario_id, proyecto_id)
    )

    nuevo = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": nuevo[0],
        "usuario_id": nuevo[1],
        "proyecto_id": nuevo[2],
        "estado": nuevo[3]
    }


def listar_inscripciones():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, usuario_id, proyecto_id, estado FROM inscripciones;"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": i[0],
            "usuario_id": i[1],
            "proyecto_id": i[2],
            "estado": i[3]
        }
        for i in rows
    ]
