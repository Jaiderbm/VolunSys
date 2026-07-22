import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})
export class RegistroComponent {
  private apiService = inject(ApiService);
  private router = inject(Router);

  form = { nombre: "", apellido: "", email: "", telefono: "", password: "", numero_documento: "" };
  error = "";
  exito = "";

  async handleRegister() {
    this.error = "";
    this.exito = "";
    
    if (this.form.password.length < 8) {
      this.error = "La contraseña debe tener al menos 8 caracteres.";
      return;
    }
    if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/.test(this.form.password)) {
      this.error = "La contraseña debe incluir al menos una mayúscula, una minúscula y un número.";
      return;
    }

    try {
      const res = await this.apiService.crearUsuario(this.form);
      if (res.success) {
        this.exito = "¡Cuenta creada exitosamente! Ahora eres Voluntario Oficial.";
        this.form = { nombre: "", apellido: "", email: "", telefono: "", password: "", numero_documento: "" };
        setTimeout(() => this.router.navigate(['/login']), 2000);
      } else {
        this.error = res.message || "Error al crear la cuenta.";
      }
    } catch (err) {
      this.error = "Error de red inesperado.";
    }
  }
}
