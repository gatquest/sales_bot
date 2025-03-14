import { Routes } from '@angular/router';
import { MainComponent } from './components/main/main.component';
import { OrdersListComponent } from './components/orders-list/orders-list.component';
import { OrderComponent } from './components/order/order.component';
import { OrderCreateComponent } from './components/order-create/order-create.component';

export const routes: Routes = [
  { path: '', component: MainComponent },
  { path: 'orders', component: OrdersListComponent },
  { path: 'order/:id', component: OrderComponent },
  { path: 'create', component: OrderCreateComponent },
  { path: '**', redirectTo: '' }
];
