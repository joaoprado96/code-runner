import re

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

