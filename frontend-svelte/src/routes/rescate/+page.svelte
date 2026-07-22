<script>
  import { onMount } from 'svelte';
  import { getRescate, crearRescate, eliminarRescate, getCiudades, getVoluntariados, crearInscripcion } from '$lib/api.js';

  let rol = "";
  let usuarioId = null;
  let registros = [];
  let ciudades = [];
  let jornadasDisponibles = [];
  let form = { tipo_animal: "", condicion: "", ubicacion: "", estado: true };

  onMount(async () => {
    rol = localStorage.getItem("rol") || "";
    usuarioId = localStorage.getItem("usuario");
    await loadData();
  });

  async function loadData() {
    try {
      registros = await getRescate();
      const ciudadesExpress = await getCiudades();
      ciudades = Array.isArray(ciudadesExpress) ? ciudadesExpress : [];
      
      const allJornadas = await getVoluntariados();
      // Filtramos las del programa 2 (Rescate)
      jornadasDisponibles = allJornadas.filter(j => j.programa_id === 2);
    } catch (e) {
      console.error("Error loading data", e);
    }
  }

  async function inscribirse(jornadaId) {
    if (!rol) {
      alert("Debes iniciar sesión para inscribirte.");
      window.location.href = "/login";
      return;
    }
    const data = { usuario_id: parseInt(usuarioId), voluntariado_id: jornadaId };
    const res = await crearInscripcion(data);
    if(res.success) {
      alert("¡Enhorabuena! Te has inscrito correctamente. Revisa 'Mis Inscripciones'.");
    }
  }

  async function submit() {
    await crearRescate(form);
    form = { tipo_animal: "", condicion: "", ubicacion: "", estado: true };
    await loadData();
  }

  async function eliminar(id) {
    if(confirm("¿Estás seguro de eliminar este registro?")){
        await eliminarRescate(id);
        await loadData();
    }
  }
</script>

