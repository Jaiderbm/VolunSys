import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-voluntariados',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './voluntariados.component.html'
})
export class VoluntariadosComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);

  voluntariados: any[] = [];
  misProgramasIds: number[] = [];
  usuarioId: any = null;
  loading = true;
  error = "";

  async ngOnInit() {
    await this.loadData();
  }

  async loadData() {
    this.loading = true;
    this.error = "";
    try {
      // Get the numeric user ID stored during login
      const rawId = typeof window !== 'undefined' ? localStorage.getItem("usuarioId") : null;
      if (rawId && rawId !== "null" && rawId !== "undefined") {
        this.usuarioId = rawId;
      }

      const data = await this.apiService.getProgramas();
      if (Array.isArray(data)) {
        this.voluntariados = data;
      }

      if (this.usuarioId) {
        try {
          const misProgs = await this.apiService.getMisProgramas(this.usuarioId);
          if (Array.isArray(misProgs)) {
            this.misProgramasIds = misProgs.map((p: any) => p.id);
          }
        } catch (e) {
          console.warn("No se pudieron obtener mis programas:", e);
        }
      }
    } catch (err) {
      console.error("Error al cargar programas:", err);
      this.error = "No se pudieron cargar los programas de voluntariado. Verifica la conexión con el servidor.";
    } finally {
      this.loading = false;
    }
  }


  async participio(programaId: number) {
    if (!this.usuarioId) {
      alert("Inicia sesión para participar.");
      this.router.navigate(['/login']);
      return;
    }
    
    try {
      const res = await this.apiService.inscribirEnPrograma({
        usuario_id: parseInt(this.usuarioId),
        programa_id: programaId
      });
      if (res && res.success) {
        alert("¡Inscrito en el programa!");
        await this.loadData();
      } else {
        alert("Error: " + (res?.message || 'No se pudo completar la inscripción.'));
      }
    } catch (err) {
      console.error(err);
      alert("Error al inscribirse al programa.");
    }
  }
}
