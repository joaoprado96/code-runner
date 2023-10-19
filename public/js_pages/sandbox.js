let dados; 
const datasets = {
    GRBE: {
        CHAVE_GRBE_1: ['OPC1', 'OPC2', 'OPC3'],
        CHAVE_GRBE_2: ['OPC1', 'OPC2']
    },
    IMS: {
        CHAVE_IMS_1: ['OPC1', 'OPC2', 'OPC3', 'OPC4'],
        CHAVE_IMS_2: ['OPC1', 'OPC2']
    },
    CICS: {
        CHAVE_CICS_1: ['OPC1', 'OPC2', 'OPC3', 'OPC4', 'OPC5'],
        CHAVE_CICS_2: ['OPC1', 'OPC2']
    },
    BATCH: {
        CHAVE_BATCH_1: ['OPC1', 'OPC2', 'OPC3'],
        CHAVE_BATCH_2: ['OPC1', 'OPC2', 'OPC3', 'OPC4']
    }
};

function mostrarConteudo(funcionalidade) {
    const conteudo = document.getElementById('conteudo');
    const menuSuperior = document.getElementById('menu-superior');
    menuSuperior.style.display = 'none'; 
    conteudo.innerHTML = ''; 

    if (funcionalidade === 'home') {
        conteudo.innerHTML = `
            <h2>Agradecemos por sua visita ao Sandbox Runner!!!</h2>
            <p>
                A ferramenta Sandbox Runner foi desenvolvida pensando nas necessidades específicas de ambientes Mainframe. 
            </p>
            <p>    
                Ela permite virtualizar e criar ambientes de teste de aplicação mainframe de forma isolada. 
            </p>
            <p>                
                Com essa ferramenta, cada usuário tem a capacidade de criar sua própria pista de teste sem impactar os outros usuários. 
            </p>
            <p>   
                É uma solução ideal para equipes que buscam otimizar seus processos de teste, garantindo integridade e eficiência.
            </p>
            <p>
                É importante salientar que ainda estamos em fase de desenvolvimento e melhorias contínuas. 
            </p>
            <p>
                Criar um processo sofisticado que permita configurações personalizadas, além de oferecer recursos para a reciclagem de arquivos, tabelas e módulos de programas. 
            </p>
            <p>
                O objetivo principal é capacitar nossos usuários a executar tarefas de forma paralela, otimizando fluxos de trabalho e maximizando a eficiência. 
            </p>
            <p>
                Pedimos sua paciência e compreensão durante este período, e incentivamos o feedback construtivo para aprimorarmos ainda mais a nossa plataforma.
            </p>
        `;
    } else if (funcionalidade === 'montarJSON') {
        menuSuperior.style.display = 'flex'; 
        menuSuperior.innerHTML = `
            <a href="#" onclick="carregarFormulario('CICS')">CICS</a>
            <a href="#" onclick="carregarFormulario('GRBE')">GRBE</a>
            <a href="#" onclick="carregarFormulario('IMS')">IMS</a>
            <a href="#" onclick="carregarFormulario('BATCH')">BATCH</a>
        `;
        conteudo.innerHTML = `
            <div id="formulario"></div>
            <button onclick="montarJSON()">Preparar Ambiente</button>
        `;
    }
}

function carregarFormulario(opcao) {
    dados = datasets[opcao];
    inicializarFormulario(dados);
}

function inicializarFormulario(dados) {
    const formulario = document.getElementById('formulario');
    formulario.innerHTML = ''; // Limpa o conteúdo anterior

    for (const chave in dados) {
        const divChave = document.createElement('div');
        divChave.className = 'chave';

        const checkboxChave = document.createElement('input');
        checkboxChave.type = 'checkbox';
        checkboxChave.id = chave;
        checkboxChave.onchange = () => toggleOpcoes(chave);

        const labelChave = document.createElement('label');
        labelChave.htmlFor = chave;
        labelChave.textContent = chave;

        divChave.appendChild(checkboxChave);
        divChave.appendChild(labelChave);

        const divOpcoes = document.createElement('div');
        divOpcoes.id = 'opcoes-' + chave;
        divOpcoes.style.marginLeft = '20px';
        divOpcoes.style.display = 'none'; 

        dados[chave].forEach(opcao => {
            const checkboxOpcao = document.createElement('input');
            checkboxOpcao.type = 'checkbox';
            checkboxOpcao.id = opcao + '-' + chave;
            checkboxOpcao.value = opcao;

            const labelOpcao = document.createElement('label');
            labelOpcao.htmlFor = opcao + '-' + chave;
            labelOpcao.textContent = opcao;

            divOpcoes.appendChild(checkboxOpcao);
            divOpcoes.appendChild(labelOpcao);
            divOpcoes.appendChild(document.createElement('br'));
        });

        formulario.appendChild(divChave);
        formulario.appendChild(divOpcoes);
    }
}

function toggleOpcoes(chave) {
    const checkboxChave = document.getElementById(chave);
    const divOpcoes = document.getElementById('opcoes-' + chave);

    if (checkboxChave.checked) {
        divOpcoes.style.display = 'block';
    } else {
        divOpcoes.style.display = 'none';
        const checkboxesOpcoes = divOpcoes.querySelectorAll('input[type="checkbox"]');
        checkboxesOpcoes.forEach(checkbox => checkbox.checked = false);
    }
}

function montarJSON() {
    const resultado = {};

    for (const chave in dados) {
        const checkboxChave = document.getElementById(chave);
        const divOpcoes = document.getElementById('opcoes-' + chave);
        if (checkboxChave.checked) {
            const selecionados = Array.from(divOpcoes.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
            if (selecionados.length > 0) {
                resultado[chave] = selecionados;
            }
        }
    }
    
    console.log(JSON.stringify(resultado));
}

// Ao carregar a página, mostre a home
window.onload = function() {
    mostrarConteudo('home');
}