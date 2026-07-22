import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-playas',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './playas.component.html'
})
export class PlayasComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);

  rol = "";
  usuarioId: any = null;
  registros: any[] = [];
  ubicaciones: any[] = [];
  jornadasDisponibles: any[] = [];
  form = { nombre_playa: "", ubicacion: "", cantidad_basura_estimada_kg: "", estado: true };

  async ngOnInit() {
    if (typeof window !== 'undefined') {
      this.rol = localStorage.getItem("rol") || "";
      this.usuarioId = localStorage.getItem("usuarioId");
    }
    await this.loadData();
  }

  async loadData() {
    try {
      const data = await this.apiService.getPlayas();
      if (Array.isArray(data)) {
        this.registros = data;
      }
      
      const ciudadesExpress = await this.apiService.getCiudades();
      this.ubicaciones = Array.isArray(ciudadesExpress) ? ciudadesExpress : [];
      
      const allJornadas = await this.apiService.getVoluntariados();
      if (Array.isArray(allJornadas)) {
        this.jornadasDisponibles = allJornadas.filter(j => j.programa_id === 1);
      }
    } catch (e) {
      console.error("Error loading data", e);
    }
  }

  async inscribirse(jornadaId: any) {
    if (!this.rol) {
      alert("Debes iniciar sesión para inscribirte.");
      this.router.navigate(['/login']);
      return;
    }
    const data = { usuario_id: parseInt(this.usuarioId), voluntariado_id: jornadaId };
    try {
      const res = await this.apiService.crearInscripcion(data);
      if (res.success) {
        alert("¡Enhorabuena! Te has inscrito correctamente. Revisa 'Mis Inscripciones'.");
      } else {
        alert("Error al inscribirse: " + res.message);
      }
    } catch (err) {
      alert("Error al inscribirse en la jornada.");
    }
  }

  async submit() {
    try {
      await this.apiService.crearPlaya(this.form);
      this.form = { nombre_playa: "", ubicacion: "", cantidad_basura_estimada_kg: "", estado: true };
      await this.loadData();
    } catch (err) {
      alert("Error al crear el registro de playa.");
    }
  }

  async eliminar(id: any) {
    if (confirm("¿Estás seguro de eliminar este registro?")) {
      try {
        await this.apiService.eliminarPlaya(id);
        await this.loadData();
      } catch (err) {
        alert("Error al eliminar el registro.");
      }
    }
  }
}
