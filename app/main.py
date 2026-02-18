from fastapi import FastAPI
from app.config.db_config import get_connection
from app.routes.pais_routes import router as pais_router

app = FastAPI()

# Registrar rutas
app.include_router(pais_router)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}

@app.get("/test-db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        return {"message": "Conexión exitosa a Neon"}
    except Exception as e:
        return {"error": str(e)}
