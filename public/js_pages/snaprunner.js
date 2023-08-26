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

var descricao = {
    "00001A": "Descrição para 00001A",
    "2233": "Descrição para 2233"
};

var jsonNavigator = document.getElementById("jsonNavigator");
var breadcrumb = document.getElementById("breadcrumb");
var dataValues = document.getElementById("dataValues");

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
renderObject(dados);
