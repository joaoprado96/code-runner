let registrosOriginais = []; // Armazena os registros originais sem filtro

document.addEventListener('click', function(event) {
    if (event.target.closest('.detalhes-btn')) {
        const btn = event.target.closest('.detalhes-btn');
        const id = parseInt(btn.getAttribute('data-id'), 10);
        exibirPopup(id);
        btn.closest('tr').classList.add('linha-clicada');
    }
});

document.addEventListener('click', function(event) {
    if (event.target.closest('.detalhes-btn2')) {
        const btn = event.target.closest('.detalhes-btn2');
        const id = parseInt(btn.getAttribute('data-id'), 10);
        exibirPopupCompleto(id);
        btn.closest('tr').classList.add('linha-clicada');
    }
});

// Função para fazer uma requisição assíncrona para obter os registros da tabela
async function getRegistros() {

    const response = await fetch('/get_estatistica', {
        headers: {
        'Content-Type': 'application/json',
        }
    });
    const registros = await response.json();

    const configuracoes = {
        filler: 1,
        protocolo: 1,
        registro: 1, 
        processamento: 1, 
        transmissao: 1,
        task: 1,
        cpu_term: 1,
        cpu_origem:1,
        cd_local_origem: 4,
        cpu_destino: 1,
        cd_local_destino: 4,
        num_transacoes: 2,
        transacao: 3,
        filler2: 1,
        tempo_cpu: 8,
        hi_processamento: 8, 
        hi_send_dados: 8,
        hi_proc_comando: 8,
        hi_gravacao_estatistica: 8,
        filler3: 8,
        vr_registro: 1,
        qtd_erros: 2,
        tempo_gasto_segundos: 2, 
        tempo_gasto_dseg: 1,
        applid_grbe: 8,
        nome_logico: 8,
        numero_entrada: 6,
        tipo_terminal: 2,
        versao_hardware: 2,
        terminal_logico: 8,
        tipo_terminal_con: 1,
        numero_serie: 8,
        numero_sequencial: 4,
        numero_task_zonada:2,
        numero_socket: 6,
        endereco_ip: 4, 
        num_transacoes_cadeia: 2,
        codigo_desconexao: 1,
        num_tentativas_transmitir: 1,
        tempo_total_gasto_io: 8,
        qtd_arquivos_lidos: 2,
        qtd_arquivos_gravados: 2,
        tamanho_input: 2,
        tamanho_output: 2,
        msg_entrada: 150,
        msg_saida: 100,
    };
    const registros2 = linhasParaRegistros(registros, configuracoes)

    return registros2;
}

function extrairValoresDaLinha(linha, configuracoes) {
    const valoresExtraidos = {};

    let indiceInicial = 0;
    for (const [nomeVariavel, tamanhoColuna] of Object.entries(configuracoes)) {
        const valor = linha.slice(indiceInicial, indiceInicial + tamanhoColuna).trim();
        if (nomeVariavel === 'processamento' || nomeVariavel === 'numero_sequencial' || nomeVariavel === 'task'){
            valoresExtraidos[nomeVariavel] = toHexString(valor)
        }
        else{
            valoresExtraidos[nomeVariavel] = valor;
        }
        
        indiceInicial += tamanhoColuna;
    }

    return valoresExtraidos;
}

function linhasParaRegistros(texto, configuracoes) {
    // Dividir a string em linhas usando a quebra de linha como delimitador
    var linhas = texto.trim().split('\n');

    // Mapear cada linha para um registro JSON usando extrairValoresDaLinha
    var registros = linhas.map(function(linha) {
        return extrairValoresDaLinha(linha, configuracoes);
    });

    return registros;
}

function processarInput() {
    // Obtém o valor da entrada
    let datasetsStr = document.getElementById('datasets').value.trim();
    
    // Se a entrada não estiver vazia
    if (datasetsStr) {
        // Divide a entrada em uma lista usando a vírgula como delimitador
        let datasetsList = datasetsStr.split(',').map(ds => ds.trim());

        // Processa a lista de datasets
        console.log(datasetsList);  // Aqui, você pode fazer o que quiser com a lista
    } else {
        alert('Por favor, insira ao menos um dataset.');
    }
}

