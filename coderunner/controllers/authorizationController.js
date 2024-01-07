const jwt = require('jsonwebtoken');
const axios = require('axios');

const secretKey = process.env.JWT_SECRET_KEY; // Use uma chave secreta segura

const generateTokenController = (req, res) => {
    // const userData = {
    //     id: req.body.id, // Suponha que o ID do usuário é enviado no corpo da requisição
    //     roles: req.body.roles // Suponha que as roles do usuário também são enviadas
    // };
    const userData = {
        id: 'JVSPNX', // Suponha que o ID do usuário é enviado no corpo da requisição
        roles: ['MI_GRBE','MI_CODERUNNER'] // Suponha que as roles do usuário também são enviadas
    };

    // Defina as opções do token, como tempo de expiração
    const options = { expiresIn: '1h' };

    try {
        // Gera o token
        const token = jwt.sign(userData, secretKey, options);

        res.json({ token: token });
    } catch (error) {
        console.error(error);
        res.status(500).send({ message: 'Erro ao gerar o token JWT' });
    }
};

module.exports = {
    generateTokenController
}