# Imagem base com Python e Node.js
FROM nikolaik/python-nodejs:latest

# Cria diretório de trabalho
WORKDIR /usr/src/app

# Atualiza pip e instala as bibliotecas Python necessárias
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install requests && \
    pip install asyncio

# Copia o resto dos arquivos
COPY . .

# Copia o arquivo package.json e package-lock.json para o diretório de trabalho
COPY package*.json ./

# Instala as dependências do Node.js
RUN npm install && \
    npm install express && \
    npm install axios && \
    npm install body-parser && \
    npm install python-shell

# Expõe a porta que o app vai rodar
EXPOSE 3000

# Comando para iniciar o app
CMD [ "node", "coderunner.js" ]
