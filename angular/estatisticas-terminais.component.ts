// pie-chart.component.ts
import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/@core/services/estatisticas-terminais/estatisticas-gerais-terminais';

@Component({
  selector: 'app-estatisticas-terminais',
  templateUrl: './estatisticas-terminais.component.html',
  styleUrls: ['./estatisticas-terminais.component.scss']
})
export class EstatisticasTerminaisComponent implements OnInit {
  dadosGrafico1: any[] = [];
  dadosPorMonitor: { [monitor: string]: any[] } = {};
  dadosQuantidadeDisponiveis: any[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.apiService.getDados1().subscribe(data => {
      this.dadosGrafico1 = this.formatChartData(data);
    });

    this.apiService.getDados2().subscribe(data => {
      this.dadosPorMonitor = this.groupDataByMonitor(data);
    });

    this.apiService.getDados4().subscribe(data => {
      this.dadosQuantidadeDisponiveis = this.formatBarChartData(data);
    });
  }

  private formatChartData(data: any[]): any[] {
    return data.map(item => ({ name: item.descricao, value: item.quantidade }));
  }

  private formatBarChartData(data: any[]): any[] {
    return data.map(item => ({
      name: item.monitor,
      value: item.QuantidadeDisponiveis
    }));
  }
  
  private groupDataByMonitor(data: any[]): { [monitor: string]: any[] } {
    const groupedData: { [monitor: string]: any[] } = {};
    data.forEach(item => {
      if (!groupedData[item.monitor]) {
        groupedData[item.monitor] = [];
      }
      groupedData[item.monitor].push({ name: item.descricao, value: item.quantidade });
    });
    return groupedData;
  }

  getMonitors(): string[] {
    return Object.keys(this.dadosPorMonitor);
  }

  view: [number,number]=[700,400];
  showLabels: boolean = true;
  explodeSlices: boolean = false;
  doughnut: boolean = true;
  gradient: boolean = false;
  showLegend: boolean = false;
  legendPosition: string = 'right';
  legendTitle: string = '';
  valueFormatting: string = '';
  labelFormatting: string = '';

  colorScheme={
    domain: ['#000066', '#FF7C00','#0131FF','#AAAAAA']
  }
}
