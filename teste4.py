
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


1 Selection View Go Run Terminal
Help
CONTROL
E VO ..
«> snaprunner.html
# snaprunner.css
public > Is pages > 15 snaprunnerjs › ( analisar
† incidentrunner.py
e (Ctri+ Enter to commit on "ma...
var dados;
V Commit
es
unner.py front
var JsonNavigator - document.getElementById("¡sonNavigator");
var breadcrumb - document. getElementById("breadcrumb");
var dataValues • document.getElementByld("dataValues");
itau-mi-testes-coderunn
us snaprunner.is ×
 snaprunner.py 9+, M O
 regressivo.py
• 00A13
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
async function analisar() A
// Obtenha o valor do usuário e da senha dos elementos de entrada
const usuario
•document.getElementById('usuario').value;
const senha
•document.getElementById('senha*).value:
const pacote
•document-getElementById(°pacote°).value;
I
const versao
•document.getElementById(°versao°).value;
const datasets - document-getElementById("datasets") . value;
const id_snap - document.getElementById("¡d_snap") .value;
alert ("Vamos processar sua solicitação, aguarde até aparecer as opções para navegar nas areas de memória, o tempo estimado é de 10 segundos")
// Verifique se o usuário e a senha foram preenchidos
if (Susuario II Isenha) {
return; // Pare a execução da função
const response2 - await fetch(*/front/snaprunner',
method: 'POST',
headers: {
"Content-Type°: 'application/json°
// Inclua o usuário e a senha no corpo da solicitação
3);
bodys JSON.stringify(fracf: usuario, senha: senha, pacote:pacote, versao: versao, datasets datasets, 16_snap: id_snap))
dados - await response2.json();
render0bject (dados)
function render0bject (obj, breadcrumbPatt - [1) {
dataValues.innerHIMLe
jsonNavigatorinnerhTML
ao.
// Adiciona o botão de voltar, se estiver em um nível que não seja o raiz
1f (breadcrumbPath. length › 0) {
const backButton - document.createElement ("button");
backButton.textContent-"Voltar"3
backButton.onclick - () => {
breadcrumbPath.pop();
let obj - dados;
breadcrumbPath =[];
breadcrumb.innerHTML - mag
renderobject (obj, breadcrumbPath);
}8
jsonNavigator.appendChild(backButton);
PROBLEMS
OUTPUT
O CO
TERMINAL
POLYGLOT NOTEBOOK DEBUGCONSOLE
[snaprunner] Code Runners O script snaprunner.py finalizou com Exit Coder 0 Bit Signal; num


