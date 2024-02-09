import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import * as XLSX from 'xlsx';

interface ApiResponse {
  resultado: boolean;
  resultado_comando: any[];
  mensagem?: string;
  monitor?: string;
}

@Component({
  selector: 'app-tabela-dinamica',
  templateUrl: './tabela-dinamica.component.html',
  styleUrls: ['./tabela-dinamica.component.css']
})
export class TabelaDinamicaComponent implements OnInit {
  dataSource = new MatTableDataSource<any>([]);
  colunasExibidas: string[] = [];

  @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor(private http: HttpClient, public dialog: MatDialog) {}

  ngOnInit() {
    this.carregarDados({ monitor: 'nomeDoMonitor', comando: 'comandoEspecifico' });
  }

  carregarDados(payload: { monitor: string; comando: string }): void {
    this.http.post<ApiResponse>('https://exemplo.com/api/comandos', payload).subscribe({
      next: (resposta) => {
        if (resposta.resultado && resposta.resultado_comando) {
          this.dataSource.data = resposta.resultado_comando;
          this.colunasExibidas = Object.keys(resposta.resultado_comando[0]);
          this.dataSource.sort = this.sort;
        } else {
          this.mostrarPopupErro(resposta.mensagem, resposta.monitor);
        }
      },
      error: (erro) => {
        console.error('Erro ao buscar dados:', erro);
        this.mostrarPopupErro("Erro de comunicação com a API.", "");
      }
    });
  }

  mostrarPopupErro(mensagem: string, monitor: string) {
    this.dialog.open(DialogComponent, {
      width: '250px',
      data: {mensagem: mensagem, monitor: monitor}
    });
  }

  // Métodos para filtragem, ordenação e exportação para Excel...
}