async function analiseBase() {
    const response2 = await fetch('/front/analise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    // Adicionar linha para esperar finalização
    const registros2 = await response2.json();
    console.log(registros2)
}

analiseBase()

let versoes                     = Object.keys(data);
let labels                      = Object.keys(data).map(key => key.replace(/[^a-zA-Z0-9]/g, ''));
let tempoMedioExecucaoData      = versoes.map(versao => data[versao].tempo_medio_execucao);
let tempoTotalExecucaoData      = versoes.map(versao => data[versao].tempo_total_execucao);
let quantidadeExecucoesData     = versoes.map(versao => data[versao].quantidade_execucoes);
let quantidadeExecutoresData    = versoes.map(versao => data[versao].quantidade_executores);
let quantidadeFalhasTestesData  = versoes.map(versao => data[versao].quantidade_falhas_teste);
let quantidadeFalhasVersaoData  = versoes.map(versao => data[versao].quantidade_falhas_versao);
let quantidadeAprovacoesData    = versoes.map(versao => data[versao].quantidade_aprovacoes);
let quantidadeTestesNaVersaoData = versoes.map(versao => data[versao].quantidade_id_teste_unicos);

var selectElement   = document.getElementById('testSelect');
var ctx             = document.getElementById('tempoChart').getContext('2d');
var ctxtotal        = document.getElementById('tempoTotalChart').getContext('2d');
var ctx2            = document.getElementById('execucoesChart').getContext('2d');
var ctx3            = document.getElementById('executoresChart').getContext('2d');
var ctx4            = document.getElementById('falhasChart').getContext('2d');
var ctxsucesso      = document.getElementById('sucessoChart').getContext('2d');

var testIDs = new Set();  // Para evitar duplicatas
for (var key in analise) {
    var testID = key.split(",")[0].slice(1);  // Extraindo o ID do teste
    testIDs.add(testID);
}

testIDs.forEach(function(testID) {
    var option = document.createElement('option');
    option.value = testID;
    option.text = testID;
    selectElement.add(option);
});

selectElement.addEventListener('change', function() {
    var selectedTestID = this.value;
    var labels  = [];
    var data    = [];
    var data2   = [];
    var data3   = [];
    var data4   = [];
    var data5   = [];
    var data6   = [];

    for (var key in analise) {
        var testID = key.split(",")[0].slice(1);
        if (testID === selectedTestID) {
            labels.push(key.split(",")[1].trim().slice(1, -2));
            data.push(analise[key]['tempo_medio_execucao']);
            data2.push(analise[key]['quantidade_execucoes']);
            data3.push(analise[key]['quantidade_executores']);
            data4.push(analise[key]['quantidade_falhas_teste']);
            data5.push(analise[key]['tempo_total_execucao']);
            data6.push(analise[key]['quantidade_sucessos_teste']);
        }
    }
    
    tempoChart.data.labels = labels;
    tempoChart.data.datasets.forEach((dataset) => {
        dataset.data = data;
    });
    execucoesChart.data.labels = labels;
    execucoesChart.data.datasets.forEach((dataset) => {
        dataset.data = data2;
    });
    executoresChart.data.labels = labels;
    executoresChart.data.datasets.forEach((dataset) => {
        dataset.data = data3;
    });
    falhasChart.data.labels = labels;
    falhasChart.data.datasets.forEach((dataset) => {
        dataset.data = data4;
    });
    tempoTotalChart.data.labels = labels;
    tempoTotalChart.data.datasets.forEach((dataset) => {
        dataset.data = data5;
    });
    sucessoChart.data.labels = labels;
    sucessoChart.data.datasets.forEach((dataset) => {
        dataset.data = data6;
    });
    tempoTotalChart.update();
    tempoChart.update();
    execucoesChart.update();
    executoresChart.update();
    falhasChart.update();
    sucessoChart.update();
});

var tempoChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'TEMPO MÉDIO DE EXECUÇÃO DO TESTE',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'TEMPO (s)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

var tempoTotalChart = new Chart(ctxtotal, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'TEMPO TOTAL DE EXECUÇÃO DO TESTE',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'TEMPO (s)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

var execucoesChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'QUANTIDADE DE EXECUÇÕES',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'EXECUÇÕES (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

var executoresChart = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'QUANTIDADE DE EXECUTORES',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'EXECUTORES (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

var falhasChart = new Chart(ctx4, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'QUANTIDADE DE FALHAS NO TESTE',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'FALHAS NO TESTE (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

var sucessoChart = new Chart(ctxsucesso, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'QUANTIDADE DE SUCESSOS NO TESTE',
            fill: false,
            data: [],
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
            borderColor: 'rgba(255, 87, 34, 1.0)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'SUCESSOS NO TESTE (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeTestesNaVersao'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE TESTES JÁ EXECUTADOS',
            data: quantidadeTestesNaVersaoData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'TEMPO (s)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('tempoMedioExecucao'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'TEMPO MÉDIO DE EXECUÇÃO',
            data: tempoMedioExecucaoData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'TEMPO (s)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('tempoTotalExecucao'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'TEMPO TOTAL DE EXECUÇÃO',
            data: tempoTotalExecucaoData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'TEMPO (s)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeExecucoes'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE SUBMISSÃO DE TESTES',
            data: quantidadeExecucoesData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'QUANTIDADE (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeExecutores'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE EXECUTORES',
            data: quantidadeExecutoresData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Nº DE PESSOAS (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeFalhasTestes'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE SUBMISSÕES COM FALHA NO TESTE',
            data: quantidadeFalhasTestesData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Nº DE FALHAS (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeFalhasVersao'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE SUBMISSÕES COM FALHA NA VERSÃO',
            data: quantidadeFalhasVersaoData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Nº DE FALHAS (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

new Chart(document.getElementById('quantidadeAprovacoes'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'QUANTIDADE DE TESTES APROVADOS',
            data: quantidadeAprovacoesData,
            backgroundColor: 'rgba(255, 87, 34, 1.0)', // Laranja semi-transparente
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Nº DE APROVAÇÕES (n)', // Adicione o label para o eixo Y aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'VERSÃO', // Adicione o label para o eixo X aqui
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

