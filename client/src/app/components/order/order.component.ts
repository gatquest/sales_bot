import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
@Component({
  standalone: true,
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit {
  orderId: string | null = null;
  order: any;
  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    // Получаем параметр 'id' из маршрута
    this.route.paramMap.subscribe(params => {
      this.orderId = params.get('id');

      this.apiService.getOrder(Number(this.orderId)).subscribe(order => {
        this.order = order;
      });
      // Теперь вы можете использовать orderId в вашем компоненте
    });
  }
}
