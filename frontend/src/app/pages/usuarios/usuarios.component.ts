import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './usuarios.component.html'
})
export class UsuariosComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);

  rolApp = '';
  usuarios: any[] = [];
  usuariosFiltrados: any[] = [];
  busqueda = '';

  form = {
    nombre: "",
    apellido: "",
    email: "",
    telefono: "",
    numero_documento: "",
    password: "",
    rol_id: 3 // Default: Voluntario
  };
  
  mensajeExito = "";
  mensajeError = "";
  procesando = false;

  async ngOnInit() {
    if (typeof window !== "undefined") {
      this.rolApp = localStorage.getItem("rol") || "";
      if (this.rolApp !== "Admin") {
        alert("Acceso Denegado. Solo Administradores.");
        this.router.navigate(['/dashboard']);
        return;
      }
    }
    await this.cargarDatos();
  }

  async cargarDatos() {
    try {
      const data = await this.apiService.getUsuarios();
      if (Array.isArray(data)) {
        this.usuarios = data;
        this.filtrarUsuarios();
      }
    } catch (err) {
      console.error("Error al cargar usuarios:", err);
    }
  }

  filtrarUsuarios() {
    const b = this.busqueda.toLowerCase();
    this.usuariosFiltrados = this.usuarios.filter(u => 
      (u.nombre && u.nombre.toLowerCase().includes(b)) || 
      (u.apellido && u.apellido.toLowerCase().includes(b)) || 
      (u.email && u.email.toLowerCase().includes(b)) || 
      (u.documento && u.documento.includes(b))
    );
  }

  getVoluntariosCount(): number {
    return this.usuarios.filter(u => u.rol === 'Voluntario').length;
  }

  getCoordinadoresCount(): number {
    return this.usuarios.filter(u => u.rol === 'Coordinador').length;
  }

  async agregar() {
    this.procesando = true;
    this.mensajeError = "";
    this.mensajeExito = "";
    
    if (!this.form.nombre || !this.form.email || !this.form.numero_documento || !this.form.password) {
      this.mensajeError = "Llena todos los campos obligatorios.";
      this.procesando = false;
      return;
    }

    try {
      const dbResponse = await this.apiService.crearUsuario(this.form);
      if (dbResponse.success) {
        this.mensajeExito = "¡Usuario creado en el sistema con éxito!";
        this.form = { nombre: "", apellido: "", email: "", telefono: "", numero_documento: "", password: "", rol_id: 3 };
        await this.cargarDatos();
        setTimeout(() => this.mensajeExito = "", 3000);
      } else {
        this.mensajeError = dbResponse.message || "Error al crear usuario.";
      }
    } catch (e) {
      this.mensajeError = "Fallo de red.";
    }
    this.procesando = false;
  }

  async borrar(id: any) {
    if (confirm("🚨 Atención: ¿Estás seguro de eliminar este usuario permanentemente? Esta acción es irreversible.")) {
      try {
        await this.apiService.eliminarUsuario(id);
        await this.cargarDatos();
      } catch (err) {
        console.error("Error al eliminar usuario:", err);
      }
    }
  }
}
