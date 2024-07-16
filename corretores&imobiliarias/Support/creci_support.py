import time

import pandas as pd

import pyautogui
pyautogui.PAUSE = 1

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from io import StringIO

from Support.Automacao.auto_support import iniciando_edge_selenium

lista_bairros_zona_norte = [
    "Acari", "Anchieta", "Barros Filho", "Bento Ribeiro", "Brás de Pina", "Campinho", "Cavalcanti", "Cascadura", "Coelho Neto", "Colégio",
    "Complexo do Alemão", "Cordovil", "Costa Barros", "Engenheiro Leal", "Engenho da Rainha", "Guadalupe", "Honório Gurgel", "Inhaúma", "Irajá",
    "Jardim América", "Madureira", "Marechal Hermes", "Oswaldo Cruz", "Parada de Lucas", "Parque Anchieta", "Parque Colúmbia", "Pavuna", "Penha",
    "Penha Circular", "Quintinho Bocaiuva", "Ricardo de Albuquerque", "Rocha Miranda", "Tómas Coelho", "Turiaçu", "Vaz Lobo", "Vicente de Carvalho",
    "Vigário Geral", "Vila da Penha", "Vila Kosmos", "Vista Alegre" 
]
lista_bairros_ilha_gov_leopoldina = [
    "Bonsucesso", "Bancários", "Cacuia", "Cidade Universitária", "Cocotá", "Freguesia", "Galeão", "Jardim Carioca", "Jardim Guanabara", "Maré",
    "Moneró", "Olaria", "Pitangueiras", "Portuguesa", "Praia da Bandeira", "Ramos", "Ribeira", "Tauá", "Zumbi" 
]
lista_bairros_tijuca = [
    "Alto da Boa Vista", "Andaraí", "Grajaú", "Maracanã", "Praça da Bandeira", "Tijuca", "Vila Isabel", "Barra da Tijuca"
]
lista_bairros_meier = [
    "Abolição", "Agua Santa", "Cachambi", "Del Castilho", "Encantado", "Engenho de Dentro", "Engenho Novo", "Higienópolis", "Jacaré", "Jacarezinho",
    "Lins de Vasconcelos", "Manguinhos", "Maria da Graça", "Méier", "Piedade", "Pilares", "Riachuelo", "Rocha", "Sampaio", "São Francisco Xavier",
    "Todos os Santos",  
]

lista_bairros = lista_bairros_zona_norte + lista_bairros_ilha_gov_leopoldina + lista_bairros_tijuca + lista_bairros_meier
dict_bairros = {}

def baixar_tabela_por_bairro(bairro):
    url = 'https://www.crecirj.conselho.net.br/form_pesquisa_cadastro_geral_site.php'
    driver = webdriver.Edge()

    # Maximize a janela do navegador
    driver.maximize_window()
    
    #Abrir pagina
    driver.get(url)
    
    # Localiza os campos do formulário e preenche-os
    campo_bairro = driver.find_element("id", "input-27")
    campo_bairro.send_keys(bairro)

    # Envie o formulário
    campo_bairro.send_keys(Keys.RETURN)

    # Aguarde um tempo para a página carregar completamente
    time.sleep(4)

    # Pular para o final da pagina
    for _ in range(25):  
        pyautogui.press('down')  # Simula pressionar a tecla de seta para baixo
        time.sleep(0.2) 

    # Mova o cursor do mouse para o ponto médio do elemento usando PyAutoGUI
    pyautogui.moveTo(171, 979)

    # Simule um clique do mouse usando PyAutoGUI
    pyautogui.click()

    time.sleep(1)

    pyautogui.click()

    time.sleep(6)

    try:
        # Encontra a tabela na página
        table = driver.find_elements('css selector', 'table')
        table_html = table[0].get_attribute('outerHTML')
    except IndexError:
        print(f"Não existe nenhuma corretora/imobiliaria em {bairro}!")
        print(f"Verifique se o nome do bairro esta certo! {bairro}\n")
        driver.quit()
        return pd.DataFrame()
    else:
        df = pd.read_html(StringIO(table_html))[0]  # Este método retorna uma lista de DataFrames, portanto, pegamos o primeiro
        driver.quit()
        print(bairro, len(df),end='; ')
        return df


dict_bairros_edit = {}    


