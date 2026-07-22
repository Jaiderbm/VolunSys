<script>
  import { crearUsuario } from '$lib/api.js';

  let form = { nombre: "", apellido: "", email: "", telefono: "", password: "", numero_documento: "" };
  let error = "";
  let exito = "";

  async function handleRegister() {
    error = "";
    exito = "";
    
    if (form.password.length < 8) {
      error = "La contraseña debe tener al menos 8 caracteres.";
      return;
    }
    if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/.test(form.password)) {
      error = "La contraseña debe incluir al menos una mayúscula, una minúscula y un número.";
      return;
    }

    try {
      const res = await crearUsuario(form);
      if (res.success) {
        exito = "¡Cuenta creada exitosamente! Ahora eres Voluntario Oficial.";
        form = { nombre: "", apellido: "", email: "", telefono: "", password: "" };
        setTimeout(() => window.location.href = "/login", 2000);
      } else {
        error = res.message || "Error al crear la cuenta.";
      }
    } catch (err) {
      error = "Error de red inesperado.";
    }
  }
</script>

<style>
  .register-container {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .glass-panel {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
  }
</style>

<div class="register-container mt-2">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6 col-md-8">
        <div class="glass-panel p-5">
          <div class="text-center mb-4">
            <h2 class="fw-bolder text-dark mb-2" style="background: linear-gradient(45deg, #f12711, #f5af19); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Únete al Cambio</h2>
            <p class="text-muted fw-medium">Regístrate como Voluntario de VolunSys</p>
          </div>

          {#if error}
            <div class="alert alert-danger py-2 small fw-bold text-center border-0 shadow-sm rounded-pill">{error}</div>
          {/if}
          {#if exito}
            <div class="alert alert-success py-2 small fw-bold text-center border-0 shadow-sm rounded-pill mt-3">{exito}</div>
          {/if}

          <form on:submit|preventDefault={handleRegister}>
            <div class="row g-3 mb-3">
              <div class="col-md-6 form-floating">
                <input type="text" class="form-control rounded-3 bg-light" id="nombre" bind:value={form.nombre} placeholder="Juan" required>
                <label for="nombre" class="ms-2 text-muted">Nombre</label>
              </div>
              <div class="col-md-6 form-floating">
                <input type="text" class="form-control rounded-3 bg-light" id="apellido" bind:value={form.apellido} placeholder="Pérez" required>
                <label for="apellido" class="ms-2 text-muted">Apellido</label>
              </div>
            </div>

            <div class="form-floating mb-3">
              <input type="text" class="form-control rounded-3 bg-light" id="numero_documento" bind:value={form.numero_documento} placeholder="123456789" required>
              <label for="numero_documento" class="text-muted">Número de Documento (Requerido)</label>
            </div>

            <div class="form-floating mb-3">
              <input type="email" class="form-control rounded-3 bg-light" id="email" bind:value={form.email} placeholder="correo@ejemplo.com" required>
              <label for="email" class="text-muted">Correo electrónico</label>
            </div>

            <div class="form-floating mb-3">
              <input type="tel" class="form-control rounded-3 bg-light" id="telefono" bind:value={form.telefono} placeholder="3000000000">
              <label for="telefono" class="text-muted">Teléfono (opcional)</label>
            </div>

            <div class="form-floating mb-4">
              <input type="password" class="form-control rounded-3 bg-light" id="password" bind:value={form.password} placeholder="Clave secreta" required>
              <label for="password" class="text-muted">Contraseña (Mín. 8 letras, 1 Número, 1 Mayúscula)</label>
            </div>

            <p class="small text-muted text-center mb-4">🎵 Nota: Al registrarte, tu rol por defecto será estrictamente <b>Voluntario</b>.</p>

            <button type="submit" class="btn btn-warning w-100 py-3 rounded-pill fw-bold shadow-sm" style="background: linear-gradient(45deg, #f12711, #f5af19); border: none; color: white; font-size: 1.1rem;">
              Crear Cuenta Oficial
            </button>
          </form>

          <div class="text-center mt-4 pt-2 border-top">
            <span class="text-muted small">¿Ya eres voluntario? <a href="/login" class="text-primary fw-bold text-decoration-none">Inicia Sesión aquí</a></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>