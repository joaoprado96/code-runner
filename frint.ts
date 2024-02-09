interface ApiResponse {
  [key: string]: any; // Permitindo que qualquer chave seja um string e seu valor seja qualquer coisa.
}

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-tabela-dinamica',
  templateUrl: './tabela-dinamica.component.html',
  styleUrls: ['./tabela-dinamica.component.css']
})
export class TabelaDinamicaComponent implements OnInit {
  colunasExibidas: string[] = [];
  dataSource: ApiResponse[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.carregarDados({ monitor: 'nomeDoMonitor', comando: 'comandoEspecifico' });
  }

  carregarDados(payload: { monitor: string; comando: string }): void {
    this.http.post<ApiResponse[]>('https://exemplo.com/api/comandos', payload).subscribe(dados => {
      this.dataSource = dados;
      if (dados && dados.length > 0) {
        this.colunasExibidas = Object.keys(dados[0]);
      }
    }, error => {
      console.error('Erro ao buscar dados:', error);
    });
  }
}