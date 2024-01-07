document.addEventListener('DOMContentLoaded', function() {
    window.onload = function() {
        criarNavbar();
    }
});

let editor;

// Opções disponíveis para o monitor
var monitorOptions = [`LOCALHOST`,'AGENRT1', 'AGENRT2', 'AGENRT3', 'AGENRT4', 'AGENRT5', 'TESTM26'];
// Opções disponíveis para a porta
var portaOptions = ['12345', '25000', '5030', '5031', '5032', '5033', '5034'];
// Opções disponíveis para o protocolo
var protocoloOptions = ['2000A','4000A'];
// Opções disponíveis para o protocolo
var logsOptions = ['Não','Sim'];


// Obtém a referência ao elemento select
var monitorSelect = document.getElementById("monitor");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < monitorOptions.length; i++) {
    var option = document.createElement("option");
    option.value = monitorOptions[i];
    option.text = monitorOptions[i];
    monitorSelect.appendChild(option);
}
// Obtém a referência ao elemento select
var portaSelect = document.getElementById("porta");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < portaOptions.length; i++) {
    var option = document.createElement("option");
    option.value = portaOptions[i];
    option.text = portaOptions[i];
    portaSelect.appendChild(option);
}

// Obtém a referência ao elemento select
var protocoloSelect = document.getElementById("protocolo");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < protocoloOptions.length; i++) {
    var option = document.createElement("option");
    option.value = protocoloOptions[i];
    option.text = protocoloOptions[i];
    protocoloSelect.appendChild(option);
}

// Obtém a referência ao elemento select
var logsSelect = document.getElementById("logs");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < logsOptions.length; i++) {
    var option = document.createElement("option");
    option.value = logsOptions[i];
    option.text = logsOptions[i];
    logsSelect.appendChild(option);
}

document.getElementById("sendButton").addEventListener("click", function() {
    var monitor = document.getElementById("monitor").value;
    var porta = document.getElementById("porta").value;
    var timeout = Number(document.getElementById("timeout").value);
    var terminais = Number(document.getElementById("terminais").value);
    var quantidade = Number(document.getElementById("quantidade").value);
    var protocolo = document.getElementById("protocolo").value;
    var logs = document.getElementById("logs").value;
    var agencia = document.getElementById("agencia").value;
    var transacao = document.getElementById("transacao").value;
    var servico = document.getElementById("servico").value;
    var entrada = document.getElementById("entrada").value;

    var data = {
        monitor: monitor,
        porta: porta,
        timeout: timeout,
        quantidade: quantidade,
        protocolo: protocolo,
        logs: logs,
        agencia: agencia,
        transacao: transacao,
        servico: servico,
        entrada: entrada
    };

    executarPython(data, terminais);
});


function executarPython(data, terminais) {
    var rota = ''
    if (terminais == 1) {
        rota = '/front/smtester'
    } else {
        rota = '/codes/smtester'
    }
    // var token = localStorage.getItem('token');
    try {
        fetch(rota, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json','num-scripts':terminais},
            body: JSON.stringify(data)
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
            document.getElementById('jsonOutput').innerText = 'Erro ao enviar POST.';
        });
    } catch (e) {
        document.getElementById('jsonOutput').innerText = 'JSON inválido.';
    }
}