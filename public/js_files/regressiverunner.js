let registrosOriginais = []; // Armazena os registros originais sem filtro

// Função para fazer uma requisição assíncrona para obter os registros da tabela
async function getRegistros() {
    const versao = document.getElementById('versao').value;
    let query = 'SELECT * FROM logs';
    
    if(versao !== 'TODAS') {
        query = "SELECT * FROM logs WHERE versao_grbe = "+"'"+versao+"'";
    } 

    console.log(query)

    const response = await fetch('/get_logs', {
        headers: {
        'Content-Type': 'application/json',
        'SQL-Query': query
        }
    });
    const registros = await response.json();

    // Se a versão não for "TODAS", verificar os registros faltantes na versão "Base"
    if (versao !== 'TODAS') {
        // Obter todos os id_teste na versão selecionada
        const idTestesVersao = new Set(registros.map(registro => registro.id_teste));

        // Fazer outra requisição para obter os registros da versão_grbe = "Base"
        const queryBase = "SELECT * FROM logs WHERE versao_grbe = 'Base'";
        const responseBase = await fetch('/get_logs', {
            headers: {
                'Content-Type': 'application/json',
                'SQL-Query': queryBase
            }
        });
        const registrosBase = await responseBase.json();

        // Filtrar os registros da versão "Base" para encontrar os registros faltantes na versão selecionada
        const registrosFaltantes = registrosBase.filter(registro => !idTestesVersao.has(registro.id_teste));

        // Adicionar os registros faltantes à lista de registros
        registros.push(...registrosFaltantes.map(registro => ({
            ...registro,
            versao_grbe: versao // Modificar a versao_grbe para a versão selecionada
        })));
    }

    return registros;
}

function atualizarCores(registros2) {
    for (let key in registros2) {
        let ball = document.getElementById(key);
        if (ball) {
            if (registros2[key] === "Ativo") {
                ball.style.backgroundColor = '#32CD32';
            } else if (registros2[key] === "Inativo") {
                ball.style.backgroundColor = 'Black';
            }
        }
    }
}

async function statusMonitores() {
    const response2 = await fetch('/front/statusmon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    const registros2 = await response2.json();
    atualizarCores(registros2)
}

// Função para enviar a solicitação POST ao clicar no botão
function enviarSolicitacao(idTeste) {
    // Obtenha o valor do usuário e da senha dos elementos de entrada
    const usuario = document.getElementById('usuario').value;
    const senha = document.getElementById('senha').value;
    const versao = document.getElementById('versao').value;

    // Verifique se o usuário e a senha foram preenchidos
    if (!usuario || !senha) {
        alert('Por favor, preencha os campos de usuário e senha.');
        return;  // Pare a execução da função
    }

    // Verifique se o usuário e a senha foram preenchidos
    if (versao == 'TODAS') {
        alert('Por favor, selecione a versão na qual você está executando o teste. Não deixar selecionado TODAS');
        return;  // Pare a execução da função
    }

    fetch(`/codes/regressivo/${idTeste}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Inclua o usuário e a senha no corpo da solicitação
        body: JSON.stringify({ id_teste: idTeste, racf: usuario, senha: senha, versao: versao })
    })
    .then(response => {
        if (response.ok) {
            // A solicitação foi bem-sucedida
            alert('Solicitação enviada com sucesso!');
        } else {
            // A solicitação falhou
            alert('Falha ao enviar a solicitação. Por favor, tente novamente. Verifique se este teste já está no novo portal no projeto do Git Hub (Code Runner)');
        }
    })
    .catch(error => {
        console.error('Ocorreu um erro:', error);
        alert('Ocorreu um erro ao processar a solicitação. Por favor, tente novamente.');
    });
}

// Função para construir a tabela com os registros obtidos
async function buildTable() {
    const registros = await getRegistros();
    registrosOriginais = registros; // Armazena os registros originais

    await statusMonitores();

    const registrosElement = document.getElementById('registros');

    // Limpar a tabela antes de construir
    registrosElement.innerHTML = '';

    // Construir as linhas da tabela
    registros.forEach(registro => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><button class="btn" onclick="enviarSolicitacao(${registro.id_teste},${registro.pilar})">Submeter</button></td>
            <td><button class="btn" onclick="alert('Botão clicado!')">Aprovar</button></td>
            <td>${registro.id}</td>
            <td>${registro.id_teste}</td>
            <td>${registro.executor}</td>
            <td>${registro.monitores}</td>
            <td>${registro.return_code}</td>
            <td>${registro.status_teste}</td>
            <td>${registro.status_versao}</td>
            <td>${registro.observacao}</td>
            <td>${registro.jobs}</td>
            <td>${registro.tempo_inicio}</td>
            <td>${registro.tempo_fim}</td>
            <td>${registro.versao_grbe}</td>
            <td>${registro.tipo}</td>
            <td>${registro.pilar}</td>
            <td>${registro.resumo}</td>
            <td>${registro.criador}</td>
    `;
        registrosElement.appendChild(row);
    });
}

