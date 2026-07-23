import os
from groq import Groq
from app.config.db_config import conn

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    from langchain.vectorstores import Chroma

# Base paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "rag", "vector_store")

# Initialize HuggingFace embeddings (cached globally)
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    print(f"Error loading HuggingFaceEmbeddings model: {e}")
    embeddings = None

def get_rag_context(user_query: str, k: int = 3) -> str:
    """Busca en ChromaDB los fragmentos vectoriales generados con HuggingFace."""
    if not embeddings:
        print("Embeddings model is not initialized.")
        return ""
    if not os.path.exists(DB_DIR):
        print(f"Vector store directory does not exist at {DB_DIR}. Running ingestion might be needed.")
        return ""
    try:
        vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        results = vector_store.similarity_search(user_query, k=k)
        context_chunks = []
        for i, doc in enumerate(results):
            source_info = f"[Fuente: {os.path.basename(doc.metadata.get('source', 'Desconocido'))}]"
            context_chunks.append(f"Fragmento {i+1} {source_info}:\n{doc.page_content}")
        return "\n---\n".join(context_chunks)
    except Exception as e:
        print(f"Error al buscar en RAG vectorial: {e}")
        return ""

def get_neon_live_data() -> str:
    """Obtiene datos actualizados desde la base de datos Neon PostgreSQL."""
    try:
        cursor = conn.cursor()
        
        # Total volunteers (rol_id = 3)
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol_id = 3")
        total_voluntarios = cursor.fetchone()[0]

        # Active programs
        cursor.execute("SELECT nombre FROM programas WHERE estado = TRUE")
        programas = [p[0] for p in cursor.fetchall()]

        # Total social hours accumulated
        cursor.execute("SELECT COALESCE(SUM(horas_voluntariado), 0) FROM participaciones WHERE asistio = TRUE")
        total_horas = cursor.fetchone()[0]

        cursor.close()

        return f"""DATOS EN TIEMPO REAL (NEON POSTGRESQL):
- Voluntarios registrados en el sistema: {total_voluntarios}
- Horas sociales/comunitarias completadas en total: {total_horas}
- Programas activos actualmente: {', '.join(programas) if programas else 'Ninguno'}
"""
    except Exception as e:
        print(f"Error consultando Neon DB en RAG: {e}")
        return "DATOS EN TIEMPO REAL (NEON POSTGRESQL): No disponibles temporalmente por error de conexión."

def _parse_message(msg):
    """Helper to handle both Pydantic models and dictionaries."""
    if hasattr(msg, "role") and hasattr(msg, "content"):
        return msg.role, msg.content
    elif isinstance(msg, dict):
        return msg.get("role", "user"), msg.get("content", "")
    else:
        return "user", str(msg)

def generate_groq_response(user_query: str, chat_history: list = None) -> str:
    """Envía la consulta + contexto RAG + datos de Neon DB a la API de Groq."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return "⚠️ Error: Falta configurar la variable de entorno GROQ_API_KEY en el archivo .env."

    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        return f"⚠️ Error al inicializar el cliente de Groq: {str(e)}"

    # Get contexts
    context_vectorial = get_rag_context(user_query)
    context_neon = get_neon_live_data()

    system_prompt = f"""## IDENTIDAD
Eres **VolunBot** 🤖, el asistente virtual oficial e inteligente de **VolunSys** — la plataforma web de gestión de voluntariado e impacto social de Colombia.

## MISIÓN DE VOLUNSYS
VolunSys conecta ciudadanos voluntarios con coordinadores y administradores en **tres programas de impacto comunitario**:
1. 🏖️ **Limpieza y Conservación de Playas** — Recolección de residuos medida en kilogramos.
2. 🐾 **Rescate y Cuidado Animal** — Atención veterinaria, vacunación y adopción de animales callejeros.
3. 👴 **Apoyo a Adultos Mayores** — Acompañamiento emocional, bingo solidario y actividades recreativas en asilos.

## ROLES DEL SISTEMA (RBAC)
- **Administrador (Rol 1)**: Acceso total, gestión de usuarios, asignación de permisos, visualización de métricas en PowerBI.
- **Coordinador / Organizador (Rol 2)**: Planificación de jornadas, creación de eventos y asignación de tareas a voluntarios inscritos.
- **Voluntario (Rol 3)**: Registro mediante formulario reactivo, inscripción a jornadas, visualización de tareas asignadas y marcado de asistencia.

## DATOS EN TIEMPO REAL DE LA BASE DE DATOS
{context_neon}

## CONTEXTO DOCUMENTAL RECUPERADO (RAG - Embeddings)
{context_vectorial if context_vectorial else '⚠️ No se encontraron fragmentos relevantes en la base de conocimiento para esta consulta.'}

## ARQUITECTURA TÉCNICA (para preguntas técnicas)
- **Frontend**: Angular 19 (Standalone Components, Reactive Forms, RxJS, Bootstrap 5.3, Glassmorphism CSS).
- **Backend API**: FastAPI (Python 3.11+), Uvicorn, Pydantic, JWT con PyJWT, Bcrypt.
- **Microservicio Ubicaciones**: Node.js + Express (Puerto 3001).
- **Base de Datos**: PostgreSQL Serverless en Neon Cloud, ORM con SQLAlchemy.
- **Motor IA**: RAG con ChromaDB (HuggingFace Embeddings all-MiniLM-L6-v2) + LLM Groq (Llama 3.3 70B).

## REGLAS DE RESPUESTA (OBLIGATORIAS)
1. **Idioma**: Responde SIEMPRE en español, de forma clara, amigable, profesional y concisa.
2. **Precisión**: Basa tus respuestas ESTRICTAMENTE en los datos provistos arriba (tiempo real + documentación RAG). NO inventes datos, cifras ni funcionalidades.
3. **Límites de conocimiento**: Si el usuario pregunta algo que NO está en tu contexto o es ajeno a VolunSys, responde amablemente: "Esa pregunta está fuera de mi alcance como asistente de VolunSys. Puedo ayudarte con temas de voluntariado, programas sociales, inscripciones y tu cuenta."
4. **Formato**: Usa listas numeradas o con viñetas (guiones) cuando enumeres opciones. Usa **negritas** para resaltar datos clave. Sé breve pero completo.
5. **Tono**: Cercano y motivacional. Motiva la participación en voluntariado cuando sea apropiado.
6. **Rol del usuario**: Si el usuario pregunta sobre acciones que requieren un rol específico (ej: asignar tareas), explícale qué rol necesita según la tabla RBAC.
7. **Saludo**: Si el mensaje es un saludo simple, responde con calidez y ofrece ayuda indicando las 3 áreas en las que puedes asistir.
"""

    try:
        messages = [{"role": "system", "content": system_prompt}]
        if chat_history:
            for msg in chat_history:
                role, content = _parse_message(msg)
                if role not in ["system", "user", "assistant"]:
                    role = "user"
                messages.append({"role": role, "content": content})
        else:
            messages.append({"role": "user", "content": user_query})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=600,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error en llamada a Groq: {e}")
        return f"Lo siento, ocurrió un problema al conectar con el servicio de IA (Groq): {str(e)}"
