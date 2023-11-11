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
        <div class="container">
            <div class="row">
                <div class="col-md-6 offset-md-3">
                    <form id="uploadForm" enctype="multipart/form-data" method="post">
                        <div class="form-group">
                            <label for="pythonFile">Arquivo (Python, html, css, javaScipt):</label>
                            <input type="file" class="form-control-file" name="pythonFile" id="pythonFile" accept=".py" required>
                        </div>
                        <div class="form-group">
                            <label for="targetDirectory">Pasta de Destino:</label>
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
    }
}


async function get() {
    let query = 'SELECT * FROM ambientes';
    
    const response = await fetch('/get_logs', {
        headers: {
        'Content-Type': 'application/json',
        'SQL-Query': query
        }
    });
    const ambientes = await response.json();
    return ambientes;
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
    let html = '<ul class="list-group" style="padding-left:' + (nivel * 20) + 'px">';
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

// Ao carregar a página, mostre a home
window.onload = function() {
    mostrarConteudo('home');
}