<script>
import { onMount, afterUpdate } from "svelte"
import { page } from '$app/stores';

let rol = ""

// Función para actualizar el rol desde localStorage
function checkAuth() {
  if (typeof window !== "undefined") {
    rol = localStorage.getItem("rol") || ""
  }
}

onMount(() => {
  checkAuth();
  // Listener para cambios de ruta (popstate)
  window.addEventListener("popstate", checkAuth);
});

// Forzar verificación en cada tick de Svelte (más robusto)
afterUpdate(() => {
  checkAuth();
});

function logout() {
  localStorage.removeItem("rol")
  localStorage.removeItem("token")
  localStorage.removeItem("usuario")
  rol = ""
  window.location.href = "/login"
}

$: isHome = $page.url.pathname === "/";
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm" style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);">
  <div class="container d-flex justify-content-between align-items-center py-2">

    <a class="navbar-brand fw-bolder fs-4" href="/">
      🌟 VolunSys
    </a>

    <div>
      {#if rol && !isHome}
        <!-- VISTA AUTENTICADA (Solo fuera de Home) -->
        <a class="btn btn-primary bg-opacity-10 shadow-sm rounded-pill px-3 me-3" style="border: 1px solid rgba(255,255,255,0.2);" href="/dashboard">🏠 Dashboard</a>
        
        <!-- Botón Perfil (Todos los roles) -->
        <a class="btn btn-light rounded-pill px-3 me-3 text-primary fw-bold shadow-sm" href="/perfil">👤 Perfil</a>
        
        <!-- Botón Mis Inscripciones (Solo Voluntarios) -->
        {#if rol === "User"}
          <a class="btn btn-light rounded-pill px-3 me-3 text-success fw-bold shadow-sm" href="/inscripciones">✅ Mis Actividades</a>
        {/if}

        <!-- Dropdown Gestión (Admin / Organizador) -->
        {#if rol === "Admin" || rol === "Coordinador"}
        <div class="dropdown d-inline-block me-3">
          <button class="btn btn-warning rounded-pill px-3 dropdown-toggle shadow-sm text-dark fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false">
            🔧 Gestión
          </button>
          <ul class="dropdown-menu shadow">
            {#if rol === "Admin"}
              <li><a class="dropdown-item" href="/usuarios">👥 Usuarios</a></li>
            {/if}
            <li><a class="dropdown-item" href="/organizador/planificacion">📅 Planificar Jornada</a></li>
            <li><a class="dropdown-item" href="/organizador/asignaciones">✍️ Asignar Tareas</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/powerbi">📊 Power BI</a></li>
          </ul>
        </div>
        {/if}

        <button class="btn btn-danger rounded-pill px-4 shadow fw-bold" on:click={logout}>
          🚪 Salir
        </button>
      {:else if rol && isHome}
        <!-- VISTA AUTENTICADA EN HOME (Simplificada) -->
        <a class="btn btn-light rounded-pill px-4 shadow fw-bold text-primary me-3" href="/dashboard">
          🚀 Ir al Dashboard
        </a>
        <button class="btn btn-outline-light rounded-pill px-4 shadow fw-bold" on:click={logout}>
          Salir
        </button>
      {:else}
        <!-- VISTA GUEST (LIMPIA) -->
        <a class="btn btn-light rounded-pill px-4 shadow fw-bold text-primary" href="/login">
          🔑 Iniciar Sesión
        </a>
      {/if}
    </div>

  </div>
</nav>
