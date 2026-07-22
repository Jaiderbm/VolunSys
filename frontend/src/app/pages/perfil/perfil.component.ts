import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent implements OnInit {
  private apiService = inject(ApiService);

  usuario: any = {
    nombre: "Cargando...",
    apellido: "",
    email: "",
    rol: "Voluntario",
    horas_sociales: 0,
    documento: ""
  };
  misProgramas: any[] = [];
  loading = true;

  async ngOnInit() {
    try {
      const usuarioId = localStorage.getItem("usuarioId") || "1";
      const data = await this.apiService.getUsuario(usuarioId);
      if (data) {
        this.usuario = { ...this.usuario, ...data };
      }
      
      const horasData = await this.apiService.getHorasSociales(usuarioId);
      if (horasData) {
        this.usuario.horas_sociales = horasData.horas_sociales || 0;
      }

      const miProgsData = await this.apiService.getMisProgramas(usuarioId);
      if (Array.isArray(miProgsData)) {
        this.misProgramas = miProgsData;
      }
    } catch (err) {
      console.error("Error cargando perfil:", err);
    } finally {
      this.loading = false;
    }
  }

  getMetaPercentage(): number {
    return Math.min(((this.usuario.horas_sociales || 0) / 80) * 100, 100);
  }

  getMisProgramasNames(): string {
    return this.misProgramas.map(p => p.nombre).join(", ");
  }
}