<div class="row mb-4">
  <div class={rol === "Admin" || rol === "Coordinador" ? "col-lg-8" : "col-lg-12"}>
    <div class="card shadow border-0 mb-4 overflow-hidden rounded-4">
      <img src="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=1200&q=80" class="card-img-top" alt="Rescate Animal" style="height: 250px; object-fit: cover;">
      <div class="card-body p-4">
        <h1 class="card-title text-warning fw-bolder mb-3" style="color: #e67e22 !important;">Rescate Animal</h1>
        <p class="card-text text-muted fs-5">Fondo y logística para salvaguardar la vida de animales callejeros, brindándoles cuidado y atención médica inmediata.</p>
        
        {#if rol === "Admin"}
        <!-- Placeholder para PowerBI -->
        <div class="alert alert-warning mt-4 border-0 shadow-sm d-flex align-items-center" role="alert">
          <div>
            <h5 class="alert-heading fw-bold mb-1">📊 Estadísticas (PowerBI)</h5>
            <p class="mb-0 small text-dark">Área destinada para visualizar el crecimiento de adopciones y rescates mediante gráficos avanzados.</p>
          </div>
        </div>
        {/if}
      </div>
    </div>
    
    <!-- Jornadas Disponibles para Inscripción -->
    {#if rol !== "Coordinador"}
    <div class="row g-4 mb-4">
      <div class="col-12">
        <h3 class="fw-bold text-dark mb-3">🐾 Jornadas de Rescate (Inscríbete)</h3>
      </div>
      {#each jornadasDisponibles as jornada}
        <div class="col-md-6">
          <div class="card border-0 shadow-sm rounded-4 h-100 bg-white">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="fw-bold text-warning mb-0" style="color: #e67e22 !important;">{jornada.titulo}</h5>
                <span class="badge bg-warning bg-opacity-10 text-dark rounded-pill px-3">{jornada.cupos} Cupos</span>
              </div>
              <p class="text-muted small mb-3">{jornada.descripcion}</p>
              <div class="d-flex align-items-center mb-4">
                <div class="me-3 small text-muted"><i class="bi bi-calendar-event me-1"></i> {jornada.fecha}</div>
                <div class="small text-muted"><i class="bi bi-clock me-1"></i> {jornada.hora}</div>
              </div>
              <button 
                class="btn {rol ? 'btn-warning' : 'btn-outline-warning'} w-100 rounded-pill fw-bold {rol ? 'text-white' : ''}" 
                style={rol ? "background-color: #e67e22; border:none;" : ""}
                on:click={() => inscribirse(jornada.id)}
              >
                {rol ? '🐈 ¡Quiero Ayudar!' : '🔑 Inicia sesión para unirte'}
              </button>
            </div>
          </div>
        </div>
      {:else}
        <div class="col-12"><p class="text-muted">No hay jornadas de rescate programadas.</p></div>
      {/each}
    </div>
    {/if}


    <!-- Data Table -->
    <div class="card shadow border-0 rounded-4">
      <div class="card-header bg-white border-bottom-0 pt-4 pb-2 px-4">
        <h5 class="fw-bold text-dark mb-0">Casos Activos</h5>
      </div>
      <div class="card-body px-4">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th class="text-secondary fw-semibold">Especie / Tipo</th>
                <th class="text-secondary fw-semibold">Condición Médica</th>
                <th class="text-secondary fw-semibold">Ciudad de Rescate</th>
                {#if rol === "Admin" || rol === "Coordinador"}
                <th class="text-center text-secondary fw-semibold">Acción</th>
                {/if}
              </tr>
            </thead>
            <tbody>
              {#each registros as reg}
                <tr>
                  <td class="fw-bolder">{reg.tipo_animal}</td>
                  <td><span class="badge bg-danger bg-opacity-75">{reg.condicion}</span></td>
                  <td>{reg.ubicacion}</td>
                  {#if rol === "Admin" || rol === "Coordinador"}
                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3 shadow-sm" on:click={() => eliminar(reg.id)}>Marcar Resuelto</button>
                  </td>
                  {/if}
                </tr>
              {:else}
                <tr><td colspan="4" class="text-center text-muted py-5">Ningún caso activo de rescate en este momento.</td></tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  {#if rol === "Admin" || rol === "Coordinador"}
  <div class="col-lg-4">
    <!-- Formulario -->
    <div class="card shadow border-0 bg-light rounded-4 mb-4">
      <div class="card-body p-4">
        <h5 class="fw-bold mb-4" style="color: #e67e22;">Reportar Nuevo Caso</h5>
        <form on:submit|preventDefault={submit}>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Tipo de Animal</label>
            <input type="text" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.tipo_animal} placeholder="Ej. Perro Criollo" required>
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Detalle Médico / Condición</label>
            <input type="text" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.condicion} placeholder="Ej. Fractura" required>
          </div>
          <div class="mb-4">
            <label class="form-label text-muted small fw-bold text-uppercase" for="ciudad-rescate">Ciudad</label>
            <select id="ciudad-rescate" class="form-select form-select-lg border-0 shadow-sm" bind:value={form.ubicacion} required>
              <option value="" disabled selected>
                {ciudades.length > 0 ? 'Seleccione la ciudad...' : 'Cargando ciudades...'}
              </option>
              {#each ciudades as ciudad}
                <option value={ciudad.nombre}>{ciudad.nombre}</option>
              {/each}
            </select>
          </div>
          <button type="submit" class="btn btn-warning btn-lg w-100 rounded-pill shadow fw-bold text-white" style="background-color: #e67e22; border:none;">Registrar Alerta</button>
        </form>
      </div>
    </div>

    <!-- Placeholder Chatbot -->
    <div class="card shadow border-0 rounded-4 text-white text-center" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);">
      <div class="card-body p-5">
        <div class="fs-1 mb-3">🐶</div>
        <h5 class="fw-bold mb-2">Bot de Urgencias Veterinarias</h5>
        <p class="small text-white-50 mb-0">Módulo IoT o Asistente AI en un futuro cercano para triage.</p>
      </div>
    </div>
  </div>
  {/if}
</div>