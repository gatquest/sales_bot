import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = '/api'; // Замените на адрес вашего FastAPI сервера

  constructor(private http: HttpClient) { }

  // Метод для выполнения GET запроса
  getData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/endpoint`); // Замените на ваш конечный адрес
  }

  getOrder(order_number: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/order/${order_number}`); // Замените на ваш конечный адрес
  }

  getOrders(): Observable<any> {
    return this.http.get(`${this.apiUrl}/orders`); // Замените на ваш конечный адрес
  }

  // Метод для выполнения POST запроса
  postData(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/endpoint`, data); // Замените на ваш конечный адрес
  }
}
