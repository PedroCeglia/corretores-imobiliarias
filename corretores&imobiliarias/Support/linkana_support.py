import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Support.Automacao.auto_support import iniciando_edge_selenium, recuperando_string_print
from Support.creci_support import verificar_cnpj_cresci
from Support.Format.format_support import formatar_cnpj

URL_LINKANA = "https://cnpj.linkana.com/"

def pesquisar_empresa_nome_linkana(nome_empresa, driver):
    campo_nome = driver.find_element(By.ID, "q")
    campo_nome.send_keys(nome_empresa)
    campo_nome.send_keys(Keys.RETURN)


def verificar_existe_empresa_linkana():
    texto = recuperando_string_print(313, 529, 500, 70)
    return not "Nenhum resultado encontrado" in texto


def verifica_empresa_no_rj_linkana():
    texto = recuperando_string_print(1119, 621, 100, 70)
    return "RJ" in texto


def recuperando_nome_fantasia_linkana(driver:webdriver.Edge):
    lista = driver.find_elements(By.TAG_NAME, "ul")[0].text
    nome_fantasia = lista.split("\nNome fantasia\n")[1].split("\nSituação cadastral\n")[0]
    return nome_fantasia


def recuperando_contatos_linkana(driver:webdriver.Edge):
    lista = driver.find_elements(By.TAG_NAME, "ul")[0].text
    email = lista.split("\nE-mail\n")[1].split("\nTelefone\n")[0]
    telefone = ""
    try:
        telefone = lista.split("\nTelefone\n")[1]
    except:
        pass
    
    contato = f"{email}, {telefone}"
    return contato


def recuperando_socios_linkana(driver:webdriver.Edge):
    lista = driver.find_elements(By.TAG_NAME, "ul")[1].text.split("\n")
    socios = ""
    for idx, item in enumerate(lista):
        if idx % 2 == 0:
            socios += f" {item} -"
    return socios

def recuperando_endereco_linkana(driver:webdriver.Edge):
    lista = driver.find_elements(By.TAG_NAME, "ul")[3].text.split("\n")
    endereco = ""
    for idx, item in enumerate(lista):
        if idx % 2 != 0:
            endereco += f" {item} -"
    return endereco


def buscar_empresa_linkana(nome_empresa, inscricao_empresa):
    driver = iniciando_edge_selenium(URL_LINKANA)
    
    pesquisar_empresa_nome_linkana(nome_empresa, driver)

    existe_empresa = verificar_existe_empresa_linkana()
    if existe_empresa:
        empresa_uf_rj = verifica_empresa_no_rj_linkana()
        if empresa_uf_rj:
            cnpj = recuperando_string_print(337, 584, 250, 60).split(" ")[1]
            cnpj_valido = verificar_cnpj_cresci(cnpj, inscricao_empresa)
            if cnpj_valido:
                cnpj = formatar_cnpj(cnpj)
                pyautogui.click(337,584)
                time.sleep(3)
                nome_fantasia = recuperando_nome_fantasia_linkana(driver)
                contatos = recuperando_contatos_linkana(driver)
                socios = recuperando_socios_linkana(driver)
                enderecos = recuperando_endereco_linkana(driver)
                driver.quit()    
                return {"Contatos":contatos, "Socios": socios, "Endereço": enderecos, "CNPJ":cnpj, "Nome Fantasia":nome_fantasia}    
    

    driver.quit()    
    return False

#buscar_empresa_linkana("2F IMOBILIARIA LTDA", "10591")


def teste_2(nome_empresa):
    driver = iniciando_edge_selenium(URL_LINKANA)
    
    pesquisar_empresa_nome_linkana(nome_empresa, driver)

    existe_empresa = verificar_existe_empresa_linkana()
    if existe_empresa:
        empresa_uf_rj = verifica_empresa_no_rj_linkana()
        if empresa_uf_rj:
            cnpj = recuperando_string_print(337, 584, 250, 60).split(" ")[1]
            pyautogui.click(337,584)
            time.sleep(3)
            contatos = recuperando_contatos_linkana(driver)
            socios = recuperando_socios_linkana(driver)
            enderecos = recuperando_endereco_linkana(driver)
            driver.quit()    
            return {"Contatos":contatos, "Socios": socios, "Endereço": enderecos}    