let dados; 
let ambientes;
let logs_ambientes;
let ambiente;
let steps = [];

var RACF = localStorage.getItem('RACF');
var SENHA = localStorage.getItem('SENHA');

function mostrarConteudo(funcionalidade) {
    const conteudo = document.getElementById('conteudo');
    const menuSuperior = document.getElementById('menu-superior');
    menuSuperior.style.display = 'none'; 
    conteudo.innerHTML = ''; 
    menuSuperior.innerHTML = ''; 

    if (funcionalidade === 'home') {
        conteudo.innerHTML = `
            <h2>Painel de Configuração do Sandbox Runner</h2>
            <p>
                A ferramenta Sandbox Runner foi desenvolvida pensando nas necessidades específicas de ambientes Mainframe. 
            </p>
            <p>    
                Você pode usar algumas das funcionalidades no menu lateral esquerdo para integir com a ferramenta em tempo de desenvolvimento.
            </p>
            <p>                
                Essa página foi criada para facilitar o processo de deploy
            </p>
        `;
    } else if (funcionalidade === 'upload') {
        conteudo.innerHTML = `
        <h2>Carregar Arquivo Temporário</h2>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <form id="uploadForm" enctype="multipart/form-data" method="post">
                        <div class="form-group">
                            <label for="pythonFile"><strong>Arquivo</strong> (.py, .html, .css, .js):</label>
                            <input type="file" class="form-control-file" name="pythonFile" id="pythonFile" accept=".py,.js,.css,.html"  required>
                        </div>
                        <div class="form-group">
                            <label for="targetDirectory"><strong>Pasta de Destino</strong></label>
                            <select name="targetDirectory" class="form-control" id="targetDirectory" required>
                                <option value="codes">codes</option>
                                <option value="front">front</option>
                                <option value="public">public</option>
                                <option value="public/js_pages">js_pages</option>
                                <option value="public/css">css</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Upload</button>
                    </form>
                </div>
            </div>
        </div>
        `;
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            fetch('/upload', {  // Certifique-se que esta é a rota correta
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        });
    } else if(funcionalidade === 'listarArquivos') {
        listarArquivos();
    } else if (funcionalidade === 'listarTabelas') {
        listarTabelas();
    } else if (funcionalidade === 'executarQuery') {
        conteudo.innerHTML = `
            <h2>Executar Query SQL</h2>
            <textarea id="sqlQuery" rows="4" class="form-control" placeholder="Escreva sua query SQL aqui..."></textarea>
            <button onclick="executarQuery()" class="btn btn-primary">Executar</button>
            <div id="queryResult" class="mt-3"></div>
        `;
    } else if (funcionalidade === 'executarPython') {
        conteudo.innerHTML = `
            <h2>Executar Código Python</h2>
            <input type="text" id="postRoute" class="form-control mb-2" placeholder="Digite a rota">
            <textarea id="jsonInput" class="form-control mb-2" rows="4" placeholder="Digite o JSON aqui..."></textarea>
            <button onclick="executarPython()" class="btn btn-primary">Executar</button>
            <div id="postResponse" class="mt-3"></div>
        `;
    }
}

function executarQuery() {
    const query = document.getElementById('sqlQuery').value;
    fetch('/get_logs', {
        method: 'GET',
        headers: { 
            'Content-Type': 'application/json',
            'SQL-Query': query
        }
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById('queryResult');
        resultElement.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    })
    .catch(error => {
        console.error('Erro ao executar query:', error);
        document.getElementById('queryResult').innerText = 'Erro ao executar query.';
    });
}

function executarPython() {
    const rota = document.getElementById('postRoute').value;
    const jsonInput = document.getElementById('jsonInput').value;

    try {
        const jsonData = JSON.parse(jsonInput);
        fetch(rota, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('postResponse').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            console.error('Erro ao enviar POST:', error);
            document.getElementById('postResponse').innerText = 'Erro ao enviar POST.';
        });
    } catch (e) {
        document.getElementById('postResponse').innerText = 'JSON inválido.';
    }
}

function Sair() {
    localStorage.clear();
    window.location.href = "home.html";
}
async function listarArquivos() {
    try {
        const response = await fetch('/list-files');
        const arquivos = await response.json();

        function construirEstrutura(dadosArquivos) {
            const raiz = {};
            dadosArquivos.forEach(({ path: caminho, lastModified }) => {
                // Normaliza o caminho do arquivo (substitui '\\' por '/')
                let caminhoNormalizado = caminho.replace(/\\/g, '/');
                
                let atual = raiz;
                caminhoNormalizado.split('/').forEach((parte, index, arr) => {
                    if (!atual[parte]) {
                        atual[parte] = index === arr.length - 1 ? { caminho: caminhoNormalizado, lastModified } : {};
                    }
                    atual = atual[parte];
                });
            });
            return raiz;
        }

        const estruturaArquivos = construirEstrutura(arquivos);
        document.getElementById('conteudo').innerHTML = gerarHtmlEstrutura(estruturaArquivos);
    } catch (error) {
        console.error('Erro ao listar arquivos:', error);
        document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao listar os arquivos.</p>';
    }
}

function gerarHtmlEstrutura(estrutura, nivel = 0) {
    let html = '        <h2>Estrutura de Arquivos</h2><ul class="list-group" style="padding-left:' + (nivel * 20) + 'px">';
    for (const nome in estrutura) {
        if (typeof estrutura[nome] === 'object' && !estrutura[nome].caminho) {
            const idSublista = 'sublista-' + Math.random().toString(36).substr(2, 9);
            html += `<li class="list-group-item list-group-item-primary" onclick="toggleSublista('${idSublista}')"><i class="fa fa-folder"></i> ${nome}</li>`;
            html += `<ul id="${idSublista}" class="list-group pl-3 collapse">` + gerarHtmlEstrutura(estrutura[nome], nivel + 1) + '</ul>';
        } else {
            html += `<li class="list-group-item"><strong>${nome}</strong> <i> - última modificação:  ${estrutura[nome].lastModified} </i> </li>`;
        }
    }
    html += '</ul>';
    return html;
}


function toggleSublista(id) {
    const sublista = document.getElementById(id);
    if (sublista) {
        sublista.classList.toggle('collapse');
        const icone = sublista.previousElementSibling.querySelector('i');
        if (icone.classList.contains('fa-folder')) {
            icone.classList.remove('fa-folder');
            icone.classList.add('fa-folder-open');
        } else {
            icone.classList.remove('fa-folder-open');
            icone.classList.add('fa-folder');
        }
    }
}

async function listarTabelas() {
    try {
        const response = await fetch('/list-tables');
        const tabelas = await response.json();

        let html = '<h2>Tabelas existentes na base</h2>';
        let tabelaAtual = '';
        tabelas.forEach(({ TABLE_NAME, COLUMN_NAME }) => {
            if (tabelaAtual !== TABLE_NAME) {
                if (tabelaAtual !== '') {
                    html += '</ul>';
                    html +='<br>'
                }
                html += `<h3><i class="fas fa-table"></i> ${TABLE_NAME}</h3><ul class="list-group">`;
                tabelaAtual = TABLE_NAME;
            }
            
            html += `<li class="list-group-item"><i class="fas fa-key"></i> ${COLUMN_NAME}</li>`;
        });

        if (tabelaAtual !== '') {
            html += '</ul>';
        }

        document.getElementById('conteudo').innerHTML = html;
    } catch (error) {
        console.error('Erro ao listar tabelas:', error);
        document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao listar as tabelas.</p>';
    }
}

// Ao carregar a página, mostre a home
window.onload = function() {
    mostrarConteudo('home');
}