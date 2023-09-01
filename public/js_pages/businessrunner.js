document.addEventListener('DOMContentLoaded', async (event) => {
    $(document).ready(function() {
        $('#trans-vol-table').DataTable();
        $('#trans-mips-table').DataTable();
    });

    await get(); // Espera a função assíncrona ser concluída
    // Esconder loader e mostrar conteúdo

    async function get() {
        // Faz uma chamada para a API para obter os dados
        const response2 = await fetch('/front/businessrunner', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ usuario: 'Joao'})
        });
        const transformed_data = await response2.json();

        // Preencher linhas de negócio
        const businessLinesDiv = document.getElementById('business-lines');
        for (const [businessLine, data] of Object.entries(transformed_data.business_lines)) {
            businessLinesDiv.innerHTML += `<h2>${businessLine}</h2>
                                            <p>Transações: ${data.trans.join(', ')}</p>
                                            <p>Grupo de Suporte: ${data.support_group}</p>`;
        }

        // Preencher grupos de suporte
        const supportGroupsDiv = document.getElementById('support-groups');
        for (const [group, lines] of Object.entries(transformed_data.support_group)) {
            supportGroupsDiv.innerHTML += `<h2>${group}</h2>
                                            <p>Linhas de Negócio: ${lines.join(', ')}</p>`;
        }

        // Preencher Volumetria por Transação
        const transVolDiv = document.getElementById('trans-vol-table-container');

        // Criar a tabela e o cabeçalho
        let transVolTable = '<table border="1"><thead><tr><th>Transação</th>';

        const allMonitors = new Set();
        for (const vol of Object.values(transformed_data.trans_vol)) {
            for (const monitor of Object.keys(vol)) {
                allMonitors.add(monitor);
            }
        }
        for (const monitor of allMonitors) {
            transVolTable += `<th>${monitor}</th>`;
        }

        transVolTable += '</tr></thead><tbody>';

        // Preencher as linhas da tabela
        for (const [trans, vol] of Object.entries(transformed_data.trans_vol)) {
            transVolTable += `<tr><td>${trans}</td>`;
            for (const monitor of allMonitors) {
                transVolTable += `<td>${vol[monitor] || 'N/A'}</td>`;
            }
            transVolTable += '</tr>';
        }

        transVolTable += '</tbody></table>';

        transVolDiv.innerHTML = transVolTable;

        // Preencher MIPS por Transação
        const transMipsDiv = document.getElementById('trans-mips-table-container');

        // Criar a tabela e o cabeçalho
        let transMipsTable = '<table border="1"><thead><tr><th>Transação</th>';
        
        const allMonitorsMIPS = new Set();
        for (const mips of Object.values(transformed_data.trans_mips)) {
            for (const monitor of Object.keys(mips)) {
                allMonitorsMIPS.add(monitor);
            }
        }
        for (const monitor of allMonitorsMIPS) {
            transMipsTable += `<th>${monitor}</th>`;
        }
        
        transMipsTable += '</tr></thead><tbody>';
        
        // Preencher as linhas da tabela
        for (const [trans, mips] of Object.entries(transformed_data.trans_mips)) {
            transMipsTable += `<tr><td>${trans}</td>`;
            for (const monitor of allMonitorsMIPS) {
                transMipsTable += `<td>${mips[monitor] || 'N/A'}</td>`;
            }
            transMipsTable += '</tr>';
        }
        
        transMipsTable += '</tbody></table>';
        
        transMipsDiv.innerHTML = transMipsTable;
        

        // Preencher terminais por linha de negócio
        const lineTerminalsDiv = document.getElementById('line-terminals');
        for (const [line, terminals] of Object.entries(transformed_data.line_terminals)) {
            lineTerminalsDiv.innerHTML += `<h2>${line}</h2>
                                            <p>Terminais: ${terminals.join(', ')}</p>`;
        }
        // Gráfico de Volumetria por Transação
        const transVolLabels = Object.keys(transformed_data.trans_vol);
        const transVolData = Object.values(transformed_data.trans_vol).map(innerObj => sumValues(innerObj));
        const transVolCtx = document.getElementById('transVolChart').getContext('2d');
        new Chart(transVolCtx, {
        type: 'bar',
        data: {
            labels: transVolLabels,
            datasets: [{
            label: 'Volumetria',
            data: transVolData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
            }]
        }
        });

        // Gráfico de MIPS por Transação
        const transMipsLabels = Object.keys(transformed_data.trans_mips);
        const transMipsData = Object.values(transformed_data.trans_mips).map(innerObj => sumValues(innerObj));
        const transMipsCtx = document.getElementById('transMipsChart').getContext('2d');
        new Chart(transMipsCtx, {
        type: 'bar',
        data: {
            labels: transMipsLabels,
            datasets: [{
            label: 'MIPS',
            data: transMipsData,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
            }]
        },
        });

        // Para Volumetria por Linha de Negócio
        const businessVolLabels = Object.keys(transformed_data.business_lines); // Supondo que cada linha de negócio tem dados de Volumetria
        const businessVolData = Object.values(transformed_data.business_lines).map(line => sumValues(line.vol || {})); // Supondo que 'vol' contém a Volumetria
        const businessVolCtx = document.getElementById('businessVolChart').getContext('2d');
        new Chart(businessVolCtx, {
        type: 'bar',
        data: {
            labels: businessVolLabels,
            datasets: [{
            label: 'Volumetria por Linha de Negócio',
            data: businessVolData,
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 1
            }]
        }
        });

        // Para MIPS por Linha de Negócio
        const businessMipsLabels = Object.keys(transformed_data.business_lines); // Supondo que cada linha de negócio tem dados de MIPS
        const businessMipsData = Object.values(transformed_data.business_lines).map(line => sumValues(line.mips || {})); // Supondo que 'mips' contém os MIPS
        const businessMipsCtx = document.getElementById('businessMipsChart').getContext('2d');
        new Chart(businessMipsCtx, {
        type: 'bar',
        data: {
            labels: businessMipsLabels,
            datasets: [{
            label: 'MIPS por Linha de Negócio',
            data: businessMipsData,
            backgroundColor: 'rgba(255, 193, 7, 0.5)',
            borderColor: 'rgba(255, 193, 7, 1)',
            borderWidth: 1
            }]
        }
        });

        // Supondo que transformed_data seja a saída da função transform_data() e que ela esteja disponível aqui.
        const monitorData = transformed_data.business_lines_monitor;


        // Separação dos rótulos e valores
        const monitorLabels = Object.keys(monitorData);  // Pega os monitores
        const datasetVol = [];  // Dataset para Volumetria
        const datasetMips = [];  // Dataset para MIPS

        monitorLabels.forEach(monitor => {
            datasetVol.push(monitorData[monitor].vol);
            datasetMips.push(monitorData[monitor].mips);
        });

        // Preparação dos dados para Chart.js
        const businessLinesMonitorData = Object.keys(transformed_data.business_lines);  // Pega as linhas de negócio
        const datasets = businessLinesMonitorData.map((line, index) => {
            return {
                label: line,
                data: monitorLabels.map((monitor, index) => {
                    if(datasetVol[index] && typeof datasetVol[index] === 'object') {
                      return datasetVol[index][line] || 0;
                    } else {
                      return 0;
                    }
                  }),
                backgroundColor: `rgba(${index * 50}, ${index * 20}, ${index * 30}, 0.5)`,  // cores aleatórias, você pode ajustar
                borderColor: `rgba(${index * 50}, ${index * 20}, ${index * 30}, 1)`,
                borderWidth: 1
            };
        });


        // Criação do gráfico
        const businessLineByMonitorChartctx = document.getElementById('businessLineByMonitorChart').getContext('2d');
        new Chart(businessLineByMonitorChartctx, {
            type: 'bar',
            data: {
                labels: monitorLabels,
                datasets: datasets
            },
            options: {
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true
                    }
                }
            }
        });

    // Função para gerar uma cor aleatória (apenas um exemplo)
    function randomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function sumValues(obj) {
        return Object.values(obj).reduce((a, b) => a + b, 0);
        }
    }
});
