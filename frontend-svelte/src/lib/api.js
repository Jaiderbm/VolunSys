const FASTAPI = "http://localhost:8000";
const EXPRESS = "http://localhost:3001/api";

// ------------------------------------
// FAST API - Voluntariados Principales
// ------------------------------------

export async function login(data) {
  const res = await fetch(`${FASTAPI}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function getUsuarios() {
  const res = await fetch(`${FASTAPI}/api/usuarios/`);
  return res.json();
}

export async function crearUsuario(data) {
  const res = await fetch(`${FASTAPI}/api/usuarios/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function eliminarUsuario(id) {
  const res = await fetch(`${FASTAPI}/api/usuarios/${id}`, { method: "DELETE" });
  return res.json();
}

export async function getCuidadoAdultos() {
  const res = await fetch(`${FASTAPI}/api/cuidado-adultos-mayores/`);
  return res.json();
}

export async function crearCuidadoAdultos(data) {
  const res = await fetch(`${FASTAPI}/api/cuidado-adultos-mayores/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function eliminarCuidadoAdultos(id) {
  const res = await fetch(`${FASTAPI}/api/cuidado-adultos-mayores/${id}`, { method: "DELETE" });
  return res.json();
}

export async function getPlayas() {
  const res = await fetch(`${FASTAPI}/api/limpieza-playas/`);
  return res.json();
}

export async function crearPlaya(data) {
  const res = await fetch(`${FASTAPI}/api/limpieza-playas/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function eliminarPlaya(id) {
  const res = await fetch(`${FASTAPI}/api/limpieza-playas/${id}`, { method: "DELETE" });
  return res.json();
}

export async function getRescate() {
  const res = await fetch(`${FASTAPI}/api/rescate-animal/`);
  return res.json();
}

export async function crearRescate(data) {
  const res = await fetch(`${FASTAPI}/api/rescate-animal/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function eliminarRescate(id) {
  const res = await fetch(`${FASTAPI}/api/rescate-animal/${id}`, { method: "DELETE" });
  return res.json();
}

export async function getVoluntariados() {
    const res = await fetch(`${FASTAPI}/api/voluntariados/`);
    return res.json();
}

export async function getInscripciones() {
  const res = await fetch(`${FASTAPI}/api/inscripciones/`);
  return res.json();
}

export async function crearInscripcion(data) {
  const res = await fetch(`${FASTAPI}/api/inscripciones/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

// NUEVOS: Programas e Inscripciones a Programas
export async function getProgramas() {
  const res = await fetch(`${FASTAPI}/api/programas/`);
  return res.json();
}

export async function inscribirEnPrograma(data) {
  const res = await fetch(`${FASTAPI}/api/programas/inscripcion`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function getMisProgramas(usuarioId) {
  const res = await fetch(`${FASTAPI}/api/programas/mis-programas/${usuarioId}`);
  return res.json();
}

export async function getUsuario(id) {
  const res = await fetch(`${FASTAPI}/api/usuarios/${id}`);
  return res.json();
}

export async function getHorasSociales(id) {
  const res = await fetch(`${FASTAPI}/api/usuarios/horas/${id}`);
  return res.json();
}

export async function confirmarAsistencia(inscripcionId, horas = 4) {
  const res = await fetch(`${FASTAPI}/api/inscripciones/confirmar/${inscripcionId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ horas })
  });
  return res.json();
}

// ------------------------------------
// EXPRESS API - Ubicaciones (Dropdowns)
// ------------------------------------

export async function getPaises() {
  const res = await fetch(`${EXPRESS}/pais`);
  return res.json();
}

export async function getCiudades() {
  const res = await fetch(`${EXPRESS}/ciudad`);
  return res.json();
}

export async function getUbicaciones() {
  const res = await fetch(`${EXPRESS}/ubicacion`);
  return res.json();
}

export async function getStats() {
  const res = await fetch(`${FASTAPI}/api/stats`);
  return res.json();
}