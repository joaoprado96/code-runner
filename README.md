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
API

A API tem três pontos de acesso:

    POST /codes/:scriptName: inicia a execução de um script Python especificado pelo scriptName. O número de execuções pode ser definido no cabeçalho 'num-scripts' (por padrão, é 1; o máximo permitido é 100).
    GET /codes/:scriptName: verifica se um script Python especificado pelo scriptName está sendo executado.
    DELETE /codes/:scriptName: interrompe a execução de um script Python especificado pelo scriptName.

## Exemplo de uso

Para iniciar um script Python chamado 'test', faça uma requisição POST para 'http://localhost:3000/codes/test'. Para verificar se 'test.py' está em execução, faça uma requisição GET para 'http://localhost:3000/codes/test'. Para parar 'test.py', faça uma requisição DELETE para 'http://localhost:3000/codes/test'.
Observações

Os scripts Python devem estar no diretório 'codes' e ter a extensão '.py'. A aplicação passará o corpo da solicitação POST como argumento para o script Python. A aplicação imprimirá as mensagens de saída do script Python no console e terminará a execução do script quando ele finalizar.

## Licença

Este projeto está sob a licença MIT. ss