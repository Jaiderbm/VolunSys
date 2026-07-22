import psycopg2
from app.config.db_config import conn
from app.config.security import hash_password

def get_usuarios():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.email, u.telefono, u.estado, r.nombre, u.numero_documento 
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        ORDER BY u.id DESC
    """)
    res = cursor.fetchall()
    return [{"id": r[0], "nombre": r[1], "apellido": r[2], "email": r[3], "telefono": r[4], "estado": r[5], "rol": r[6], "documento": r[7]} for r in res]

def crear_usuario(data):
    cursor = conn.cursor()
    hashed_pwd = hash_password(data.get("password", "123456"))
    
    rol_id = data.get("rol_id", 3)
    try:
        cursor.execute("""
            INSERT INTO usuarios 
            (nombre, apellido, email, telefono, tipo_documento_id, numero_documento, rol_id, password)
            VALUES (%s, %s, %s, %s, 1, %s, %s, %s)
        """, (
            data.get("nombre", ""),
            data.get("apellido", ""),
            data.get("email", ""),
            data.get("telefono", ""),
            data.get("numero_documento", "000"),
            rol_id,
            hashed_pwd
        ))
        conn.commit()
        return {"success": True}
    except psycopg2.IntegrityError:
        conn.rollback()
        return {"success": False, "message": "El documento o el correo ingresados ya han sido registrados. Por favor, intente con otros."}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": "Error interno al guardar. Contactar soporte."}

def actualizar_usuario(id, data):
    # simplificado
    return {"success": True}

def eliminar_usuario(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    return {"success": True}

def get_usuario(id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, email, rol_id, numero_documento FROM usuarios WHERE id = %s", (id,))
    u = cursor.fetchone()
    if u:
        return {"id": u[0], "nombre": u[1], "apellido": u[2], "email": u[3], "rol_id": u[4], "documento": u[5]}
    return None

def get_horas_sociales(usuario_id: int):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(p.horas_voluntariado) 
        FROM participaciones p
        JOIN inscripciones i ON p.inscripcion_id = i.id
        WHERE i.usuario_id = %s AND p.asistio = TRUE
    """, (usuario_id,))
    res = cursor.fetchone()
    return res[0] if res and res[0] else 0