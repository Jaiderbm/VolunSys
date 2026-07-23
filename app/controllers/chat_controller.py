import os
from app.rag.rag_service import generate_groq_response

def process_chat_message(messages: list) -> dict:
    """
    Procesa un mensaje de chat enviándolo al servicio RAG con Groq.
    """
    try:
        if not messages:
            return {"response": "Hola. ¿En qué puedo ayudarte hoy?"}

        # Extraer correctamente el texto del último mensaje
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            user_query = last_message.content
        elif isinstance(last_message, dict):
            user_query = last_message.get("content", "")
        else:
            user_query = str(last_message)

        lowered_query = user_query.lower()

        # Preguntas de seguridad estrictamente bloqueadas (claves, passwords, tokens)
        security_keywords = ["clave", "contraseña", "contrasena", "password", "secret", "token", "credencial"]
        if any(keyword in lowered_query for keyword in security_keywords):
            return {"response": "Por razones de seguridad y privacidad, no puedo brindar información sobre claves, contraseñas ni datos sensibles."}

        # Generar respuesta usando el servicio RAG
        reply = generate_groq_response(user_query, messages)
        return {"response": reply}
    except Exception as e:
        print(f"Error in process_chat_message: {e}")
        return {"response": f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}"}

