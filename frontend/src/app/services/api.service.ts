import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  private FASTAPI = "http://127.0.0.1:8000";
  private EXPRESS = "http://localhost:3001/api";

  // ------------------------------------
  // FAST API - Voluntariados Principales
  // ------------------------------------

  async login(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/login`, data));
  }

  async getUsuarios(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/usuarios/`));
  }

  async crearUsuario(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/usuarios/`, data));
  }

  async eliminarUsuario(id: any): Promise<any> {
    return lastValueFrom(this.http.delete(`${this.FASTAPI}/api/usuarios/${id}`));
  }

  async getCuidadoAdultos(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/cuidado-adultos-mayores/`));
  }

  async crearCuidadoAdultos(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/cuidado-adultos-mayores/`, data));
  }

  async eliminarCuidadoAdultos(id: any): Promise<any> {
    return lastValueFrom(this.http.delete(`${this.FASTAPI}/api/cuidado-adultos-mayores/${id}`));
  }

  async getPlayas(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/limpieza-playas/`));
  }

  async crearPlaya(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/limpieza-playas/`, data));
  }

  async eliminarPlaya(id: any): Promise<any> {
    return lastValueFrom(this.http.delete(`${this.FASTAPI}/api/limpieza-playas/${id}`));
  }

  async getRescate(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/rescate-animal/`));
  }

  async crearRescate(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/rescate-animal/`, data));
  }

  async eliminarRescate(id: any): Promise<any> {
    return lastValueFrom(this.http.delete(`${this.FASTAPI}/api/rescate-animal/${id}`));
  }

  async getVoluntariados(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/voluntariados/`));
  }

  async crearVoluntariado(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/voluntariados/`, data));
  }

  async getInscripciones(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/inscripciones/`));
  }

  async crearInscripcion(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/inscripciones/`, data));
  }

  // Programas e Inscripciones a Programas
  async getProgramas(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/programas/`));
  }

  async inscribirEnPrograma(data: any): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/programas/inscripcion`, data));
  }

  async getMisProgramas(usuarioId: any): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/programas/mis-programas/${usuarioId}`));
  }

  async getUsuario(id: any): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/usuarios/${id}`));
  }

  async getHorasSociales(id: any): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/usuarios/horas/${id}`));
  }

  async confirmarAsistencia(inscripcionId: any, horas: number = 4): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/inscripciones/confirmar/${inscripcionId}`, { horas }));
  }

  async asignarTarea(inscripcionId: any, tarea: string): Promise<any> {
    return lastValueFrom(this.http.post(`${this.FASTAPI}/api/inscripciones/asignar/${inscripcionId}`, { tarea }));
  }

  // ------------------------------------
  // EXPRESS API - Ubicaciones (Dropdowns)
  // ------------------------------------

  async getPaises(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.EXPRESS}/pais`));
  }

  async getCiudades(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.EXPRESS}/ciudad`));
  }

  async getUbicaciones(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.EXPRESS}/ubicacion`));
  }

  async getStats(): Promise<any> {
    return lastValueFrom(this.http.get(`${this.FASTAPI}/api/stats`));
  }

  async eliminarVoluntariado(id: any): Promise<any> {
    return lastValueFrom(this.http.delete(`${this.FASTAPI}/api/voluntariados/${id}`));
  }
}
