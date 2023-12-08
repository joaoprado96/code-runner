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
    // Mapeia os dados para o formato desejado
    const formattedData = data.map(item => ({
      name: item.monitor,
      value: item.QuantidadeDisponiveis
    }));
  
    // Ordena os dados por nome do monitor em ordem alfabética
    formattedData.sort((a, b) => a.name.localeCompare(b.name));
  
    return formattedData;
  }
  
  
  private groupDataByMonitor(data: any[]): { [monitor: string]: any[] } {
    const groupedData: { [monitor: string]: any[] } = {};
  
    // Agrupar os dados por monitor
    data.forEach(item => {
      if (!groupedData[item.monitor]) {
        groupedData[item.monitor] = [];
      }
      groupedData[item.monitor].push({ name: item.descricao, value: item.quantidade });
    });
  
    // Ordenar as chaves (monitores) por ordem alfabética
    const sortedMonitors = Object.keys(groupedData).sort();
  
    // Criar um novo objeto com os monitores ordenados
    const sortedGroupedData: { [monitor: string]: any[] } = {};
    sortedMonitors.forEach(monitor => {
      sortedGroupedData[monitor] = groupedData[monitor];
    });
  
    return sortedGroupedData;
  }
  
  private combineDataForBarChart(data: any[]): any[] {
    const combinedData: any[] = [];
  
    data.forEach(item => {
      combinedData.push({ 
        name: item.monitor + ' - ' + item.descricao, 
        value: item.quantidade 
      });
    });
  
    // Ordenar por nome do monitor e descrição
    combinedData.sort((a, b) => a.name.localeCompare(b.name));
  
    return combinedData;

  }
    private prepareStackedBarData(data: any[]): any[] {
    const result = {};

    data.forEach(item => {
      if (!result[item.monitor]) {
        result[item.monitor] = { name: item.monitor, series: [] };
      }
      result[item.monitor].series.push({
        name: item.descricao,
        value: item.quantidade
      });
    });

    return Object.values(result);
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
