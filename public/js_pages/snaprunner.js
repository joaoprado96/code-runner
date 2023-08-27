document.addEventListener("DOMContentLoaded", function() {
    // Seu código aqui
    $(document).ready(function() {
        $('.select2').select2({
            placeholder: 'Selecione uma opção depois de carregar o arquivo',
            allowClear: true
        });
      });
      const modal   = document.getElementById("myModal");
      const modal2  = document.getElementById("myModal2");
      const btn     = document.getElementById("openModalBtn");
      const btn2    = document.getElementById("openModalBtn2");
      const span    = document.getElementsByClassName("close")[0];
      const span2    = document.getElementsByClassName("close2")[0];

    
      btn.onclick = function() {
        const formElement3     = document.getElementById("jsonAREAS");
        const formElement4     = document.getElementById("jsonAREAS2");
        formElement3.innerHTML = '';
        formElement4.innerHTML = '';
        formElement3.reset();
        formElement4.reset();
        // A função 'algumaFuncaoParaPegarJSON()' deve retornar o JSON que você quer exibir
        renderJsonAsForm(dados, formElement3);
        modal.style.display = "block";
      }
    
      span.onclick = function() {
        modal.style.display = "none";
      }
    
      window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      }
      btn2.onclick = function() {
        const formElement3     = document.getElementById("jsonAREAS");
        const formElement4     = document.getElementById("jsonAREAS2");
        formElement3.innerHTML = '';
        formElement4.innerHTML = '';
        formElement3.reset();
        formElement4.reset();
        const fields = ["AGEDSECT.AGE35CDA","AGEDSECT.AGE35CDB"];
        const extractedFields = extractFieldsFromJson(dados, fields);
        console.log(extractedFields)

        // A função 'algumaFuncaoParaPegarJSON()' deve retornar o JSON que você quer exibir
        renderJsonAsForm(extractedFields, formElement4);
        modal2.style.display = "block";
      }
    
      span2.onclick = function() {
        modal2.style.display = "none";
      }
    
      window.onclick = function(event) {
        if (event.target == modal2) {
          modal2.style.display = "none";
        }
      }      
  });

var dados;
var selectElement   = document.getElementById("areaSelect");
var jsonNavigator   = document.getElementById("jsonNavigator");
var breadcrumb      = document.getElementById("breadcrumb");
var dataValues      = document.getElementById("dataValues");
var formElement     = document.getElementById("jsonForm");
var formElement2    = document.getElementById("jsonBPH");

async function carregar(){
    const usuario = document.getElementById('usuario').value;
    const senha   = document.getElementById('senha').value;
    const baseline= document.querySelector('input[name="baseline"]:checked').value;
    const pacote  = document.getElementById('pacote').value;
    const versao  = document.getElementById('versao').value;
    const datasets= document.getElementById('datasets').value;
    const id_snap = document.getElementById('id_snap').value;
    const modo    = document.querySelector('input[name="modo"]:checked').value;
    if (!usuario || !senha || !datasets || !id_snap ){
        alert("Preencha as informações minimas: usuario, senha, arquivo e id do snap")
        return;
    }
    // Resetar os elementos
    while(selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }
    jsonNavigator.innerHTML     = '';
    breadcrumb.innerHTML        = '';
    dataValues.innerHTML        = '';
    formElement.innerHTML       = '';
    formElement2.innerHTML      = '';
    formElement.reset();
    formElement2.reset();
    document.getElementById('carregarButton').disabled   = true;

    runVLD();
    runPRE();
    runBPH();
}

async function liberar(){
    document.getElementById('carregarButton').disabled  = false;
    document.getElementById('analisarButton').disabled  = true;
    document.getElementById('openModalBtn').disabled    = true;
    document.getElementById('openModalBtn2').disabled   = true;
    document.getElementById('liberarButton').disabled   = true;
    document.getElementById('usuario').disabled         = false;
    document.getElementById('senha').disabled           = false;
    document.getElementById('pacote').disabled          = false;
    document.getElementById('versao').disabled          = false;
    document.getElementById('datasets').disabled        = false;
    document.getElementById('id_snap').disabled         = false;
    // Resetar os elementos
    while(selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }
    jsonNavigator.innerHTML     = '';
    breadcrumb.innerHTML        = '';
    dataValues.innerHTML        = '';
    formElement.innerHTML       = '';
    formElement2.innerHTML      = '';
    formElement.reset();
    formElement2.reset();
}


