document.addEventListener('DOMContentLoaded', function() {
    loadNavbar();
    loadFooter();
    initializeGrid();
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
function initializeGrid() {
    // Substitua new agGrid.Grid(...) por agGrid.createGrid(...)
    const gridDiv = document.getElementById('myGrid');
    const gridApi = agGrid.createGrid(gridDiv, gridOptions);
}

function onGridReady(params) {
    fetch('/codes/terminais_consulta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            // Adicione aqui outros cabeçalhos necessários
        },
        body: JSON.stringify({
             chave: 'valor'
        })
    })
    .then(response => response.json())
    .then(data => {
        const columnDefs = Object.keys(data[0]).map(key => {
            return { field: key, sortable: true, filter: true };
        });

        params.api.setColumnDefs(columnDefs);
        params.api.setRowData(data);
    });
}

const gridOptions = {
    defaultColDef: {
        flex: 1,
        minWidth: 100,
        resizable: true,
    },
    columnDefs: [],
    pagination: true,
    paginationPageSize: 1000,
    paginationPageSizeSelector: [500, 1000, 2000, 5000, 10000],
    onGridReady: onGridReady,
};