<script>
  import { onMount } from "svelte"
  import { getUsuarios, crearUsuario, eliminarUsuario } from "$lib/api"

  let rolApp = "";
  let usuarios = [];
  let usuariosFiltrados = [];
  let busqueda = "";

  let form = {
    nombre: "",
    apellido: "",
    email: "",
    telefono: "",
    numero_documento: "",
    password: "",
    rol_id: 3 // Default: Voluntario
  };
  
  let mensajeExito = "";
  let mensajeError = "";
  let procesando = false;

  onMount(async () => {
    if (typeof window !== "undefined") {
      rolApp = localStorage.getItem("rol") || "";
      if(rolApp !== "Admin") {
        alert("Acceso Denegado. Solo Administradores.");
        window.location.href = "/dashboard";
      }
    }
    await cargarDatos();
  });

  async function cargarDatos() {
    usuarios = await getUsuarios();
    usuariosFiltrados = usuarios;
  }

  function filtrarUsuarios() {
    const b = busqueda.toLowerCase();
    usuariosFiltrados = usuarios.filter(u => 
      u.nombre.toLowerCase().includes(b) || 
      u.email.toLowerCase().includes(b) || 
      u.documento.includes(b)
    );
  }

  async function agregar() {
    procesando = true;
    mensajeError = "";
    mensajeExito = "";
    
    if(!form.nombre || !form.email || !form.numero_documento || !form.password) {
      mensajeError = "Llena todos los campos obligatorios.";
      procesando = false;
      return;
    }

    try {
      const dbResponse = await crearUsuario(form);
      if(dbResponse.success) {
        mensajeExito = "¡Usuario creado en el sistema con éxito!";
        form = { nombre: "", apellido: "", email: "", telefono: "", numero_documento: "", password: "", rol_id: 3 };
        await cargarDatos();
        setTimeout(() => mensajeExito = "", 3000);
      } else {
        mensajeError = dbResponse.message || "Error al crear usuario.";
      }
    } catch(e) {
      mensajeError = "Fallo de red.";
    }
    procesando = false;
  }

  async function borrar(id) {
    if(confirm("🚨 Atención: ¿Estás seguro de eliminar este usuario permanentemente? Esta acción es irreversible.")) {
      await eliminarUsuario(id);
      await cargarDatos();
    }
  }
</script>

