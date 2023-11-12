let dados; 
let ambientes;
let logs_ambientes;
let ambiente;
let steps = [];

var RACF = localStorage.getItem('RACF');
var SENHA = localStorage.getItem('SENHA');

if (!RACF || !SENHA) {
    window.location.href = "home.html";
}

function mostrarConteudo(funcionalidade) {
    const conteudo = document.getElementById('conteudo');
    const menuSuperior = document.getElementById('menu-superior');
    menuSuperior.style.display = 'none'; 
    conteudo.innerHTML = ''; 
    menuSuperior.innerHTML = ''; 

    if (funcionalidade === 'home') {
        conteudo.innerHTML = `
            <h2>Agradecemos por sua visita ao Sandbox Runner!!!</h2>
            <p>
                A ferramenta Sandbox Runner foi desenvolvida pensando nas necessidades específicas de ambientes Mainframe. 
            </p>
            <p>    
                Ela permite virtualizar e criar ambientes de teste de aplicação mainframe de forma isolada. 
            </p>
            <p>                
                Com essa ferramenta, cada usuário tem a capacidade de criar sua própria pista de teste sem impactar os outros usuários. 
            </p>
            <p>   
                É uma solução ideal para equipes que buscam otimizar seus processos de teste, garantindo integridade e eficiência.
            </p>
            <p>
                É importante salientar que ainda estamos em fase de desenvolvimento e melhorias contínuas. 
            </p>
            <p>
                Criar um processo sofisticado que permita configurações personalizadas, além de oferecer recursos para a reciclagem de arquivos, tabelas e módulos de programas. 
            </p>
            <p>
                O objetivo principal é capacitar nossos usuários a executar tarefas de forma paralela, otimizando fluxos de trabalho e maximizando a eficiência. 
            </p>
            <p>
                Pedimos sua paciência e compreensão durante este período, e incentivamos o feedback construtivo para aprimorarmos ainda mais a nossa plataforma.
            </p>
        `;
    } else if (funcionalidade === 'criarambiente') {
        menuSuperior.style.display = 'flex'; 
        menuSuperior.innerHTML = `
            <a href="#" onclick="ListarOpcoesAmbiente('CICS')">CICS</a>
            <a href="#" onclick="ListarOpcoesAmbiente('GRBE')">GRBE</a>
            <a href="#" onclick="ListarOpcoesAmbiente('IMS')">IMS</a>
            <a href="#" onclick="ListarOpcoesAmbiente('BATCH')">BATCH</a>
        `;
        conteudo.innerHTML = `
            <div id="criaForm">
                <label for="nome">NOME</label>
                <input type="text" id="nome" name="nome"><br>
                <label for="configuracao">CONFIGURAÇÃO</label>
                <input type="text" id="configuracao" name="configuracao"><br>
                <label for="versao">VERSÃO</label>
                <input type="number" id="versao" name="versao"><br>
            </div>
            <div id="formulario"></div>
            <button onclick="criarambiente()">CRIAR AMBIENTE</button>
        `;
    } else if (funcionalidade === 'ambientes') {
        menuSuperior.style.display = 'flex'; 
        menuSuperior.innerHTML = `
            <a href="#" onclick="PrepararAmbiente()">PREPARAR</a>
            <a href="#" onclick="DestruirAmbiente()">DESTRUIR</a>
            <a href="#" onclick="ConsultarAmbiente()">CONSULTAR</a>
            <a href="#" onclick="DeletarAmbiente()">DELETAR</a>
        `;
        carregarAmbientes();
    } else if (funcionalidade === 'LogsDeAmbiente') {
        carregarLogsDeAmbientes();
    } else if (funcionalidade === 'configuracaoManual') {
        conteudo.innerHTML = '';
        conteudo.innerHTML = `
        <div id="configForm">
            <label>Escolha uma ação: 
                <select id="actionSelect" onchange="showActionFields()">
                    <option value="create">Create</option>
                    <option value="copy">Copy</option>
                </select>
            </label>
            <div id="actionFields"></div>
            <button onclick="adicionarStep()">ADICIONAR STEP</button>
        </div>
    `;
        for (const chave in steps) {
            conteudo.innerHTML += `
                <div>
                    <input type="checkbox" id="${chave}" onchange="toggleOpcoes('${chave}')">
                    <label for="${chave}">${chave}</label>
                    <div id="opcoes-${chave}" style="display: none;">
                        ${dados[chave].map(opcao => `<label><input type="checkbox" value="${opcao}" onchange="atualizarVisualizacaoJSON()">${opcao}</label>`).join('')}
                    </div>
                </div>
            `;
        }
        conteudo.innerHTML += `
        <div class="json-container">
            <pre id="visualizacaoJSON"></pre>
            <button onclick="gerarJSONFinal()">RODAR CONFIGURAÇÕES</button>
        </div>
    `;
        atualizarVisualizacaoJSON(); // Adicione esta linha
    }
}