async function runVLD(){
    const usuario = document.getElementById('usuario').value;
    const senha   = document.getElementById('senha').value;
    const baseline= document.querySelector('input[name="baseline"]:checked').value;
    const pacote  = document.getElementById('pacote').value;
    const versao  = document.getElementById('versao').value;
    const datasets= document.getElementById('datasets').value;
    const id_snap = document.getElementById('id_snap').value;
    const modo    = document.querySelector('input[name="modo"]:checked').value;
    const responseV = await fetch('/front/snaprunnerVLD',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({racf: usuario,senha:senha,pacote:pacote,baseline:baseline,versao:versao,datasets:datasets,id_snap:id_snap,modo:modo})
    });
    dadosV = await responseV.json();
    
    // Valida se os códigos de validação acusaram erro
    if (dadosV.status == "Falha"){
        alert(dadosV.mensagem);
        return;
    }
    // Continuar com as tratativas trazer a lista de CSECT disponíveis
    if (dadosV.status != 'Falha'){
        document.getElementById('analisarButton').disabled  = false;
        document.getElementById('liberarButton').disabled   = false;
        document.getElementById('usuario').disabled         = true;
        document.getElementById('senha').disabled           = true;
        document.getElementById('pacote').disabled          = true;
        document.getElementById('versao').disabled          = true;
        document.getElementById('datasets').disabled        = true;
        document.getElementById('id_snap').disabled         = true;
        for (var i = 0; i < dadosV.areas.length; i++) {
            var option = document.createElement("option");
            option.value = dadosV.areas[i];
            option.text = dadosV.areas[i];
            selectElement.appendChild(option);
          }
    }
}

async function runPRE(){
    const usuario = document.getElementById('usuario').value;
    const senha   = document.getElementById('senha').value;
    const baseline= document.querySelector('input[name="baseline"]:checked').value;
    const pacote  = document.getElementById('pacote').value;
    const versao  = document.getElementById('versao').value;
    const datasets= document.getElementById('datasets').value;
    const id_snap = document.getElementById('id_snap').value;
    const modo    = document.querySelector('input[name="modo"]:checked').value;
    const responseP = await fetch('/front/snaprunnerPRE',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({racf: usuario,senha:senha,pacote:pacote,baseline:baseline,versao:versao,datasets:datasets,id_snap:id_snap,modo:modo})
    });
    dadosP = await responseP.json();
    renderJsonAsForm(dadosP, formElement);
}

async function runBPH(){
    const usuario = document.getElementById('usuario').value;
    const senha   = document.getElementById('senha').value;
    const baseline= document.querySelector('input[name="baseline"]:checked').value;
    const pacote  = document.getElementById('pacote').value;
    const versao  = document.getElementById('versao').value;
    const datasets= document.getElementById('datasets').value;
    const id_snap = document.getElementById('id_snap').value;
    const modo    = document.querySelector('input[name="modo"]:checked').value;
    const responseB = await fetch('/front/snaprunnerBPH',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({racf: usuario,senha:senha,pacote:pacote,baseline:baseline,versao:versao,datasets:datasets,id_snap:id_snap,modo:modo})
    });
    dadosB = await responseB.json();
    
    // Valida se os códigos de validação acusaram erro
    if (dadosB.status == "Falha"){
        alert(dadosB.mensagem);
        return;
    }
    // Continuar com as tratativas trazer a lista de CSECT disponíveis
    if (dadosB.status != 'Falha'){
        renderJsonAsForm(dadosB, formElement2);
    }
}

