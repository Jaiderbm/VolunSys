import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-asignaciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './asignaciones.component.html',
  styleUrl: './asignaciones.component.css'
})
export class AsignacionesComponent implements OnInit {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  inscripciones: any[] = [];
  inscripcionesFiltradas: any[] = [];
  busqueda = "";
  loading = true;
  error = "";
  mensajeExito = "";
  
  tareasSugeridas = [
    "Logística y Equipos",
    "Primeros Auxilios",
    "Registro de Asistencia",
    "Gestión de Residuos",
    "Guía de Recorrido",
    "Atención al Público",
    "Coordinación de Transporte"
  ];

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.loading = true;
    this.error = "";
    this.cdr.detectChanges();

    this.apiService.getInscripciones()
      .then((data: any) => {
        this.inscripciones = Array.isArray(data) ? data : [];
        this.filtrarInscripciones();
      })
      .catch(() => {
        this.error = "Error al cargar las inscripciones.";
      })
      .finally(() => {
        this.loading = false;
        this.cdr.detectChanges();
      });
  }

  filtrarInscripciones() {
    const b = this.busqueda.toLowerCase().trim();
    if (!b) {
      this.inscripcionesFiltradas = [...this.inscripciones];
      return;
    }
    this.inscripcionesFiltradas = this.inscripciones.filter(i => 
      (i.usuario && i.usuario.toLowerCase().includes(b)) ||
      (i.voluntariado && i.voluntariado.toLowerCase().includes(b)) ||
      (i.tarea && i.tarea.toLowerCase().includes(b))
    );
  }

  getTotalCount(): number {
    return this.inscripciones.length;
  }

  getAsignadosCount(): number {
    return this.inscripciones.filter(i => i.tarea && i.tarea.trim() !== '').length;
  }

  getPendientesCount(): number {
    return this.inscripciones.length - this.getAsignadosCount();
  }

  getInitials(name: string): string {
    if (!name) return 'V';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  }

  handleAsignar(id: any, event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const tarea = selectElement.value;
    if (!tarea) return;
    
    this.apiService.asignarTarea(id, tarea)
      .then((data: any) => {
        if (data && data.success) {
          this.mensajeExito = "¡Tarea asignada con éxito!";
          setTimeout(() => this.mensajeExito = "", 3500);
          this.loadData();
        } else {
          alert("Error al asignar tarea.");
        }
      })
      .catch(() => {
        alert("Error al asignar tarea.");
      });
  }
}