async function ListarOpcoesAmbiente(opcao) {
    if (opcao === 'CICS'){
        ambiente = 'CICS';
        dados = await listar_cics();
    }
    else if (opcao === 'GRBE') {
        ambiente = 'GRBE';
        dados = await listar_grbe();
    }
    else if (opcao === 'IMS') {
        ambiente = 'IMS';
        dados = await listar_ims();
    }
    else if (opcao === 'BATCH') {
        ambiente = 'BATCH';
        dados = await listar_batch();
    }
    inicializarFormulario(dados);
}

async function listar_cics() {    
    const response = await fetch('/codes/ambiente_cics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({usuario: RACF, senha: SENHA})
    });
    const lista_json = await response.json();
    return lista_json;
}
async function listar_grbe() {
    const response = await fetch('/codes/ambiente_grbe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({usuario: RACF, senha: SENHA})
        });
        const lista_json = await response.json();
        return lista_json;
}
async function listar_ims(){
    const response = await fetch('/codes/ambiente_ims', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({usuario: RACF, senha: SENHA})
        });
        const lista_json = await response.json();
        return lista_json;
}

async function listar_batch(){
    const response = await fetch('/codes/ambiente_batch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({usuario: RACF, senha: SENHA})
        });
        const lista_json = await response.json();
        return lista_json;
}

function inicializarFormulario(dados) {
    const formulario = document.getElementById('formulario');
    formulario.innerHTML = ''; // Limpa o conteúdo anterior

    for (const chave in dados) {
        // Criação da seção da chave
        const divChave = document.createElement('div');
        divChave.className = 'chave';

        // Checkbox para a chave
        const checkboxChave = document.createElement('input');
        checkboxChave.type = 'checkbox';
        checkboxChave.id = chave;
        checkboxChave.onchange = () => toggleOpcoes(chave);

        // Label para a chave
        const labelChave = document.createElement('label');
        labelChave.htmlFor = chave;
        labelChave.textContent = chave;

        // Adiciona o checkbox e label da chave ao div
        divChave.appendChild(checkboxChave);
        divChave.appendChild(labelChave);

        // Campo de filtro para cada chave
        const filtroInput = document.createElement('input');
        filtroInput.type = 'text';
        filtroInput.placeholder = 'Filtrar...';
        // Dentro de inicializarFormulario, ao criar o filtroInput
        filtroInput.className = `filtro-input filtro-${chave}`; // Adiciona as classes ao campo de filtro
        filtroInput.onkeypress = (e) => {
            if (e.key === 'Enter') {
                filtrarOpcoes(chave, filtroInput.value);
            }
        };

        // Adiciona o campo de filtro ao div da chave
        divChave.appendChild(filtroInput);

        // Div para as opções da chave
        const divOpcoes = document.createElement('div');
        divOpcoes.id = 'opcoes-' + chave;
        divOpcoes.className = 'opcoes';
        divOpcoes.style.display = 'none'; // Inicialmente oculto
        divOpcoes.style.marginLeft = '20px';

        // Adiciona as opções
        dados[chave].forEach(opcao => {
            const checkboxOpcao = document.createElement('input');
            checkboxOpcao.type = 'checkbox';
            checkboxOpcao.id = opcao + '-' + chave;
            checkboxOpcao.value = opcao;

            const labelOpcao = document.createElement('label');
            labelOpcao.htmlFor = opcao + '-' + chave;
            labelOpcao.textContent = opcao;

            const divOpcao = document.createElement('div');
            divOpcao.appendChild(checkboxOpcao);
            divOpcao.appendChild(labelOpcao);

            divOpcoes.appendChild(divOpcao);
        });

        // Adiciona o div da chave e das opções ao formulário
        formulario.appendChild(divChave);
        formulario.appendChild(divOpcoes);
    }
}

