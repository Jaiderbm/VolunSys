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
