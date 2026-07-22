<script>
import "bootstrap/dist/css/bootstrap.min.css"
import Navbar from "$lib/components/Navbar.svelte"
import Footer from "$lib/components/Footer.svelte"
</script>

<div class="d-flex flex-column min-vh-100 bg-light">
  <!-- Componente Reutilizable Navbar -->
  <Navbar />

  <main class="container mt-5">
    <slot />
  </main>

  <!-- Componente Reutilizable Footer -->
  <Footer />
</div>

<style>
  :global(body) {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
</style>