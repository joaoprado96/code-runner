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

// (CODIGO NOVO)
function atualizarCores(registros2) {
    for (let key in registros2) {
        let ball = document.getElementById(key);
        let labelBola = document.getElementById('label-' + key);

        console.log(labelBola)
        if (ball) {
            if (registros2[key][0] === "Ativo") {
                ball.style.backgroundColor = '#32CD32';
                console.log(labelBola[key])
                labelBola.textContent = registros2[key][1];
            } else if (registros2[key][0] === "Inativo") {
                ball.style.backgroundColor = 'Black';
                labelBola.textContent = registros2[key][1];
            }
        }
    }
}

function openPopupDel() {
    var popup = document.getElementById("popupDel");
    popup.style.display = "block";
    console.log(popup)
}

function closePopupClose() {
    var popup = document.getElementById("popupDel");
    const racf = document.getElementById('executor').value;
    const justificativa = document.getElementById('observacao').value;
    popup.style.display = "none";
    fetch(`/codes/teste`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'num-scripts': 1
        },
        // Inclua o usuário e a senha no corpo da solicitação
        body: JSON.stringify({ id: id, racf: usuario, justificativa: justificativa })
    });

    // Confirmação de envio (remova esta linha se não quiser a confirmação)
    alert('Esse registro será removido!');
}

function deletaLog(id) {
    fetch(`/codes/teste`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'num-scripts': 1
        },
        // Inclua o usuário e a senha no corpo da solicitação
        body: JSON.stringify({ id: id })
    });

    // Confirmação de envio (remova esta linha se não quiser a confirmação)
    alert('Esse registro será removido!');
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
    });

    // Confirmação de envio (remova esta linha se não quiser a confirmação)
    alert('Solicitação enviada com sucesso!');
}

// (CODIGO NOVO)
function definirCoresPorStatusVersao() {
    const registrosElement = document.getElementById('registros');
    const linhas = registrosElement.getElementsByTagName('tr');

    for (let i = 0; i < linhas.length; i++) {
        const registro = registrosOriginais[i];
        const statusVersao = registro.status_versao;
        const statusTeste = registro.status_teste;
        const linha = linhas[i];

        if (statusVersao === 'Sucesso' && statusTeste === 'Sucesso' ) {
            linha.style.backgroundColor = '#d9fadc'; // Verde claro
        } else if (statusVersao === 'Sucesso' && statusTeste === 'Falha') {
            linha.style.backgroundColor = '#ffffcc'; // Amarelo claro
        } else if (statusVersao === 'Falha') {
            linha.style.backgroundColor = '#ffd8d6'; // Vermelho claro
        } else if (statusVersao === 'Base') {
            linha.style.backgroundColor = '#f0f0f0'; // Cinza claro
        }
        linha.addEventListener('mouseover', realcarLinha);
        linha.addEventListener('mouseout', restaurarLinha);
    }
}

// (CODIGO NOVO)
function definirCoresPorStatusVersaoPopup() {
    const registrosElement = document.getElementById('tabelaExecucoes');
    const linhas = registrosElement.getElementsByTagName('tr');

    for (let i = 1; i < linhas.length; i++) {
        const registro = registrosOriginais[i-1];
        const statusVersao = registro.status_versao;
        const statusTeste = registro.status_teste;
        const linha = linhas[i];

        if (statusVersao === 'Sucesso' && statusTeste === 'Sucesso' ) {
            linha.style.backgroundColor = '#d9fadc'; // Verde claro
        } else if (statusVersao === 'Sucesso' && statusTeste === 'Falha') {
            linha.style.backgroundColor = '#ffffcc'; // Amarelo claro
        } else if (statusVersao === 'Falha') {
            linha.style.backgroundColor = '#ffd8d6'; // Vermelho claro
        } else if (statusVersao === 'Base') {
            linha.style.backgroundColor = '#f0f0f0'; // Cinza claro
        }
        linha.addEventListener('mouseover', realcarLinha);
        linha.addEventListener('mouseout', restaurarLinha);
    }
}

