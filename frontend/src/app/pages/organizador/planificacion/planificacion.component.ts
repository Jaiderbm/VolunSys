import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-planificacion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './planificacion.component.html'
})
export class PlanificacionComponent implements OnInit {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  programas: any[] = [];
  ciudades: any[] = [];
  jornadas: any[] = [];
  jornadasFiltradas: any[] = [];
  loading = true;
  error = "";
  busqueda = "";
  rolApp = "Organizador";

  nuevaJornada = {
    titulo: "",
    descripcion: "",
    fecha: "",
    hora: "",
    cupos: 10,
    programa_id: "",
    ciudad_id: ""
  };

  ngOnInit() {
    if (typeof window !== 'undefined') {
      this.rolApp = localStorage.getItem("rol") || "Organizador";
    }
    this.loadData();
  }

  loadData() {
    this.loading = true;
    this.error = "";
    this.cdr.detectChanges();

    const progsPromise = this.apiService.getProgramas()
      .then((progs: any) => {
        this.programas = Array.isArray(progs) ? progs : [];
      })
      .catch(() => {
        this.programas = [];
      });

    const cidsPromise = this.apiService.getCiudades()
      .then((cids: any) => {
        this.ciudades = Array.isArray(cids) ? cids : [];
      })
      .catch(() => {
        this.ciudades = [];
      });

    const volsPromise = this.apiService.getVoluntariados()
      .then((vols: any) => {
        this.jornadas = Array.isArray(vols) ? vols : [];
        this.filtrarJornadas();
      })
      .catch(() => {
        this.jornadas = [];
        this.jornadasFiltradas = [];
      });

    Promise.all([progsPromise, cidsPromise, volsPromise])
      .catch(() => {
        this.error = "Error al cargar datos iniciales.";
      })
      .finally(() => {
        this.loading = false;
        this.cdr.detectChanges();
      });
  }

  filtrarJornadas() {
    const q = this.busqueda.toLowerCase().trim();
    if (!q) {
      this.jornadasFiltradas = [...this.jornadas];
      return;
    }
    this.jornadasFiltradas = this.jornadas.filter(j => 
      (j.titulo && j.titulo.toLowerCase().includes(q)) ||
      (j.descripcion && j.descripcion.toLowerCase().includes(q)) ||
      this.getProgramaNombre(j.programa_id).toLowerCase().includes(q) ||
      this.getCiudadNombre(j.ciudad_id).toLowerCase().includes(q)
    );
  }

  getProgramaNombre(id: any): string {
    const p = this.programas.find(prog => prog.id == id);
    return p ? p.nombre : 'Programa General';
  }

  getCiudadNombre(id: any): string {
    const c = this.ciudades.find(cid => cid.id == id);
    return c ? c.nombre : 'Ubicación Especial';
  }

  handleCrear() {
    if (!this.nuevaJornada.programa_id || !this.nuevaJornada.ciudad_id) {
      alert("Por favor selecciona programa y ciudad.");
      return;
    }
    
    this.apiService.crearVoluntariado(this.nuevaJornada)
      .then((data: any) => {
        if (data && (data.id || data.success || data.titulo)) {
          alert("¡Jornada planificada y publicada!");
          this.nuevaJornada = {
            titulo: "",
            descripcion: "",
            fecha: "",
            hora: "",
            cupos: 10,
            programa_id: "",
            ciudad_id: ""
          };
          this.loadData();
        } else {
          alert("Error al guardar la jornada.");
        }
      })
      .catch(() => {
        alert("Error al guardar la jornada.");
      });
  }

  handleBorrar(id: any) {
    if (confirm("🚨 ¿Estás seguro de eliminar esta jornada permanentemente? Esto cancelará todas las inscripciones asociadas.")) {
      this.apiService.eliminarVoluntariado(id)
        .then((res: any) => {
          if (res && res.success) {
            alert("¡Jornada eliminada correctamente!");
            this.loadData();
          } else {
            alert("Error al eliminar la jornada: " + (res.message || ""));
          }
        })
        .catch(() => {
          alert("Error de conexión al eliminar la jornada.");
        });
    }
  }
}
