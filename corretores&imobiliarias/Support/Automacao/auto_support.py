import easyocr

'''
import logging
logging.getLogger('easyocr').setLevel(logging.ERROR) # Configura o nível de logging para suprimir os avisos da EasyOCR
'''
import time
import pyautogui
pyautogui.PAUSE = 1

import pygetwindow

from selenium import webdriver

def iniciando_edge_pyautogui(url):
    pyautogui.press("win")
    time.sleep(1)
    pyautogui.write("edge")
    time.sleep(1)
    pyautogui.press("enter")
    
    time.sleep(1)
    # Ativar o modo de tela cheia pressionando windows + up
    esta_maximizado = verificar_edge_maximizado()
    if not esta_maximizado:
        pyautogui.hotkey('win', 'up')

    time.sleep(2)
    pyautogui.write(url)  
    pyautogui.press("enter")
    time.sleep(3)


def verificar_edge_maximizado():
    # Obter todas as janelas abertas atualmente
    janelas = pygetwindow.getAllWindows()

    # Procurar a janela do Microsoft Edge entre as janelas abertas
    for janela in janelas:
        if "Microsoft​ Edge" in janela.title:
            # Verificar se a janela está maximizada
            return janela.isMaximized
    else:
        print("A janela do Microsoft Edge não está aberta.")
        return False


def iniciando_edge_selenium(url):
    driver = webdriver.Edge()

    # Maximize a janela do navegador
    driver.maximize_window()
    
    #Abrir pagina
    driver.get(url)
    time.sleep(3)
    return driver


def recuperando_string_print(x1, y1, width, height):
    '''
    Captura um print da tela e transforma em string
    '''
    # Inicializa o EasyOCR para o idioma português
    reader = easyocr.Reader(['pt'])

    # Captura uma região da tela onde o texto está localizado (ajuste as coordenadas conforme necessário)
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

    # Salva a captura de tela em um arquivo temporário
    screenshot_path = "screenshot_temp.png"
    screenshot.save(screenshot_path)

    # Usa EasyOCR para realizar OCR na imagem
    resultados = reader.readtext(screenshot_path)
    
    # Extrai o texto dos resultados
    texto_copiado = ""
    for resultado in resultados:
        texto_copiado += resultado[1] + " "
    return texto_copiado.strip()