function toggleOpcoes(chave) {
    const divOpcoes = document.getElementById('opcoes-' + chave);
    const checkboxChave = document.getElementById(chave);
    const filtroInput = document.querySelector(`.filtro-${chave}`);

    // Verifica se o filtroInput existe antes de tentar acessar seu valor
    const filtro = filtroInput ? filtroInput.value : '';

    if (checkboxChave.checked) {
        // Se a chave está marcada e há algo no filtro, mostra as opções
        if (filtro !== '') {
            divOpcoes.style.display = '';
            filtrarOpcoes(chave, filtro); // Aplica a filtragem atual
        } else {
            // Se não houver filtro, mantém as opções ocultas
            divOpcoes.style.display = 'none';
        }
    } else {
        // Se a chave está desmarcada, esconde as opções e desmarca todas
        divOpcoes.style.display = 'none';
        desmarcarTodasOpcoes(chave);
    }
}

function desmarcarTodasOpcoes(chave) {
    const divOpcoes = document.getElementById('opcoes-' + chave);
    const checkboxesOpcoes = divOpcoes.querySelectorAll('input[type=checkbox]');

    checkboxesOpcoes.forEach(checkbox => {
        checkbox.checked = false;
    });
}


function filtrarOpcoes(chave, filtro) {
    const divOpcoes = document.getElementById('opcoes-' + chave);
    const opcoes = divOpcoes.querySelectorAll('div');

    let deveExibirTodas = filtro === '*';

    opcoes.forEach(div => {
        if (deveExibirTodas) {
            // Se o filtro for *, exibe todas as opções
            div.style.display = '';
        } else {
            // Caso contrário, aplica a lógica de filtragem normal
            const opcao = div.querySelector('input').value;
            if (opcao.toLowerCase().includes(filtro.toLowerCase())) {
                div.style.display = '';
            } else {
                div.style.display = 'none';
            }
        }
    });

    divOpcoes.style.display = deveExibirTodas || filtro !== '' ? '' : 'none';
}


