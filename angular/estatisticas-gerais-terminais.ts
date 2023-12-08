// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private apiURL1 = 'https://mi-coderunner.apps.zcxdev.tech.itau/consulta-geral';
  private apiURL2 = 'https://mi-coderunner.apps.zcxdev.tech.itau/consulta-geral-monitor';
  private apiURL3 = 'https://mi-coderunner.apps.zcxdev.tech.itau/consulta-disponiveis-unicos';
  private apiURL4 = 'https://mi-coderunner.apps.zcxdev.tech.itau/consulta-disponiveis-unicos-monitor';

  constructor(private http: HttpClient) {}

  getDados1(): Observable<any[]> {
    return this.http.get<any[]>(this.apiURL1);
  }
  getDados2(): Observable<any[]> {
    return this.http.get<any[]>(this.apiURL2);
  }
  getDados3(): Observable<any[]> {
    return this.http.get<any[]>(this.apiURL3);
  }
  getDados4(): Observable<any[]> {
    return this.http.get<any[]>(this.apiURL4);
  }
}
