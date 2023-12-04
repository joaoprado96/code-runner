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

    // Verifica se 'data' é um array
    if (Array.isArray(data)) {
        // Calcula o total somando as quantidades de todos os itens
        const totalQuantidade = data.reduce((total, item) => total + item.quantidade, 0);

        data.forEach(item => {
            // Calcula a porcentagem para cada item
            const porcentagem = (item.quantidade / totalQuantidade * 100).toFixed(2); // Arredonda para 2 casas decimais
            estatisticasDescricao.innerHTML += `<p>${item.descricao}: ${item.quantidade} (${porcentagem}%)</p>`;
        });
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

    const tabelaEstatisticas = document.getElementById('tabelaEstatisticas');
    const totalPorMonitor = {};

    // Calcula a soma total para cada monitor
    dados.forEach(item => {
        if (!totalPorMonitor[item.monitor]) {
            totalPorMonitor[item.monitor] = 0;
        }
        totalPorMonitor[item.monitor] += item.quantidade;
    });

    let monitorAtual = '';

    // Preenche a tabela com os dados
    dados.forEach(item => {
        if (item.monitor !== monitorAtual) {
            if (monitorAtual !== '') {
                // Adiciona o total do monitor anterior
                tabelaEstatisticas.innerHTML += `<tr class="total-monitor">
                                                    <td>Total (${monitorAtual})</td>
                                                    <td></td>
                                                    <td>${totalPorMonitor[monitorAtual]}</td>
                                                </tr>`;
            }
            monitorAtual = item.monitor;
        }

        tabelaEstatisticas.innerHTML += `<tr>
                                            <td>${item.descricao}</td>
                                            <td>${item.monitor}</td>
                                            <td>${item.quantidade}</td>
                                         </tr>`;
    });

    // Adiciona o total para o último monitor
    if (monitorAtual !== '') {
        tabelaEstatisticas.innerHTML += `<tr class="total-monitor">
                                            <td>Total (${monitorAtual})</td>
                                            <td></td>
                                            <td>${totalPorMonitor[monitorAtual]}</td>
                                        </tr>`;
    }
}

