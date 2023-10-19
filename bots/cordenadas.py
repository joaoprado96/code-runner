import pyautogui
import time

print("Mova o cursor do mouse para a região desejada...")
time.sleep(5)  # Aguarde 5 segundos para mover o cursor

x, y = pyautogui.position()
print(f"Coordenadas do cursor do mouse: x={x}, y={y}")
