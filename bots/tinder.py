import pygetwindow as gw
import pyautogui
import time
import random

# Obtém uma lista de todas as janelas abertas
janelas_abertas = gw.getAllTitles()

# Imprime o título de cada janela
for janela in janelas_abertas:
    if 'Tinder' in janela:
        print(janela)
        titulo_da_janela = janela  # Substitua pelo título da sua janela

# Defina o caminho para a imagem que você deseja encontrar
imagem_a_localizar = 'img/match.PNG'

# Obtenha a janela com o título especificado
janela = gw.getWindowsWithTitle(titulo_da_janela)

if len(janela) == 0:
    print(f"Janela '{titulo_da_janela}' não encontrada.")
else:
    janela = janela[0]
    janela.activate()


    while True:
       
        # Tente localizar a imagem em toda a tela
        localizacao = pyautogui.locateOnScreen(imagem_a_localizar)
        if localizacao is not None:
            x, y, _, _ = localizacao  # Obtenha as coordenadas
            # Ajuste as coordenadas para o clique (subtrai 10 da coordenada x e 5 da coordenada y, por exemplo)
            x -= 0  # Ajuste para a esquerda
            y -= 0   # Ajuste para cima
            pyautogui.click(x, y)
            intervalo_aleatorio = random.uniform(0.1, 0.5)
            print(f"A coordenada encontrada x={x} e y={y} e o tempo é {intervalo_aleatorio}s")
            time.sleep(intervalo_aleatorio)
            pyautogui.click(x-300, y)
            print(f"Imagem encontrada e clicada. Aguardando {intervalo_aleatorio:.2f} segundos.")
        
        else:
            print(f"Imagem não encontrada na tela.")