// tabela.component.ts
import { Component, OnInit } from '@angular/core';
import { ApiService } from './tabela.service';

@Component({
  selector: 'app-tabela',
  template: `
    <p-table [value]="dados" [paginator]="true" [rows]="10" [sortField]="sortField" [sortOrder]="sortOrder">
      <ng-template pTemplate="header">
        <tr>
          <th *ngFor="let col of colunas" pSortableColumn="{{col}}">
            {{col}}
            <p-sortIcon [field]="col"></p-sortIcon>
          </th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-rowData>
        <tr>
          <td *ngFor="let col of colunas">
            {{rowData[col]}}
          </td>
        </tr>
      </ng-template>
    </p-table>
  `
})
export class TabelaComponent implements OnInit {
  dados: any[] = [];
  colunas: string[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getDados().subscribe(data => {
      this.dados = data;
      this.colunas = data.length > 0 ? Object.keys(data[0]) : [];
    });
  }
}