<div class="container mt-5 mb-5">
  
  <!-- Encabezado y Estadísticas -->
  <div class="row mb-4">
    <div class="col-lg-12">
      <h1 class="fw-bolder text-dark mb-2">Centro de Control de Usuarios 👥</h1>
      <p class="text-muted fs-5">Módulo exclusivo de administración. Gestiona accesos, designa Organizadores u observa la actividad de la comunidad.</p>
    </div>
  </div>

  <div class="row g-4 mb-4">
    <div class="col-md-4">
      <div class="card border-0 shadow-sm rounded-4 h-100" style="background: linear-gradient(135deg, #1e3c72, #2a5298); color:white;">
        <div class="card-body p-4 d-flex flex-column justify-content-center">
          <h5 class="fw-bold mb-1">Total Usuarios Cadastrados</h5>
          <h1 class="display-3 fw-bolder mb-0">{usuarios.length}</h1>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-0 shadow-sm rounded-4 h-100 bg-white">
        <div class="card-body p-4 d-flex flex-column justify-content-center">
          <h5 class="fw-bold mb-1 text-success">Voluntarios Listos</h5>
          <h1 class="display-3 fw-bolder text-dark mb-0">{usuarios.filter(u=>u.rol==='Voluntario').length}</h1>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-0 shadow-sm rounded-4 h-100 bg-white">
        <div class="card-body p-4 d-flex flex-column justify-content-center">
          <h5 class="fw-bold mb-1 text-primary">Coordinadores (Organizadores)</h5>
          <h1 class="display-3 fw-bolder text-dark mb-0">{usuarios.filter(u=>u.rol==='Coordinador').length}</h1>
        </div>
      </div>
    </div>
  </div>

  <hr class="my-5 opacity-25">

  <div class="row">
    <!-- Tabla Interactiva -->
    <div class="col-lg-8">
      <div class="card border-0 shadow rounded-4 mb-4">
        <div class="card-header bg-white border-bottom-0 pt-4 pb-2 px-4 d-flex justify-content-between align-items-center">
          <h4 class="fw-bold text-dark mb-0">Directorio Oficial</h4>
          <input type="text" class="form-control form-control-sm w-50 rounded-pill px-3 shadow-none bg-light border-0" placeholder="🔍 Buscar por nombre o doc..." bind:value={busqueda} on:input={filtrarUsuarios}>
        </div>
        <div class="card-body px-4">
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th class="text-secondary fw-semibold">Personal</th>
                  <th class="text-secondary fw-semibold">Contacto</th>
                  <th class="text-secondary fw-semibold">Rol Asignado</th>
                  <th class="text-center text-secondary fw-semibold">Gestión</th>
                </tr>
              </thead>
              <tbody>
                {#each usuariosFiltrados as u}
                  <tr>
                    <td>
                      <div class="fw-bolder text-dark">{u.nombre} {u.apellido}</div>
                      <small class="text-muted">Doc: {u.documento}</small>
                    </td>
                    <td>
                      <div>{u.email}</div>
                      <small class="text-muted">Tel: {u.telefono || 'N/A'}</small>
                    </td>
                    <td>
                      {#if u.rol === "Admin"}
                        <span class="badge bg-danger rounded-pill px-3 py-1">Administrador</span>
                      {:else if u.rol === "Coordinador"}
                        <span class="badge bg-primary rounded-pill px-3 py-1">Coordinador</span>
                      {:else}
                        <span class="badge bg-success rounded-pill px-3 py-1">Voluntario</span>
                      {/if}
                    </td>
                    <td class="text-center">
                      {#if u.rol !== "Admin"}
                      <button class="btn btn-sm btn-outline-danger shadow-sm rounded-pill px-3 fw-bold" on:click={() => borrar(u.id)}>Retirar</button>
                      {:else}
                      <span class="text-muted small">Protegido</span>
                      {/if}
                    </td>
                  </tr>
                {:else}
                  <tr><td colspan="4" class="text-center text-muted py-5">No se encontraron usuarios activos en el filtro.</td></tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Formulario de Creación con RBAC -->
    <div class="col-lg-4">
      <div class="card border-0 shadow bg-light rounded-4">
        <div class="card-body p-4">
          <h4 class="fw-bold text-primary mb-4">Añadir Nuevo Perfil</h4>
          
          {#if mensajeExito}
            <div class="alert alert-success px-3 py-2 small fw-bold rounded-3">{mensajeExito}</div>
          {/if}
          {#if mensajeError}
            <div class="alert alert-danger px-3 py-2 small fw-bold rounded-3">{mensajeError}</div>
          {/if}

          <form on:submit|preventDefault={agregar}>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label text-muted small fw-bold text-uppercase">Nombre</label>
                <input type="text" class="form-control border-0 shadow-sm" bind:value={form.nombre} required>
              </div>
              <div class="col-6">
                <label class="form-label text-muted small fw-bold text-uppercase">Apellido</label>
                <input type="text" class="form-control border-0 shadow-sm" bind:value={form.apellido} required>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-bold text-uppercase">Doc. Identidad</label>
              <input type="text" class="form-control border-0 shadow-sm" bind:value={form.numero_documento} required>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-bold text-uppercase">Correo Oficial</label>
              <input type="email" class="form-control border-0 shadow-sm" bind:value={form.email} required>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-bold text-uppercase">Contraseña</label>
              <input type="password" class="form-control border-0 shadow-sm" bind:value={form.password} minlength="8" required placeholder="Min 8, Núm, Mayúscula">
            </div>

            <div class="mb-4 p-3 bg-white border shadow-sm rounded-3">
              <label class="form-label text-dark fw-bold text-uppercase">Otorgar Nivel de Acceso</label>
              <select class="form-select border-0 bg-light fw-bold text-primary" bind:value={form.rol_id}>
                <option value={3}>⭐ Voluntario Básico</option>
                <option value={2}>🛠️ Organizador / Coordinador</option>
                <option value={1}>👑 Administrador General</option>
              </select>
              <div class="form-text mt-2" style="font-size: 0.75rem;">Nota: Dar permisos Admin otorga acceso a estas configuraciones de plataforma. Use con precaución.</div>
            </div>

            <button type="submit" class="btn btn-primary d-block w-100 py-3 rounded-pill fw-bold shadow" disabled={procesando}>
              {#if procesando} ⏳ Guardando... {:else} Autorizar y Crear Usuario {/if}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

</div>