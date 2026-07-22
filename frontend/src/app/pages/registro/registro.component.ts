import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})
export class RegistroComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  registroForm!: FormGroup;
  error = "";
  exito = "";

  ngOnInit() {
    this.registroForm = this.fb.group({
      nombre: ['', [Validators.required]],
      apellido: ['', [Validators.required]],
      numero_documento: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      telefono: [''],
      password: ['', [
        Validators.required, 
        Validators.minLength(8),
        Validators.pattern(/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/)
      ]]
    });
  }

  // Getter auxiliar para acceder fácilmente a los controles desde la plantilla HTML
  get f() {
    return this.registroForm.controls;
  }

  async handleRegister() {
    this.error = "";
    this.exito = "";

    if (this.registroForm.invalid) {
      this.registroForm.markAllAsTouched();
      this.error = "Por favor, completa correctamente todos los campos obligatorios.";
      return;
    }

    try {
      const formValue = this.registroForm.value;
      const res = await this.apiService.crearUsuario(formValue);
      if (res.success) {
        this.exito = "¡Cuenta creada exitosamente! Ahora eres Voluntario Oficial.";
        this.registroForm.reset();
        setTimeout(() => this.router.navigate(['/login']), 2000);
      } else {
        this.error = res.message || "Error al crear la cuenta.";
      }
    } catch (err) {
      this.error = "Error de red inesperado.";
    }
  }
}
