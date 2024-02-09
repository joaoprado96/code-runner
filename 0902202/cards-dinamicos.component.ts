import { Component, Input, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { DialogErrorComponent } from './dialog-error.component'; // Ajuste o caminho conforme necessário

interface ApiResponse {
  resultado: boolean;
  resultado_comandos: any[];
  mensagem?: string;
  monitor?: string;
}

@Component({
  selector: 'app-cards-dinamicos',
  templateUrl: './cards-dinamicos.component.html',
  styleUrls: ['./cards-dinamicos.component.css']
})
export class CardsDinamicosComponent implements OnInit {
  @Input() monitor: string;
  @Input() comando: string;
  
  dados: any[] = [];

  constructor(private http: HttpClient, public dialog: MatDialog) { }

  ngOnInit(): void {
    // Garantir que monitor e comando sejam passados antes de fazer a chamada
    if (this.monitor && this.comando) {
      this.carregarDados();
    }
  }

  carregarDados(): void {
    const payload = { monitor: this.monitor, comando: this.comando };
    const url = 'https://exemplo.com/api/comandos'; // Substitua pela sua URL real

    this.http.post<ApiResponse>(url, payload).subscribe({
      next: (response) => {
        if (response.resultado && response.resultado_comandos) {
          this.dados = response.resultado_comandos;
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

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
}

// <app-cards-dinamicos [monitor]="'ValorDoMonitor'" [comando]="'ValorDoComando'"></app-cards-dinamicos>
