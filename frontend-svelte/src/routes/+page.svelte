<script>
  import { onMount } from "svelte";
  let rol = "";

  onMount(() => {
    rol = localStorage.getItem("rol") || "";
  });
</script>

<style>
  .hero-animated {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1559027615-cd76efc2c3fa?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-position: center;
    min-height: 80vh;
    display: flex;
    align-items: center;
    color: white;
  }
</style>

<!-- HERO SECTION -->
<div class="hero-animated text-center mb-5">
  <div class="container position-relative" style="z-index: 3;">
    <h1 class="display-3 fw-bolder mb-4" style="color: #fff; letter-spacing: -1px; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);">¡Transforma tu ciudad hoy! 🌟</h1>
    <p class="lead mb-5 fs-4 fw-medium mx-auto" style="max-width: 800px; color: #f0f0f0; text-shadow: 1px 1px 6px rgba(0,0,0,0.9);">
      VolunSys es el puente interactivo entre tus ganas de ayudar y las comunidades locales que te necesitan.
    </p>
    <div class="d-flex justify-content-center gap-3 flex-wrap">
      {#if !rol}
        <a href="/registro" class="btn btn-warning btn-lg fw-bold rounded-pill shadow-lg px-5 py-3 fs-5" style="background: linear-gradient(45deg, #f5af19, #f12711); border:none; color:white;">
          ¡Únete como Voluntario!
        </a>
        <a href="/login" class="btn btn-outline-light btn-lg fw-bold rounded-pill px-5 py-3 fs-5" style="border-width: 2px; color: white; border-color: white;">
          Iniciar Sesión
        </a>
      {:else}
        <a href="/dashboard" class="btn btn-light btn-lg fw-bold rounded-pill px-5 py-3 fs-5 shadow-sm text-primary">
          🚀 Ir a mi Panel
        </a>
      {/if}
    </div>
  </div>
</div>


<div class="container">

  <!-- COMO FUNCIONA (DIDÁCTICO) -->
  <div class="text-center mb-5 mt-5">
    <h2 class="fw-bold mb-3" style="color: #1e3c72; font-size: 2.5rem;">¿Cómo funciona? 🤔</h2>
    <p class="text-muted fs-5 mb-5">Un proceso sencillo, transparente y diseñado para generar impacto real.</p>
    
    <div class="row position-relative timeline-wrapper">
      <div class="col-md-4 mb-4 mb-md-0 position-relative">
        <div class="timeline-step text-primary">📝</div>
        <h4 class="fw-bold">1. Te Registras</h4>
        <p class="text-muted px-3">Crea tu cuenta gratuita. Solo te pediremos tu nombre, documento y correo para identificarte oficialmente.</p>
      </div>
      <div class="col-md-4 mb-4 mb-md-0 position-relative">
        <div class="timeline-step text-warning">🔍</div>
        <h4 class="fw-bold">2. Exploras</h4>
        <p class="text-muted px-3">Navega por las jornadas disponibles (Rescate animal, Playas, Adultos Mayores) y lee los detalles.</p>
      </div>
      <div class="col-md-4 position-relative">
        <div class="timeline-step text-success">🤝</div>
        <h4 class="fw-bold">3. Participas</h4>
        <p class="text-muted px-3">Haz clic en Inscribirse, acude a la fecha del evento y suma horas a tu historial de impacto social.</p>
      </div>
    </div>
  </div>

  <hr class="my-5 text-muted opacity-25">

  <!-- PRÓXIMOS EVENTOS (INTERACTIVOS) -->
  <div class="text-center mb-5 mt-5">
    <h2 class="fw-bold mb-3" style="color: #1e3c72; font-size: 2.5rem;">Próximas Jornadas 📅</h2>
    <p class="text-muted fs-5">Haz clic en la tarjeta que más te guste para ver la información detallada.</p>
  </div>

  <div class="row g-4 mb-5">
    <!-- Clickable Card 1 -->
    <div class="col-md-4">
       <a href="/playas" class="card h-100 glass-card rounded-4 p-4 text-center text-decoration-none">
         <div class="fs-1 mb-3">🏖️</div>
         <div class="event-date mb-3 mx-auto shadow-sm">15 de Abril, 2026</div>
         <h4 class="fw-bold text-dark event-title transition">Limpieza Salguero</h4>
         <p class="text-muted mt-2">Jornada intensiva de limpieza de costas con más de 200 voluntarios esperados. ¡Súmate!</p>
         <div class="mt-auto pt-3">
           <span class="badge rounded-pill bg-light text-primary border px-3 py-2">Explorar Programa</span>
         </div>
       </a>
    </div>
    <!-- Clickable Card 2 -->
    <div class="col-md-4">
       <a href="/rescate" class="card h-100 glass-card rounded-4 p-4 text-center text-decoration-none">
         <div class="fs-1 mb-3">🐶</div>
         <div class="event-date mb-3 mx-auto shadow-sm" style="background: linear-gradient(45deg, #11998e, #38ef7d);">22 de Abril, 2026</div>
         <h4 class="fw-bold text-dark event-title transition">Vacunación Animal</h4>
         <p class="text-muted mt-2">Apoyo a la fundación local para la vacunación masiva de perros y gatos callejeros.</p>
         <div class="mt-auto pt-3">
           <span class="badge rounded-pill bg-light text-warning border px-3 py-2">Explorar Programa</span>
         </div>
       </a>
    </div>
    <!-- Clickable Card 3 -->
    <div class="col-md-4">
       <a href="/adultos" class="card h-100 glass-card rounded-4 p-4 text-center text-decoration-none">
         <div class="fs-1 mb-3">👴🏼</div>
         <div class="event-date mb-3 mx-auto shadow-sm" style="background: linear-gradient(45deg, #8E2DE2, #4A00E0);">01 de Mayo, 2026</div>
         <h4 class="fw-bold text-dark event-title transition">Bingo Solidario</h4>
         <p class="text-muted mt-2">Acompañamiento y actividades lúdicas para la tercera edad en el asilo de la ciudad.</p>
         <div class="mt-auto pt-3">
           <span class="badge rounded-pill bg-light text-primary border px-3 py-2">Explorar Programa</span>
         </div>
       </a>
    </div>
  </div>

</div>