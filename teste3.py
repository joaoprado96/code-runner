import difflib
import re

def get_remark(line):
    match = re.search(r'([#@*%$!]\w+[#@*%$!])', line)
    return match.group() if match else None

def comparar_codigos(codigo_original, codigo_alterado):
    d = difflib.Differ()
    linhas_original = codigo_original.splitlines()
    linhas_alterado = codigo_alterado.splitlines()

    comparação = list(d.compare(linhas_original, linhas_alterado))

    linhas_modificadas = []
    linhas_modificadas_conteudo = []
    linhas_incluidas = []
    linhas_incluidas_conteudo = []
    linhas_deletadas = []
    linhas_deletadas_conteudo = []

    novos_remarks = {}
    modificacoes_remarks = {}

    for num_linha, (linha_original, linha_alterado) in enumerate(zip(linhas_original, linhas_alterado), start=1):
        if linha_original != linha_alterado:
            linhas_modificadas.append(num_linha)
            linhas_modificadas_conteudo.append(linha_alterado)
            
            remark_original = get_remark(linha_original)
            remark_alterado = get_remark(linha_alterado)

            if remark_original != remark_alterado:
                modificacoes_remarks[num_linha] = (remark_original, remark_alterado)
        else:
            remark_alterado = get_remark(linha_alterado)
            if num_linha > len(linhas_original):
                novos_remarks[num_linha] = remark_alterado

    linhas_incluidas = [num_linha for num_linha in range(len(linhas_original) + 1, len(linhas_alterado) + 1)]
    linhas_incluidas_conteudo = linhas_alterado[len(linhas_original):]
    linhas_deletadas = [num_linha for num_linha in range(len(linhas_alterado) + 1, len(linhas_original) + 1)]
    linhas_deletadas_conteudo = linhas_original[len(linhas_alterado):]

    return {
        'quantidade_linhas_alteradas': len(linhas_modificadas),
        'linhas_alteradas': linhas_modificadas,
        'linhas_alteradas_conteudo': linhas_modificadas_conteudo,
        'modificacoes_remarks': modificacoes_remarks,
        'novos_remarks': novos_remarks,
        'quantidade_linhas_incluidas': len(linhas_incluidas),
        'linhas_incluidas': linhas_incluidas,
        'linhas_incluidas_conteudo': linhas_incluidas_conteudo,
        'quantidade_linhas_deletadas': len(linhas_deletadas),
        'linhas_deletadas': linhas_deletadas,
        'linhas_deletadas_conteudo': linhas_deletadas_conteudo
    }

# Exemplo de uso
codigo_original = """
linha1 #ABC# linha_modificada
linha2 #DEF#
linha3 linha_modificada #GHI#
linha4 #JKL#
"""

codigo_alterado = """
linha1_modificada #ABC# %nova_linha #123%
linha2_modificada #XYZ# nova_linha $456$
"""

resultado = comparar_codigos(codigo_original, codigo_alterado)

print("Quantidade de linhas alteradas:", resultado['quantidade_linhas_alteradas'])
print("Linhas alteradas:", resultado['linhas_alteradas'])
print("Conteúdo das linhas alteradas:", resultado['linhas_alteradas_conteudo'])
print("Modificações de remarks:", resultado['modificacoes_remarks'])
print("Novos remarks:", resultado['novos_remarks'])
print("Quantidade de linhas incluídas:", resultado['quantidade_linhas_incluidas'])
print("Linhas incluídas:", resultado['linhas_incluidas'])
print("Conteúdo das linhas incluídas:", resultado['linhas_incluidas_conteudo'])
print("Quantidade de linhas deletadas:", resultado['quantidade_linhas_deletadas'])
print("Linhas deletadas:", resultado['linhas_deletadas'])
print("Conteúdo das linhas deletadas:", resultado['linhas_deletadas_conteudo'])
