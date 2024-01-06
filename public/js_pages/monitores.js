let monitoresData = [];

document.addEventListener('DOMContentLoaded', function() {
    criarNavbar();
    fetchMonitores();

    document.getElementById('filterName').addEventListener('input', filterMonitores);
    document.getElementById('filterParticao').addEventListener('change', filterMonitores);
    document.getElementById('filterAmbiente').addEventListener('change', filterMonitores);
});

function fetchMonitores() {
    // Definindo as opções da solicitação POST
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ /* dados que você quer enviar, se necessário */ })
    };

    fetch('/front/monitores_ativos', requestOptions)
        .then(response => response.json())
        .then(data => {
            monitoresData = ordenarMonitores(data);
            displayMonitores(data);
        })
        .catch(error => console.error('Erro ao buscar monitores:', error));
}

function ordenarMonitores(data) {
    return data.sort((a, b) => {
        if (a.status === b.status) {
            return a.monitor.localeCompare(b.monitor); // Ordenar alfabeticamente por nome se os status forem iguais
        }
        return a.status === 'Ativo' ? 1 : -1; // Colocar inativos primeiro
    });
}

function displayMonitores(data) {
    const container = document.getElementById('cardsContainer');
    container.innerHTML = '';

    data.forEach(monitor => {
        const card = document.createElement('div');
        card.className = `card ${monitor.status === 'Ativo' ? 'ativo' : 'inativo'}`;
        card.innerHTML = `
            <div class="card-header">
                <div class="card-title-overlay">${monitor.monitor}</div>
            </div>
            <div class="card-content">
                <p><i class="fas fa-briefcase"></i> Job Name: ${monitor.jobname}</p>
                <div class="info-row">
                    <p><i class="fas fa-server"></i> Partição: ${monitor.particao}</p>
                    <p><i class="fas fa-network-wired"></i> Ambiente: ${monitor.ambiente}</p>
                </div>
                <p><i class="${monitor.status === 'Ativo' ? 'fas fa-check-circle' : 'fas fa-times-circle'}"></i> Status: ${monitor.status}</p>
            </div>
        `;
        container.appendChild(card);
    });
}

function filterMonitores() {
    const filterName = document.getElementById('filterName').value.toLowerCase();
    const filterParticao = document.getElementById('filterParticao').value;
    const filterAmbiente = document.getElementById('filterAmbiente').value;

    const filteredData = monitoresData.filter(monitor => {
        return (monitor.monitor.toLowerCase().includes(filterName) || filterName === '') &&
               (monitor.particao === filterParticao || filterParticao === '') &&
               (monitor.ambiente === filterAmbiente || filterAmbiente === '');
    });

    displayMonitores(filteredData);
}
