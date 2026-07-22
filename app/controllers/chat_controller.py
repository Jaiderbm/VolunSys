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
    try:
        db_context = get_platform_context()

        system_instruction = f"""Eres VolunBot 🤖, el asistente inteligente y oficial de VolunSys.
VolunSys conecta voluntarios con programas de ayuda social y ambiental.

Usa estos datos en tiempo real para responder con precisión:
{db_context}

Responde siempre en español. Sé claro, amigable y conciso.
Cuando listes opciones o programas, usa listas numeradas o con guiones, un elemento por línea.
"""
        formatted_messages = [{"role": "system", "content": system_instruction}]
        for msg in messages:
            role = "user" if msg.role == "user" else "assistant"
            formatted_messages.append({"role": role, "content": msg.content})

        # --- Provider chain: fastest first ---
        from g4f.Provider import PollinationsAI, WeWordle, Felo, BlackboxPro

        # 1) WeWordle – suele ser el más rápido
        reply = _try_provider(WeWordle, "gpt-4o-mini", formatted_messages)
        if reply:
            return {"response": reply}

        # 2) PollinationsAI con modelo 'openai'
        reply = _try_provider(PollinationsAI, "openai", formatted_messages)
        if reply:
            return {"response": reply}

        # 3) Felo
        reply = _try_provider(Felo, "gpt-4o-mini", formatted_messages)
        if reply:
            return {"response": reply}

        # 4) BlackboxPro
        reply = _try_provider(BlackboxPro, "gpt-4o-mini", formatted_messages)
        if reply:
            return {"response": reply}

        # 5) Default client (auto-select)
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=formatted_messages,
                timeout=20,
            )
            reply = response.choices[0].message.content
            if reply and reply.strip():
                return {"response": reply.strip()}
        except Exception as e:
            print(f"Default client failed: {e}")

        return {"response": "Hola 👋 Ahora mismo tengo problemas de conexión con el proveedor de IA. Por favor intenta de nuevo en unos segundos."}

    except Exception as e:
        return {"response": f"Error al procesar tu mensaje: {str(e)}"}
