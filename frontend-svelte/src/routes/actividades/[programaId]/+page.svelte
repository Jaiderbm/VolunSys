<script>
import { onMount } from "svelte";
import { page } from "$app/stores";
import { getVoluntariados, crearInscripcion } from "$lib/api.js";

let programaId = $page.params.programaId;
let actividades = [];
let misInscripciones = []; // IDs de voluntariados en los que ya estoy inscrito
let loading = true;
let error = "";
let usuarioId = null;

async function loadData() {
  try {
    usuarioId = localStorage.getItem("usuarioId") || 1;
    const allActividades = await getVoluntariados();
    actividades = allActividades.filter(a => a.programa_id == programaId || !a.programa_id); 
    
    // Obtener mis inscripciones reales (Simulado por ahora si no hay endpoint de 'mis-inscripciones')
    const { getInscripciones } = await import("$lib/api.js");
    const todasInsc = await getInscripciones();
    misInscripciones = todasInsc.filter(i => i.usuario_id == usuarioId);
  } catch (err) {
    error = "Error al cargar actividades.";
  } finally {
    loading = false;
  }
}

async function inscribirse(voluntariadoId) {
  const res = await crearInscripcion({
    usuario_id: usuarioId,
    voluntariado_id: voluntariadoId,
    estado: "Pendiente"
  });
  if (res.id) {
    alert("¡Inscripción exitosa! Ahora puedes confirmar tu asistencia.");
    loadData();
  } else {
    alert("Error al inscribirse.");
  }
}

async function confirmar(inscripcionId) {
  const { confirmarAsistencia } = await import("$lib/api.js");
  const res = await confirmarAsistencia(inscripcionId);
  if (res.success) {
    alert("¡Asistencia confirmada! Gracias por tu ayuda.");
    loadData();
  }
}

onMount(loadData);
</script>

<div class="container py-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold text-primary">Próximas Jornadas</h2>
    <a href="/voluntariados" class="btn btn-outline-secondary rounded-pill">Volver</a>
  </div>

  {#if loading}
    <div class="text-center my-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
  {:else if error}
    <div class="alert alert-danger">{error}</div>
  {:else if actividades.length === 0}
    <div class="text-center my-5 p-5 bg-white shadow-sm rounded-4">
      <h4 class="text-muted">No hay jornadas programadas para este programa aún.</h4>
    </div>
  {:else}
    <div class="row g-4">
      {#each actividades as act}
        <div class="col-md-6">
          <div class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden">
            <div class="row g-0">
              <div class="col-4 bg-info bg-opacity-10 d-flex align-items-center justify-content-center">
                <span class="fs-1">🗓️</span>
              </div>
              <div class="col-8">
                <div class="card-body">
                  <h5 class="card-title fw-bold">{act.titulo}</h5>
                  <p class="card-text text-muted small mb-2">
                    {act.descripcion || 'Sin descripción'}
                  </p>
                  <div class="d-flex flex-wrap gap-2 mb-3">
                    <span class="badge bg-light text-dark border">📅 {act.fecha}</span>
                    <span class="badge bg-light text-dark border">⏰ {act.hora}</span>
                    <span class="badge bg-light text-dark border">👥 Cupos: {act.cupos}</span>
                  </div>

                  {#if misInscripciones.find(i => i.voluntariado_id == act.id)}
                    {#if misInscripciones.find(i => i.voluntariado_id == act.id).estado === 'Completado'}
                      <button class="btn btn-success w-100 rounded-pill fw-bold disabled">
                        ✅ Asistencia Confirmada
                      </button>
                    {:else}
                      <button class="btn btn-warning w-100 rounded-pill fw-bold" on:click={() => confirmar(misInscripciones.find(i => i.voluntariado_id == act.id).id)}>
                        Confirmar Asistencia
                      </button>
                    {/if}
                  {:else}
                    <button class="btn btn-primary w-100 rounded-pill fw-bold" on:click={() => inscribirse(act.id)}>
                      Inscribirse a la Jornada
                    </button>
                  {/if}
                </div>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .card {
    transition: transform 0.2s;
  }
  .card:hover {
    transform: translateY(-5px);
  }
</style>
