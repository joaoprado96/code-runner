const jwt = require('jsonwebtoken');
const axios = require('axios');
require('dotenv').config();

const validaAcessoOPA = async (req, res, next) => {
    const token = req.headers['authorization'];
    const path = req.headers['path'];

    console.log(token);

    if (!token) {
        return res.status(401).send({ message: "Token não fornecido" });
    }

    try {
        // Decodificar o token sem verificar a assinatura
        const decoded = jwt.decode(token, { complete: true });

        if (!decoded) {
            return res.status(400).send({ message: "Token inválido ou mal formatado." });
        }

        // Suponha que as roles estão na claim 'roles' do payload do token
        const grupos = decoded.payload.roles;
        console.log(grupos);

        // Continuar com a lógica para verificar o acesso no OPA
        const requestBody = {
            input: {
                token,
                path,
                grupos
            }
        };

        const response = await axios.post('http://localhost:3000/front/valida_opa', requestBody);

        // if (response.data.result === true) {
        if (response.data.resultado === true) {
            next(); // Acesso permitido, continua para o próximo middleware ou rota
        } else {
            res.status(403).send({ message: "Acesso negado pelo OPA" });
        }
    } catch (error) {
        console.error(error);
        res.status(500).send({ message: "Erro desconhecido ao decodificar o token" });
    }
};

module.exports = {
    validaAcessoOPA
}
