// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private apiUrl = 'http://sua-api.com/api/dados';

  constructor(private http: HttpClient) {}

  getDados(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
