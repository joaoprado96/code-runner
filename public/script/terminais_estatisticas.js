document.addEventListener('DOMContentLoaded', function() {
    loadNavbar();
    loadFooter();
    fetchEstatisticas(); // Chama a função para carregar as estatísticas
    fetchEstatisticasV2();
});

function loadNavbar() {
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    fetch('terminais_navbar.html')
        .then(response => response.text())
        .then(html => {
            navbarPlaceholder.innerHTML = html;
        }).catch(error => {
            console.error('Falha ao carregar o navbar:', error);
        });
}
function loadFooter() {
    const footerPlaceholder = document.getElementById('footer-placeholder');
    fetch('terminais_footer.html')
        .then(response => response.text())
        .then(html => {
            footerPlaceholder.innerHTML = html;
        }).catch(error => {
            console.error('Falha ao carregar o footer:', error);
        });
}

function fetchEstatisticas() {
    fetch('/codes/terminais_analise', {
        method: 'POST',
        // Adicione quaisquer headers necessários, como Content-Type ou tokens de autenticação
    })
    .then(response => response.text()) // Primeiro, obtemos a resposta como texto
    .then(text => {
        const data = JSON.parse(text); // Em seguida, convertemos o texto em um objeto JavaScript
        displayEstatisticas(data);
    })
    .catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
    });
}

function fetchEstatisticasV2() {
    fetch('/codes/terminais_analiseV2', {
        method: 'POST',
        // Adicione quaisquer headers necessários, como Content-Type ou tokens de autenticação
    })
    .then(response => response.text()) // Primeiro, obtemos a resposta como texto
    .then(text => {
        const data = JSON.parse(text); // Em seguida, convertemos o texto em um objeto JavaScript
        displayEstatisticasV2(data);
    })
    .catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
    });
}


function displayEstatisticas(data) {
    const estatisticasDescricao = document.getElementById('estatisticasDescricao');
    const graficoContainer = document.getElementById('graficoContainer');

    // Verifica se 'data' é um array
    if (Array.isArray(data)) {
        // Calcula o total somando as quantidades de todos os itens
        const totalQuantidade = data.reduce((total, item) => total + item.quantidade, 0);

        // Prepara os dados para o gráfico
        const labels = data.map(item => item.descricao);
        const quantidades = data.map(item => item.quantidade);
        const cores = data.map((_, i) => `hsl(30, ${90 + i * 5}%, ${50 + i * 10}%)`); // Diferentes tons de laranja

        // Cria o gráfico de pizza
        const graficoData = {
            labels: labels,
            datasets: [{
                label: 'terminais',
                data: quantidades,
                backgroundColor: cores,
            }]
        };

        const config = {
            type: 'pie',
            data: graficoData,
            options: {}
        };

        new Chart(graficoContainer, config);

        // Limpa a descrição anterior e adiciona os novos dados em forma de cards
        estatisticasDescricao.innerHTML = '<div class="row">'; // Inicia uma nova linha para os cards
        data.forEach(item => {
            const porcentagem = (item.quantidade / totalQuantidade * 100).toFixed(2);
            estatisticasDescricao.innerHTML += `
                <div class="col-md-6 mb-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title"><strong>${item.descricao}</strong></h6>
                            <p class="card-text">terminais: ${item.quantidade} (${porcentagem}%)</p>
                        </div>
                    </div>
                    <br>
                </div>`;
        });
        estatisticasDescricao.innerHTML += '</div>'; // Fecha a linha dos cards
    } else {
        estatisticasDescricao.innerHTML = '<p>Nenhum dado encontrado para descrição.</p>';
    }
}

function displayEstatisticasV2(dados) {
    // Ordena os dados primeiro por monitor e depois por descrição
    dados.sort((a, b) => {
        if (a.monitor === b.monitor) {
            return a.descricao.localeCompare(b.descricao);
        }
        return a.monitor.localeCompare(b.monitor);
    });

    const estatisticasContainer = document.getElementById('estatisticasContainer');
    estatisticasContainer.innerHTML = ''; // Limpa conteúdo anterior

    let dadosPorMonitor = {};
    
    // Agrupa os dados por monitor
    dados.forEach(item => {
        if (!dadosPorMonitor[item.monitor]) {
            dadosPorMonitor[item.monitor] = [];
        }
        dadosPorMonitor[item.monitor].push(item);
    });

    // Cria um card e gráfico para cada monitor
    for (let monitor in dadosPorMonitor) {
        let monitorData = dadosPorMonitor[monitor];
        let labels = monitorData.map(item => item.descricao);
        let quantidades = monitorData.map(item => item.quantidade);
        const cores = monitorData.map((_, i) => `hsl(30, ${90 + i * 5}%, ${50 + i * 10}%)`); // Diferentes tons de laranja

        // Cria um novo elemento div para o card
        let cardDiv = document.createElement('div');
        cardDiv.className = 'card mb-4';
        let canvasId = 'grafico-' + monitor;

        // Conteúdo do card
        cardDiv.innerHTML = `
            <div class="card-body">
                <h4 class="card-title"><strong>${monitor}</strong></h4>
                <canvas id="${canvasId}"></canvas>
                <div class="estatisticas-texto"></div>
            </div>`;

        estatisticasContainer.appendChild(cardDiv);

        // Configuração do gráfico
        let graficoData = {
            labels: labels,
            datasets: [{
                label: `${monitor}`,
                data: quantidades,
                backgroundColor: cores,
            }]
        };

        let config = {
            type: 'pie',
            data: graficoData,
            options: {}
        };

        // Renderiza o gráfico
        new Chart(document.getElementById(canvasId), config);

        // Adiciona os dados em texto no card
        let estatisticasTextoDiv = cardDiv.querySelector('.estatisticas-texto');
        let estatisticasTexto = '';
        monitorData.forEach(item => {
            estatisticasTexto += `<p>${item.descricao}: ${item.quantidade}</p>`;
        });

        estatisticasTextoDiv.innerHTML = estatisticasTexto;
    }
}

