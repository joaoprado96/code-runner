import pygetwindow as gw
import pyautogui
import time
import random

# Obtém uma lista de todas as janelas abertas
janelas_abertas = gw.getAllTitles()

# Imprime o título de cada janela
for janela in janelas_abertas:
    print(janela)

# Defina o título da janela que contém a área desejada
titulo_da_janela = "Instagram - Google Chrome"  # Substitua pelo título da sua janela

# Defina o caminho para a imagem que você deseja encontrar
imagem_a_localizar = 'img/like.PNG'

# Obtenha a janela com o título especificado
janela = gw.getWindowsWithTitle(titulo_da_janela)

if len(janela) == 0:
    print(f"Janela '{titulo_da_janela}' não encontrada.")
else:
    janela = janela[0]
    janela.activate()

    # Defina as coordenadas da região a ser capturada (x, y, largura, altura)
    regiao_de_busca = (100, 100, 1000, 600)  # Substitua pelas coordenadas da sua região
    
    # Defina o número de vezes que deseja rolar a tela
    numero_de_rolagens = 100

    while True:
        pyautogui.scroll(-100)  # Rola para baixo
        
        # Tente localizar a imagem em toda a tela
        localizacao = pyautogui.locateOnScreen(imagem_a_localizar)
        if localizacao is not None:
            x, y, _, _ = localizacao  # Obtenha as coordenadas
            # Ajuste as coordenadas para o clique (subtrai 10 da coordenada x e 5 da coordenada y, por exemplo)
            x -= -3  # Ajuste para a esquerda
            y -= 8   # Ajuste para cima
            pyautogui.click(x, y)
            intervalo_aleatorio = random.uniform(6.0, 15.0)
            print(f"A coordenada encontrada x={x} e y={y} e o tempo é {intervalo_aleatorio}s")
            time.sleep(intervalo_aleatorio)
            pyautogui.scroll(-500)  # Role para baixo
            print(f"Imagem encontrada e clicada. Aguardando {intervalo_aleatorio:.2f} segundos.")
        
        else:
            print(f"Imagem não encontrada na tela.")