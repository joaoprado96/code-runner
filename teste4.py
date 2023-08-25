
import json

def adicionar_elementos_json(objeto_json, novos_elementos):
    for chave, valor in novos_elementos.items():
        if chave not in objeto_json:
            objeto_json[chave] = valor

def adicionar_objeto(dict_principal, chave, dict_adicionar):
    dict_principal[chave] = dict_adicionar
    return dict_principal

def salvar_linhas_com_prefixo(texto, prefixo_alvo, prefixos_ignorados,json):
    linhas_salvas = []
    
    salvar = False
    prefixo_alvo = 'AGEDSECT'
    prefixos_ignorados = ['   ', 'Symbol']

    for linha in texto.split('\n'):
        auxiliar = linha
        if auxiliar.startswith(prefixo_alvo):
            salvar = not salvar

        if salvar and not any(linha.startswith(p) for p in prefixos_ignorados):
            novo={
                auxiliar[0:8]: auxiliar[9:16]
                }
            if auxiliar:
                if (auxiliar[0:8] != prefixo_alvo):
                    adicionar_elementos_json(json,novo)

    return '\n'.join(linhas_salvas)

# Ordenando o dicionário pelos valores hexadecimais
sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1], 16))}


# Exemplo de uso
obj_principal={}
objeto_json = {}


# Exemplo de uso
texto = """
AGEDSECT linha 1
         linha 2
         linha 3
AGE40MO1 linha 6
AGE40MO2 linha 6         

Symbol   linha 5
AGE40MO3 linha 6
AGE40MO4 linha 6
AGE40MO5 linha 6
AGEDSECT linha 1

BCPDSECT linha 1
"""

prefixo_alvo = "XXXXXX"
prefixos_ignorados = ["BBBBBB", "CCCCCC"]

resultado = salvar_linhas_com_prefixo(texto, prefixo_alvo, prefixos_ignorados,objeto_json)

adicionar_objeto(obj_principal,'AGEDSECT',objeto_json)

json_str = json.dumps(obj_principal, indent=4)  # 4 espaços para indentação
print(json_str)



<!DOCTYPE html>
<html>
<head>
    <title>Navegador JSON</title>
</head>
<body>
    <h1>Navegador JSON</h1>
    <div id="jsonNavigator"></div>

    <script>
        var jsonNavigator = document.getElementById("jsonNavigator");

        async function fetchJsonData() {
            try {
                var response = await fetch('/snaprunner', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // You can add data here if needed
                });

                if (response.ok) {
                    var jsonData = await response.json();
                    renderObject(jsonData, jsonNavigator);
                } else {
                    console.error('Failed to fetch JSON data');
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        }

        function renderObject(obj, element) {
            var ul = document.createElement("ul");

            for (var key in obj) {
                if (typeof obj[key] === "object") {
                    var li = document.createElement("li");
                    li.textContent = key;
                    li.addEventListener("click", async function () {
                        ul.innerHTML = "";
                        var response = await fetch('/snaprunner', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ key: key }) // You can add data here if needed
                        });
                        if (response.ok) {
                            var nestedJsonData = await response.json();
                            renderObject(nestedJsonData, ul);
                        }
                    });
                    ul.appendChild(li);
                } else {
                    var li = document.createElement("li");
                    li.textContent = key + ": " + obj[key].toString();
                    ul.appendChild(li);
                }
            }

            element.appendChild(ul);
        }

        fetchJsonData();
    </script>
</body>
</html>

<!DOCTYPE html>
<html>
<head>
    <title>Navegador JSON</title>
</head>
<body>
    <h1>Navegador JSON</h1>
    <div id="jsonNavigator"></div>

    <script>
        var dados = {
            "AGEDSECT": {
                "AGE35CDA": ["00001A", "2233"],
                "AGE35CDB": ["00001A", "2233"],
                "AGE35CDC": ["00001A", "2233"]
            },
            "AG2DSECT": {
                "AGE25CDA": ["00001A", "2233"],
                "AGE25CDB": ["00001A", "2233"],
                "AGE25CDC": ["00001A", "2233"]
            }
        };

        var jsonNavigator = document.getElementById("jsonNavigator");

        function renderObject(obj, element) {
            var ul = document.createElement("ul");

            for (var key in obj) {
                if (typeof obj[key] === "object") {
                    var li = document.createElement("li");
                    li.textContent = key;
                    li.addEventListener("click", function () {
                        ul.innerHTML = "";
                        renderObject(obj[key], ul);
                    });
                    ul.appendChild(li);
                } else {
                    var li = document.createElement("li");
                    li.textContent = key + ": " + obj[key].toString();
                    ul.appendChild(li);
                }
            }

            element.appendChild(ul);
        }

        renderObject(dados, jsonNavigator);
    </script>
</body>
</html>


