let ambiente;
let editor;
let editor2;

function mostrarConteudo(funcionalidade) {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = ''; 
    validarAcesso(() => {
            // O código aqui será executado após a validação e o atraso de 500ms
            // Por exemplo: carregar o conteúdo da funcionalidade
            if (funcionalidade === 'home') {
                conteudo.innerHTML = `
                    <div class="conteudo">
                        <h2>Bem vindo ao CODERUNNER !! </h2>
                    <div>
                    <div class="conteudo">
                        <p>
                        A plataforma CodeRunner foi meticulosamente desenvolvida para atender às necessidades específicas dos ambientes Mainframe. Com um forte enfoque na utilização do Python, a plataforma permite a automatização eficiente de processos, análise aprofundada de dados, descoberta de insights e a implementação de iniciativas modernas no campo da programação.
                        </p>
                        <p>    
                            Nossa interface intuitiva, acessível através do menu lateral esquerdo, facilita a interação com diversas funcionalidades essenciais durante o ciclo de desenvolvimento. Estas incluem a visualização e o gerenciamento de arquivos, a execução de queries SQL, a análise de estruturas de tabelas de banco de dados, e a execução de scripts Python diretamente na plataforma.
                        </p>
                        <p>                
                            Esta página foi especialmente projetada para otimizar o processo de deploy. Com a funcionalidade de upload, você pode facilmente carregar seus códigos e executá-los em um ambiente seguro e controlado. A plataforma também suporta a visualização e a análise detalhada de logs, proporcionando uma visão clara do desempenho e do resultado de suas execuções.
                        </p>
                        <p>
                            Além disso, a CodeRunner oferece uma estrutura organizada para a visualização da hierarquia de arquivos, melhorando significativamente a experiência do usuário ao navegar e gerenciar arquivos de diferentes formatos, como Python, HTML, CSS e JavaScript.
                        </p>
                        <p>
                            Com a CodeRunner, seu fluxo de trabalho de desenvolvimento se torna mais eficiente, transparente e adaptável às rápidas mudanças e desafios do mundo da programação moderna. Seja para implementar pequenas automações ou para gerenciar grandes conjuntos de dados, a CodeRunner está aqui para ajudá-lo a alcançar seus objetivos com maior rapidez e eficácia.
                        </p>
                        <h2>Funcionalidades Principais</h2>
                        <p>
                            O CodeRunner é equipado com várias funcionalidades poderosas, projetadas para facilitar o desenvolvimento, teste e deploy de scripts Python em ambientes Mainframe:
                        </p>
                        <ul>
                            <li><strong>Execução de Scripts Python:</strong> Permite a execução de scripts Python de forma eficiente, com suporte para execução simultânea de múltiplos scripts.</li>
                            <li><strong>Upload de Arquivos:</strong> Funcionalidade para carregar arquivos temporários, suportando diversos formatos como .py, .html, .css e .js.</li>
                            <li><strong>Listagem de Arquivos e Tabelas:</strong> Fornece uma visualização clara dos arquivos e tabelas disponíveis no sistema, facilitando a gestão e o acesso a recursos importantes.</li>
                            <li><strong>Execução de Queries SQL:</strong> Permite a execução de queries SQL diretamente na interface, com uma visualização clara dos resultados.</li>
                            <li><strong>Integração com Bancos de Dados:</strong> Configuração simplificada para conexão com bancos de dados MySQL, permitindo operações diretas de consulta e manipulação.</li>
                        </ul>
                        <h2>Explicação da Rota Principal do CodeRunner</h2>
                        <p>
                            A rota principal do CodeRunner é designada para a execução de scripts Python. Esta rota é essencial para a funcionalidade principal da plataforma, permitindo aos usuários executar código Python de forma eficiente e controlada.
                        </p>
                        
                        <h2>Processamento da Requisição</h2>
                        <ul>
                            <li>
                                <strong>Recebimento do Script:</strong> A rota recebe o nome do script Python como parte do caminho da URL (por exemplo, <code>/codes/:scriptName</code>). O script correspondente deve estar localizado na pasta 'codes'.
                            </li>
                            <li>
                                <strong>Verificação de Existência:</strong> Antes de executar o script, a rota verifica se o arquivo especificado existe no diretório.
                            </li>
                            <li>
                                <strong>Tratamento de Erros:</strong> Se o arquivo não for encontrado, a rota retorna um erro 404, indicando que o código não foi encontrado.
                            </li>
                        </ul>
                    
                        <h2>Execução do Python</h2>
                        <ul>
                            <li>
                                <strong>Configuração da Execução:</strong> A rota configura as opções de execução do script, como a saída em tempo real e a passagem dos dados do formulário como argumentos para o script.
                            </li>
                            <li>
                                <strong>Execução Simultânea:</strong> É possível executar múltiplos scripts simultaneamente, com a rota lendo o número desejado de execuções simultâneas do cabeçalho 'num-scripts'. Existe um limite de 100 scripts simultâneos para evitar sobrecarga.
                            </li>
                        </ul>
                    
                        <h2>Processamento e Resposta</h2>
                        <ul>
                            <li>
                                <strong>Monitoramento da Execução:</strong> A rota monitora a execução do script e captura a saída, esperando que seja um JSON válido. Se não for, um erro é registrado.
                            </li>
                            <li>
                                <strong>Finalização e Resposta:</strong> Após a execução do script, a rota finaliza o processo e retorna a saída. Em caso de erro, um log detalhado é fornecido.
                            </li>
                            <li>
                                <strong>Gerenciamento de Recursos:</strong> A rota assegura que os recursos sejam liberados após a execução, mantendo a eficiência e estabilidade do sistema.
                            </li>
                        </ul>
                        <h2>Estrutura do código Python</h2>
                        <p>
                            Ao utilizar o CodeRunner para transformar seu código Python em uma API, você receberá um objeto JSON no formato de texto. Este texto deve ser capturado através da função <code>sys.argv</code> do Python. Após receber o objeto JSON, você pode convertê-lo em um objeto Python utilizando a função <code>json.loads</code>. O processamento deste objeto pode então ser realizado conforme necessário, e a resposta final pode ser devolvida para o CodeRunner no formato JSON, usando a função <code>json.dumps</code>.
                        </p>

                        <p>Veja um exemplo de como seu código Python pode ser estruturado:</p>

                        <pre>
                        <code>
                        import sys
                        import json

                        def main():
                            # Recebendo o objeto JSON do CodeRunner
                            body = sys.argv[1]
                            data = json.loads(body)

                            # Processamento para montar o objeto de resposta JSON
                            jsonresposta = {
                                "retorno": "Exemplo de retorno",
                            }

                            # Devolvendo resposta para o CodeRunner
                            print(json.dumps(jsonresposta))

                        main()
                        </code>
                        </pre>
                        <p>
                            Neste exemplo, a função <code>main</code> inicia recebendo o objeto JSON como texto através de <code>sys.argv[1]</code>. Em seguida, o texto é convertido em um objeto Python com <code>json.loads</code>. Após o processamento necessário, um novo objeto JSON é montado e enviado de volta para o CodeRunner utilizando <code>json.dumps</code> para convertê-lo novamente em texto.
                        </p>
                        <h2>Relizando uma chamada de API</h2>
                        <p>
                    Agora você pode chamar seu código através de um API.
                        </p>

                        <p>Veja um exemplo de chamada em Javascript:</p>

                        <pre>
                        <code>
                        const url = /codes/nomeDoSeuScript;

                        // Substitua este objeto pelos dados que você quer enviar para o seu script Python
                        const dataToSend = {
                            key1: 'value1',
                            key2: 'value2'
                        };

                        fetch(url, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(dataToSend)
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Resposta do Script:', data);
                            // Manipule a resposta aqui
                        })
                        .catch(error => console.error('Erro ao executar o script:', error));
                        });

                        </code>
                        </pre>
                        <p>
                            Muito obrigado por estar usando nossa plataforma !!!!!!!!!
                        </p>
                        <div>
                `;
            } else if (funcionalidade === 'upload') {
                conteudo.innerHTML = `
                <div class="conteudo">
                    <h2>Carregar Arquivo Temporário</h2>
                <div>
                <div class="conteudo">
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
                                            <option value="codes/regressivo">regressivo</option>
                                            <option value="version">version</option>
                                            <option value="api">api</option>
                                            <option value="front">front</option>
                                            <option value="public">public</option>
                                            <option value="public/js_pages">js_pages</option>
                                            <option value="public/css">css</option>
                                            <option value="public/css/icons">icons</option>
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
                <div class="conteudo">
                    <h2>Executar Query SQL</h2>
                </div>
                <div class="conteudo">
                    <textarea id="sqlQuery" rows="4" class="form-control" placeholder="Escreva sua query SQL aqui..."></textarea>
                    <button onclick="executarQuery()" class="btn btn-primary">Executar</button>
                    <div id="queryResult" class="mt-3"></div>
                    <div class="conteudo">
                    <h2> Resposta da consulta </h2>
                        <div id="jsonOutput2" class="json-editor"></div> <!-- Contêiner para o jsoneditor -->
                    </div>
                </div>
                `;
            } else if (funcionalidade === 'executarPython') {
                conteudo.innerHTML = `
                <div class="conteudo">
                    <h2>Executar Código Python</h2>
                </div>
                <div class="conteudo">
                    <input type="text" id="postRoute" class="form-control mb-2" placeholder="Digite a rota">
                    <textarea id="jsonInput" class="form-control mb-2" rows="4" placeholder="Digite o JSON aqui..."></textarea>
                    <button onclick="executarPython()" class="btn btn-primary">Executar</button>

                    <div class="conteudo">
                        <h2> Resposta do Python </h2>
                        <div id="jsonOutput" class="json-editor"></div> <!-- Contêiner para o jsoneditor -->
                    </div>
                </div>
                `;
            } else if (funcionalidade === 'usoMemoria') {
                mostrarUsoDeMemoria();
            } else if (funcionalidade === 'processosPython') {
                mostrarProcessosPython();
            } else if (funcionalidade === 'mostrarLogs') {
            mostrarLogs();
            }

    });
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
            // Cria ou atualiza o jsoneditor com a resposta
            const container = document.getElementById("jsonOutput2");
            if (!editor2) {
                editor2 = new JSONEditor(container, {});
            }
            editor2.set(data);
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
            // Cria ou atualiza o jsoneditor com a resposta
            const container = document.getElementById("jsonOutput");
            if (!editor) {
                editor = new JSONEditor(container, {});
            }
            editor.set(data);
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
        document.getElementById('conteudo').innerHTML = '<div class="conteudo"><h2>Estrutura de Arquivos</h2></div>' + gerarHtmlEstrutura(estruturaArquivos);
    } catch (error) {
        console.error('Erro ao listar arquivos:', error);
        document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao listar os arquivos.</p>';
    }
}

