# Fase 1: Imagem base Python
FROM python:3.10 as build-python

# Cria diretório de trabalho
WORKDIR /usr/src/app

# Copia os arquivos de requirements (se você tiver)
COPY requirements.txt ./

# Atualiza pip e instala as bibliotecas Python necessárias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o resto dos arquivos
COPY . .

# Fase 2: Imagem base Node.js
FROM node:14

# Cria diretório de trabalho
WORKDIR /usr/src/app

# Copia os arquivos Python construídos na primeira fase
COPY --from=build-python /usr/src/app .

# Copia o arquivo package.json e package-lock.json para o diretório de trabalho
COPY package*.json ./

# Instala as dependências do Node.js
RUN npm install

# Expõe a porta que o app vai rodar
EXPOSE 3000

# Comando para iniciar o app
CMD [ "node", "coderunner.js" ]
