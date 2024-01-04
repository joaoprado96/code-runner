require('dotenv').config();

const connectDB = require('./config/db');
const lugaresRoutes = require('./routes/lugaresRoutes');


const app = express();

// Conectar ao banco de dados
connectDB();

// Middleware para parsear o corpo das requisições JSON
app.use(express.json());

// Servindo arquivos estáticos
app.use(express.static('public'));

// Definindo as rotas da API
app.use('/api', lugaresRoutes);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));
