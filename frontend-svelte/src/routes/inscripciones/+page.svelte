<script>
  import { onMount } from "svelte";
  import { getInscripciones } from "$lib/api";

  let inscripciones = [];
  let cargando = true;

  onMount(async () => {
    inscripciones = await getInscripciones();
    cargando = false;
  });
</script>

<div class="container mt-5">
  <div class="row mb-5">
    <div class="col-12">
      <h1 class="fw-bolder text-dark mb-2">✅ Mis Inscripciones Sociales</h1>
      <p class="text-muted fs-5">Rastrea tus programas activos y las jornadas donde has confirmado participación.</p>
    </div>
  </div>

  <div class="row">
    <div class="col-lg-12">
      <div class="card border-0 shadow-sm rounded-4">
        <div class="card-body p-4">
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th class="text-secondary fw-semibold">Programa / Jornada</th>
                  <th class="text-secondary fw-semibold">Fecha de Registro</th>
                  <th class="text-secondary fw-semibold">Tarea Asignada</th>
                  <th class="text-secondary fw-semibold">Estado</th>
                  <th class="text-center text-secondary fw-semibold">Acción</th>
                </tr>
              </thead>
              <tbody>
                {#each inscripciones as ins}
                  <tr>
                    <td>
                      <div class="fw-bold text-dark">{ins.voluntariado}</div>
                      <small class="text-muted">Inscrito como: {ins.usuario}</small>
                    </td>
                    <td>{ins.fecha}</td>
                    <td>
                      {#if ins.tarea}
                        <span class="badge bg-info bg-opacity-10 text-info fw-bold border border-info rounded-pill px-3">✨ {ins.tarea}</span>
                      {:else}
                        <span class="text-muted small italic">Pendiente por asignar...</span>
                      {/if}
                    </td>
                    <td>
                      <span class="badge {ins.estado === 'Confirmada' ? 'bg-success' : 'bg-primary'} bg-opacity-10 {ins.estado === 'Confirmada' ? 'text-success' : 'text-primary'} rounded-pill px-3 py-1">
                        {ins.estado || 'Confirmada'}
                      </span>
                    </td>
                    <td class="text-center">
                      <button class="btn btn-sm btn-outline-success rounded-pill px-3 fw-bold" disabled={ins.estado === 'Confirmada'}>
                        {ins.estado === 'Confirmada' ? '✅ Asistencia Marcada' : 'Marcar Asistencia'}
                      </button>
                    </td>
                  </tr>

                {:else}
                  {#if cargando}
                    <tr><td colspan="4" class="text-center py-5">Cargando datos...</td></tr>
                  {:else}
                    <tr><td colspan="4" class="text-center py-5 text-muted">Aún no te has inscrito en ninguna jornada. ¡Ve a la pestaña Explorar!</td></tr>
                  {/if}
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>