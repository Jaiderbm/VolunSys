<script>
  import { login } from '$lib/api.js';

  let email = "";
  let password = "";
  let error = "";

  async function handleLogin() {
    try {
      const res = await login({ email, password });
      if (res.success) {
        localStorage.setItem("token", res.access_token);
        localStorage.setItem("rol", res.rol);
        localStorage.setItem("usuario", res.usuario);
        window.location.href = "/dashboard";
      } else {
        error = res.message || "Error al iniciar sesión.";
      }
    } catch (err) {
      error = "Falla de red. Intente de nuevo.";
    }
  }
</script>

<style>
  .login-container {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .glass-panel {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    overflow: hidden;
  }
  .bg-gradient-side {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3rem;
  }
</style>

<div class="login-container">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-9">
        <div class="glass-panel row g-0">
          
          <!-- Image/Gradient Side -->
          <div class="col-md-5 bg-gradient-side text-center d-none d-md-flex">
            <h2 class="fw-bolder mb-3">👋 Bienvenido de Nuevo</h2>
            <p class="opacity-75">Tu comunidad te espera. Ingresa tus credenciales para administrar tus voluntariados.</p>
            <div class="mt-4 opacity-50">
              <svg width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            </div>
          </div>

          <!-- Form Side -->
          <div class="col-md-7 p-5">
            <div class="text-center mb-4">
              <h3 class="fw-bold text-dark">Iniciar Sesión</h3>
              <p class="text-muted small">Ingresa tus datos para continuar</p>
            </div>
            
            {#if error}
              <div class="alert alert-danger py-2 small fw-bold text-center">{error}</div>
            {/if}

            <form on:submit|preventDefault={handleLogin}>
              <div class="form-floating mb-3">
                <input type="email" class="form-control rounded-3" id="email" placeholder="name@example.com" bind:value={email} required>
                <label for="email" class="text-muted">Correo electrónico</label>
              </div>
              <div class="form-floating mb-4">
                <input type="password" class="form-control rounded-3" id="password" placeholder="Password" bind:value={password} required>
                <label for="password" class="text-muted">Contraseña</label>
              </div>
              
              <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill fw-bold shadow-sm" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none;">
                Entrar a mi Cuenta
              </button>
            </form>
            
            <div class="text-center mt-4 pt-2 border-top">
              <span class="text-muted small">¿No tienes cuenta? <a href="/registro" class="text-primary fw-bold text-decoration-none">Regístrate como voluntario</a></span>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</div>