// Função para filtrar os registros por coluna
function filtrarRegistros() {
    const checkboxUltimasExecucoes = document.getElementById('checkbox-ultimas-execucoes');
    const exibirSomenteUltimasExecucoes = checkboxUltimasExecucoes.checked;

    let registrosFiltrados = registrosOriginais;

    if (exibirSomenteUltimasExecucoes) {
        const idTestesUnicos = [...new Set(registrosOriginais.map(registro => registro.id_teste))];
        registrosFiltrados = idTestesUnicos.map(idTeste => {
            const registrosDoId = registrosOriginais.filter(registro => registro.id_teste === idTeste);
            const ultimaExecucao = registrosDoId.reduce((max, registro) => {
                return new Date(registro.timestamp) > new Date(max.timestamp) ? registro : max;
            });
            return ultimaExecucao;
        });
    }

    const filtroColunas = ['id','id_teste', 'executor', 'monitores', 'return_code', 'status_teste', 'status_versao', 'observacao', 'jobs', 'tempo_inicio', 'tempo_fim', 'versao_grbe', 'tipo', 'pilar', 'resumo', 'criador'];

    filtroColunas.forEach(coluna => {
        const filtroValor = document.getElementById(`filtro-${coluna}`).value.toLowerCase();
        if (filtroValor) {
            registrosFiltrados = registrosFiltrados.filter(registro => {
                const valorColuna = registro[coluna];
                if (!isNaN(parseFloat(valorColuna))) {
                    const filtroNum = parseFloat(filtroValor);
                    const valorColunaNum = parseFloat(valorColuna);
                    return valorColunaNum === filtroNum;
                }
                if (typeof valorColuna === 'string') {
                    return valorColuna.toLowerCase().includes(filtroValor);
                }
                return false;
            });
        }
    });

    const registrosElement = document.getElementById('registros');
    registrosElement.innerHTML = '';

    registrosFiltrados.forEach(registro => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><button class="btn" onclick="enviarSolicitacao(${registro.id_teste})">Submeter</button></td>
            <td><button class="btn" onclick="alert('Botão clicado!')">Aprovar</button></td>
            <td>${registro.id}</td>
            <td>${registro.id_teste}</td>
            <td>${registro.executor}</td>
            <td>${registro.monitores}</td>
            <td>${registro.return_code}</td>
            <td>${registro.status_teste}</td>
            <td>${registro.status_versao}</td>
            <td>${registro.observacao}</td>
            <td>${registro.jobs}</td>
            <td>${registro.tempo_inicio}</td>
            <td>${registro.tempo_fim}</td>
            <td>${registro.versao_grbe}</td>
            <td>${registro.tipo}</td>
            <td>${registro.pilar}</td>
            <td>${registro.resumo}</td>
            <td>${registro.criador}</td>
        `;
        registrosElement.appendChild(row);
    });
}


// Chamada da função para construir a tabela ao carregar a página
window.onload = function() {
    buildTable();
};
