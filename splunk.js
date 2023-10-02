var splunkjs = require('splunk-sdk');

// Defina as configurações de conexão
var service = new splunkjs.Service({
    username: "YOUR_USERNAME",
    password: "YOUR_PASSWORD",
    scheme: "https",
    host: "YOUR_SPLUNK_HOST",
    port: "8089", // Normalmente é 8089 para a REST API
    version: "5.0"
});

// Realize a consulta
var searchQuery = "search index=YOUR_INDEX YOUR_SEARCH_QUERY";
var searchParams = {
    exec_mode: "blocking"
};

service.oneshotSearch(searchQuery, searchParams, function(err, results) {
    if (err) {
        console.error("Erro ao consultar Splunk:", err);
        return;
    }
    
    var fields = results.fields;
    var rows = results.rows;

    for(var i = 0; i < rows.length; i++) {
        var values = rows[i];
        console.log("Resultado:", values);
    }
});
