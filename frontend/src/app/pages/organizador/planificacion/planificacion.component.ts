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
  loading = true;
  error = "";

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

    Promise.all([progsPromise, cidsPromise])
      .catch(() => {
        this.error = "Error al cargar datos iniciales.";
      })
      .finally(() => {
        this.loading = false;
        this.cdr.detectChanges();
      });
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
          this.cdr.detectChanges();
        } else {
          alert("Error al guardar la jornada.");
        }
      })
      .catch(() => {
        alert("Error al guardar la jornada.");
      });
  }
}
