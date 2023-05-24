# CodeRunner

CodeRunner é uma aplicação backend construída com Node.js que permite a execução de scripts Python a partir de requisições HTTP. A aplicação utiliza Express para configurar o servidor, bodyParser para analisar solicitações JSON e a biblioteca PythonShell para executar os scripts Python.

## Requisitos

    Node.js
    npm
    Python

## Dependências

    Express
    Body-parser
    Python-shell
    Axios
    File System (fs)
    Path

## Instalação

Clone este repositório e instale as dependências com o seguinte comando:
```
npm install
```

## Uso

Para iniciar a aplicação, execute o seguinte comando:
```
node coderunner.js
```

A aplicação agora estará ouvindo na porta 3000.


### POST /codes/:scriptName: 

Inicia a execução de um script Python especificado pelo scriptName. O número de execuções pode ser definido no cabeçalho `num-scripts` (por padrão, é 1; o máximo permitido é 100).

### GET /codes/:scriptName: 

Verifica se um script Python especificado pelo scriptName está sendo executado.

### DELETE /codes/:scriptName: 

Interrompe a execução de um script Python especificado pelo scriptName.

## Exemplo de uso

Antes de utilizar você deve criar um script Python dentro da pasta codes para executar alguma ação, após isso:

Para iniciar um script Python chamado 'test', faça uma requisição POST para `http://localhost:3000/codes/test` 

Para verificar se 'test.py' está em execução, faça uma requisição GET para `http://localhost:3000/codes/test` 

Para parar 'test.py', faça uma requisição DELETE para `http://localhost:3000/codes/test`


## Observações

Os scripts Python devem estar no diretório 'codes' e ter a extensão '.py'. A aplicação passará o corpo da solicitação POST como argumento para o script Python. A aplicação imprimirá as mensagens de saída do script Python no console e terminará a execução do script quando ele finalizar.


## Detalehs do funcionamento

O aplicativo CodeRunner é uma aplicação `backend` construída em `Node.js` que tem como principal objetivo executar scripts Python através de requisições HTTP. Aqui está uma visão detalhada de como o código funciona:

### Importação de módulos: 

No início do código, vários módulos do Node.js e bibliotecas de terceiros são importados, incluindo express, bodyParser, PythonShell, fs, path e axios.

### Inicialização do servidor express: 

Em seguida, uma instância do servidor express é criada e a porta na qual o servidor vai ouvir é definida como 3000.

### Middleware: 

O middleware bodyParser.json() é usado para que o servidor possa analisar corretamente as solicitações recebidas que contêm JSON.

### Inicialização da estrutura de controle de scripts:

É criada uma variável "runningScripts" que será um objeto JavaScript para manter o controle de quais scripts Python estão atualmente em execução.

### Endpoints do servidor: 

São definidos três endpoints para o servidor:

[POST] Este endpoint inicia a execução de um script Python especificado pelo parâmetro "scriptName" da rota. O número de instâncias do script a serem iniciadas é determinado pelo cabeçalho 'num-scripts' na solicitação, com um valor padrão de 1 e um limite máximo de 100. Cada instância do script é executada usando a biblioteca PythonShell, com o corpo da solicitação POST sendo passado como argumento para o script.

[GET] Este endpoint verifica se um script Python especificado pelo parâmetro "scriptName" da rota está em execução. Responde com uma mensagem indicando o status de execução do script.

[DELETE] Este endpoint interrompe a execução de um script Python especificado pelo parâmetro "scriptName" da rota. Faz isso enviando um sinal de 'SIGINT' para o processo filho Python associado ao script e, em seguida, remove a referência ao script do objeto runningScripts.

    
### Iniciar o servidor: 

Finalmente, o servidor express é iniciado e começa a ouvir na porta definida.

Este aplicativo é útil quando você precisa executar e gerenciar a execução de vários scripts Python através de um serviço web, possibilitando um controle preciso sobre a execução e o término dos scripts. Além disso, ao utilizar a biblioteca PythonShell, o servidor pode imprimir a saída dos scripts em tempo real, tornando mais fácil o monitoramento do progresso de cada script.

## Licença

Este projeto está sob a licença MIT. ss