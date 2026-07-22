import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private apiService = inject(ApiService);
  private router = inject(Router);

  email = '';
  password = '';
  error = '';

  async handleLogin() {
    this.error = '';
    try {
      console.log('[LOGIN] Attempting login with:', this.email);
      const res = await this.apiService.login({ email: this.email, password: this.password });
      console.log('[LOGIN] Response:', res);
      if (res.success) {
        localStorage.setItem("token", res.access_token);
        localStorage.setItem("rol", res.rol);
        localStorage.setItem("usuario", res.usuario);
        localStorage.setItem("usuarioId", res.usuarioId || res.usuario);
        this.router.navigate(['/dashboard']);
      } else {
        this.error = res.message || "Credenciales incorrectas.";
      }
    } catch (err: any) {
      console.error('[LOGIN] Error:', err);
      if (err?.error?.message) {
        this.error = err.error.message;
      } else if (err?.message) {
        this.error = err.message;
      } else {
        this.error = "Error de conexión con el servidor. Verifique que el backend esté corriendo.";
      }
    }
  }
}
