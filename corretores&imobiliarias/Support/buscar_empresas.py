import pandas as pd

from Support.linkana_support import buscar_empresa_linkana as _buscar_empresa_linkana
from Support.cnpjbiz_support import buscar_empresa_cnpjbiz


def _buscar_dados_empresas_linkana(empresa):
    nome_empresa = empresa["Identificação"]
    inscricao_empresa = empresa["Inscrição"]

    dados_novos = {}
    recuperou = _buscar_empresa_linkana(nome_empresa, inscricao_empresa)
    if not recuperou or "error" in recuperou:
        if "error" in recuperou:
            dados_novos.update(recuperou)

        print("Não Achou: ", nome_empresa)
    else:
        dados_novos.update(recuperou)

    return dados_novos


def _buscar_dados_empresa_transformar_df_linkana(empresa):
    try:
        dados_novos = _buscar_dados_empresas_linkana(empresa)
    except Exception as e:
        print(e)
        return pd.DataFrame()
    else:
        print(dados_novos)
        if len(dados_novos) > 0:
            dados_empresa = dict(empresa)
            for idx_item, valor in dados_novos.items():
                #valor_str = transformando_lista_string(valor)
                dados_empresa.update({idx_item: valor})
            return pd.DataFrame(dados_empresa, index=[0])
            

def buscar_todas_empresas_bairro_linkana(df:pd.DataFrame):
    completos_columns = ["Inscrição","Identificação","CNPJ","Nome Fantasia","Situação","Certidão de Regularidade","Contato","Natureza","Bairro","Contatos","Socios","Endereço"]
    completos_df = pd.DataFrame(columns=completos_columns)
    incompletos_columns = ["Inscrição","Identificação","Situação","Certidão de Regularidade","Contato","Natureza","Bairro","error"]
    incompletos_df = pd.DataFrame(columns=incompletos_columns)

    for idx, empresa in df.iterrows():
        try:
            empresa_completa = _buscar_dados_empresa_transformar_df_linkana(empresa)
            if not empresa_completa.empty and not "error" in empresa_completa:
                completos_df = pd.concat([completos_df, empresa_completa], ignore_index=True)
            elif "error" in empresa_completa:
                incompletos_df = pd.concat([incompletos_df, empresa_completa], ignore_index=True)
                print("DEu erro: ", idx)
        except Exception as e:
                print("DEu erro: ", idx, e)
    if "error" in incompletos_df:
        incompletos_df.drop(columns="error")
                

    return completos_df, incompletos_df


def _buscar_dados_empresas_cnpjbiz(empresa):
    nome_empresa = empresa["Identificação"]
    inscricao_empresa = empresa["Inscrição"]

    dados_novos = {}
    recuperou = buscar_empresa_cnpjbiz(nome_empresa, inscricao_empresa)

    print("Recuperou", recuperou)
    if not recuperou or "error" in recuperou:
        if "error" in recuperou:
            dados_novos.update(recuperou)

        print("Não Achou: ", nome_empresa)
    else:
        dados_novos.update(recuperou)

    print("DAdos Novos", dados_novos)
    
    return dados_novos


def _buscar_dados_empresa_transformar_df_cnpjbiz(empresa):
    try:
        dados_novos = _buscar_dados_empresas_cnpjbiz(empresa)
    except Exception as e:
        print(e)
        return pd.DataFrame()
    else:
        print(dados_novos)
        if len(dados_novos) > 0:
            dados_empresa = dict(empresa)
            for idx_item, valor in dados_novos.items():
                dados_empresa.update({idx_item: valor})
            return pd.DataFrame(dados_empresa, index=[0])
        

def buscar_todas_empresas_bairro_cnpjbiz(df:pd.DataFrame):
    completos_columns = ["Inscrição","Identificação","CNPJ","Nome Fantasia","Situação","Certidão de Regularidade","Contato","Natureza","Bairro","Contatos","Socios","Endereço"]
    completos_df = pd.DataFrame(columns=completos_columns)
    incompletos_columns = ["Inscrição","Identificação","Situação","Certidão de Regularidade","Contato","Natureza","Bairro","error"]
    incompletos_df = pd.DataFrame(columns=incompletos_columns)

    for idx, empresa in df.iterrows():
        try:
            empresa_completa = _buscar_dados_empresa_transformar_df_cnpjbiz(empresa)
            if not empresa_completa.empty and not "error" in empresa_completa:
                completos_df = pd.concat([completos_df, empresa_completa], ignore_index=True)
            elif "error" in empresa_completa:
                incompletos_df = pd.concat([incompletos_df, empresa_completa], ignore_index=True)
                print("DEu erro: ", idx)
        except Exception as e:
                print("DEu erro: ", idx, e)
    if "error" in incompletos_df:
        incompletos_df.drop(columns="error")
                

    return completos_df, incompletos_df