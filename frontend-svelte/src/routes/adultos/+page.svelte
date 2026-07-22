<script>
  import { onMount } from 'svelte';
  import { getCuidadoAdultos, crearCuidadoAdultos, eliminarCuidadoAdultos, getCiudades, getVoluntariados, crearInscripcion } from '$lib/api.js';

  let rol = "";
  let usuarioId = null;
  let registros = [];
  let ciudades = [];
  let jornadasDisponibles = [];
  let form = { nombre_adulto: "", edad: "", condicion_medica: "", ubicacion: "", estado: true };

  onMount(async () => {
    rol = localStorage.getItem("rol") || "";
    usuarioId = localStorage.getItem("usuario");
    await loadData();
  });

  async function loadData() {
    try {
      registros = await getCuidadoAdultos();
      const ciudadesExpress = await getCiudades();
      ciudades = Array.isArray(ciudadesExpress) ? ciudadesExpress : [];
      
      const allJornadas = await getVoluntariados();
      // Filtramos las del programa 3 (Adultos)
      jornadasDisponibles = allJornadas.filter(j => j.programa_id === 3);
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
    await crearCuidadoAdultos(form);
    form = { nombre_adulto: "", edad: "", condicion_medica: "", ubicacion: "", estado: true };
    await loadData();
  }

  async function eliminar(id) {
    if(confirm("¿Estás seguro de eliminar este registro?")){
        await eliminarCuidadoAdultos(id);
        await loadData();
    }
  }
</script>

<div class="row mb-4">
  <div class={rol === "Admin" || rol === "Coordinador" ? "col-lg-8" : "col-lg-12"}>
    <div class="card shadow border-0 mb-4 overflow-hidden rounded-4">
      <img src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=1200&q=80" class="card-img-top" alt="Adultos Mayores" style="height: 250px; object-fit: cover;">
      <div class="card-body p-4">
        <h1 class="card-title text-primary fw-bolder mb-3">Apoyo a Adultos Mayores</h1>
        <p class="card-text text-muted fs-5">Este programa promueve el acompañamiento emocional y el apoyo a adultos mayores en estado de vulnerabilidad.</p>
        
        {#if rol === "Admin"}
        <!-- Placeholder para PowerBI exclusivo de administradores -->
        <div class="alert alert-primary mt-4 border-0 shadow-sm d-flex align-items-center" role="alert">
          <div>
            <h5 class="alert-heading fw-bold mb-1">📊 Espacio Analítico PowerBI</h5>
            <p class="mb-0 small">Aquí insertaremos el Dashboard interactivo de Microsoft PowerBI para analizar el alcance de este programa.</p>
          </div>
        </div>
        {/if}
      </div>
    </div>
    
    <!-- Jornadas Disponibles para Inscripción -->
    {#if rol !== "Coordinador"}
    <div class="row g-4 mb-4">
      <div class="col-12">
        <h3 class="fw-bold text-dark mb-3">👵 Jornadas de Acompañamiento (Inscríbete)</h3>
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
                {rol ? '🤝 ¡Quiero Participar!' : '🔑 Inicia sesión para unirte'}
              </button>
            </div>
          </div>
        </div>
      {:else}
        <div class="col-12"><p class="text-muted">No hay jornadas de acompañamiento programadas.</p></div>
      {/each}
    </div>
    {/if}


    <!-- Data Table -->
    <div class="card shadow border-0 rounded-4">
      <div class="card-header bg-white border-bottom-0 pt-4 pb-2 px-4">
        <h5 class="fw-bold text-dark mb-0">Registros y Beneficiarios</h5>
      </div>
      <div class="card-body px-4">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th class="text-secondary fw-semibold">Nombre</th>
                <th class="text-secondary fw-semibold">Edad</th>
                <th class="text-secondary fw-semibold">Condición</th>
                <th class="text-secondary fw-semibold">Ubicación</th>
                {#if rol === "Admin" || rol === "Coordinador"}
                <th class="text-center text-secondary fw-semibold">Acción</th>
                {/if}
              </tr>
            </thead>
            <tbody>
              {#each registros as reg}
                <tr>
                  <td class="fw-medium">{reg.nombre_adulto}</td>
                  <td>{reg.edad}</td>
                  <td><span class="badge bg-secondary fw-normal">{reg.condicion_medica}</span></td>
                  <td>{reg.ubicacion}</td>
                  {#if rol === "Admin" || rol === "Coordinador"}
                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-danger rounded-pill px-3 shadow-sm" on:click={() => eliminar(reg.id)}>Borrar</button>
                  </td>
                  {/if}
                </tr>
              {:else}
                <tr><td colspan="5" class="text-center text-muted py-5">No hay registros todavía en la base de datos de FastAPI.</td></tr>
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
        <h5 class="fw-bold text-primary mb-4">Agregar Beneficiario</h5>
        <form on:submit|preventDefault={submit}>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Nombre del Adulto</label>
            <input type="text" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.nombre_adulto} placeholder="Ej. Juan Pérez" required>
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Edad</label>
            <input type="number" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.edad} placeholder="Ej. 75" required>
          </div>
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold text-uppercase">Condición Médica</label>
            <input type="text" class="form-control form-control-lg border-0 shadow-sm" bind:value={form.condicion_medica} placeholder="Ej. Hipertensión">
          </div>
          <div class="mb-4">
            <label class="form-label text-muted small fw-bold text-uppercase" for="ubicacion-adultos">Ubicación</label>
            <select id="ubicacion-adultos" class="form-select form-select-lg border-0 shadow-sm" bind:value={form.ubicacion} required>
              <option value="" disabled selected>
                {ciudades.length > 0 ? 'Seleccione la ciudad...' : 'Cargando ciudades...'}
              </option>
              {#each ciudades as ciudad}
                <option value={ciudad.nombre}>{ciudad.nombre}</option>
              {/each}
            </select>
          </div>
          <button type="submit" class="btn btn-primary btn-lg w-100 rounded-pill shadow fw-bold">Guardar Registro</button>
        </form>
      </div>
    </div>

    <!-- Placeholder Chatbot -->
    <div class="card shadow border-0 rounded-4 bg-dark text-white text-center" style="background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);">
      <div class="card-body p-5">
        <div class="fs-1 mb-3">🤖</div>
        <h5 class="fw-bold mb-2">Asistente IA (Chatbot)</h5>
        <p class="small text-white-50 mb-0">Espacio reservado para la ventana del Chatbot inteligente que asiste a los voluntarios.</p>
      </div>
    </div>
  </div>
  {/if}
</div>