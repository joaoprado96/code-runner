<!DOCTYPE html>
<html>
<head>
<style>
  table {
    border-collapse: collapse;
    width: 100%;
  }

  th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
  }

  tr.success {
    background-color: green;
  }
</style>
</head>
<body>

<table>
  <tr>
    <th>Coluna 1</th>
    <th>Coluna 2</th>
    <th>Coluna 3</th>
    <th>Coluna 4</th>
  </tr>
  <tr>
    <td>Dado 1</td>
    <td>Dado 2</td>
    <td>Dado 3</td>
    <td>Sucesso</td>
  </tr>
  <tr class="success">
    <td>Dado 4</td>
    <td>Dado 5</td>
    <td>Dado 6</td>
    <td>Sucesso</td>
  </tr>
  <tr>
    <td>Dado 7</td>
    <td>Dado 8</td>
    <td>Dado 9</td>
    <td>Outro Valor</td>
  </tr>
</table>

</body>
</html>










<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Principal</title>
</head>
<body>
    <button onclick="abrirJanela('caminho_do_seu_arquivo.txt')">Abrir Janela</button>

    <script>
        function abrirJanela(caminhoDoArquivo) {
            const url = 'nova_janela.html?arquivo=' + encodeURIComponent(caminhoDoArquivo);
            window.open(url, '_blank', 'width=500, height=400');
        }
    </script>
</body>
</html>


<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova Janela</title>
</head>
<body>
    <pre id="conteudo"></pre> <!-- Usando a tag <pre> para manter a formatação do arquivo de texto -->

    <script>
        function getQueryParam(name) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        }

        function carregarArquivo() {
            const caminhoDoArquivo = getQueryParam('arquivo');
            fetch(caminhoDoArquivo)
                .then(response => response.text())
                .then(data => {
                    document.getElementById('conteudo').textContent = data;
                })
                .catch(error => {
                    console.error("Erro ao carregar o arquivo:", error);
                });

            // Atualizar a página a cada 2 segundos
            setTimeout(function(){
                location.reload();
            }, 2000);
        }

        carregarArquivo();
    </script>
</body>
</html>
