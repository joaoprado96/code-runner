import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import * as XLSX from 'xlsx';
import { DialogErrorComponent } from './dialog-error.component';

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
  @Input() monitor: string;
  @Input() comando: string;

  dataSource = new MatTableDataSource<any>([]);
  colunasExibidas: string[] = [];

  @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor(private http: HttpClient, public dialog: MatDialog) {}

  ngOnInit() {
    // Ajuste para verificar se monitor e comando estão definidos
    if (this.monitor && this.comando) {
      this.carregarDados({ monitor: this.monitor, comando: this.comando });
    }
  }

  carregarDados(payload: { monitor: string; comando: string }): void {
    this.http.post<ApiResponse>('https://exemplo.com/api/comandos', payload).subscribe({
      next: (response) => {
        if (response.resultado && response.resultado_comando) {
          this.dataSource.data = response.resultado_comando;
          this.colunasExibidas = Object.keys(response.resultado_comando[0] || {});
          this.dataSource.sort = this.sort;
        } else {
          this.mostrarPopupErro(response.mensagem || 'Erro desconhecido', response.monitor || 'Desconhecido');
        }
      },
      error: () => {
        this.mostrarPopupErro('Erro de comunicação com a API', 'Desconhecido');
      }
    });
  }

  mostrarPopupErro(mensagem: string, monitor: string) {
    this.dialog.open(DialogErrorComponent, {
      data: { mensagem, monitor }
    });
  }

  aplicarFiltro(event: Event) {
    const filtroValor = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filtroValor.trim().toLowerCase();
  }

  exportarParaExcel(): void {
    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(this.dataSource.data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'DadosExportados');
    XLSX.writeFile(wb, 'dados_exportados.xlsx');
  }
}
// <!-- Outro componente's template -->
// <app-tabela-dinamica [monitor]="'NomeDoMonitor'" [comando]="'ComandoEspecifico'"></app-tabela-dinamica>
