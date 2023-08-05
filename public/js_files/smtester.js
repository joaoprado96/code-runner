// Opções disponíveis para o monitor
var monitorOptions = [`LOCALHOST`,'AGENRT1', 'AGENRT2', 'AGENRT3', 'AGENRT4', 'AGENRT5', 'TESTM26'];

// Obtém a referência ao elemento select
var monitorSelect = document.getElementById("monitor");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < monitorOptions.length; i++) {
    var option = document.createElement("option");
    option.value = monitorOptions[i];
    option.text = monitorOptions[i];
    monitorSelect.appendChild(option);
}

// Opções disponíveis para a porta
var portaOptions = ['12345', '25000', '5030', '5031', '5032', '5033', '5034'];

// Obtém a referência ao elemento select
var portaSelect = document.getElementById("porta");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < portaOptions.length; i++) {
    var option = document.createElement("option");
    option.value = portaOptions[i];
    option.text = portaOptions[i];
    portaSelect.appendChild(option);
}

// Opções disponíveis para o protocolo
var protocoloOptions = ['2000A','4000A'];

// Obtém a referência ao elemento select
var protocoloSelect = document.getElementById("protocolo");

// Itera sobre as opções disponíveis e cria elementos option
for (var i = 0; i < protocoloOptions.length; i++) {
    var option = document.createElement("option");
    option.value = protocoloOptions[i];
    option.text = protocoloOptions[i];
    protocoloSelect.appendChild(option);
}

// Opções disponíveis para o protocolo
var logsOptions = ['Não','Sim'];

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

    fetch('/codes/smtester', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'num-scripts': terminais
        },
        body: JSON.stringify(data)
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        setInterval(updateLog, 1000);
    });
});

document.getElementById("cancelButton").addEventListener("click", function() {
    fetch('/codes/smtester', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
});
function updateLog() {
// Faz a requisição para o servidor para obter as logs
fetch('/page/smtester/sysout.txt') // <-- Endpoint correto do servidor
.then(response => response.text())
.then(data => {
    // Garantir que a variável data seja tratada como uma string
    data = data.toString();

    // Preenche a div com as informações de logs
    document.getElementById("logContainer").textContent = data;

});
}
