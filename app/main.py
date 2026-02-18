from fastapi import FastAPI
from app.config.db_config import get_connection

# Routers
from app.routes.pais_routes import router as pais_router
from app.routes.ciudades_routes import router as ciudades_router
from app.routes.usuarios_routes import router as usuarios_router
from app.routes.tipos_voluntariado_routes import router as tipos_router
from app.routes.programas_routes import router as programas_router
from app.routes.proyectos_routes import router as proyectos_router
from app.routes.voluntariados_routes import router as voluntariados_router
from app.routes.inscripciones_routes import router as inscripciones_router
from app.routes.auth_routes import router as auth_router   # 👈 JWT


def create_app() -> FastAPI:
    app = FastAPI(
        title="VolunSys API",
        version="1.0.0"
    )

    # Registrar rutas
    app.include_router(auth_router, tags=["Auth"])  # 👈 LOGIN

    app.include_router(pais_router, prefix="/paises", tags=["Paises"])
    app.include_router(ciudades_router, prefix="/ciudades", tags=["Ciudades"])
    app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
    app.include_router(tipos_router, prefix="/tipos-voluntariado", tags=["Tipos"])
    app.include_router(programas_router, prefix="/programas", tags=["Programas"])
    app.include_router(proyectos_router, prefix="/proyectos", tags=["Proyectos"])
    app.include_router(voluntariados_router, prefix="/voluntariados", tags=["Voluntariados"])
    app.include_router(inscripciones_router, prefix="/inscripciones", tags=["Inscripciones"])

    @app.get("/")
    def root():
        return {"message": "API funcionando"}

    @app.get("/test-db")
    def test_db():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            cur.close()
            conn.close()
            return {"message": "Conexión exitosa a Neon"}
        except Exception as e:
            return {"error": str(e)}

    return app


app = create_app()
