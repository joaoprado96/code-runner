// pie-chart.component.ts
import { Component, OnInit } from '@angular/core';
import { ChartType } from 'chart.js';
import { ApiService } from './api.service';

@Component({
  selector: 'app-pie-chart',
  template: `
    <div>
      <canvas baseChart
        [data]="pieChartData"
        [labels]="pieChartLabels"
        [chartType]="pieChartType">
      </canvas>
    </div>
  `
})
export class PieChartComponent implements OnInit {
  pieChartLabels: string[] = [];
  pieChartData: number[] = [];
  pieChartType: ChartType = 'pie';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getDados().subscribe(data => {
      this.pieChartLabels = Object.keys(data);
      this.pieChartData = Object.values(data);
    });
  }
}