// (CODIGO NOVO)
function realcarLinha(event) {
    event.target.style.backgroundColor = 'lightgray'; // Cor de realce
}

// (CODIGO NOVO)
function restaurarLinha(event) {
    event.target.style.backgroundColor = ''; // Remove o realce
}


// Função para construir a tabela com os registros obtidos
// (CODIGO NOVO)
async function buildTable(ordens = []) {
    const registros = await getRegistros();
    registrosOriginais = registros; // Armazena os registros originais

    await statusMonitores();

    const registrosElement = document.getElementById('registros');

    // (CODIGO NOVO)
    // Ordenar registros se as ordens estiverem definidas
    if (ordens.length > 0) {
        registros.sort((a, b) => {
            for (const ordem of ordens) {
                const coluna = ordem.coluna;
                const modo = ordem.modo;
                
                if (a[coluna] < b[coluna]) {
                    return modo === 'asc' ? -1 : 1;
                }
                if (a[coluna] > b[coluna]) {
                    return modo === 'asc' ? 1 : -1;
                }
            }
            return 0;
        });
    }

    // Limpar a tabela antes de construir
    registrosElement.innerHTML = '';

    // Construir as linhas da tabela
    registros.forEach(registro => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><button class="btn" onclick="enviarSolicitacao(${registro.id_teste},${registro.pilar})">Submeter</button></td>
            <td><button class="btn" onclick="abrirPopupExecucoes(${registro.id_teste})">Ver Execuções</button></td>
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
    // (CODIGO NOVO)
    definirCoresPorStatusVersao();
}

// (CODIGO NOVO)
function exportarParaExcel() {
    const tabela = document.getElementById('registros');
    const nomeArquivo = 'regressivo.xlsx';
    
    const planilha = XLSX.utils.table_to_book(tabela, { sheet: "Regressivo" });
    
    XLSX.writeFile(planilha, nomeArquivo);
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
            <td><button class="btn" onclick="abrirPopupExecucoes(${registro.id_teste})">Ver Execuções</button></td>
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
    // (CODIGO NOVO)
    definirCoresPorStatusVersao();
}

// (CODIGO NOVO)
function abrirPopupExecucoes(idTeste) {
    const popup = document.getElementById('popupExecucoes');
    const tabelaExecucoes = document.getElementById('tabelaExecucoes');

    // Limpa o conteúdo anterior da tabela
    tabelaExecucoes.querySelector('tbody').innerHTML = '';

    // Filtra as execuções pelo id_teste específico
    const execucoes = registrosOriginais.filter(registro => registro.id_teste === idTeste);

    // Preenche a tabela com as execuções
    execucoes.forEach(execucao => {
        const tempoInicio = new Date(execucao.tempo_inicio).getTime();
        const tempoFim = new Date(execucao.tempo_fim).getTime();
        const tempoExecucao = (tempoFim - tempoInicio) / 1000; // Tempo em segundos

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${execucao.id}</td>
            <td>${execucao.id_teste}</td>
            <td>${execucao.executor}</td>
            <td>${execucao.versao_grbe}</td>
            <td>${execucao.return_code}</td>
            <td>${execucao.status_teste}</td>
            <td>${execucao.status_versao}</td>
            <td>${tempoExecucao} segundos</td>
            <td>${execucao.observacao}</td>
        `;
        tabelaExecucoes.querySelector('tbody').appendChild(row);
    });
    definirCoresPorStatusVersaoPopup()
    popup.style.display = 'block';
}

function fecharPopupExecucoes() {
    const popup = document.getElementById('popupExecucoes');
    popup.style.display = 'none';
}


// Chamada da função para construir a tabela ao carregar a página
window.onload = function() {
    // (CODIGO NOVO)
    buildTable([
        { coluna: 'id_teste', modo: 'asc' },
        { coluna: 'tempo_inicio', modo: 'desc' }
    ]);
};
