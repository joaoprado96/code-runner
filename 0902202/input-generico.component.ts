import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-input-generico',
  templateUrl: './input-generico.component.html',
  styleUrls: ['./input-generico.component.css']
})
export class InputGenericoComponent implements OnInit {
  monitores: string[] = [];
  monitorSelecionado: string = '';
  comando: string = '';
  exibirComo: 'tabela' | 'cards' = 'tabela'; // Opção para exibir como tabela ou cards
  dadosCarregados: any[] = []; // Dados que serão passados para o componente filho

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.carregarMonitores();
  }

  carregarMonitores(): void {
    // Substitua pela sua URL real
    const url = 'https://exemplo.com/api/monitores';
    this.http.get<{[key: string]: any}>(url).subscribe({
      next: (response) => {
        this.monitores = Object.keys(response); // Assumindo que os monitores são as chaves do objeto
      },
      error: (error) => {
        console.error('Erro ao buscar monitores:', error);
      }
    });
  }

  onComandoChange(event: Event): void {
    this.comando = (event.target as HTMLInputElement).value.toUpperCase();
  }
}
