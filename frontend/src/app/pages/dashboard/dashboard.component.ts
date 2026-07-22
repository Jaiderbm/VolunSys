import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  private apiService = inject(ApiService);

  rol = '';
  nombre_usuario = '';
  miTarea = '';

  async ngOnInit() {
    if (typeof window !== 'undefined') {
      this.rol = localStorage.getItem("rol") || "";
      this.nombre_usuario = this.rol === "Admin" ? "Administrador Jefe" : (this.rol === "Coordinador" ? "Organizador" : "Voluntario");
      
      if (this.rol === "User") {
        try {
          const ins = await this.apiService.getInscripciones();
          if (Array.isArray(ins)) {
            // Buscar la última tarea asignada
            const ultimaConTarea = [...ins].reverse().find(i => i.tarea && i.tarea !== "");
            if (ultimaConTarea) {
              this.miTarea = ultimaConTarea.tarea;
            }
          }
        } catch (err) {
          console.error("Error al cargar inscripciones:", err);
        }
      }
    }
  }
}