function gerarHtmlEstrutura(estrutura, nivel = 0) {
    let html = '<div class="conteudo"><ul class="list-group" style="padding-left:' + (nivel * 20) + 'px">';
    for (const nome in estrutura) {
        if (typeof estrutura[nome] === 'object' && !estrutura[nome].caminho) {
            const idSublista = 'sublista-' + Math.random().toString(36).substr(2, 9);
            html += `<li class="list-group-item list-group-item-primary" onclick="toggleSublista('${idSublista}')"><i class="fa fa-folder"></i> ${nome}</li>`;
            html += `<ul id="${idSublista}" class="list-group pl-3 collapse">` + gerarHtmlEstrutura(estrutura[nome], nivel + 1) + '</ul>';
        } else {
            html += `<li class="list-group-item"><strong>${nome}</strong> <i> - última modificação:  ${estrutura[nome].lastModified} </i> </li>`;
        }
    }
    html += '</ul></div>';
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

        let html = '<div class="conteudo"><h2>Tabelas existentes na base</h2></div><div class="conteudo">';
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
            html += '</ul></div>';
        }

        document.getElementById('conteudo').innerHTML = html;
    } catch (error) {
        console.error('Erro ao listar tabelas:', error);
        document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao listar as tabelas.</p>';
    }
}

