import g4f
from g4f.client import Client
import json
import asyncio
from app.config.db_config import conn

import time

_cached_context = None
_last_fetch_time = 0.0
_CACHE_TTL = 300  # Cache duration: 5 minutes

def get_platform_context() -> str:
    global _cached_context, _last_fetch_time
    now = time.time()
    
    # Return cached context if still valid
    if _cached_context is not None and (now - _last_fetch_time) < _CACHE_TTL:
        return _cached_context
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre, descripcion FROM programas WHERE estado = TRUE")
        programas = cursor.fetchall()
        cursor.execute("SELECT titulo, fecha FROM voluntariados ORDER BY fecha LIMIT 6")
        voluntariados = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol_id = 3")
        voluntarios = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(horas_voluntariado), 0) FROM participaciones WHERE asistio = TRUE")
        horas = cursor.fetchone()[0]
        prog_str = "\n".join([f"- {p[0]}: {p[1]}" for p in programas])
        vol_str = "\n".join([f"- {v[0]} (fecha: {v[1]})" for v in voluntariados])
        
        context_data = f"""DATOS DE VOLUNSYS (en tiempo real):
- Voluntarios registrados: {voluntarios}
- Horas sociales completadas: {horas}

Programas Activos:
{prog_str}

Próximos Voluntariados:
{vol_str}
"""
        _cached_context = context_data
        _last_fetch_time = now
        return context_data
    except Exception as e:
        print(f"Error loading chat context: {e}")
        # Return stale cache if DB error occurs
        if _cached_context is not None:
            return _cached_context
        return ""
    finally:
        cursor.close()


def _try_provider(provider_cls, model: str, messages: list) -> str | None:
    """Attempt a single provider, return text or None on failure."""
    try:
        client = Client(provider=provider_cls)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=15,
        )
        text = response.choices[0].message.content
        if text and text.strip():
            return text.strip()
    except Exception as e:
        print(f"Provider {provider_cls.__name__} failed: {e}")
    return None


def process_chat_message(messages: list) -> dict:
    import os
    import concurrent.futures
    import urllib.request
    from g4f.Provider import WeWordle, Felo, AnyProvider

    try:
        db_context = get_platform_context()

        system_instruction = f"""Eres VolunBot 🤖, el asistente inteligente y oficial de VolunSys.
VolunSys conecta voluntarios con programas de ayuda social y ambiental.

Usa estos datos en tiempo real para responder con precisión:
{db_context}

Responde siempre en español. Sé claro, amigable y conciso.
Cuando listes opciones o programas, usa listas numeradas o con guiones, un elemento por línea.
"""
        # 1. Intentar usar la API oficial de Gemini si está configurada en .env
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                gemini_contents = []
                for msg in messages:
                    role = "user" if msg.role == "user" else "model"
                    gemini_contents.append({
                        "role": role,
                        "parts": [{"text": msg.content}]
                    })
                
                payload = {
                    "contents": gemini_contents,
                    "systemInstruction": {
                        "parts": [{"text": system_instruction}]
                    },
                    "generationConfig": {
                        "temperature": 0.7,
                    }
                }
                
                req = urllib.request.Request(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    reply = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    if reply and reply.strip():
                        return {"response": reply.strip()}
            except Exception as gemini_err:
                print(f"Error calling Gemini API: {gemini_err}")

        # 2. Si no hay API Key o falla, usar proveedores gratuitos en paralelo
        formatted_messages = [{"role": "system", "content": system_instruction}]
        for msg in messages:
            role = "user" if msg.role == "user" else "assistant"
            formatted_messages.append({"role": role, "content": msg.content})

        providers = [
            (WeWordle, "gpt-4o-mini"),
            (Felo, "gpt-4o-mini"),
            (AnyProvider, "gpt-4o-mini")
        ]

        def worker(provider_cls, model_name):
            return _try_provider(provider_cls, model_name, formatted_messages)

        reply = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(providers)) as executor:
            futures = {executor.submit(worker, p, m): p for p, m in providers}
            
            # Recorrer a medida que completan y tomar el primero exitoso
            for future in concurrent.futures.as_completed(futures):
                p = futures[future]
                try:
                    result = future.result()
                    if result:
                        reply = result
                        print(f"[CHATBOT] Fastest successful provider: {p.__name__}")
                        break
                except Exception as e:
                    print(f"[CHATBOT] Provider {p.__name__} raised exception in thread: {e}")

        if reply:
            return {"response": reply}

        # 3. Cliente por defecto (auto-select secuencial de g4f)
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted_messages,
                timeout=10,
            )
            reply = response.choices[0].message.content
            if reply and reply.strip():
                return {"response": reply.strip()}
        except Exception as e:
            print(f"Default client failed: {e}")

        return {"response": "Hola 👋 Ahora mismo tengo problemas de conexión con el proveedor de IA. Por favor intenta de nuevo en unos segundos."}

    except Exception as e:
        return {"response": f"Error al procesar tu mensaje: {str(e)}"}
