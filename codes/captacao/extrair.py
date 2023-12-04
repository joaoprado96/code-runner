from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def extrair_info_com_selenium(url):
    # Caminho para o seu WebDriver
    path_to_webdriver = "C:/Users/joaop/OneDrive/Documents/GitHub/code-runner/codes/captacao/chromedriver.exe"

    # Inicializar o WebDriver
    service = Service(path_to_webdriver)
    driver = webdriver.Chrome(service=service)

    try:
        # Acessar a URL
        driver.get(url)

        # Esperar até que o elemento desejado esteja presente
        # Modifique o seletor para encontrar o elemento que você deseja
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 'seu_xpath_aqui'))
        )

        # Extrair informações
        # Modifique esta parte para extrair as informações desejadas
        elemento = driver.find_element(By.XPATH, 'seu_xpath_aqui')
        texto = elemento.text

        # Estruturar os dados em um dicionário
        dados = {"texto": texto}

        # Converter o dicionário em JSON
        json_dados = json.dumps(dados, ensure_ascii=False)

        return json_dados
    finally:
        # Fechar o navegador após a extração
        driver.quit()

# Exemplo de uso
url = 'https://www.webmotors.com.br/comprar/suzuki/burgman-i/125cc/2012-2013/2039583?pos=f2039583a:&np=1'
print(extrair_info_com_selenium(url))
