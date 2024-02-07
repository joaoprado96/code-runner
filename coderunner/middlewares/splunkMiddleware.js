const axios = require('axios');

// Função auxiliar para enviar dados ao Splunk com retentativas
const sendDataToSplunk = async (data, attempts = 3) => {
  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      await axios.post('https://your-splunk-instance/services/collector', data, {
        headers: {
          'Authorization': `Splunk SPLUNK_AUTH_TOKEN`,
          'Content-Type': 'application/json',
        },
      });
      console.log(`Dados enviados ao Splunk na tentativa ${attempt}`);
      break; // Sai do loop se o envio for bem-sucedido
    } catch (error) {
      console.error(`Erro ao enviar dados para o Splunk na tentativa ${attempt}:`, error.message);
      if (attempt < attempts) {
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt)); // Espera 1s, 2s, etc.
      }
    }
  }
};

// Middleware para capturar e enviar dados ao Splunk
const enviaSplunk = (req, res, next) => {
  const { method, url, headers, body, query, ip } = req;
  const requestDetails = {
    method,
    url,
    headers,
    body,
    query,
    ip,
    timestamp: new Date().toISOString(),
  };

  // Chama a função de envio sem esperar pela resposta para não bloquear o processamento da requisição
  sendDataToSplunk({ event: requestDetails }).catch(error => {
    // Erros após as retentativas são apenas logados e não bloqueiam a aplicação
    console.error('Falha após máximas retentativas de envio para o Splunk:', error.message);
  });

  next(); // Continua o processamento da requisição imediatamente
};

module.exports = {
    enviaSplunk
}