def baixar_tabela_todos_bairros():
    for bairro in lista_bairros:
        tabela_bairro = baixar_tabela_por_bairro(bairro)
        dict_bairros.update({bairro:tabela_bairro})
        dict_bairros_edit = dict_bairros.copy()


def editar_campos_empresa():
    for bairro, tb in dict_bairros_edit.items():
        try:
            tb.drop(columns=['Unnamed: 5'], inplace=True)
        except KeyError:
            pass
        
        for index, linha in tb.iterrows():
            nome = linha["Identificação"]
            tb.at[index, "Bairro"] = bairro
            
            if " PJ " in nome:
                novo_nome = nome.replace(" PJ P", "").replace(" PJ ", "")
                tb.at[index, "Identificação"] = novo_nome
                tb.at[index, "Natureza"] = "PJ P"
            elif " PF " in nome:
                novo_nome = nome.replace(" PF P", "").replace(" PF ", "")
                tb.at[index, "Identificação"] = novo_nome
                tb.at[index,"Natureza"] = "PF P"
        print("Bairro:", bairro)


def preencher_nan_com_vazio(df):
    # Iterar sobre todas as células do DataFrame
    for coluna in df.columns:
        for indice, valor in df[coluna].items():
            if pd.isna(valor):  # Verificar se o valor é NaN
                df.at[indice, coluna] = ""  # Substituir NaN por uma string vazia
    return df


def preencher_bairros_nan_com_vazio(dict_bairros_p):
    new_dict = {}
    for bairro, tb in dict_bairros_p.items():
        novo_df = preencher_nan_com_vazio(tb)
        new_dict.update({bairro: novo_df})

    return new_dict.copy()


def verifica_aitvos_inativos(dataframe):
    ativos = 0
    inativos = 0
    for index, linha in dataframe.iterrows():
        if "PJ" in  linha["Natureza"]:
            if linha["Situação"] == "ATIVO":
                ativos += 1 
            else: 
                inativos += 1
    return (ativos, inativos)


def contar_ativos_inativos_todos_bairros():
    ativos_qnt = 0
    inativos_qnt = 0
    
    for bairro, tb in dict_bairros_edit.items():
        novo_ativos_qnt, novo_inativos_qnt = verifica_aitvos_inativos(tb)
        ativos_qnt += novo_ativos_qnt
        inativos_qnt += novo_inativos_qnt

    print("Ativos", ativos_qnt)
    print("Inativos", inativos_qnt)
    print("Total", ativos_qnt + inativos_qnt)


def bairros_ativos_disponiveis(bairros):
    novo_dict = {}
    for bairro_nome, bairro_tabela in bairros.items():
        print(bairro_nome)
        if not bairro_tabela.empty:
            nova_tabela = bairro_tabela.loc[bairro_tabela["Situação"] == "ATIVO"]
            nova_tabela = nova_tabela.loc[bairro_tabela["Certidão de Regularidade"] == "REGULAR"]
            novo_dict.update({bairro_nome:nova_tabela})
        else:
            print("Vazio",bairro_nome)
    return novo_dict.copy()


def verificar_cnpj_cresci(cnpj, inscricao_empresa):
    # empresa = {informações da linha do dataframe}
    # Entrar no Cresci
    driver = iniciando_edge_selenium('https://www.crecirj.conselho.net.br/form_pesquisa_cadastro_geral_site.php')
    # Digitar o CNPJ
    time.sleep(1)
    campo_cnpj = driver.find_element("id", "input-21")
    time.sleep(1)
    campo_cnpj.send_keys(cnpj)
    time.sleep(1)
    # Envie o formulário
    campo_cnpj.send_keys(Keys.RETURN)
    time.sleep(2)
    # Verificar se é compativel
    try:
        # Encontra a tabela na página
        table = driver.find_elements('css selector', 'table')
        table_html = table[0].get_attribute('outerHTML')
    except IndexError:
        driver.quit()
        return False
    else:
        df = pd.read_html(StringIO(table_html))[0]  # Este método retorna uma lista de DataFrames, portanto, pegamos o primeiro
        driver.quit()
        # Recuperando dados da empresa
        empreasa_info = df.iloc[0]
        empresa_inscricao = empreasa_info["Inscrição"]

        if int(empresa_inscricao) == int(inscricao_empresa):
            return True
        else:
            print(f"A inscriçãoda da empresa {inscricao_empresa} é diferente de {empresa_inscricao}")
            return False