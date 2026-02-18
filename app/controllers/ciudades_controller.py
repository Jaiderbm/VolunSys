from app.config.db_config import get_connection


def crear_ciudad(nombre: str, pais_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ciudades (nombre, pais_id)
        VALUES (%s, %s)
        RETURNING id, nombre, pais_id, estado;
        """,
        (nombre, pais_id)
    )

    nueva = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": nueva[0],
        "nombre": nueva[1],
        "pais_id": nueva[2],
        "estado": nueva[3]
    }


def listar_ciudades():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre, pais_id, estado FROM ciudades;"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": c[0],
            "nombre": c[1],
            "pais_id": c[2],
            "estado": c[3]
        }
        for c in rows
    ]
