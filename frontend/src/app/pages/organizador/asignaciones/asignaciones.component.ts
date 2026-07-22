import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-asignaciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './asignaciones.component.html'
})
export class AsignacionesComponent implements OnInit {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  inscripciones: any[] = [];
  loading = true;
  error = "";
  
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
      })
      .catch(() => {
        this.error = "Error al cargar las inscripciones.";
      })
      .finally(() => {
        this.loading = false;
        this.cdr.detectChanges();
      });
  }

  handleAsignar(id: any, event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const tarea = selectElement.value;
    if (!tarea) return;
    
    this.apiService.asignarTarea(id, tarea)
      .then((data: any) => {
        if (data && data.success) {
          alert("¡Tarea asignada con éxito!");
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
