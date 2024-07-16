import pandas as pd


def editar_campos_empresa(dict_bairros_edit):
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


def preencher_nan_com_vazio(df:pd.DataFrame):
    # Iterar sobre todas as células do DataFrame
    for coluna in df.columns:
        for indice, valor in df[coluna].items():
            if pd.isna(valor):  # Verificar se o valor é NaN
                df.at[indice, coluna] = ""  # Substituir NaN por uma string vazia
    return df


def filter_empresas_ativas_regulares(bairros):
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


def filter_empresas_PJ_ativas(df:pd.DataFrame):
    if len(df) > 0:
        novo_df = df[df['Natureza'].str.contains('PJ') == True].copy()
        novo_df = novo_df[novo_df['Situação'] == "ATIVO"].copy()
        return novo_df
    else:
        return pd.DataFrame(columns=["Inscrição", "Identificação", "Situação", "Certidão de Regularidade", "Contato", "Natureza", "Bairro"])


def remover_pos_fixo_df(df:pd.DataFrame):
    df_novo = pd.DataFrame()
    for idx, item in df.iterrows():
        item_dict = dict(item)
        nome_antigo = item_dict["Identificação"]
        nome_novo = nome_antigo.replace("LTDA", "")
        nome_novo = nome_novo.replace("EIRELI", "")
        nome_novo = nome_novo.replace("S/A", "")
        nome_novo = nome_novo.replace(".", "")
        nome_novo = nome_novo.replace("-", "")
        nome_novo = nome_novo.replace("ME", "")
        nome_novo = nome_novo.replace("VICEVERSA", "VICE-VERSA")
        item_dict["Identificação"] = nome_novo
        item_df = pd.DataFrame(item_dict, index=[0])
        df_novo = pd.concat([df_novo, item_df], ignore_index=True)
    return df_novo
    

def trocar_coluna_entre_dfs(
        df_og: pd.DataFrame, new_df: pd.DataFrame, 
        id_col: str = 'Inscrição', indice_new_item: str = 'Identificação'
) -> pd.DataFrame:
    
    df_novo_restaurado = df_og.copy()  # Criando uma cópia do dataframe novo para evitar modificações indesejadas
    
    # Criando um dicionário de mapeamento entre os IDs do dataframe novo e as identificações do dataframe antigo
    mapeamento = dict(zip(new_df[id_col], new_df[indice_new_item]))
    
    # Restaurando os valores originais da coluna "Identificação" no dataframe novo com base no ID
    df_novo_restaurado['Identificação'] = df_og[id_col].map(mapeamento)
    
    return df_novo_restaurado


def transforma_dataframe_em_lista(dataframe):
    # Transforma o DataFrame em uma lista de listas
    lista = dataframe.values.tolist()

    # Retorna a lista
    return lista


def filtrar_df_from_df(df_og, df_filter, col_id="Inscrição"):
    '''
    Remove do df Original (og), os itens onde a coluna de indice (col_id)
    é igual em algum item da df_og e df_filter
    '''
    return df_og[~df_og[col_id].isin(df_filter[col_id])]