async function buildTable(ordens = []) {
    const registros = await getRegistros();
    registrosOriginais = registros; // Armazena os registros originais
    registrosGlobal = registros;

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
    registros.forEach((registro, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td><button data-id="${index}" class="btn detalhes-btn" title="Resumo"><i class="fas fa-eye"></i></button></td>
        <td><button class="btn" onclick="alert('${registro.msg_saida}')"title="Buscar"> <i class="fas fa-search"></i></button></td>
        <td><button data-id="${index}" class="btn detalhes-btn2" title="Detalhes"><i class="fas fa-terminal"></i></button></td>
        <td>${registro.protocolo}</td>
        <td>${registro.registro}</td>
        <td>${registro.processamento}</td>
        <td>${registro.transacao}</td>
        <td>${registro.task}</td>
        <td>${registro.cpu_term}</td>
        <td>${registro.cpu_origem}</td>
        <td>${registro.cpu_destino}</td>
        <td>${registro.hi_processamento}</td>
        <td>${registro.applid_grbe}</td>
        <td>${registro.nome_logico}</td>
        <td>${registro.terminal_logico}</td>
        <td>${registro.numero_serie}</td>
        <td>${registro.numero_sequencial}</td>
    `;
        registrosElement.appendChild(row);
    });

}


// Função para filtrar os registros por coluna
function filtrarRegistros() {
    let registrosFiltrados = registrosOriginais;

    const filtroColunas = ['protocolo','registro', 'processamento', 'transacao', 'task', 'cpu_term', 'cpu_origem', 'cpu_destino', 'hi_processamento', 'applid_grbe', 'nome_logico', 'terminal_logico', 'numero_serie', 'numero_sequencial'];

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

    registrosFiltrados.forEach((registro, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td><button data-id="${index}" class="btn detalhes-btn" title="Resumo"><i class="fas fa-eye"></i></button></td>
        <td><button class="btn" onclick="alert('${registro.msg_saida}')"title="Buscar"> <i class="fas fa-search"></i></button></td>
        <td><button data-id="${index}" class="btn detalhes-btn2" title="Detalhes"><i class="fas fa-terminal"></i></button></td>
        <td>${registro.protocolo}</td>
        <td>${registro.registro}</td>
        <td>${registro.processamento}</td>
        <td>${registro.transacao}</td>
        <td>${registro.task}</td>
        <td>${registro.cpu_term}</td>
        <td>${registro.cpu_origem}</td>
        <td>${registro.cpu_destino}</td>
        <td>${registro.hi_processamento}</td>
        <td>${registro.applid_grbe}</td>
        <td>${registro.nome_logico}</td>
        <td>${registro.terminal_logico}</td>
        <td>${registro.numero_serie}</td>
        <td>${registro.numero_sequencial}</td>
        `;
        registrosElement.appendChild(row);
    });
}

