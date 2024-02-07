const axios = require('axios');

// Configurações do Splunk para diferentes ambientes
const splunkConfigs = {
  "DES": {
    "url": "https://splunk-instance-des/services/collector",
    "authorization": "Splunk SPLUNK_AUTH_TOKEN_DES"
  },
  "HOM": {
    "url": "https://splunk-instance-hom/services/collector",
    "authorization": "Splunk SPLUNK_AUTH_TOKEN_HOM"
  },
  "PROD": {
    "url": "https://splunk-instance-prod/services/collector",
    "authorization": "Splunk SPLUNK_AUTH_TOKEN_PROD"
  }
};

// Função auxiliar para enviar dados ao Splunk com retentativas
const sendDataToSplunk = async (data, attempts = 3) => {
  const ambiente = process.env.AMBIENTE || "DES"; // Usa "DES" como padrão se AMBIENTE não estiver definido
  const { url, authorization } = splunkConfigs[ambiente];

  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      await axios.post(url, data, {
        headers: {
          'Authorization': authorization,
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
    console.error('Falha após máximas retentativas de envio para o Splunk:', error.message);
  });

  next(); // Continua o processamento da requisição imediatamente
};

module.exports = {
    enviaSplunk
}