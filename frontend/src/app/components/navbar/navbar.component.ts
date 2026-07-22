import { Component, OnInit, inject } from '@angular/core';
import { Router, NavigationEnd, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './navbar.component.html'
})
export class NavbarComponent implements OnInit {
  private router = inject(Router);
  rol = '';
  isHome = false;
  dropdownOpen = false;

  ngOnInit() {
    this.checkAuth();
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.checkAuth();
      }
    });
  }

  checkAuth() {
    if (typeof window !== 'undefined') {
      this.rol = localStorage.getItem('rol') || '';
      this.isHome = this.router.url === '/' || this.router.url === '/home';
    }
  }

  logout() {
    localStorage.removeItem('rol');
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    this.rol = '';
    this.router.navigate(['/login']);
  }
}
