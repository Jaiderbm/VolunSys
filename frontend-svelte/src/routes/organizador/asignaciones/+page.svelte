<script>
  import { onMount } from "svelte";
  import { getInscripciones } from "$lib/api";

  let inscripciones = [];
  let loading = true;
  let error = "";
  
  // Lista de tareas sugeridas según el programa
  const tareasSugeridas = [
    "Logística y Equipos",
    "Primeros Auxilios",
    "Registro de Asistencia",
    "Gestión de Residuos",
    "Guía de Recorrido",
    "Atención al Público",
    "Coordinación de Transporte"
  ];

  async function loadData() {
    try {
      inscripciones = await getInscripciones();
    } catch (err) {
      error = "Error al cargar las inscripciones.";
    } finally {
      loading = false;
    }
  }

  async function handleAsignar(id, tarea) {
    if (!tarea) return;
    try {
      const res = await fetch(`http://localhost:8000/api/inscripciones/asignar/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tarea })
      });
      const data = await res.json();
      if (data.success) {
        alert("¡Tarea asignada con éxito!");
        loadData(); // Recargar
      }
    } catch (err) {
      alert("Error al asignar tarea.");
    }
  }

  onMount(loadData);
</script>

<div class="container py-5">
  <div class="row mb-4">
    <div class="col">
      <h2 class="fw-bold">✍️ Asignación de Actividades</h2>
      <p class="text-muted">Asigna roles específicos a los voluntarios que se han inscrito en las jornadas.</p>
    </div>
  </div>

  {#if loading}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
  {:else if error}
    <div class="alert alert-danger">{error}</div>
  {:else}
    <div class="row g-4">
      {#each inscripciones as i}
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="badge bg-light text-primary border rounded-pill px-3">{i.voluntariado}</span>
                <span class="text-muted small">{i.fecha}</span>
              </div>
              <h5 class="fw-bold mb-1">{i.usuario}</h5>
              <p class="text-muted small mb-3">Estado: <span class="fw-bold">{i.estado || 'Pendiente'}</span></p>
              
              <div class="border-top pt-3">
                <label class="form-label small fw-bold text-muted">Tarea Asignada:</label>
                {#if i.tarea}
                  <div class="alert alert-info py-2 px-3 rounded-pill small mb-2 d-flex justify-content-between align-items-center">
                    <span>✨ {i.tarea}</span>
                  </div>
                {/if}
                
                <select class="form-select form-select-sm rounded-3 mb-2" on:change={(e) => handleAsignar(i.id, e.target.value)}>
                  <option value="">{i.tarea ? 'Cambiar tarea...' : 'Asignar nueva tarea...'}</option>
                  {#each tareasSugeridas as t}
                    <option value={t}>{t}</option>
                  {/each}
                </select>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
