import json
from app.config.db_config import conn

def get_dashboard_stats():
    cursor = conn.cursor()
    try:
        query = """
        SELECT json_build_object(
            'total_voluntarios', (SELECT COUNT(*) FROM usuarios WHERE rol_id = 3),
            'programas_activos', (SELECT COUNT(*) FROM programas WHERE estado = TRUE),
            'inscripciones_totales', (SELECT COUNT(*) FROM inscripciones),
            'horas_sociales', (SELECT COALESCE(SUM(horas_voluntariado), 0) FROM participaciones WHERE asistio = TRUE),
            'chart_voluntarios_programa', (
                SELECT json_build_object(
                    'labels', COALESCE(json_agg(nombre), '[]'::json),
                    'data', COALESCE(json_agg(total), '[]'::json)
                ) FROM (
                    SELECT p.nombre, COUNT(pu.usuario_id) AS total
                    FROM programas p 
                    LEFT JOIN programas_usuarios pu ON p.id = pu.programa_id 
                    GROUP BY p.nombre
                ) q1
            ),
            'chart_voluntarios_rol', (
                SELECT json_build_object(
                    'labels', COALESCE(json_agg(nombre), '[]'::json),
                    'data', COALESCE(json_agg(total), '[]'::json)
                ) FROM (
                    SELECT r.nombre, COUNT(u.id) AS total
                    FROM roles r 
                    LEFT JOIN usuarios u ON r.id = u.rol_id 
                    GROUP BY r.nombre
                ) q2
            ),
            'chart_top_voluntariados', (
                SELECT json_build_object(
                    'labels', COALESCE(json_agg(titulo), '[]'::json),
                    'data', COALESCE(json_agg(total), '[]'::json)
                ) FROM (
                    SELECT v.titulo, COUNT(i.id) as total
                    FROM voluntariados v 
                    LEFT JOIN inscripciones i ON v.id = i.voluntariado_id 
                    GROUP BY v.titulo 
                    ORDER BY total DESC 
                    LIMIT 5
                ) q3
            )
        );
        """
        cursor.execute(query)
        res = cursor.fetchone()[0]
        
        # If psycopg2 didn't auto-deserialize the json, load it manually
        if isinstance(res, str):
            res = json.loads(res)
            
        return res
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None
    finally:
        cursor.close()
