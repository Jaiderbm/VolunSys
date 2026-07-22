import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-inscripciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inscripciones.component.html'
})
export class InscripcionesComponent implements OnInit {
  private apiService = inject(ApiService);

  inscripciones: any[] = [];
  cargando = true;

  async ngOnInit() {
    await this.loadInscripciones();
  }

  async loadInscripciones() {
    this.cargando = true;
    try {
      const data = await this.apiService.getInscripciones();
      if (Array.isArray(data)) {
        this.inscripciones = data;
      }
    } catch (err) {
      console.error("Error cargando inscripciones:", err);
    } finally {
      this.cargando = false;
    }
  }

  async marcarAsistencia(inscripcion: any) {
    if (inscripcion.estado === 'Confirmada') return;
    try {
      const res = await this.apiService.confirmarAsistencia(inscripcion.id, 4);
      if (res.success) {
        alert("¡Asistencia confirmada!");
        await this.loadInscripciones();
      } else {
        alert("Error al confirmar asistencia: " + res.message);
      }
    } catch (err) {
      console.error("Error al marcar asistencia:", err);
      alert("Error de red al marcar asistencia.");
    }
  }
}
