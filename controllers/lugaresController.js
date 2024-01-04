const Lugar = require('../models/lugarModel');

exports.adicionarLugar = async (req, res) => {
    const {
        nome, descricao, rua, cep, cnpj, cidade, bairro, regiao, entrada, latitude, longitude, linha_metro, estacao, estrelas,
        avaliacao_clientes, avaliacao_pagina, descricao_pagina, link_pagina, midia_pagina,
        acessibilidade, musica, estacionamento, cover, kids, website, premio, estilo_musical,
        cozinha, local, preco, tipo_evento, hobby, ambiente, cartao, dias, nivel, link_cardapio, horarios_funcionamento, pet, estilo_servico,
        glutenfree, lactosefree
    } = req.body;

    try {
        // Verifica se o id já existe na base de dados
        const lugarExistente = await Lugar.findOne({ nome, cep, cnpj });
        if (lugarExistente) {
            return res.status(400).json({ message: 'Erro: um lugar com esse nome, CEP e CNPJ já existe.' });
        }

        // Cria um novo lugar se o id não existir
        const novoLugar = new Lugar({
            nome, descricao, rua, cep, cnpj, cidade, bairro, regiao, entrada, latitude, longitude, linha_metro, estacao, estrelas,
            avaliacao_clientes, avaliacao_pagina, descricao_pagina, link_pagina, midia_pagina,
            acessibilidade, musica, estacionamento, cover, kids, website, premio, estilo_musical,
            cozinha, local, preco, tipo_evento, hobby, ambiente, cartao, dias, nivel, link_cardapio, horarios_funcionamento, pet, estilo_servico,
            glutenfree, lactosefree
        });

        await novoLugar.save();
        res.status(201).json(novoLugar);
    } catch (err) {
        console.log(err.message);
        res.status(500).json({ message: err.message });
    }
};


// Nova função para buscar lugares
exports.buscarLugares = async (req, res) => {
    try {
        // Obtém os campos válidos do esquema do modelo
        const camposValidos = Object.keys(Lugar.schema.paths);

        const query = {};
        for (const key in req.query) {
            // Verifica se o campo é válido
            if (!camposValidos.includes(key)) {
                return res.status(400).json({ message: `Parâmetro inválido: ${key}` });
            }

            // Constrói a query com base nos campos válidos
            if (req.query[key] instanceof Array) {
                query[key] = { $in: req.query[key] };
            } else {
                query[key] = req.query[key];
            }
        }

        const lugares = await Lugar.find(query);
        res.status(200).json(lugares);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
};
