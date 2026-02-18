from app.config.db_config import get_connection


def crear_tipo(nombre: str, descripcion: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tipos_voluntariado (nombre, descripcion)
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


def listar_tipos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre, descripcion, estado FROM tipos_voluntariado;"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": t[0],
            "nombre": t[1],
            "descripcion": t[2],
            "estado": t[3]
        }
        for t in rows
    ]
