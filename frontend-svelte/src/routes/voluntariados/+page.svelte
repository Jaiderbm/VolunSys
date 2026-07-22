<script>
import { onMount } from "svelte";
import { getProgramas, inscribirEnPrograma, getMisProgramas } from "$lib/api.js";

let voluntariados = [];
let misProgramasIds = [];
let usuarioId = null;
let loading = true;
let error = "";

async function loadData() {
  try {
    const rawUser = localStorage.getItem("usuario");
    if (rawUser) {
      // Asumiendo que 'usuario' en localStorage es un string o ID
      // Si el backend devuelve un objeto en el login, ajustamos
       usuarioId = localStorage.getItem("usuarioId") || 1; // Fallback para test
    }

    voluntariados = await getProgramas();
    if (usuarioId) {
      const misProgs = await getMisProgramas(usuarioId);
      misProgramasIds = misProgs.map(p => p.id);
    }
  } catch (err) {
    error = "Error al cargar programas.";
  } finally {
    loading = false;
  }
}

async function participio(programaId) {
  if (!usuarioId) {
    alert("Inicia sesión para participar.");
    return;
  }
  const res = await inscribirEnPrograma({ usuario_id: usuarioId, programa_id: programaId });
  if (res.success) {
    alert("¡Inscrito en el programa!");
    loadData();
  } else {
    alert("Error: " + res.message);
  }
}

onMount(loadData);

</script>

<h1 class="mb-4">Programas de Voluntariado</h1>

{#if loading}
  <div class="text-center my-5">
    <div class="spinner-border text-primary" role="status"></div>
    <p class="mt-2">Cargando programas...</p>
  </div>
{:else if error}
  <div class="alert alert-danger">{error}</div>
{:else}
  <div class="row">
    {#each voluntariados as v}
      <div class="col-md-4 mb-4">
        <div class="card shadow h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title fw-bold">{v.nombre}</h5>
            <p class="card-text text-muted">{v.descripcion || 'Sin descripción disponible.'}</p>
            
            <div class="mt-auto">
              {#if misProgramasIds.includes(v.id)}
                <button class="btn btn-outline-success w-100 fw-bold disabled">
                  ✅ Inscrito
                </button>
                <a href="/actividades/{v.id}" class="btn btn-primary w-100 mt-2 fw-bold">
                  Ver Actividades
                </a>
              {:else}
                <button class="btn btn-success w-100 fw-bold" on:click={() => participio(v.id)}>
                  Inscribirse al Programa
                </button>
              {/if}
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
{/if}