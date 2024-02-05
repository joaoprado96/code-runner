TABELA = {
    "LOCALHOST":{"ip":"127.0.0.1","porta":12345,"cpuid":"C","agencia":"3000"},
    "TESTER2":{"ip":"XXXXXXXX","porta":"5033","cpuid":"C","agencia":"3000"},
    "TESTER3":{"ip":"XXXXXXXX","porta":"5033","cpuid":"C","agencia":"3000"},
    "TESTER4":{"ip":"XXXXXXXX","porta":"5033","cpuid":"C","agencia":"3000"},
    "TESTER5":{"ip":"XXXXXXXX","porta":"5033","cpuid":"C","agencia":"3000"}
}

# Cada opção tem atributos que especificam:
# 1) Se é obrigatória (required), 
# 2) seu tipo (type) 
# 3) aceita atribuição de valor (assignment), 
# 4) o comprimento do valor (length), 
# 5) Os valores permitidos (values).

COMANDOS = {
  "TASK": {
    "options": {
      "ID": {"required": True, "type": "string", "assignment": True, "length": "any"},
      "ST": {"required": False, "type": "string", "assignment": True, "values": ["AT", "IN"]},
      "GER": {"required": False, "type": "flag", "assignment": False}
    }
  },
  "RESUMO": {
    "options": {
      "MEMORIA": {"required": False, "type": "flag", "assignment": False}
    }
  },
  "HTTPCON": {
    "options": {
      "ID": {"required": True, "type": "string", "assignment": True, "length": "any"}
    }
  }
}

MODELO = {
  "modelos": {
    "modeloX": [
      {"campo": "campo1", "largura": 10},
      {"campo": "campo2", "largura": 20},
      {"campo": "campo3", "largura": 36}
    ],
    "modeloY": [
      {"campo": "campoA", "largura": 15},
      {"campo": "campoB", "largura": 15},
      {"campo": "campoC", "largura": 36}
    ]
  }
}

MODELO_IGNORAR = {
  "IGNORAR": {
    "TRAN":   ['DISPLAY','----------------'],
    "TASK":   ['DISPLAY','----------------'],
    "CON":    ['DISPLAY','----------------'],
    "CONIP":  ['DISPLAY','----------------','CONEXOES COM OUTRAS','ENVIADAS','RECEBIDAS', 'NOME DA'],
    "ARQ":    ['DISPLAY','----------------'],
    "MOD":    ['DISPLAY','----------------'],
  }
}

