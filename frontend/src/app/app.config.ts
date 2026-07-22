import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

// Registro global de Chart.js (necesario para ng2-charts en apps standalone)
import {
  Chart,
  BarController, BarElement, CategoryScale, LinearScale,
  Tooltip, Legend, Title,
  DoughnutController, ArcElement,
  LineController, LineElement, PointElement
} from 'chart.js';

Chart.register(
  BarController, BarElement, CategoryScale, LinearScale,
  Tooltip, Legend, Title,
  DoughnutController, ArcElement,
  LineController, LineElement, PointElement
);

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient()
  ],
};