function exibirPopupCompleto(index) {
    console.log(index);
    const registro = registrosOriginais[index];
    const chavesIgnoradas = ['filler', 'filler2', 'filler3']; // Adicione mais chaves conforme necessário.


    let conteudoPopup = '';
    for (const [chave, valor] of Object.entries(registro)) {
        if (chavesIgnoradas.includes(chave)) {
            continue; // Se a chave estiver na lista de ignorados, continue para a próxima iteração.
        }
    
        const [chaveTransformada, valorTransformado] = transformarChaveValor(chave, valor);
        conteudoPopup += `<strong>${chaveTransformada}:</strong> ${valorTransformado}<br>`;
    }
    
    document.getElementById('popupInfo').innerHTML = conteudoPopup;

    // Mostrar o popup
    document.getElementById('customPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('customPopup').style.display = 'none';
}

function exibirPopup(index) {
    console.log(index);
    const registro = registrosOriginais[index];
    const chavesIgnoradas = ['filler', 'filler2', 'filler3','transmissao','num_transacoes_cadeia','hi_send_dados','hi_proc_comando','hi_gravacao_estatistica','vr_registro','versao_hardware','num_transacoes','gtd_erros','tempo_gasto_segundos','tempo_gasto_dseg','numero_task_zonada','numero_socket','endereco_ip','codigo_desconexao','num_tentativas_transmitir','qtd_arquivos_lidos','qtd_arquivos_gravados','tempo_total_gasto_io','tempo_cpu','tipo_terminal_con','qtd_erros','cpu_term']; // Adicione mais chaves conforme necessário.


    let conteudoPopup = '';
    for (const [chave, valor] of Object.entries(registro)) {
        if (chavesIgnoradas.includes(chave)) {
            continue; // Se a chave estiver na lista de ignorados, continue para a próxima iteração.
        }
    
        const [chaveTransformada, valorTransformado] = transformarChaveValor(chave, valor);
        conteudoPopup += `<strong>${chaveTransformada}:</strong> ${valorTransformado}<br>`;
    }
    
    document.getElementById('popupInfo').innerHTML = conteudoPopup;

    // Mostrar o popup
    document.getElementById('customPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('customPopup').style.display = 'none';
}

function toHexString(input) {
    // Convertendo a string para um buffer UTF-8 usando TextEncoder
    let utf8Array = new TextEncoder().encode(input);

    // Convertendo o array UTF-8 para uma string hexadecimal
    return Array.from(utf8Array).map(byte => byte.toString(16).padStart(2, '0')).join('').toUpperCase();
}

function transformarChaveValor(chave, valor) {
    switch (chave) {
        case "protocolo":
            switch(valor){
                case '2':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Transação'];
                case '4':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Serviço'];
                case 'b':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Transação'];
                default:
                    return [chave.toUpperCase(), valor];
            }
        case "registro":
            switch(valor){
                case '2':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Transação'];
                case '4':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Serviço'];
                case 'c':
                    return [chave.toUpperCase(), valor.toLowerCase() + ' - Status de Processamento'];
                default:
                    return [chave.toUpperCase(), valor];
            }
        case "processamento":
            switch(valor){
                case '2':
                    return [chave.toUpperCase(), valor];
                default:
                    return [chave.toUpperCase(), valor];
            }
        case "transmissao":
            switch(valor){
                case '2':
                    return [chave.toUpperCase(), valor];
                default:
                    return [chave.toUpperCase(), valor];
            }
        case "task":
            switch(valor){
                default:
                    return [chave.toUpperCase(), valor];
            }
        case "cpu_term":
            switch(valor){
                default:
                    return ['CPU TERMINAL', valor];
            }
        case "cpu_origem":
            switch(valor){
                default:
                    return ['CPU ORIGEM', valor];
            }
        case "cd_local_origem":
            switch(valor){
                default:
                    return ['CÓDIGO LOCAL DE ORIGEM', valor];
            }
        case "cpu_destino":
            switch(valor){
                default:
                    return ['CPU DESTINO', valor];
            }
        case "cd_local_destino":
            switch(valor){
                default:
                    return ['CÓDIGO LOCAL DESTINO', valor];
            }
        case "num_transacoes":
            switch(valor){
                default:
                    return ['NÚMERO DE TRANSAÇÕES EM CADEIA', valor];
            }
        case "transacao":
            switch(valor){
                default:
                    return ['TRANSAÇÃO', valor];
            }
        case "tempo_cpu":
            switch(valor){
                default:
                    return ['TEMPO TOTAL DE CPU', valor];
            }
        case "hi_processamento":
            switch(valor){
                default:
                    return ['HORÁRIO DO INÍCIO DO PROCESSAMENTO', valor];
            }
        case "hi_send_dados":
            switch(valor){
                default:
                    return ['HORÁRIO DO INÍCIO DE ENVIO DOS DADOS', valor];
            }
        case "hi_proc_comando":
            switch(valor){
                default:
                    return ['HORÁRIO DE PROCESSAMENTO DO COMANDO', valor];
            }
        case "hi_gravacao_estatistica":
            switch(valor){
                default:
                    return ['HORÁRIO DE GRAVAÇÃO DO ESTATÍSTICA', valor];
            }
        case "vr_registro":
            switch(valor){
                default:
                    return ['VERSÃO DO REGISTRO', valor];
            }
        case "qtd_erros":
            switch(valor){
                default:
                    return ['QUANTIDADE DE ERROS', valor];
            }
        case "tempo_gasto_segundos":
            switch(valor){
                default:
                    return ['TEMPO GASTO EM SEGUNDOS', valor];
            }
        case "tempo_gasto_dseg":
            switch(valor){
                default:
                    return ['TEMPO GASTO EM DÉCIMO DE SEGUNDOS', valor];
            }
        case "applid_grbe":
            switch(valor){
                default:
                    return ['APPLID GRBE', valor];
            }
        case "nome_logico":
            switch(valor){
                default:
                    return ['NOME LÓGICO', valor];
            }
        case "numero_entrada":
            switch(valor){
                default:
                    return ['NÚMERO ENTRADA', valor];
            }
        case "tipo_terminal":
            switch(valor){
                default:
                    return ['TIPO DE TERMINAL', valor];
            }
        case "versao_hardware":
            switch(valor){
                default:
                    return ['VERSÃO DE HARDWARE', valor];
            }
        case "terminal_logico":
            switch(valor){
                default:
                    return ['TERMINAL LÓGICO', valor];
            }
        case "tipo_terminal_con":
            switch(valor){
                default:
                    return ['TIPO TERMINAL CONECTADO', valor];
            }
        case "numero_serie":
            switch(valor){
                default:
                    return ['NÚMERO DE SÉRIE', valor];
            }
        case "numero_sequencial":
            switch(valor){
                default:
                    return ['NÚMERO SEQUENCIAL OU HEXADECIMAL', valor];
            }
        case "numero_task_zonada":
            switch(valor){
                default:
                    return ['NÚMERO DA TASK EM ZONADO', valor];
            }
        case "numero_socket":
            switch(valor){
                default:
                    return ['NÚMERO DO SOCKET', valor];
            }
        case "endereco_ip":
            switch(valor){
                default:
                    return ['ENDEREÇO DE IP', valor];
            }
        case "num_transacoes_cadeia":
            switch(valor){
                default:
                    return ['NÚMERO DE TRANSAÇÕES NA CADEIA', valor];
            }
        case "codigo_desconexao":
            switch(valor){
                default:
                    return ['CÓDIGO DE DESCONEXÃO', valor];
            }
        case "num_tentativas_transmitir":
            switch(valor){
                default:
                    return ['NÚMERO DE TENTATIVAS DE TRANSMISSÃO', valor];
            }
        case "tempo_total_gasto_io":
            switch(valor){
                default:
                    return ['TEMPO TOTAL GASTO EM I/O', valor];
            }
        case "qtd_arquivos_lidos":
            switch(valor){
                default:
                    return ['QUANTIDADE DE ARQUIVOS LIDOS', valor];
            }
        case "qtd_arquivos_gravados":
            switch(valor){
                default:
                    return ['QUANTIDADE DE ARQUIVOS GRAVADOS', valor];
            }
        case "tamanho_input":
            switch(valor){
                default:
                    return ['TAMANHO DA MENSAGEM RECEBIDA', valor];
            }
        case "tamanho_output":
            switch(valor){
                default:
                    return ['TAMANHO DA MENSAGEM ENVIADA', valor];
            }
        case "msg_entrada":
            switch(valor){
                default:
                    return ['MENSAGEM RECEBIDA DO CANAL', valor];
            }
        case "msg_saida":
            switch(valor){
                default:
                    return ['MENSAGEM ENVIADA PARA O CANAL', valor];
            }
        default:
            // Se a chave não precisar de transformação especial, retorne como está
            return [chave.toUpperCase(), valor];
    }
}


// Chamada da função para construir a tabela ao carregar a página
window.onload = function() {
    // (CODIGO NOVO)
    buildTable([
        { coluna: 'nome', modo: 'asc' },
        { coluna: 'tempo_inicio', modo: 'desc' }
    ]);
};
