import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType, Chart, registerables } from 'chart.js';
import { ApiService } from '../../services/api.service';

Chart.register(...registerables);

@Component({
  selector: 'app-powerbi',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './powerbi.component.html',
  styleUrl: './powerbi.component.css'
})
export class PowerBIComponent implements OnInit {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  isLoading = true;
  hasError = false;

  stats = {
    total_voluntarios: 0,
    horas_sociales: 0,
    programas_activos: 0,
    inscripciones_totales: 0
  };

  // ── Gráfica 1: Voluntarios por Programa (Barras) ──────────────────────────
  barChartType: ChartType = 'bar';
  barChartData: ChartData<'bar'> = {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [
        'rgba(99,102,241,0.85)',
        'rgba(16,185,129,0.85)',
        'rgba(245,158,11,0.85)',
        'rgba(239,68,68,0.85)',
        'rgba(59,130,246,0.85)',
      ],
      borderRadius: 8,
      borderSkipped: false
    }]
  };
  barChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 600 },
    plugins: { legend: { display: false } },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1 },
        grid: { color: 'rgba(0,0,0,0.05)' }
      },
      x: { grid: { display: false } }
    }
  };

  // ── Gráfica 2: Usuarios por Rol (Doughnut) ────────────────────────────────
  doughnutChartType: ChartType = 'doughnut';
  doughnutChartData: ChartData<'doughnut'> = {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [
        'rgba(99,102,241,0.9)',
        'rgba(16,185,129,0.9)',
        'rgba(245,158,11,0.9)',
        'rgba(239,68,68,0.9)',
      ],
      hoverOffset: 8,
      borderWidth: 2,
      borderColor: '#fff'
    }]
  };
  doughnutChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 600 },
    plugins: {
      legend: {
        position: 'bottom',
        labels: { padding: 20, font: { size: 13 } }
      }
    }
  };

  // ── Gráfica 3: Top Voluntariados (Barras horizontales) ────────────────────
  hbarChartType: ChartType = 'bar';
  hbarChartData: ChartData<'bar'> = {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [
        'rgba(99,102,241,0.85)',
        'rgba(16,185,129,0.85)',
        'rgba(245,158,11,0.85)',
        'rgba(239,68,68,0.85)',
        'rgba(59,130,246,0.85)',
      ],
      borderRadius: 8,
      borderSkipped: false
    }]
  };
  hbarChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 600 },
    indexAxis: 'y' as const,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { stepSize: 1 },
        grid: { color: 'rgba(0,0,0,0.05)' }
      },
      y: { grid: { display: false } }
    }
  };

  ngOnInit(): void {
    this.loadStats();
  }

  private loadStats(): void {
    this.isLoading = true;
    this.hasError = false;

    this.apiService.getStats()
      .then((data: any) => {
        if (!data) {
          this.hasError = true;
          this.isLoading = false;
          this.cdr.detectChanges();
          return;
        }

        this.stats = {
          total_voluntarios: data.total_voluntarios ?? 0,
          horas_sociales: data.horas_sociales ?? 0,
          programas_activos: data.programas_activos ?? 0,
          inscripciones_totales: data.inscripciones_totales ?? 0
        };

        // Chart 1 — Voluntarios por Programa
        const prog = data.chart_voluntarios_programa;
        if (prog?.labels?.length) {
          this.barChartData = {
            ...this.barChartData,
            labels: prog.labels,
            datasets: [{ ...this.barChartData.datasets[0], data: prog.data }]
          };
        }

        // Chart 2 — Usuarios por Rol
        const rol = data.chart_voluntarios_rol;
        if (rol?.labels?.length) {
          this.doughnutChartData = {
            ...this.doughnutChartData,
            labels: rol.labels,
            datasets: [{ ...this.doughnutChartData.datasets[0], data: rol.data }]
          };
        }

        // Chart 3 — Top Voluntariados
        const top = data.chart_top_voluntariados;
        if (top?.labels?.length) {
          this.hbarChartData = {
            ...this.hbarChartData,
            labels: top.labels,
            datasets: [{ ...this.hbarChartData.datasets[0], data: top.data }]
          };
        }

        this.isLoading = false;
        // Force Angular to detect all changes
        this.cdr.detectChanges();
      })
      .catch((err: any) => {
        console.error('Error loading stats:', err);
        this.hasError = true;
        this.isLoading = false;
        this.cdr.detectChanges();
      });
  }
}
