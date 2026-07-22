# -*- coding: utf-8 -*-
"""
Script de seed: inserta ~60 registros en la BD de VolunSys
Ejecutar: python seed_data.py
"""
import sys
import os
import psycopg2
import random
from dotenv import load_dotenv

# Forzar UTF-8 en Windows
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

print("Iniciando seed de datos...")

# ─── 1. Voluntarios ────────────────────────────────────────────────────────
voluntarios = [
    ("Ana", "Garcia", "ana.garcia@email.com"),
    ("Carlos", "Lopez", "carlos.lopez@email.com"),
    ("Maria", "Rodriguez", "maria.rodriguez@email.com"),
    ("Juan", "Martinez", "juan.martinez@email.com"),
    ("Laura", "Perez", "laura.perez@email.com"),
    ("Diego", "Hernandez", "diego.hernandez@email.com"),
    ("Sofia", "Gonzalez", "sofia.gonzalez@email.com"),
    ("Andres", "Torres", "andres.torres@email.com"),
    ("Valentina", "Diaz", "valentina.diaz@email.com"),
    ("Miguel", "Ramirez", "miguel.ramirez@email.com"),
    ("Isabella", "Castro", "isabella.castro@email.com"),
    ("Sebastian", "Vargas", "sebastian.vargas@email.com"),
    ("Camila", "Moreno", "camila.moreno@email.com"),
    ("Felipe", "Jimenez", "felipe.jimenez@email.com"),
    ("Natalia", "Ruiz", "natalia.ruiz@email.com"),
    ("Daniel", "Medina", "daniel.medina@email.com"),
    ("Gabriela", "Suarez", "gabriela.suarez@email.com"),
    ("Julian", "Ortega", "julian.ortega@email.com"),
    ("Paola", "Reyes", "paola.reyes@email.com"),
    ("Ricardo", "Navarro", "ricardo.navarro@email.com"),
    ("Adriana", "Soto", "adriana.soto@email.com"),
    ("Esteban", "Aguilar", "esteban.aguilar@email.com"),
    ("Daniela", "Flores", "daniela.flores@email.com"),
    ("Santiago", "Cruz", "santiago.cruz@email.com"),
    ("Mariana", "Vega", "mariana.vega@email.com"),
    ("Alejandro", "Ramos", "alejandro.ramos@email.com"),
    ("Luisa", "Santos", "luisa.santos@email.com"),
    ("Sergio", "Romero", "sergio.romero@email.com"),
    ("Paula", "Guzman", "paula.guzman@email.com"),
    ("Christian", "Molina", "christian.molina@email.com"),
]

print(f"  Insertando {len(voluntarios)} voluntarios...")
nuevos_user_ids = []
for nombre, apellido, email in voluntarios:
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    ex = cur.fetchone()
    if not ex:
        num_doc = "".join([str(random.randint(0, 9)) for _ in range(10)])
        cur.execute(
            """INSERT INTO usuarios (nombre, apellido, email, password, rol_id, estado, tipo_documento_id, numero_documento)
               VALUES (%s, %s, %s, %s, 3, TRUE, 1, %s) RETURNING id""",
            (nombre, apellido, email, "demo1234", num_doc)
        )
        nuevos_user_ids.append(cur.fetchone()[0])
    else:
        nuevos_user_ids.append(ex[0])

conn.commit()
print(f"  OK: {len(nuevos_user_ids)} voluntarios listos")

# ─── 2. Programas ──────────────────────────────────────────────────────────
cur.execute("SELECT id, nombre FROM programas WHERE estado = TRUE")
programas = cur.fetchall()
print(f"  OK: {len(programas)} programas activos")

# ─── 3. Inscripciones a programas ─────────────────────────────────────────
print("  Inscribiendo voluntarios en programas...")
prog_insc = 0
for uid in nuevos_user_ids:
    progs_sel = random.sample(programas, k=min(random.randint(1,2), len(programas)))
    for prog_id, _ in progs_sel:
        cur.execute("SELECT 1 FROM programas_usuarios WHERE usuario_id=%s AND programa_id=%s", (uid, prog_id))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO programas_usuarios (usuario_id, programa_id, estado) VALUES (%s, %s, TRUE)",
                (uid, prog_id)
            )
            prog_insc += 1
conn.commit()
print(f"  OK: {prog_insc} inscripciones a programas")

# ─── 4. Voluntariados ─────────────────────────────────────────────────────
# Necesitamos proyecto_id y tipo_voluntariado_id
proyecto_id = None
try:
    cur.execute("SELECT id FROM proyectos LIMIT 1")
    row = cur.fetchone()
    proyecto_id = row[0] if row else None
except Exception:
    conn.rollback()

# Si no hay ningún proyecto en la BD, creamos uno por defecto asociado a un programa activo
if not proyecto_id:
    try:
        cur.execute("SELECT id, nombre, descripcion FROM programas LIMIT 1")
        prog_row = cur.fetchone()
        if prog_row:
            prog_id, prog_nombre, prog_desc = prog_row
            cur.execute("""
                INSERT INTO proyectos (nombre, programa_id, descripcion)
                VALUES (%s, %s, %s) RETURNING id
            """, (f"Proyecto - {prog_nombre}", prog_id, prog_desc))
            proyecto_id = cur.fetchone()[0]
            conn.commit()
            print(f"  OK: Creado proyecto por defecto id={proyecto_id}")
    except Exception as e:
        conn.rollback()
        print(f"  ADVERTENCIA: No se pudo crear proyecto por defecto: {e}")

