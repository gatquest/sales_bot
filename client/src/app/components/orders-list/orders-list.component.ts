import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, } from '@angular/router';


@Component({
  standalone: true,
  selector: 'app-orders-list',
  templateUrl: './orders-list.component.html',
  styleUrls: ['./orders-list.component.css'],
  imports: [CommonModule, RouterModule]
})
export class OrdersListComponent implements OnInit {
  orders: any[] = [];

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    console.log('OrdersListComponent initialized');
    this.apiService.getOrders().subscribe((orders:any) => {
      this.orders = orders;
    });
  }

  navigateToOrder(id: number) {
    this.router.navigate(['/order', id]);
  }
}
