<script>
import { onMount } from "svelte";
import { getProgramas, getCiudades } from "$lib/api.js";

let programas = [];
let ciudades = [];
let loading = true;
let error = "";

let nuevaJornada = {
  titulo: "",
  descripcion: "",
  fecha: "",
  hora: "",
  cupos: 10,
  programa_id: "",
  ciudad_id: ""
};

async function loadData() {
  try {
    programas = await getProgramas();
    ciudades = await getCiudades();
  } catch (err) {
    error = "Error al cargar datos iniciales.";
  } finally {
    loading = false;
  }
}

async function handleCrear() {
  if (!nuevaJornada.programa_id || !nuevaJornada.ciudad_id) {
    alert("Por favor selecciona programa y ciudad.");
    return;
  }
  
  // Realizar POST a /voluntariados/
  try {
      const FASTAPI = "http://localhost:8000";
      const res = await fetch(`${FASTAPI}/voluntariados/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevaJornada)
      });
      const data = await res.json();
      if (data.id) {
          alert("¡Jornada planificada y publicada!");
          nuevaJornada = { titulo: "", descripcion: "", fecha: "", hora: "", cupos: 10, programa_id: "", ciudad_id: "" };
      }
  } catch (err) {
      alert("Error al guardar la jornada.");
  }
}

onMount(loadData);
</script>

<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-10">
      
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="fw-bold text-dark">Planificación de Jornadas 🛠️</h2>
          <p class="text-muted">Como organizador, define las próximas actividades para los voluntarios.</p>
        </div>
      </div>

      {#if loading}
        <div class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      {:else}
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-4">
            <h5 class="fw-bold mb-4">Nueva Jornada de Voluntariado</h5>
            
            <form on:submit|preventDefault={handleCrear}>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Nombre de la Actividad</label>
                  <input type="text" class="form-control rounded-3" bind:value={nuevaJornada.titulo} placeholder="Ej: Limpieza de Playa Salguero" required>
                </div>

                <div class="col-md-6">
                  <label class="form-label fw-bold small">Programa Asociado</label>
                  <select class="form-select rounded-3" bind:value={nuevaJornada.programa_id} required>
                    <option value="">Selecciona un programa...</option>
                    {#each programas as p}
                      <option value={p.id}>{p.nombre}</option>
                    {/each}
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label fw-bold small">Descripción Detallada</label>
                  <textarea class="form-control rounded-3" rows="3" bind:value={nuevaJornada.descripcion} placeholder="Explica de qué trata la jornada..." required></textarea>
                </div>

                <div class="col-md-4">
                  <label class="form-label fw-bold small">Fecha</label>
                  <input type="date" class="form-control rounded-3" bind:value={nuevaJornada.fecha} required>
                </div>

                <div class="col-md-4">
                  <label class="form-label fw-bold small">Hora</label>
                  <input type="time" class="form-control rounded-3" bind:value={nuevaJornada.hora} required>
                </div>

                <div class="col-md-4">
                  <label class="form-label fw-bold small">Cupos Disponibles</label>
                  <input type="number" class="form-control rounded-3" bind:value={nuevaJornada.cupos} min="1" required>
                </div>

                <div class="col-md-12">
                  <label class="form-label fw-bold small">Ciudad / Ubicación</label>
                  <select class="form-select rounded-3" bind:value={nuevaJornada.ciudad_id} required>
                    <option value="">Selecciona una ciudad...</option>
                    {#each ciudades as c}
                      <option value={c.id}>{c.nombre}</option>
                    {/each}
                  </select>
                </div>

                <div class="col-12 mt-4">
                  <button type="submit" class="btn btn-primary btn-lg w-100 rounded-pill fw-bold shadow-sm">
                    Publicar Jornada
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      {/if}

    </div>
  </div>
</div>
