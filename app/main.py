from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.routes.usuarios_routes import router as usuarios_router
from app.routes.voluntariados_routes import router as voluntariados_router
from app.routes.inscripciones_routes import router as inscripciones_router
from app.routes.cuidado_adultos_mayores_routes import router as cuidado_adultos_mayores_router
from app.routes.limpieza_playas_routes import router as limpieza_playas_router
from app.routes.rescate_animal_routes import router as rescate_animal_router
from app.routes.stats_routes import router as stats_router
from app.routes.programas_routes import router as programas_router
from app.routes.chat_routes import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuarios"])
app.include_router(voluntariados_router, prefix="/api", tags=["Voluntariados"])
app.include_router(inscripciones_router, prefix="/api", tags=["Inscripciones"])
app.include_router(cuidado_adultos_mayores_router, prefix="/api", tags=["Cuidado"])
app.include_router(limpieza_playas_router, prefix="/api", tags=["Limpieza"])
app.include_router(rescate_animal_router, prefix="/api", tags=["Rescate"])
app.include_router(programas_router, prefix="/api/programas", tags=["Programas"])
app.include_router(stats_router, prefix="/api", tags=["Estadisticas"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
