<script>
  import { onMount } from 'svelte';
  import { getPlayas, crearPlaya, eliminarPlaya, getCiudades, getVoluntariados, crearInscripcion } from '$lib/api.js';

  let rol = "";
  let usuarioId = null;
  let registros = [];
  let ubicaciones = [];
  let jornadasDisponibles = [];
  let form = { nombre_playa: "", ubicacion: "", cantidad_basura_estimada_kg: "", estado: true };

  onMount(async () => {
    rol = localStorage.getItem("rol") || "";
    usuarioId = localStorage.getItem("usuario");
    await loadData();
  });

  async function loadData() {
    try {
      registros = await getPlayas();
      const ciudadesExpress = await getCiudades();
      ubicaciones = Array.isArray(ciudadesExpress) ? ciudadesExpress : [];
      
      const allJornadas = await getVoluntariados();
      // Filtramos las del programa 1 (Playa)
      jornadasDisponibles = allJornadas.filter(j => j.programa_id === 1);
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
    await crearPlaya(form);
    form = { nombre_playa: "", ubicacion: "", cantidad_basura_estimada_kg: "", estado: true };
    await loadData();
  }

  async function eliminar(id) {
    if(confirm("¿Estás seguro de eliminar este registro?")){
        await eliminarPlaya(id);
        await loadData();
    }
  }
</script>

<div class="row mb-4">
  <div class={rol === "Admin" || rol === "Coordinador" ? "col-lg-8" : "col-lg-12"}>
    <div class="card shadow border-0 mb-4 overflow-hidden rounded-4">
      <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80" class="card-img-top" alt="Limpieza Playas" style="height: 250px; object-fit: cover;">
      <div class="card-body p-4">
        <h1 class="card-title text-success fw-bolder mb-3">Limpieza de Playas</h1>
        <p class="card-text text-muted fs-5">Programa para proteger el medio ambiente mediante jornadas de limpieza y recolección de residuos en las playas locales.</p>
        
        {#if rol === "Admin"}
        <!-- Placeholder para PowerBI -->
        <div class="alert alert-success mt-4 border-0 shadow-sm d-flex align-items-center" role="alert">
          <div>
            <h5 class="alert-heading fw-bold mb-1">📊 Panel de Sostenibilidad PowerBI</h5>
            <p class="mb-0 small">Este espacio contendrá las métricas visuales para rastrear los kilos de basura recolectada históricamente.</p>
          </div>
        </div>
        {/if}
      </div>
    </div>

    <!-- Jornadas Disponibles para Inscripción (NUEVO) -->
    {#if rol !== "Coordinador"}
    <div class="row g-4 mb-4">
      <div class="col-12">
        <h3 class="fw-bold text-dark mb-3">📅 Jornadas Disponibles (Inscríbete Aquí)</h3>
      </div>
      {#each jornadasDisponibles as jornada}
        <div class="col-md-6">
          <div class="card border-0 shadow-sm rounded-4 h-100 bg-white">
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="fw-bold text-primary mb-0">{jornada.titulo}</h5>
                <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill px-3">{jornada.cupos} Cupos</span>
              </div>
              <p class="text-muted small mb-3">{jornada.descripcion}</p>
              <div class="d-flex align-items-center mb-4">
                <div class="me-3 small text-muted"><i class="bi bi-calendar-event me-1"></i> {jornada.fecha}</div>
                <div class="small text-muted"><i class="bi bi-clock me-1"></i> {jornada.hora}</div>
              </div>
              <button 
                class="btn {rol ? 'btn-primary' : 'btn-outline-primary'} w-100 rounded-pill fw-bold" 
                on:click={() => inscribirse(jornada.id)}
              >
                {rol ? '🚀 ¡Quiero Participar!' : '🔑 Inicia sesión para unirte'}
              </button>
            </div>
          </div>
        </div>
      {:else}
        <div class="col-12"><p class="text-muted">No hay jornadas abiertas en este momento.</p></div>
      {/each}
    </div>
    {/if}

    <!-- Data Table -->
    <div class="card shadow border-0 rounded-4">
      <div class="card-header bg-white border-bottom-0 pt-4 pb-2 px-4">
        <h5 class="fw-bold text-dark mb-0">Histórico de Actividad en Playas</h5>
      </div>
      <div class="card-body px-4">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th class="text-secondary fw-semibold">Nombre de Playa</th>
                <th class="text-secondary fw-semibold">Ubicación</th>
                <th class="text-secondary fw-semibold">Basura Estimada (Kg)</th>
                {#if rol === "Admin" || rol === "Coordinador"}
                <th class="text-center text-secondary fw-semibold">Acción</th>
                {/if}
              </tr>
            </thead>
            <tbody>
              {#each registros as reg}
                <tr>
                  <td class="fw-medium text-success">{reg.nombre_playa}</td>
                  <td>{reg.ubicacion}</td>
                  <td><span class="badge bg-success bg-opacity-75 fs-6 px-3">{reg.cantidad_basura_estimada_kg} Kg</span></td>
                  {#if rol === "Admin" || rol === "Coordinador"}
                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3 shadow-sm" on:click={() => eliminar(reg.id)}>Borrar</button>
                  </td>
                  {/if}
                </tr>
              {:else}
                <tr><td colspan="4" class="text-center text-muted py-5">No hay jornadas de limpieza registradas aún.</td></tr>
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
        <h5 class="fw-bold text-success mb-4">Registrar Nueva Playa</h5>
        <form on:submit|preventDefault={submit}>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Nombre de la Playa</label>
            <input type="text" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.nombre_playa} placeholder="Ej. Playa Salguero" required>
          </div>
          <div class="mb-4">
            <label class="form-label text-muted small fw-bold text-uppercase" for="ubicacion-playa">Ubicación</label>
            <select id="ubicacion-playa" class="form-select form-select-lg border-0 shadow-sm" bind:value={form.ubicacion} required>
              <option value="" disabled selected>
                {ubicaciones.length > 0 ? 'Seleccione la ciudad...' : 'Cargando ciudades...'}
              </option>
              {#each ubicaciones as ubi}
                <option value={ubi.nombre}>{ubi.nombre}</option>
              {/each}
            </select>
          </div>
          <div class="mb-4">
            <label class="form-label text-muted small fw-bold text-uppercase">Basura a Recolectar (Kg)</label>
            <input type="number" step="0.1" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.cantidad_basura_estimada_kg} placeholder="Ej. 150.5" required>
          </div>
          <button type="submit" class="btn btn-success btn-lg w-100 rounded-pill shadow fw-bold">Añadir Jornada</button>
        </form>
      </div>
    </div>

    <!-- Placeholder Chatbot -->
    <div class="card shadow border-0 rounded-4 text-white text-center" style="background: linear-gradient(135deg, #134e5e 0%, #71b280 100%);">
      <div class="card-body p-5">
        <div class="fs-1 mb-3">💬</div>
        <h5 class="fw-bold mb-2">Bot Orientador Ecológico</h5>
        <p class="small text-white-50 mb-0">Asistente automatizado en construcción.</p>
      </div>
    </div>
  </div>
  {/if}
</div>