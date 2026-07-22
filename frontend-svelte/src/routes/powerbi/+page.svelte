<script>
  import { onMount } from "svelte";
  import { getStats } from "$lib/api";

  // Tu link actual de Power BI
  let powerBIUrl = "https://app.powerbi.com/view?r=eyJrIjoiYjdkOGQ2ZGMtZjY5NC00YmFkLWI2MDAtMTc3NDQzMTI2N2IzIiwidCI6IjFlOWFhYmU4LTY3ZjgtNGYxYy1hMzI5LWE3NTRlOTI0OTlhZSIsImMiOjR9"; 
  
  let stats = {
    total_voluntarios: 0,
    horas_sociales: 0,
    programas_activos: 0,
    inscripciones_totales: 0
  };

  onMount(async () => {
    try {
      stats = await getStats();
    } catch (e) {
      console.error("Error loading stats", e);
    }
  });
</script>

<style>
  .dashboard-container {
    padding: 2rem;
    background: #f8f9fa;
    min-height: 100vh;
  }
  .card-stats {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: none;
    transition: transform 0.3s;
  }
  .card-stats:hover {
    transform: translateY(-5px);
  }
  iframe {
    width: 100%;
    height: 80vh;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: none;
  }
</style>

<div class="dashboard-container">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold text-dark">📊 Panel de Estadísticas (Power BI)</h2>
    <span class="badge bg-primary rounded-pill px-3 py-2">Datos en Tiempo Real</span>
  </div>

  <div class="row g-4 mb-5">
    <div class="col-md-3">
      <div class="card-stats text-center">
        <h6 class="text-muted small">Total Voluntarios</h6>
        <h4 class="fw-bold text-primary">{stats.total_voluntarios}</h4>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card-stats text-center">
        <h6 class="text-muted small">Horas Sociales</h6>
        <h4 class="fw-bold text-success">{stats.horas_sociales}h</h4>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card-stats text-center">
        <h6 class="text-muted small">Programas Activos</h6>
        <h4 class="fw-bold text-warning">{stats.programas_activos}</h4>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card-stats text-center">
        <h6 class="text-muted small">Inscripciones</h6>
        <h4 class="fw-bold text-info">{stats.inscripciones_totales}</h4>
      </div>
    </div>
  </div>


  <div class="row">
    <div class="col-12">
      <!-- Opción A: Mostrar el reporte de Power BI si el link funciona -->
      <div class="card shadow-lg border-0 rounded-4 overflow-hidden bg-white">
        {#if powerBIUrl && !powerBIUrl.includes("YOUR_EMBED_URL_HERE")}
          <iframe title="VolunSys Dashboard" src={powerBIUrl} allowFullScreen="true" style="height: 75vh;"></iframe>
        {:else}
          <!-- Opción B: Fallback con captura de pantalla -->
          <div class="p-5 text-center">
            <h4 class="fw-bold mb-3">📊 Dashboard VolunSys</h4>
            <p class="text-muted">Si no lograste publicar el link, guarda una captura como <b>dashboard.png</b> en la carpeta <code>static/</code>.</p>
            <div class="mt-4">
              <img src="/dashboard.png" alt="Captura Power BI" class="img-fluid rounded-4 shadow-sm border" on:error={(e) => e.target.src='https://via.placeholder.com/800x500?text=Sube+tu+captura+como+dashboard.png+en+static/'} />
            </div>
            <p class="small text-primary mt-4 fw-bold">💡 Tip: Muestra tu Power BI Desktop y usa esta imagen en la web como respaldo.</p>
          </div>
        {/if}
      </div>
    </div>
  </div>

</div>