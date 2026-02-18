from app.config.db_config import get_connection


def crear_proyecto(nombre: str, programa_id: int, descripcion: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO proyectos (nombre, programa_id, descripcion)
        VALUES (%s, %s, %s)
        RETURNING id, nombre, estado;
        """,
        (nombre, programa_id, descripcion)
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


def listar_proyectos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre, programa_id, estado FROM proyectos;"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "nombre": p[1],
            "programa_id": p[2],
            "estado": p[3]
        }
        for p in rows
    ]
