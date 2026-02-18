from app.config.db_config import get_connection
from app.config.security import hash_password  


def crear_usuario(nombre: str, correo: str, password: str, pais_id: int, ciudad_id: int):

    # Encriptar contraseña antes de guardar
    password = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios (nombre, correo, password, pais_id, ciudad_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, nombre, correo, estado;
        """,
        (nombre, correo, password, pais_id, ciudad_id)
    )

    nuevo = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": nuevo[0],
        "nombre": nuevo[1],
        "correo": nuevo[2],
        "estado": nuevo[3]
    }


def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre, correo, estado FROM usuarios;"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": u[0],
            "nombre": u[1],
            "correo": u[2],
            "estado": u[3]
        }
        for u in rows
    ]
