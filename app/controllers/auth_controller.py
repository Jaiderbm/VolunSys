import traceback
from app.config.db_config import conn
from app.config.security import verify_password, create_access_token

def login(data):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, r.nombre, u.password
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE u.email = %s AND u.estado = true
        """, (data.get("email", ""),))

        user = cursor.fetchone()
        print(f"[LOGIN] Email: {data.get('email')}, User found: {user is not None}")

        if not user:
            return {"success": False, "message": "Email o clave incorrectos"}

        password_ok = verify_password(data.get("password", ""), user[3])
        print(f"[LOGIN] Password verification: {password_ok}")

        if password_ok:
            token = create_access_token({"sub": data.get("email", ""), "rol": user[2]})
            return {
                "success": True,
                "usuario": user[1],
                "usuarioId": str(user[0]),
                "rol": user[2],
                "access_token": token,
                "token_type": "bearer"
            }

        return {"success": False, "message": "Email o clave incorrectos"}
    except Exception as e:
        print(f"[LOGIN ERROR] {traceback.format_exc()}")
        try:
            conn.rollback()
        except:
            pass
        return {"success": False, "message": "Error interno del servidor. Intente de nuevo."}