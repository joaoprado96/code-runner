import re


<!DOCTYPE html>
<html>
<head>
  <title>Sua Página</title>
</head>
<body>
  <script>
    // Função para gerar um ID único
    function generateUniqueID() {
      return 'id_' + Math.random().toString(36).substr(2, 9);
    }

    // Verifica se o ID já foi gerado anteriormente e obtém ou gera o ID
    var uniqueID = sessionStorage.getItem('uniqueID');
    if (!uniqueID) {
      uniqueID = generateUniqueID();
      sessionStorage.setItem('uniqueID', uniqueID);
    }

    // Cria um objeto JSON com o ID
    var jsonData = {
      id: uniqueID
    };

    // Exemplo: exibindo o JSON no console
    console.log(jsonData);

    // Você pode usar esse JSON como quiser, por exemplo, enviá-lo para o servidor ou armazená-lo localmente no navegador

  </script>
</body>
</html>














def substituir_racf(linha, racf, sufixo):
    padrao_job = r"//(\w+)\s+JOB(.*)"
    match = re.match(padrao_job, linha)
    if match:
        prefixo = match.group(1)
        resto_linha = match.group(2)
        return f"//{racf}{sufixo} JOB{resto_linha}"
    else:
        return linha

def substituir_racf_no_job(jcl, racf, sufixo):
    # Dividir o JCL em linhas
    linhas = jcl.splitlines()

    # Iterar pelas linhas e substituir a linha que contém o padrão soajda
    for i, linha in enumerate(linhas):
        linhas[i] = substituir_racf(linha, racf, sufixo)

    # Juntar as linhas novamente em um JCL completo
    novo_jcl = "\n".join(linhas)

    return novo_jcl

def verifica_quebra_linhas(texto):
    # Verificar se a variável texto já está dividida em linhas
    if '\n' in texto:
        # A variável texto já está dividida em linhas
        linhas = texto.splitlines()
    else:
        linhas = texto

    return linhas

def remover_caracteres_especiais(texto):
    texto_limpo = texto.replace('\x00', '').replace('\b00', '')
    return texto_limpo

jcl1='''
//XYZ12343   JOB  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//       USER=NOTIFY
//STEP01 EXEC=MISB01
//SYSOUT DD *
//SYSOUT DD *
'''

jcl2='''
//* VINIGIM SEURACF
//XYZ12343   JOB 2    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//       USER=NOTIFY
//STEP01 EXEC=MISB01
//SYSOUT DD *
//SYSOUT DD *
'''

jcl3='''
//* VINIGIM SEURACF
//* JOB PARA TESTE
//XYZ12343   JOB 2  XX  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
//STEP01 EXEC=MISB01
//SYSOUT DD *
//SYSOUT DD *
'''

jcl4='''
//* VINIGIM SEURACF
//XYZ12343   JOB 2  XX  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
/* TESTE DA SOLUÇÃO DO OUTBOUND
//STEP01 EXEC=MISB01
//SYSOUT DD *
//SYSOUT DD *
'''

racf = "JVSPPNX"
sufixo = "J"

# Exemplos de uso:
jcl1_novo = substituir_racf_no_job(jcl1, racf, sufixo)
jcl2_novo = substituir_racf_no_job(jcl2, racf, sufixo)
jcl3_novo = substituir_racf_no_job(jcl3, racf, sufixo)
jcl4_novo = substituir_racf_no_job(jcl4, racf, sufixo)

print(jcl1_novo)
print("-------")
print(jcl2_novo)
print("-------")
print(jcl3_novo)
print("-------")
print(jcl4_novo)


<!DOCTYPE html>
<html>
<head>
    <title>Pop-up com formulário</title>
</head>
<body>

<!-- Botão que abre o pop-up -->
<button onclick="openPopup()">Clique aqui para digitar informações</button>

<!-- Pop-up -->
<div id="popup" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #f9f9f9; padding: 20px; border: 1px solid #ccc;">
    <h2>Informe suas informações:</h2>
    <form>
        <label for="nome">Nome:</label>
        <input type="text" id="nome" required><br>
        <label for="email">E-mail:</label>
        <input type="email" id="email" required><br>
        <input type="submit" value="Enviar">
    </form>
    <button onclick="closePopup()">Fechar</button>
</div>

<script>
function openPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "block";
}

function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
}
</script>

</body>
</html>


import mysql.connector

# Função para conectar ao banco de dados
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="seu_usuario",
        password="sua_senha",
        database="sua_base_de_dados"
    )

def deletar_registro_por_id(registro_id):
    try:
        connection = conectar_bd()
        cursor = connection.cursor()

        # Deleta o registro com o ID informado
        delete_query = "DELETE FROM logs WHERE id = %s"
        cursor.execute(delete_query, (registro_id,))

        connection.commit()
        print("Registro deletado com sucesso.")
    except mysql.connector.Error as error:
        print(f"Erro ao deletar registro: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def alterar_registro_por_id(registro_id, novos_dados):
    try:
        connection = conectar_bd()
        cursor = connection.cursor()

        # Atualiza os campos com os novos dados para o registro com o ID informado
        update_query = "UPDATE logs SET "
        update_values = ", ".join([f"{campo} = %s" for campo in novos_dados.keys()])
        update_query += update_values + " WHERE id = %s"

        # Concatenando os valores novos com o ID do registro
        valores = list(novos_dados.values())
        valores.append(registro_id)

        cursor.execute(update_query, valores)

        connection.commit()
        print("Registro alterado com sucesso.")
    except mysql.connector.Error as error:
        print(f"Erro ao alterar registro: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



<!DOCTYPE html>
<html>
<head>
    <title>Alterar Label com Botão</title>
</head>
<body>

<!-- Label que será alterada -->
<label id="conteudo-label">Conteúdo Inicial</label>

<!-- Botão que irá alterar o conteúdo do label -->
<button onclick="alterarConteudoLabel()">Clique para Alterar</button>

<script>
function alterarConteudoLabel() {
    // Obtém o elemento do label pelo seu ID
    var label = document.getElementById("conteudo-label");

    // Altera o conteúdo do label
    label.innerHTML = "Novo Conteúdo do Label";
}
</script>

</body>
</html>


<!DOCTYPE html>
<html>
<head>
    <title>Ícone como Botão</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>

<!-- Conteúdo da página aqui -->

</body>
</html>


<!-- Exemplo de botão com ícone usando a classe 'fas' da Font Awesome -->
<button><i class="fas fa-heart"></i> Curtir</button>


Submit (Enviar):

Ícone: <i class="fas fa-paper-plane"></i>
Significado: O ícone do avião de papel é frequentemente usado para representar a ação de envio ou submissão.
Aprovar:

Ícone: <i class="fas fa-check-circle"></i>
Significado: O ícone do círculo de seleção com um sinal de "check" é comumente usado para representar aprovação ou confirmação.
Logs:

Ícone: <i class="fas fa-clipboard-list"></i>
Significado: O ícone da lista de clipboard representa logs ou registros, frequentemente usado em sistemas para mostrar atividades ou eventos registrados.
Alterar:

Ícone: <i class="fas fa-edit"></i>
Significado: O ícone do lápis é geralmente usado para representar a ação de edição ou alteração.
Visualizar:

Ícone: <i class="fas fa-eye"></i>
Significado: O ícone do olho é comumente usado para representar a ação de visualização ou exibição de informações.
Deletar:

Ícone: <i class="fas fa-trash-alt"></i>
Significado: O ícone da lixeira é amplamente utilizado para representar a ação de exclusão ou remoção de elementos.
