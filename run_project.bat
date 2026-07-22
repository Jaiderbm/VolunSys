@echo off
title VolunSys System Launcher
color 0B

echo ==========================================================
echo               VOLUNSYS SYSTEM LAUNCHER
echo ==========================================================
echo.

:: Step 1: Cleaning Temporary Files
echo [1/3] Limpiando archivos temporales y caches...
echo ----------------------------------------------------------

:: Delete Python cache directories
if exist "app\__pycache__" (
    echo - Eliminando cache de app/
    rd /s /q "app\__pycache__"
)
if exist "app\controllers\__pycache__" (
    echo - Eliminando cache de controllers/
    rd /s /q "app\controllers\__pycache__"
)
if exist "app\config\__pycache__" (
    echo - Eliminando cache de config/
    rd /s /q "app\config\__pycache__"
)
if exist "app\routes\__pycache__" (
    echo - Eliminando cache de routes/
    rd /s /q "app\routes\__pycache__"
)
if exist "app\models\__pycache__" (
    echo - Eliminando cache de models/
    rd /s /q "app\models\__pycache__"
)

:: Delete Angular caches
if exist "frontend\.angular\cache" (
    echo - Eliminando cache de compilacion de Angular
    rd /s /q "frontend\.angular\cache"
)

:: Delete temporary test script if exists
if exist "test_providers_speed.py" (
    echo - Eliminando script de prueba temporal
    del /q "test_providers_speed.py"
)

echo - Limpieza completada con exito.
echo.

:: Step 2: Database Status
echo [2/3] Verificando base de datos...
echo ----------------------------------------------------------
echo - Base de datos configurada en Neon (Cloud).
echo - No requiere iniciar un servicio de base de datos local.
echo.

:: Step 3: Starting Services
echo [3/3] Iniciando los servicios en ventanas independientes...
echo ----------------------------------------------------------

:: 1. Start FastAPI Backend API
echo - Iniciando Backend API (FastAPI) en el puerto 8000...
start "Backend API (FastAPI)" cmd /k "cd /d %~dp0 && .venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: 2. Start Locations Microservice (Express)
echo - Iniciando Microservicio de Ubicaciones (Express) en el puerto 3001...
start "Microservicio Ubicaciones (Express)" cmd /k "cd /d %~dp0microservicio_ubicaciones && node index.js"

:: 3. Start Angular Frontend
echo - Iniciando Frontend (Angular) en el puerto 4200...
start "Frontend (Angular)" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ==========================================================
echo ¡Todos los servicios han sido lanzados en ventanas dedicadas!
echo - API Backend: http://127.0.0.1:8000
echo - Microservicio Ubicaciones: http://localhost:3001
echo - Frontend Angular: http://localhost:4200
echo ==========================================================
echo.
pause
