<script>
  import { onMount } from 'svelte';
  import { getInscripciones } from '$lib/api';
  
  let rol = "";
  let nombre_usuario = "";
  let miTarea = "";

  onMount(async () => {
    if (typeof window !== "undefined") {
      rol = localStorage.getItem("rol") || "";
      nombre_usuario = rol === "Admin" ? "Administrador Jefe" : (rol === "Coordinador" ? "Organizador" : "Voluntario");
      
      if (rol === "User") {
        const ins = await getInscripciones();
        // Buscar la última tarea asignada
        const ultimaConTarea = ins.reverse().find(i => i.tarea && i.tarea !== "");
        if (ultimaConTarea) {
          miTarea = ultimaConTarea.tarea;
        }
      }
    }
  });
</script>

<style>
  .dashboard-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    border-radius: 20px;
    overflow: hidden;
  }
  .dashboard-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  }
  .card-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: inline-block;
  }
</style>

<div class="container mt-5">
  {#if miTarea && rol === "User"}
    <div class="alert alert-info border-0 rounded-4 shadow-sm p-4 mb-5 d-flex align-items-center animate__animated animate__fadeInDown" style="background: linear-gradient(90deg, #e3f2fd 0%, #ffffff 100%);">
      <div class="fs-1 me-4">🚀</div>
      <div>
        <h4 class="fw-bold mb-1 text-primary">¡Tienes una nueva tarea asignada!</h4>
        <p class="mb-0 text-dark opacity-75">Tu próxima misión es: <span class="fw-bolder fs-5 text-uppercase">{miTarea}</span>. Prepárate para el impacto social.</p>
      </div>
      <a href="/inscripciones" class="btn btn-primary rounded-pill ms-auto px-4 fw-bold">Ver Detalles</a>
    </div>
  {/if}

  <div class="row mb-5 align-items-center">
    <div class="col-md-8">
      <h1 class="fw-bolder text-dark mb-1">¡Bienvenido, <span class="text-primary">{nombre_usuario}</span>! 👋</h1>
      <p class="text-muted fs-5">Tu panel central de operaciones VolunSys. Aquí tienes el control de todo.</p>
    </div>
    <div class="col-md-4 text-md-end">
      <span class="badge rounded-pill px-4 py-2 fs-6 shadow-sm" style="background: linear-gradient(45deg, #11998e, #38ef7d);">
        🟢 Nivel de Acceso: {rol}
      </span>
    </div>
  </div>

  <div class="row g-4">
    <!-- Usuarios (Social) - Solo Admin -->
    {#if rol === "Admin"}
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-white">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">👥</span>
          </div>
          <h4 class="fw-bold mb-2">Gestión de Usuarios</h4>
          <p class="text-muted small">Administra las cuentas y roles de la plataforma.</p>
          <a href="/usuarios" class="btn btn-primary rounded-pill w-100 fw-bold mt-2">
            Administrar Usuarios
          </a>
        </div>
      </div>
    </div>
    {/if}


    <!-- Gestión de Programas (Active for Admin/Coordinador) -->
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-white">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">📅</span>
          </div>
          <h4 class="fw-bold mb-2">Planificación</h4>
          <p class="text-muted small">Crea y organiza nuevas jornadas de impacto social.</p>
          {#if rol === "Admin" || rol === "Coordinador"}
            <a href="/organizador/planificacion" class="btn btn-warning rounded-pill w-100 fw-bold mt-2 text-dark">Planificar Ahora</a>
          {:else}
            <a href="/voluntariados" class="btn btn-outline-warning rounded-pill w-100 fw-bold mt-2 text-dark">Ver Calendario</a>
          {/if}
        </div>
      </div>
    </div>

    <!-- Asignaciones (NEW for Organizer/Admin) -->
    {#if rol === "Admin" || rol === "Coordinador"}
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-white border-start border-4 border-info">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">✍️</span>
          </div>
          <h4 class="fw-bold mb-2 text-info">Asignar Tareas</h4>
          <p class="text-muted small">Asigna actividades específicas a los voluntarios inscritos.</p>
          <a href="/organizador/asignaciones" class="btn btn-info rounded-pill w-100 fw-bold mt-2 text-white">Ir a Asignaciones</a>
        </div>
      </div>
    </div>
    {/if}

    <!-- Mis Inscripciones (For Volunteers) -->
    {#if rol === "User"}
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-white border-start border-4 border-success">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">✅</span>
          </div>
          <h4 class="fw-bold mb-2 text-success">Mis Actividades</h4>
          <p class="text-muted small">Revisa tus inscripciones y las tareas que te han asignado.</p>
          <a href="/inscripciones" class="btn btn-success rounded-pill w-100 fw-bold mt-2">Ver Mis Tareas</a>
        </div>
      </div>
    </div>
    {/if}

    <!-- Power BI / Analytics -->
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-dark text-white">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">📊</span>
          </div>
          <h4 class="fw-bold mb-2 text-warning">Impacto Real</h4>
          <p class="text-white-50 small">Visualiza métricas y resultados mediante Power BI.</p>
          <a href="/powerbi" class="btn btn-warning rounded-pill w-100 fw-bold mt-2 text-dark">Abrir Dashboard</a>
        </div>
      </div>
    </div>

    <!-- Programas Detallados -->
    <div class="col-lg-4 col-md-6">
      <div class="card dashboard-card h-100 shadow-sm border-0 bg-primary text-white" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="card-body p-4 text-center">
          <div class="mb-3">
            <span class="fs-1">🏖️</span>
          </div>
          <h4 class="fw-bold mb-2">Explorar Áreas</h4>
          <p class="text-white-50 small">Explora las playas, rescate y apoyo a adultos.</p>
          <div class="d-flex gap-2 mt-3">
            <a href="/playas" class="btn btn-sm btn-light rounded-pill flex-grow-1">🏖️ Playas</a>
            <a href="/rescate" class="btn btn-sm btn-light rounded-pill flex-grow-1">🐾 Rescate</a>
            <a href="/adultos" class="btn btn-sm btn-light rounded-pill flex-grow-1">👵 Adultos</a>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>