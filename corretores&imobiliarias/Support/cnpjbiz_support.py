import time
import pyautogui
import pyperclip

from Support.Automacao.auto_support import iniciando_edge_pyautogui, recuperando_string_print
from Support.creci_support import verificar_cnpj_cresci

URL_CNPJBIZ = "https://cnpj.biz/empresas"

def pesquisar_empresa_nome_cnpjbiz(nome_empresa):
    '''
    Pesquisa uma empresa pelo nome
    '''
    time.sleep(2)
    pyperclip.copy(nome_empresa)
    time.sleep(1)
    pyautogui.click(1062, 409)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)



def verificar_existe_empresa_cnpjbiz():
    '''
    Verifica se ao pesquisar a empresa, sera exibido uma mensagem de erro
    Caso não seja encontrado nada sera retornado verdadeiro, caso o contrario falso
    '''
    deu_ruim = recuperando_string_print(639, 235, 500, 300)
    time.sleep(1)
    if "Opa! Alguma coisa saiu errado" in deu_ruim:
        print("Deu ruim")
        return False
    else:
        return True
    


def verifica_empresa_no_rj_cnpjbiz():
    print("OIOI")
    regiao = recuperando_string_print(639, 430, 300, 100)
    time.sleep(1)
    return "Rio de Janeiro/RJ" in regiao



def capturar_cnpj_empresa_cnpjbiz():
    '''
    Captura um print da tela onde o cnpj deve estar. 
    E transforma essa imagem em texto
    '''
    pyautogui.moveTo(445,430)
    texto = recuperando_string_print(445, 430, 300, 200).split(" ")[0]
    return texto



def mover_ate_empresa_cnpjbiz(nome_empresa):
    downs = 6 if len(nome_empresa) > 49 else 5
    pyautogui.PAUSE = .5
    for _ in range(downs):
        pyautogui.press("down")
    pyautogui.PAUSE = 1



def abrindo_empresa_cnpjbiz():
    pyautogui.click(445,430)



def direcionando_contatos_endereco_cnpjbiz():
    pyautogui.PAUSE = .5
    for _ in range(9):
        pyautogui.press("down")
    pyautogui.PAUSE = 1



def direcionando_nome_fantasia_cnpjbiz():
    time.sleep(4)
    pyautogui.PAUSE = .5
    for _ in range(6):
        pyautogui.press("down")
    pyautogui.PAUSE = 1



def recuperar_nome_fantasia_cnpjbiz():
    nome_fantasia_texto = recuperando_string_print(0, 0, 1000, 1000).replace(":", "")
    try:
        nome_fantasia_texto = nome_fantasia_texto.split(" Nome Fantasia ")[1].split(" Data da Abertura ")[0]
        return nome_fantasia_texto
    except:
        return "Nenhum Nome Fantasia encontrado"



def recuperando_contatos_cnpj_biz(contatos_texto_og):
    # Digitar o CNPJ
    time.sleep(2)
    contatos=""
    try:
        contatos_texto = contatos_texto_og.split("Contatos ")[1].split(" Localização ")[0]
        contatos_texto = contatos_texto.replace("(Ligar)", "")
        contatos_texto = contatos_texto.replace("Telefone(s): ", "")
        contatos_texto = contatos_texto.replace(")", "")
        contatos_texto = contatos_texto.replace("(", "")
        contatos_texto = contatos_texto.replace("E-mails", "")
        contatos_texto = contatos_texto.replace("E-mail:", "")
        
        contatos_texto = contatos_texto.replace(" Enviar Email", "")
        contatos_texto = contatos_texto.replace(" Enviar E-mail", "")
        contatos_texto = contatos_texto.replace(" Whatsapp", "")
        contatos_texto = contatos_texto.replace(". ", ".") 

        contatos = contatos_texto
    except:
        contatos = ""
    return contatos



def recuperando_socios_cnpj_biz():
    pyautogui.PAUSE = .5
    for _ in range(12):
        pyautogui.press("down")
    pyautogui.PAUSE = 1
    socios_texto = recuperando_string_print(0, 0, 1000, 1000)
    try:
        socios_texto = socios_texto.split("Quadro de Sócios e Administradores")[1].split("Qualificação do responsável pela empresa: ")[0]
        socios_texto = socios_texto.replace(" Sócio ", " - ")
        socios_texto = socios_texto.replace(" Sócio-Administrador ", " - ")

        return socios_texto
    except:
        return "Nenhum Socio Encontrado"
    


def recuperando_endereco_cnpj_biz(endereco_texto_og):
    try:
        endereco_texto = endereco_texto_og.split("Para correspondência:")[1].split("Procurar no Google Maps")[0]
        print(endereco_texto)

        return endereco_texto
    except:
        return "Nenhum Socio Encontrado"
    


def buscar_empresa_cnpjbiz(nome_empresa, inscricao_empresa):
    pyautogui.PAUSE = 1
    iniciando_edge_pyautogui(URL_CNPJBIZ)
    time.sleep(2)
    pesquisar_empresa_nome_cnpjbiz(nome_empresa)
    
    existe_empresa = verificar_existe_empresa_cnpjbiz()
    
    if existe_empresa:
        mover_ate_empresa_cnpjbiz(nome_empresa)
        for i in range(10):
            # Verificar se é no RJ
            empresa_uf_RJ = verifica_empresa_no_rj_cnpjbiz()

            if empresa_uf_RJ:
                print("É no rio")
                cnpj = capturar_cnpj_empresa_cnpjbiz()
                print(cnpj)
                cnpj_valido = verificar_cnpj_cresci(cnpj, inscricao_empresa)
            
                if cnpj_valido:
                    abrindo_empresa_cnpjbiz()
                    direcionando_nome_fantasia_cnpjbiz()
                    nome_fantasia = recuperar_nome_fantasia_cnpjbiz()
                    direcionando_contatos_endereco_cnpjbiz()

                    contatos_endereco_texto_og = recuperando_string_print(0, 0, 1000, 1000)
                    contatos = recuperando_contatos_cnpj_biz(contatos_endereco_texto_og)
                    endereco = recuperando_endereco_cnpj_biz(contatos_endereco_texto_og)
                    socios = recuperando_socios_cnpj_biz()
                    print("Nome: ", nome_empresa)
                    dados_novos = {"Contatos":contatos, "Socios": socios, "Endereço": endereco, "CNPJ": cnpj, "Nome Fantasia":nome_fantasia}
                    pyautogui.click(1888, 18)
                    return dados_novos
                else:
                    pyautogui.press("down")
            else:
                pyautogui.press("down")
    else:
        pyautogui.click(1888, 18)
        return {"error": "Nenhuma empresa encontrada"}
        


    pyautogui.click(1888, 18)
    return False
    
