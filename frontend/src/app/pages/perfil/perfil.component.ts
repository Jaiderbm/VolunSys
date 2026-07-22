import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent implements OnInit {
  private apiService = inject(ApiService);
  private router = inject(Router);

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
    if (typeof window === 'undefined') {
      return;
    }
    try {
      const usuarioId = localStorage.getItem("usuarioId");
      if (!usuarioId || usuarioId === "undefined" || usuarioId === "null") {
        this.router.navigate(['/login']);
        return;
      }
      
      const rolLocal = localStorage.getItem("rol");
      if (rolLocal) {
        this.usuario.rol = rolLocal;
      }

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
