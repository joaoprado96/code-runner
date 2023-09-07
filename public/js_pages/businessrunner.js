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


        // Preencher o dashboard de estatísticas gerais
        const generalStatsDiv = document.getElementById('generalStats');
        for (const [key, value] of Object.entries(transformed_data.general_stats)) {
            const friendlyName = getFriendlyName(key);
            generalStatsDiv.innerHTML += `
            <div class="form-entry">
                <div class="description"><strong>${friendlyName}</strong></div>
                <div class="value">${value}</div>
            </div>`;
        }

        // Preencher o dashboard de estatísticas de programa
        const programStatsDiv = document.getElementById('programStats');

        for (const [program, stats] of Object.entries(transformed_data.program_stats)) {
            const programDiv = document.createElement('div');
            programDiv.classList.add('program-box');
            programDiv.innerHTML = `<strong>PROGRAMA: ${program}</strong>`;
        
            // Adicionar linhas de negócio
            const businessLinesDiv = document.createElement('div');
            businessLinesDiv.classList.add('form-entry');
            businessLinesDiv.innerHTML = '<div class="description"><strong>LINHA(S)</strong></div>';
            stats.business_lines.forEach(line => {
                const lineItem = document.createElement('span');
                lineItem.classList.add('line-box');
                lineItem.textContent = line;
                businessLinesDiv.appendChild(lineItem);
            });
            programDiv.appendChild(businessLinesDiv);
        
            // Adicionar transações
            const transactionsDiv = document.createElement('div');
            transactionsDiv.classList.add('form-entry');
            transactionsDiv.innerHTML = '<div class="description"><strong>TRANSAÇÕES</strong></div>';
            stats.transactions.forEach(transaction => {
                const transactionItem = document.createElement('span');
                transactionItem.classList.add('transaction-box');
                transactionItem.textContent = transaction;
                transactionsDiv.appendChild(transactionItem);
            });
            programDiv.appendChild(transactionsDiv);
        
            programStatsDiv.appendChild(programDiv);
        }
        
        const businessLinesDiv = document.getElementById('business-lines');

        for (const [businessLine, data] of Object.entries(transformed_data.business_lines)) {
            const businessDiv = document.createElement('div');
            businessDiv.classList.add('business-box');
            businessDiv.innerHTML = `<h2>${businessLine}</h2>`;
            
            // Adicionar transações
            const transDiv = document.createElement('div');
            transDiv.innerHTML = 'Transações:';
            data.trans.forEach(transaction => {
                const transItem = document.createElement('span');
                transItem.classList.add('transaction-box');
                transItem.textContent = transaction;
                transDiv.appendChild(transItem);
            });
            businessDiv.appendChild(transDiv);
            
            // Adicionar grupo de suporte
            const supportGroupDiv = document.createElement('div');
            supportGroupDiv.innerHTML = 'Grupo de Suporte:';
            
            data.support_group.forEach(group => {
                const groupItem = document.createElement('span');
                groupItem.classList.add('support-group-box');
                groupItem.textContent = group;
                supportGroupDiv.appendChild(groupItem);
            });
        
            businessDiv.appendChild(supportGroupDiv);
            
            businessLinesDiv.appendChild(businessDiv);
        }
       
        const supportGroupsDiv = document.getElementById('support-groups');

        for (const [group, lines] of Object.entries(transformed_data.support_group)) {
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('group-box');
            groupDiv.innerHTML = `<h2>${group}</h2>`;
            
            const linesDiv = document.createElement('div');
            linesDiv.innerHTML = 'Linhas de Negócio:';
            
            lines.forEach(line => {
                const lineItem = document.createElement('span');
                lineItem.classList.add('line-box');
                lineItem.textContent = line;
                linesDiv.appendChild(lineItem);
            });
        
            groupDiv.appendChild(linesDiv);
            
            supportGroupsDiv.appendChild(groupDiv);
        }
     
        // Preencher Volumetria por Transação
        // Preencher Volumetria por Transação
        const transVolDiv = document.getElementById('trans-vol-table-container');

        // Criar a tabela e o cabeçalho
        let transVolTable = '<table border="1"><thead><tr><th>Transação</th>';
        transVolTable += '<th>Soma Total</th>';

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
        // Primeiro, ordene as transações com base na soma de todos os monitores
        const sortedTransactions = Object.entries(transformed_data.trans_vol).sort((a, b) => {
            const sumA = Object.values(a[1]).reduce((acc, val) => acc + (val || 0), 0);
            const sumB = Object.values(b[1]).reduce((acc, val) => acc + (val || 0), 0);
            return sumB - sumA;  // ordem decrescente, mude para sumA - sumB para ordem crescente
        });

        for (const [trans, vol] of sortedTransactions) {
            const totalSum = Object.values(vol).reduce((acc, val) => acc + (val || 0), 0);

            transVolTable += `<tr><td>${trans}</td>`;
            // Adicionar soma total em cada linha
            transVolTable += `<td>${totalSum}</td>`;
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
        transMipsTable += '<th>Soma Total</th>';
        
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
        // Primeiro, ordene as transações com base na soma de todos os monitores
        const sortedTransactionsMIPS = Object.entries(transformed_data.trans_mips).sort((a, b) => {
            const sumA = Object.values(a[1]).reduce((acc, val) => acc + (val || 0), 0);
            const sumB = Object.values(b[1]).reduce((acc, val) => acc + (val || 0), 0);
            return sumB - sumA;  // ordem decrescente, mude para sumA - sumB para ordem crescente
        });
        
        for (const [trans, mips] of sortedTransactionsMIPS) {
            const totalSumMIPS = Object.values(mips).reduce((acc, val) => acc + (val || 0), 0);
        
            transMipsTable += `<tr><td>${trans}</td>`;
            transMipsTable += `<td>${totalSumMIPS}</td>`;
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
            const lineDiv = document.createElement('div');
            lineDiv.classList.add('line-terminal-box');
            lineDiv.innerHTML = `<h2>${line}</h2>`;
            
            const terminalsDiv = document.createElement('div');
            terminalsDiv.innerHTML = 'Terminais:';
            
            terminals.forEach(terminal => {
                const terminalItem = document.createElement('span');
                terminalItem.classList.add('terminal-box');
                terminalItem.textContent = terminal;
                terminalsDiv.appendChild(terminalItem);
            });
        
            lineDiv.appendChild(terminalsDiv);
            
            lineTerminalsDiv.appendChild(lineDiv);
        }
        
        // Gráfico de Volumetria por Transação
        const transVolLabels = Object.keys(transformed_data.trans_vol);
        const transVolData = Object.values(transformed_data.trans_vol)
                                  .map(innerObj => sumValues(innerObj))
                                  .filter(value => value !== 0);  // Filtra valores zero
        
        // Atualiza os rótulos para corresponder aos dados filtrados
        const filteredLabels = transVolLabels.filter((_, index) => transVolData[index] !== 0);
        
        const maxValueVol = Math.max(...transVolData);
        const minValueVol = Math.min(...transVolData);
        const scaleVol = 255 / (maxValueVol - minValueVol || 1);
        
        const transVolCtx = document.getElementById('transVolChart').getContext('2d');
        
        
        new Chart(transVolCtx, {
            type: 'bar',
            data: {
                labels: transVolLabels,
                datasets: [{
                    label: 'Volumetria',
                    data: transVolData,
                    backgroundColor: transVolData.map(value => getGreenColor((value - minValueVol) * scaleVol)),
                    borderColor: transVolData.map(value => getGreenBorderColor((value - minValueVol) * scaleVol)),
                    borderWidth: 1,
                    hoverBackgroundColor: transVolData.map(value => getGreenColor((value - minValueVol) * scaleVol + 10)),
                    hoverBorderColor: transVolData.map(value => getGreenBorderColor((value - minValueVol) * scaleVol + 10)),
                    hoverBorderWidth: 2,
                    barThickness: 10,  // Defina a espessura desejada aqui
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        barPercentage: 0.5,
                        categoryPercentage: 1.0,
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'end'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',
                    borderWidth: 1
                },
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }
        });

        // Gráfico de MIPS por Transação
        const transMipsLabels = Object.keys(transformed_data.trans_mips);
        const transMipsData = Object.values(transformed_data.trans_mips)
                              .map(innerObj => sumValues(innerObj))
                              .filter(value => value !== 0);  // Filtra valores zero
        
        // Atualiza os rótulos para corresponder aos dados filtrados
        const filteredMipsLabels = transMipsLabels.filter((_, index) => transMipsData[index] !== 0);
        
        const maxValue = Math.max(...transMipsData);
        const minValue = Math.min(...transMipsData);
        const scale = 255 / (maxValue - minValue || 1);
        
        const transMipsCtx = document.getElementById('transMipsChart').getContext('2d');
        
        new Chart(transMipsCtx, {
            type: 'bar',
            data: {
                labels: transMipsLabels,
                datasets: [{
                    label: 'MIPS',
                    data: transMipsData,
                    backgroundColor: transMipsData.map(value => getGreenColor((value - minValue) * scale)),
                    borderColor: transMipsData.map(value => getGreenBorderColor((value - minValue) * scale)),
                    borderWidth: 1,
                    hoverBackgroundColor: transMipsData.map(value => getGreenColor((value - minValue) * scale + 10)),
                    hoverBorderColor: transMipsData.map(value => getGreenBorderColor((value - minValue) * scale + 10)),
                    hoverBorderWidth: 2,
                    barThickness: 10,  // Defina a espessura desejada aqui
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        barPercentage: 0.5,
                        categoryPercentage: 1.0,
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'end'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',
                    borderWidth: 1
                },
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }
        });


        // Para Volumetria por Linha de Negócio
        const businessVolLabels = Object.keys(transformed_data.business_lines);
        const businessVolData = Object.values(transformed_data.business_lines).map(line => sumValues(line.vol || {}));
        const businessVolCtx = document.getElementById('businessVolChart').getContext('2d');
        
        new Chart(businessVolCtx, {
            type: 'bar',
            data: {
                labels: businessVolLabels,
                datasets: [{
                    label: 'Volumetria por Linha de Negócio',
                    data: businessVolData,
                    backgroundColor: 'rgba(76, 175, 80, 0.5)',  // Cor verde com 50% de transparência
                    borderColor: 'rgba(76, 175, 80, 1)',  // Cor verde sólida
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(76, 175, 80, 0.7)',  // Cor verde ao passar o mouse com 70% de transparência
                    hoverBorderColor: 'rgba(76, 175, 80, 1)',  // Cor verde sólida ao passar o mouse
                    hoverBorderWidth: 2  // Aumenta a espessura da borda ao passar o mouse
                }]
            },
            options: {
                legend: {
                    position: 'bottom',  // Posiciona a legenda na parte inferior
                    align: 'end'  // Alinha a legenda à direita
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',  // Tooltip de fundo preto com 70% de transparência
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',  // Borda do tooltip
                    borderWidth: 1
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                // Para adicionar uma leve sombra em cada barra
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',  // Cor verde para a borda
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,  // Deslocamento vertical da sombra
                        shadowBlur: 10,  // Desfoque da sombra
                        shadowColor: 'rgba(0,0,0,0.3)'  // Cor da sombra com 30% de transparência
                    }
                }
            }
        });
        

        // Para MIPS por Linha de Negócio
        const businessMipsLabels = Object.keys(transformed_data.business_lines);
        const businessMipsData = Object.values(transformed_data.business_lines).map(line => sumValues(line.mips || {}));
        const businessMipsCtx = document.getElementById('businessMipsChart').getContext('2d');
        
        new Chart(businessMipsCtx, {
            type: 'bar',
            data: {
                labels: businessMipsLabels,
                datasets: [{
                    label: 'MIPS por Linha de Negócio',
                    data: businessMipsData,
                    backgroundColor: 'rgba(76, 175, 80, 0.5)',  // Cor verde com 50% de transparência
                    borderColor: 'rgba(76, 175, 80, 1)',  // Cor verde sólida
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(76, 175, 80, 0.7)',  // Cor verde ao passar o mouse com 70% de transparência
                    hoverBorderColor: 'rgba(76, 175, 80, 1)',  // Cor verde sólida ao passar o mouse
                    hoverBorderWidth: 2  // Aumenta a espessura da borda ao passar o mouse
                }]
            },
            options: {
                legend: {
                    position: 'bottom',  // Posiciona a legenda na parte inferior
                    align: 'end'  // Alinha a legenda à direita
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',  // Tooltip de fundo preto com 70% de transparência
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',  // Borda do tooltip
                    borderWidth: 1
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                // Para adicionar uma leve sombra em cada barra
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',  // Cor verde para a borda
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,  // Deslocamento vertical da sombra
                        shadowBlur: 10,  // Desfoque da sombra
                        shadowColor: 'rgba(0,0,0,0.3)'  // Cor da sombra com 30% de transparência
                    }
                }
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
        const businessLinesMonitorData = Object.keys(transformed_data.business_lines);
        const totalBusinessLines = businessLinesMonitorData.length;
        
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
                backgroundColor: getGreenScaleColor(index, totalBusinessLines),
                borderColor: getGreenScaleBorderColor(index, totalBusinessLines),
                borderWidth: 1,
                hoverBackgroundColor: getGreenScaleColor(index + 1, totalBusinessLines),
                hoverBorderColor: getGreenScaleBorderColor(index + 1, totalBusinessLines),
                hoverBorderWidth: 2
            };
        });
        
        // Criação do gráfico
        const businessLineVolByMonitorChartctx = document.getElementById('businessLineVolByMonitorChart').getContext('2d');
        new Chart(businessLineVolByMonitorChartctx, {
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
                },
                legend: {
                    position: 'bottom',
                    align: 'end'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',
                    borderWidth: 1
                },
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }
        });

        const datasets2 = businessLinesMonitorData.map((line, index) => {
            return {
                label: line,
                data: monitorLabels.map((monitor, index) => {
                    if(datasetMips[index] && typeof datasetMips[index] === 'object') {
                        return datasetMips[index][line] || 0;
                    } else {
                        return 0;
                    }
                }),
                backgroundColor: getGreenScaleColor(index, totalBusinessLines),
                borderColor: getGreenScaleBorderColor(index, totalBusinessLines),
                borderWidth: 1,
                hoverBackgroundColor: getGreenScaleColor(index + 1, totalBusinessLines),
                hoverBorderColor: getGreenScaleBorderColor(index + 1, totalBusinessLines),
                hoverBorderWidth: 2
            };
        });
        
        // Criação do gráfico
        const businessLineMipsByMonitorChartctx = document.getElementById('businessLineMipsByMonitorChart').getContext('2d');
        new Chart(businessLineMipsByMonitorChartctx, {
            type: 'bar',
            data: {
                labels: monitorLabels,
                datasets: datasets2
            },
            options: {
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'end'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    titleFontColor: 'white',
                    bodyFontColor: 'white',
                    borderColor: 'rgba(0,0,0,0.9)',
                    borderWidth: 1
                },
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgba(0, 255, 0, 1)',
                        borderSkipped: 'bottom',
                        shadowOffsetX: 0,
                        shadowOffsetY: 3,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }
        });
            // const $ = go.GraphObject.make;

            // const myDiagram = $(go.Diagram, "myDiagramDiv", {
            // "undoManager.isEnabled": true,
            // layout: $(go.TreeLayout)
            // });
            
            // myDiagram.nodeTemplate =
            // $(go.Node, "Auto",
            //     $(go.Shape, "RoundedRectangle", { strokeWidth: 0 },
            //     new go.Binding("fill", "color")),
            //     $(go.TextBlock, { margin: 8 },
            //     new go.Binding("text", "key"))
            // );

            // myDiagram.linkTemplate =
            // $(go.Link,
            //     $(go.Shape, { strokeWidth: 1.5 }),
            //     $(go.Shape, { toArrow: "Standard", stroke: null })
            // );

            // // Converter o JSON em um formato que GoJS pode entender
            // var nodeDataArray = [];
            // var linkDataArray = [];
            
            // Object.keys(transformed_data.business_lines_program).forEach((businessLine, index) => {
            // nodeDataArray.push({ key: businessLine, color: "lightblue" });
            // transformed_data.business_lines_program[businessLine].forEach(program => {
            //     if (!programExistsInNodeDataArray(nodeDataArray, program)) {
            //         nodeDataArray.push({ key: program, color: "lightgreen" });
            //     }
            //     linkDataArray.push({ from: businessLine, to: program });
            //     });
            // });

            // var yCoordGreen = 0;
            // var yCoordBlue = 0;
            // const verticalSpacing = 100; // Espaço vertical entre os nós
            
            // nodeDataArray = nodeDataArray.map((node, index) => {
            //     let xCoord;
            //     if (node.color === "lightgreen") {
            //         xCoord = 500;  // Coluna da esquerda
            //         yCoordGreen += verticalSpacing;
            //     } else {
            //         xCoord = 10; // Coluna da direita
            //         yCoordBlue += verticalSpacing;
            //     }
            //     return {
            //         ...node,
            //         loc: `${xCoord} ${node.color === "lightgreen" ? yCoordGreen : yCoordBlue}`
            //     };
            // });

            // myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);


    function getGreenColor(value) {
        const greenValue = Math.min(255, Math.max(0, value));
        return `rgba(0, ${greenValue}, 0, 0.5)`;
    }
    
    function getGreenBorderColor(value) {
        const greenValue = Math.min(255, Math.max(0, value));
        return `rgba(0, ${greenValue}, 0, 1)`;
    }            
    function getGreenScaleColor(index, total) {
        const step = Math.floor(255 / total);
        const greenValue = step * index;
        return `rgba(0, ${greenValue}, 0, 0.5)`;
    }
    
    function getGreenScaleBorderColor(index, total) {
        const step = Math.floor(255 / total);
        const greenValue = step * index;
        return `rgba(0, ${greenValue}, 0, 1)`;
    }
            
    function programExistsInNodeDataArray(nodeDataArray, program) {
        return nodeDataArray.some(item => item.key === program);
    }
    function getFriendlyName(key) {
        const friendlyNames = {
            num_trans: "TRANSAÇÕES",
            num_programs: "PROGRAMAS",
            num_business_lines: "LINHAS DE NEGÓCIO",
            num_monitors: "MONITORES",
            num_support_groups: "GRUPOS DE SUPORTE",
            num_siglas: "SIGLAS"
        };
        return friendlyNames[key] || key; // Retorna o valor amigável, ou a própria chave se não estiver no mapa
    }     
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