async function analisar(){
    const usuario = document.getElementById('usuario').value;
    const senha   = document.getElementById('senha').value;
    const baseline= document.querySelector('input[name="baseline"]:checked').value;
    const pacote  = document.getElementById('pacote').value;
    const versao  = document.getElementById('versao').value;
    const datasets= document.getElementById('datasets').value;
    const id_snap = document.getElementById('id_snap').value;
    const modo    = document.querySelector('input[name="modo"]:checked').value;
    var selectedOptions = $('#areaSelect').val();

    if (!usuario || !senha || !baseline || !versao || !datasets || !id_snap || !modo){
        alert("Está faltando preencher dados de entrada")
        return;
    }
    const response = await fetch('/front/snaprunnerRUN',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify({racf: usuario,senha:senha,pacote:pacote,baseline:baseline,versao:versao,datasets:datasets,id_snap:id_snap,modo:modo,areas:selectedOptions})
    });
    dados = await response.json();
    renderObject(dados)
    document.getElementById('openModalBtn').disabled    = false;
    document.getElementById('openModalBtn2').disabled   = false;
}

function renderJsonAsForm(obj, element) {
    for (var key in obj) {
        var value = obj[key];
        var fieldSet = document.createElement('fieldset');
        var legend = document.createElement('legend');
        legend.innerHTML = key;
        fieldSet.appendChild(legend);

        if (Array.isArray(value)) {
            var arrayDiv = document.createElement('div');
            arrayDiv.className = 'array-container';
            value.forEach(function (item) {
                var itemDiv = document.createElement('div');
                itemDiv.className = 'array-item';
                itemDiv.textContent = item;
                arrayDiv.appendChild(itemDiv);
            });
            fieldSet.appendChild(arrayDiv);
        } else if (typeof value === 'object') {
            renderJsonAsForm(value, fieldSet);
        } else {
            var input = document.createElement('input');
            input.type = 'text';
            input.value = value;
            fieldSet.appendChild(input);
        }

        element.appendChild(fieldSet);
    }
}

function renderObject(obj, breadcrumbPath = []) {
    dataValues.innerHTML = "";
    jsonNavigator.innerHTML = "";

    // Adiciona o botão de voltar, se estiver em um nível que não seja o raiz
    if (breadcrumbPath.length > 0) {
        const backButton = document.createElement("button");
        backButton.textContent = "Voltar";
        backButton.onclick = () => {
            breadcrumbPath.pop();
            let obj = dados;
            breadcrumbPath = [];
            breadcrumb.innerHTML = "";
            renderObject(obj, breadcrumbPath);
        };
        jsonNavigator.appendChild(backButton);
    }

    const select = document.createElement("select");
    select.appendChild(new Option("-- Selecione --", ""));

    for (const key in obj) {
        const option = new Option(key, key);
        select.appendChild(option);
    }

    select.addEventListener("change", function() {
        if (select.value) {
            if (breadcrumbPath.length > 1){
                breadcrumbPath.pop();
            }
            breadcrumbPath.push(select.value);
            updateBreadcrumb(breadcrumbPath);
            if (Array.isArray(obj[select.value])) {
                displayValues(obj[select.value]);
            } else {
                renderObject(obj[select.value], breadcrumbPath);
            }
        }
    });

    jsonNavigator.appendChild(select);
}

function updateBreadcrumb(breadcrumbPath) {
    breadcrumb.innerHTML = breadcrumbPath.join(" > ");
}

function displayValues(values) {
dataValues.innerHTML = "";
    // Se existir o primeiro valor
    if (values[0]) {
    const div1 = document.createElement("div");
    div1.textContent = `Deslocamento: ${values[0]}`;
    dataValues.appendChild(div1);
    }

    // Se existir o segundo valor
    if (values[1]) {
    const div2 = document.createElement("div");
    div2.textContent = `Tamanho do campo: ${values[1]}`;
    dataValues.appendChild(div2);
    }
    // Se existir o segundo valor
    if (values[2]) {
        const div3 = document.createElement("div");
        div3.textContent = `Conteúdo do campo: ${values[2]}`;
        dataValues.appendChild(div3);
        }
}

function extractFieldsFromJson(jsonObj, fieldsToExtract) {
    const result = {};

    function helper(obj, field, res) {
        let [first, ...rest] = field.split(".");
        if (!obj.hasOwnProperty(first)) return;

        if (rest.length === 0) {
            res[first] = obj[first];
        } else {
            res[first] = res[first] || {};
            helper(obj[first], rest.join("."), res[first]);
        }
    }

    fieldsToExtract.forEach(field => {
        helper(jsonObj, field, result);
    });

    return result;
}