import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-actividad-detalle',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './actividad-detalle.component.html',
  styleUrl: './actividad-detalle.component.css'
})
export class ActividadDetalleComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private apiService = inject(ApiService);

  programaId = '';
  actividades: any[] = [];
  misInscripciones: any[] = [];
  loading = true;
  error = '';
  usuarioId: any = null;

  async ngOnInit() {
    this.programaId = this.route.snapshot.params['programaId'] || '';
    if (typeof window !== 'undefined') {
      this.usuarioId = localStorage.getItem("usuarioId") || "1";
    }
    await this.loadData();
  }

  async loadData() {
    this.loading = true;
    try {
      const allActividades = await this.apiService.getVoluntariados();
      if (Array.isArray(allActividades)) {
        this.actividades = allActividades.filter((a: any) => a.programa_id == this.programaId || !a.programa_id);
      }

      const todasInsc = await this.apiService.getInscripciones();
      if (Array.isArray(todasInsc)) {
        this.misInscripciones = todasInsc.filter((i: any) => i.usuario_id == this.usuarioId);
      }
    } catch (err) {
      this.error = "Error al cargar actividades.";
    } finally {
      this.loading = false;
    }
  }

  getInscripcionForAct(actId: number): any {
    return this.misInscripciones.find(i => i.voluntariado_id == actId);
  }

  async inscribirse(voluntariadoId: number) {
    try {
      const res = await this.apiService.crearInscripcion({
        usuario_id: parseInt(this.usuarioId),
        voluntariado_id: voluntariadoId,
        estado: "Pendiente"
      });
      if (res && (res.id || res.success)) {
        alert("¡Inscripción exitosa! Ahora puedes confirmar tu asistencia.");
        await this.loadData();
      } else {
        alert("Error al inscribirse.");
      }
    } catch (err) {
      alert("Error de red al inscribirse.");
    }
  }

  async confirmar(inscripcionId: number) {
    try {
      const res = await this.apiService.confirmarAsistencia(inscripcionId);
      if (res && res.success) {
        alert("¡Asistencia confirmada! Gracias por tu ayuda.");
        await this.loadData();
      } else {
        alert("Error al confirmar asistencia.");
      }
    } catch (err) {
      alert("Error de red al confirmar asistencia.");
    }
  }
}