tipo_vol_id = 1 # Por defecto Presencial (id=1)
try:
    cur.execute("SELECT id FROM tipos_voluntariado LIMIT 1")
    row = cur.fetchone()
    if row:
        tipo_vol_id = row[0]
except Exception:
    conn.rollback()

voluntariados_data = [
    ("Limpieza Playa Norte",          "Limpieza de costas y retiro de plasticos",      "2026-08-01"),
    ("Rescate Perros Callejeros",     "Rescate y adopcion de perros en abandono",      "2026-08-05"),
    ("Visita Hogar Anciano Centro",   "Visitas y actividades con adultos mayores",     "2026-08-10"),
    ("Jornada Ambiental Parque",      "Siembra de arboles en parque metropolitano",   "2026-08-15"),
    ("Taller Arte Adultos Mayores",   "Taller de pintura y manualidades",              "2026-08-18"),
    ("Rescate Gatos Zona Sur",        "Esterilizacion y adopcion felina",              "2026-08-20"),
    ("Limpieza Rio Local",            "Jornada de limpieza del rio de la ciudad",     "2026-09-01"),
    ("Visita Hospital Geriatrico",    "Lectura y compania a adultos mayores",          "2026-09-05"),
    ("Festival Mascotas Adoptables",  "Evento de adopcion de mascotas",               "2026-09-10"),
    ("Recoleccion Basura Playa Sur",  "Limpieza costera con grupos eco",              "2026-09-15"),
    ("Cuidado Adultos Norte",         "Actividades recreativas para adultos mayores", "2026-09-20"),
    ("Rescate Animal Rural",          "Atencion a animales en zona rural",            "2026-09-25"),
]

print(f"  Insertando voluntariados...")
vol_ids = []
for titulo, desc, fecha in voluntariados_data:
    cur.execute("SELECT id FROM voluntariados WHERE titulo = %s", (titulo,))
    ex = cur.fetchone()
    if not ex:
        if proyecto_id:
            if tipo_vol_id:
                cur.execute(
                    """INSERT INTO voluntariados (proyecto_id, tipo_voluntariado_id, titulo, descripcion, fecha, cupos, estado)
                       VALUES (%s, %s, %s, %s, %s, 30, TRUE) RETURNING id""",
                    (proyecto_id, tipo_vol_id, titulo, desc, fecha)
                )
            else:
                cur.execute(
                    """INSERT INTO voluntariados (proyecto_id, titulo, descripcion, fecha, cupos, estado)
                       VALUES (%s, %s, %s, %s, 30, TRUE) RETURNING id""",
                    (proyecto_id, titulo, desc, fecha)
                )
            vol_ids.append(cur.fetchone()[0])
        else:
            print(f"  Advertencia: Saltando '{titulo}' porque no hay proyecto_id.")
    else:
        vol_ids.append(ex[0])
conn.commit()
print(f"  OK: {len(vol_ids)} voluntariados listos")

# ─── 5. Inscripciones + participaciones ───────────────────────────────────
print("  Creando inscripciones y horas sociales...")
insc_count = 0
part_count = 0
total_horas = 0

for vol_id in vol_ids:
    n = random.randint(5, 10)
    participantes = random.sample(nuevos_user_ids, k=min(n, len(nuevos_user_ids)))
    for uid in participantes:
        cur.execute("SELECT id FROM inscripciones WHERE voluntariado_id=%s AND usuario_id=%s", (vol_id, uid))
        ex_i = cur.fetchone()
        if not ex_i:
            cur.execute(
                "INSERT INTO inscripciones (usuario_id, voluntariado_id, estado) VALUES (%s, %s, 'confirmada') RETURNING id",
                (uid, vol_id)
            )
            insc_id = cur.fetchone()[0]
            insc_count += 1
        else:
            insc_id = ex_i[0]

        cur.execute("SELECT id FROM participaciones WHERE inscripcion_id = %s", (insc_id,))
        if not cur.fetchone():
            horas = random.randint(2, 8)
            cur.execute(
                "INSERT INTO participaciones (inscripcion_id, asistio, horas_voluntariado) VALUES (%s, TRUE, %s)",
                (insc_id, horas)
            )
            part_count += 1
            total_horas += horas

conn.commit()
print(f"  OK: {insc_count} inscripciones + {part_count} participaciones ({total_horas}h totales)")

# ─── Resumen ──────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM usuarios WHERE rol_id = 3")
print(f"\nEstado final DB:")
print(f"  Voluntarios: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM inscripciones")
print(f"  Inscripciones: {cur.fetchone()[0]}")
cur.execute("SELECT COALESCE(SUM(horas_voluntariado),0) FROM participaciones WHERE asistio=TRUE")
print(f"  Horas sociales: {cur.fetchone()[0]}h")

cur.close()
conn.close()
print("\nSeed completado!")
