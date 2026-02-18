from app.config.db_config import get_connection
from app.config.security import verify_password, create_access_token


def login_user(correo: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, correo, password FROM usuarios WHERE correo=%s;",
        (correo,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return {"error": "Usuario no existe"}

    if not verify_password(password, user[2]):
        return {"error": "Contraseña incorrecta"}

    token = create_access_token({"sub": user[1]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