function mostrarUsoDeMemoria() {
    fetch('/monitor-memory')
        .then(response => response.json())
        .then(data => {
            const conteudo = document.getElementById('conteudo');
            conteudo.innerHTML = `
                <div class="conteudo">
                    <h2>Uso da Memória do Sistema</h2>
                </div>
                
                <div class="conteudo">
                    <div class="memory-info">
                        <h3>Memória do Sistema:</h3>
                        <p><strong>Total:</strong> ${data.systemMemoryInfo.totalMemory} - A quantidade total de memória RAM disponível no sistema.</p>
                        <p><strong>Livre:</strong> ${data.systemMemoryInfo.freeMemory} - Memória RAM não utilizada e disponível para novos processos.</p>
                        <p><strong>Usada:</strong> ${data.systemMemoryInfo.usedMemory} - Memória RAM sendo usada por todos os processos do sistema.</p>
                        <p><strong>Disponível:</strong> ${data.systemMemoryInfo.availableMemory} - Memória RAM disponível para novos processos, incluindo a memória em uso que pode ser liberada.</p>
                        <p><strong>Percentual Livre:</strong> ${data.systemMemoryInfo.freeMemoryPercentage} - Porcentagem da memória total que está livre e disponível para uso.</p>
                        <br>
                        <h3>Memória do Processo:</h3>
                        <p><strong>Heap Total:</strong> ${data.processMemoryInfo.heapTotal} - Total de memória alocada para o heap do Node.js.</p>
                        <p><strong>Heap Usado:</strong> ${data.processMemoryInfo.heapUsed} - Memória do heap ativamente usada pelo aplicativo.</p>
                        <p><strong>Memória Externa:</strong> ${data.processMemoryInfo.externalMemory} - Memória usada por objetos externos ao motor JavaScript V8.</p>
                        <p><strong>RSS (Resident Set Size):</strong> ${data.processMemoryInfo.rss} - Total de memória que o processo ocupa na RAM.</p>
                        <p><strong>Uso de Memória:</strong> ${data.processMemoryInfo.memoryUsagePercentage} - Porcentagem da memória total do sistema usada pelo processo do Node.js.</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Erro ao obter dados de uso de memória:', error);
            document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao obter dados de uso de memória.</p>';
        });
}

function mostrarProcessosPython() {
    fetch('/python-processes')
        .then(response => response.json())
        .then(processos => {
            const conteudo = document.getElementById('conteudo');
            let html = '<div class="conteudo"><h2>Processos Python em Execução</h2>';


            let memoriaTotal = 0;

            if (processos.length === 0) {
                html += '<div class="conteudo"><p>Nenhum processo Python em execução no momento.</p></div>';
            } else {
                html += '<div class="conteudo"><ul>';
                processos.forEach(processo => {
                    html += `<li><div><strong>PID:</strong> ${processo.pid} - <strong>Comando:</strong> ${processo.cmd} - <strong>Memória:</strong> ${processo.memoryUsage} KB </div><button onclick="encerrarProcesso(${processo.pid})">Encerrar</button></li>`;
                    memoriaTotal += processo.memoryUsage;
                });
                html += '</ul>';
                html += `<p><strong>Processos Python em Execução:</strong> ${processos.length}</p>`;
                html += `<p><strong>Memória Total Usada:</strong> ${memoriaTotal} KB</p></div>`;
            }


            conteudo.innerHTML = html;
        })
        .catch(error => {
            console.error('Erro ao buscar processos Python:', error);
            document.getElementById('conteudo').innerHTML = '<p>Ocorreu um erro ao buscar processos Python.</p>';
        });
}
function mostrarLogs() {
    const numLogs = 10; // Defina o número de logs que deseja buscar
    fetch(`/logger?numLogs=${numLogs}`)
    .then(response => response.json())
    .then(logs => {
        const conteudo = document.getElementById('conteudo');
        // Limpa o conteúdo antes de adicionar novos logs
        conteudo.innerHTML = '<div class="conteudo"><h2>Últimas LOGS de execução</h2></div>';

        logs.forEach(log => {
            const logContainer = document.createElement('div');
            logContainer.className = 'log-card';
            conteudo.appendChild(logContainer);
            const options = {
                mode: 'view',
                search: false,
            };

            // Verifique se o log.body é uma string e tente parseá-la
            if (typeof log.body === 'string') {
                try {
                    log.body = JSON.parse(log.body);
                } catch (e) {
                    // Se ocorrer um erro no parse, mantenha como string
                    // Isso pode acontecer se o body não for um JSON válido
                }
            }

            // Se log for uma string de JSON escapada, parseie para um objeto JavaScript
            if (typeof log === 'string') {
                try {
                    log = JSON.parse(log);
                } catch (e) {
                    // Se não for um JSON válido, imprima o erro no console
                    console.error('Erro ao parsear log:', e);
                }
            }

            // Inicialize o JSONEditor com o log parseado ou string original
            const editor = new JSONEditor(logContainer, options);
            editor.set(log);
        });
    })
    .catch(error => {
        console.error('Erro ao buscar logs:', error);
    });
}

function encerrarProcesso(pid) {
    fetch(`/python-process/${pid}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        mostrarProcessosPython(); // Atualizar a lista após encerrar um processo
    })
    .catch(error => {
        alert(error.message);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    window.onload = function() {
        criarNavbar();
        mostrarConteudo('home');
    }
});

function validarAcesso(callback) {
    var token = localStorage.getItem('token');
    if (!token) {
        alert('Token não encontrado. Redirecionando para a página inicial.');
        window.location.href = '/page/home';
        return;
    }

    fetch('/front/valida_opa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: token, path:'/page/admin.html' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 200 && data.resultado) {
            console.log('Acesso validado.');
            setTimeout(callback, 50); // Aguarda 500ms e depois executa o callback
        } else {
            alert('Acesso negado ou token expirou.');
            window.location.href = '/page/home';
        }
    })
    .catch(error => {
        console.error('Erro ao validar o acesso:', error);
        alert('Ocorreu um erro ao validar o acesso.');
        window.location.href = '/page/home';
    });
}
