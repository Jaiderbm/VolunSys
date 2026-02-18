from app.config.db_config import get_connection


def crear_voluntariado(usuario_id: int, tipo_id: int, fecha_inicio, fecha_fin=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO voluntariados
        (usuario_id, tipo_voluntariado_id, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s)
        RETURNING id, usuario_id, tipo_voluntariado_id, estado;
        """,
        (usuario_id, tipo_id, fecha_inicio, fecha_fin)
    )

    nuevo = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": nuevo[0],
        "usuario_id": nuevo[1],
        "tipo_voluntariado_id": nuevo[2],
        "estado": nuevo[3]
    }


def listar_voluntariados():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, usuario_id, tipo_voluntariado_id,
               fecha_inicio, fecha_fin, estado
        FROM voluntariados;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": v[0],
            "usuario_id": v[1],
            "tipo_voluntariado_id": v[2],
            "fecha_inicio": v[3],
            "fecha_fin": v[4],
            "estado": v[5]
        }
        for v in rows
    ]
