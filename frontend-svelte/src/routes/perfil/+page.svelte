<script>
  import { onMount } from "svelte";
  import { getUsuario, getHorasSociales, getMisProgramas } from "$lib/api";

  let usuario = {
    nombre: "Cargando...",
    apellido: "",
    email: "",
    rol: "Voluntario",
    horas_sociales: 0,
    documento: ""
  };
  let misProgramas = [];
  let loading = true;

  onMount(async () => {
    try {
      const usuarioId = localStorage.getItem("usuarioId") || 1;
      const data = await getUsuario(usuarioId);
      if (data) {
        usuario = { ...usuario, ...data };
      }
      
      const horasData = await getHorasSociales(usuarioId);
      usuario.horas_sociales = horasData.horas_sociales;

      misProgramas = await getMisProgramas(usuarioId);
    } catch (err) {
      console.error("Error cargando perfil:", err);
    } finally {
      loading = false;
    }
  });
</script>

<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-lg-8">
      
      <!-- Card de Perfil Premium -->
      <div class="card border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="card-header border-0 p-5 text-white" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);">
          <div class="d-flex align-items-center">
            <div class="avatar-circle me-4">
              <span class="fs-1 fw-bold text-primary">{usuario.nombre[0]}{usuario.apellido[0] || ""}</span>
            </div>
            <div>
              <h2 class="fw-bolder mb-0 text-white">{usuario.nombre} {usuario.apellido}</h2>
              <span class="badge bg-light text-primary rounded-pill px-3 mt-2">{usuario.rol} Oficial</span>
            </div>
          </div>
        </div>

        <div class="card-body p-5 bg-white">
          {#if loading}
            <div class="text-center py-5">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
          {:else}
            <div class="row g-4">
              
              <!-- Estadísticas de Impacto -->
              <div class="col-md-6">
                <div class="p-4 rounded-4 bg-light border-start border-primary border-4 shadow-sm h-100">
                  <h6 class="text-uppercase text-muted fw-bold small mb-3">Tiempo de Servicio Social</h6>
                  <div class="d-flex align-items-baseline">
                    <h1 class="display-4 fw-bolder text-dark mb-0">{usuario.horas_sociales}</h1>
                    <span class="ms-2 fw-bold text-secondary">Horas</span>
                  </div>
                  <div class="progress mt-3" style="height: 8px;">
                    <div class="progress-bar bg-primary" role="progressbar" style="width: {(usuario.horas_sociales/80)*100}%;"></div>
                  </div>
                  <small class="text-muted mt-2 d-block">Meta Social: 80 Horas</small>
                </div>
              </div>

              <div class="col-md-6">
                <div class="p-4 rounded-4 bg-light border-start border-success border-4 shadow-sm h-100">
                  <h6 class="text-uppercase text-muted fw-bold small mb-3">Programas Inscritos</h6>
                  <h1 class="display-4 fw-bolder text-dark mb-0">{misProgramas.length}</h1>
                  <small class="text-muted mt-2 d-block">
                    {#if misProgramas.length > 0}
                      Participando en: {misProgramas.map(p => p.nombre).join(", ")}.
                    {:else}
                      Aún no te has inscrito en ningún programa.
                    {/if}
                  </small>
                </div>
              </div>
          {/if}

            <!-- Información Personal -->
            <div class="col-12 mt-5">
              <h5 class="fw-bold text-dark border-bottom pb-3 mb-4">Información de Seguridad</h5>
              <div class="row g-3">
                <div class="col-sm-6 text-muted">
                  <label class="d-block small fw-bold">Correo Electrónico</label>
                  <span class="text-dark fw-medium">{usuario.email}</span>
                </div>
                <div class="col-sm-6 text-muted">
                  <label class="d-block small fw-bold">Documento de Identidad</label>
                  <span class="text-dark fw-medium">{usuario.documento || 'No registrado'}</span>
                </div>
                <div class="col-sm-6 text-muted mt-3">
                  <label class="d-block small fw-bold">Estado de Cuenta</label>
                  <span class="badge bg-success rounded-pill px-3">Activo y Verificado</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</div>

<style>
  .avatar-circle {
    width: 100px;
    height: 100px;
    background-color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  }
</style>
