import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import gspread
from gspread_dataframe import set_with_dataframe

import pandas as pd

def criar_planilha_gs(nome_planilha):
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds)  # Substitua 'credentials.json' pelo caminho do seu arquivo de credenciais

    # Cria uma nova planilha com o nome fornecido
    nova_planilha = client.create(nome_planilha)

    # Retorna o objeto da planilha recém-criada
    return nova_planilha


def ler_planilha(nome_planilha, nome_pagina):
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds) 

    # Abre a planilha pelo nome
    planilha = client.open(nome_planilha)

    # Seleciona a página desejada
    pagina = planilha.worksheet(nome_pagina)

    # Lê os dados da página como uma lista de listas
    dados = pagina.get_all_values()

    # Retorna os dados
    return dados


def editar_planilha(nome_planilha, nome_pagina, dados):
    # Autentica usando credenciais do Google Cloud Platform
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds)
    # Abre a planilha pelo nome
    planilha = client.open(nome_planilha)

    # Seleciona a página desejada
    pagina = planilha.worksheet(nome_pagina)

    # Limpa os dados existentes na página
    pagina.clear()

    # Preenche a página com os novos dados
    for i, linha in enumerate(dados, start=1):
        pagina.update(f"A{i}", [str(valor) for valor in linha])


def transforma_dataframe_em_lista(dataframe):
    # Transforma o DataFrame em uma lista de listas
    lista = dataframe.values.tolist()

    # Retorna a lista
    return lista


def baixar_pagina_planilha(nome_planilha, nome_pagina):
    # Autentica usando credenciais do Google Cloud Platform
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds) 

    # Abre a planilha pelo nome
    planilha = client.open(nome_planilha)

    # Seleciona a página desejada
    pagina = planilha.worksheet(nome_pagina)

    # Obtém os dados da página como DataFrame
    dataframe = pd.DataFrame(pagina.get_all_records())

    # Retorna o DataFrame
    return dataframe


def criar_planilha_e_popular(dicionario, nome_planilha):
    # Cria uma nova planilha com o nome fornecido
    nova_planilha = criar_planilha_gs(nome_planilha)

    # Para cada chave no dicionário
    for chave, valor in dicionario.items():
        # Cria uma nova página na planilha com o nome da chave
        nova_pagina = nova_planilha.add_worksheet(title=chave, rows=1, cols=1)

        # Transforma o valor associado à chave em um DataFrame
        dataframe = pd.DataFrame(valor)

        # Preenche a nova página com o DataFrame
        set_with_dataframe(nova_pagina, dataframe)


def atualizar_planilha_gs(nome_planilha, dicionario_df):
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds)

    # Abre a planilha existente pelo nome
    planilha = client.open(nome_planilha)

    # Para cada chave no dicionário de DataFrames
    for chave, dataframe in dicionario_df.items():
        # Verifica se a página já existe na planilha, se não existir, cria uma nova
        try:
            pagina = planilha.worksheet(chave)
        except gspread.exceptions.WorksheetNotFound:
            pagina = planilha.add_worksheet(title=chave, rows=1, cols=1)

        # Preenche a página com o DataFrame correspondente
        set_with_dataframe(pagina, dataframe)


def atualizar_pagina_planilha(nome_planilha, nome_pagina, dataframe):
    creds = validar_token_google_sheets()
    client = gspread.authorize(creds)

    # Abre a planilha existente pelo nome
    planilha = client.open(nome_planilha)

    # Verifica se a página já existe na planilha, se não existir, cria uma nova
    try:
        pagina = planilha.worksheet(nome_pagina)
    except gspread.exceptions.WorksheetNotFound:
        pagina = planilha.add_worksheet(title=nome_pagina, rows=1, cols=1)

    # Preenche a página com o DataFrame correspondente
    set_with_dataframe(pagina, dataframe)


SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]


def validar_token_google_sheets():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds
 

