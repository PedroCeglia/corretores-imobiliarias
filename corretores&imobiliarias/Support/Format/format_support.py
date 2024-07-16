def formatar_cnpj(cnpj):
    cnpj_formatado = ""
    for i, char in enumerate(cnpj):
        if i == 1 or i == 4:
            cnpj_formatado += char + '.'
        elif i == 7:
            cnpj_formatado += char + '/'
        elif i == 11:
            cnpj_formatado += char + '-'
        else:
            cnpj_formatado += char
    return cnpj_formatado


def transformando_lista_string(lista):
    if type(lista) == type([]):
        nova_lista = []
        for item in lista:
            if type(item) == type([]):
                nova_lista.append(", ".join(item))
            else:
                nova_lista.append(item)
        return " | ".join(nova_lista)