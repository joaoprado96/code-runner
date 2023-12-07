// pie-chart.component.ts
import { Component, OnInit } from '@angular/core';
import { ChartType } from 'chart.js';
import { ApiService } from './api.services';

@Component({
  selector: 'app-pie-charts',
  template: `
    <div *ngFor="let chartData of chartsData">
      <canvas baseChart
        [data]="chartData.data"
        [labels]="chartData.labels"
        [chartType]="chartType">
      </canvas>
    </div>
  `
})
export class PieChartsComponent implements OnInit {
  chartsData: any[] = [];
  chartType: ChartType = 'pie';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getDados().subscribe(dataList => {
      this.chartsData = dataList.map(data => ({
        labels: Object.keys(data),
        data: Object.values(data)
      }));
    });
  }
}