function criarambiente() {
    const resultado = {};

    for (const chave in dados) {
        const checkboxChave = document.getElementById(chave);
        const divOpcoes = document.getElementById('opcoes-' + chave);
        if (checkboxChave.checked) {
            const selecionados = Array.from(divOpcoes.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
            if (selecionados.length > 0) {
                resultado[chave] = selecionados;
            }
        }
    }
    criar(resultado);
}

function showActionFields() {
    const action = document.getElementById('actionSelect').value;
    const actionFieldsDiv = document.getElementById('actionFields');
    actionFieldsDiv.innerHTML = '';

    if (action === 'create') {
        actionFieldsDiv.innerHTML = `
            To: <input type="text" id="toField"><br>
            Volser: <input type="text" id="volserField"><br>
            CNPJ: <input type="text" id="cnpjField"><br>
            Unit: <input type="text" id="unitField"><br>
            <!-- Adicione os demais campos aqui conforme especificado -->
        `;
    } else if (action === 'copy') {
        actionFieldsDiv.innerHTML = `
            From: <input type="text" id="fromField" value="aaaaa"><br>
            Member: <input type="text" id="memberField" value="aaaaa"><br>
            To: <input type="text" id="toCopyField" value="aaaaa"><br>
        `;
    }
}

function adicionarStep() {
    const action = document.getElementById('actionSelect').value;

    if (!validarFormulario(action)) {
        // Se a validação falhar, interrompemos a execução da função aqui
        return;
    }

    let step = {
        action: action
    };

    if (action === 'create') {
        step.to = document.getElementById('toField').value;
        step.config = {
            volser: document.getElementById('volserField').value,
            cnpj: document.getElementById('cnpjField').value,
            unit: document.getElementById('unitField').value
            // Adicione os demais campos aqui
        };
    } else if (action === 'copy') {
        step.from = document.getElementById('fromField').value;
        step.member = document.getElementById('memberField').value;
        step.to = document.getElementById('toCopyField').value;
    }

    steps.push(step);
    atualizarVisualizacaoJSON();
}

function validarFormulario(action) {
    if (action === 'create') {
        if (!document.getElementById('toField').value.trim() ||
            !document.getElementById('volserField').value.trim() ||
            !document.getElementById('cnpjField').value.trim() ||
            !document.getElementById('unitField').value.trim()) {
            // Há um campo vazio
            alert('Por favor, preencha todos os campos necessários.');
            return false;
        }
    } else if (action === 'copy') {
        if (!document.getElementById('fromField').value.trim() ||
            !document.getElementById('memberField').value.trim() ||
            !document.getElementById('toCopyField').value.trim()) {
            // Há um campo vazio
            alert('Por favor, preencha todos os campos necessários.');
            return false;
        }
    }
    return true;
}

function atualizarVisualizacaoJSON() {
    const visualizacaoJSON = document.getElementById('visualizacaoJSON');
    
    if (steps.length === 0) {
        visualizacaoJSON.innerHTML = "Nenhum step foi adicionado ainda.";
    } else {
        let stepsHtml = "";
        for (let i = 0; i < steps.length; i++) {
            stepsHtml += `<h3>Step ${i + 1}</h3>`;
            stepsHtml += renderJsonToForm(steps[i]);
        }
        visualizacaoJSON.innerHTML = stepsHtml;
    }
}

function renderJsonToForm(jsonObj) {
    let formHtml = '<div class="json-group">';
    formHtml += '<div class="form-group">';

    for (const key in jsonObj) {
        if (jsonObj.hasOwnProperty(key)) {
            const value = jsonObj[key];
            
            if (typeof value === "object" && !Array.isArray(value)) {
                formHtml += `<h4>${key}</h4>`;
                formHtml += renderJsonToForm(value);
            } else {
                formHtml += `
                        <label for="${key}">${key}</label>
                        <input type="text" id="${key}" name="${key}" value="${value}" class="form-input" readonly>
                `;
            }
        }
    }

    formHtml += '</div></div>';
    console.log(formHtml);
    return formHtml;
}


function gerarJSONFinal() {
    const jsonFinal = {};

    steps.forEach((step, index) => {
        jsonFinal[`STEP${String(index + 1).padStart(2, '0')}`] = step;
    });

    console.log(jsonFinal);
    alert("Clique em OK para copiar o JSON");
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

async function getlogs() {
    let query = 'SELECT * FROM logs_ambientes';
    
    const response = await fetch('/get_logs', {
        headers: {
        'Content-Type': 'application/json',
        'SQL-Query': query
        }
    });
    const logs_ambientes = await response.json();
    return logs_ambientes;
}



async function carregarAmbientes() {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = '';
    ambientes = await get();
    
    let tableHTML = `
        <br>
        <table>
            <thead>
                <tr>
                    <th>Identificador</th>
                    <th>Nome</th>
                    <th>Versão</th>
                    <th>Configurações</th>
                    <th>Ambiente</th>
                    <th>Criador</th>
                    <th>Data de Criação</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;

    ambientes.forEach(ambiente => {
        tableHTML += `
            <tr onclick="linhaSelecionada(this)">
                <td>${ambiente.identificador}</td>
                <td>${ambiente.nome}</td>
                <td>${ambiente.versao}</td>
                <td>${ambiente.configuracoes}</td>
                <td>${ambiente.ambiente}</td>
                <td>${ambiente.criador}</td>
                <td>${new Date(ambiente.data_criacao).toLocaleString()}</td>
                <td>${ambiente.status}</td>
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    conteudo.innerHTML = tableHTML;
}

async function carregarLogsDeAmbientes() {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = '';
    logs_ambientes = await getlogs();
    
    let tableHTML = `
        <br>
        <table>
            <thead>
                <tr>
                    <th>Identificador</th>
                    <th>Executor</th>
                    <th>Horário</th>
                    <th>Ação Executada</th>
                    <th>Resultado</th>
                </tr>
            </thead>
            <tbody>
    `;

    logs_ambientes.forEach(log => {
        tableHTML += `
            <tr onclick="linhaSelecionada(this)">
                <td>${log.identificador}</td>
                <td>${log.executor}</td>
                <td>${new Date(log.ultima_modificacao).toLocaleString()}</td>
                <td>${log.acao_executada}</td>
                <td>${log.resultado}</td>
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    conteudo.innerHTML = tableHTML;
}

function linhaSelecionada(linha) {
    const linhas = document.querySelectorAll('tbody tr');
    linhas.forEach(l => {
        if (l === linha) {
            l.classList.add('selected');
        } else {
            l.classList.remove('selected');
        }
    });
}

function getIdentificador() {
    const linhaSelecionada = document.querySelector('.selected');
    if (!linhaSelecionada) {
        return false;
    }
    
    const primeiraCelula = linhaSelecionada.querySelector('td');
    return primeiraCelula ? primeiraCelula.textContent : 'Sem identificador';
}

function PrepararAmbiente() {
    const dados = getIdentificador();
    if (dados === false) {
        alert('Selecione uma opção ...');
        return
    }
    alert('Preparando ambiente no MAINFRAME');
    preparar(dados);
    // Restante do código para PrepararAmbiente...
    mostrarConteudo('ambientes');
}

function DestruirAmbiente() {
    const dados = getIdentificador();
    if (dados === false) {
        alert('Selecione uma opção ...');
        return
    }
    alert('Destruindo ambiente no MAINFRAME');
    destruir(dados);
    // Restante do código para DestruirAmbiente...
    mostrarConteudo('ambientes');
}

function ConsultarAmbiente() {
    const dados = getIdentificador();
    if (dados === false) {
        alert('Selecione uma opção ...');
        return
    }
    alert('Consultar Formulário: ' + dados);
    // Restante do código para ConsultarAmbiente...
    mostrarConteudo('ambientes');
}

function DeletarAmbiente() {
    const dados = getIdentificador();
    if (dados === false) {
        alert('Selecione uma opção ...');
        return
    }
    deletar(dados);
}

function Sair() {
    localStorage.clear();
    window.location.href = "home.html";
}


async function criar(dados) {    
    const nome = document.getElementById('nome').value;
    const configuracao = document.getElementById('configuracao').value;
    const versao = document.getElementById('versao').value;   
    const response = await fetch('/codes/ambiente_criar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({data: dados, usuario: RACF, senha: SENHA, nome: nome, configuracao: configuracao, versao: versao, ambiente: ambiente})
    });
    const ambientes = await response.json();
    alert(`Você sera redirecionado para pagina de ambientes, seu identificador é: ${ambientes['identificador']}`);
    mostrarConteudo('ambientes');
    return ambientes;
}

async function preparar(dados) {    
    const response = await fetch('/codes/ambiente_preparar', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({identificador: dados, usuario: RACF, senha: SENHA})
    });
    const resposta = await response.json();
    mostrarConteudo('ambientes');
    return resposta;
}

async function destruir(dados) {    
    const response = await fetch('/codes/ambiente_destruir', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({identificador: dados, usuario: RACF, senha: SENHA})
    });
    const resposta = await response.json();
    mostrarConteudo('ambientes');
    return resposta;
}

async function deletar(dados) {    
    const response = await fetch('/codes/ambiente_deletar', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({identificador: dados, usuario: RACF, senha: SENHA})
    });
    const resposta = await response.json();
    mostrarConteudo('ambientes');
    return resposta;
}

// Ao carregar a página, mostre a home
window.onload = function() {
    mostrarConteudo('home');
}