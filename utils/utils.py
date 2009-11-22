# -*- coding: utf-8 -*-
def moeda(numero):
    """
    Retorna uma string no formato de moeda brasileira.

    No python 2.4 nao existe o metodo locale.currency.

    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    >>> locale.currency(1.99, grouping=True)
    """

    try:
        contador = 0
        preco_str = ''
        num = numero.__str__()
        if '.' in num:
            preco, centavos = num.split('.')
        else:
            preco = num
            centavos = '00'

        tamanho = len(preco)
        while tamanho > 0:
            preco_str = preco_str + preco[tamanho-1]
            contador += 1
            if contador == 3 and tamanho > 1:
                preco_str = preco_str + '.'
                contador = 0
            tamanho -= 1

        tamanho = len(preco_str)
        str_preco = ''
        while tamanho > 0:
            str_preco = str_preco + preco_str[tamanho-1]
            tamanho -= 1
        #print str_preco
        return "R$ %s,%s" % (str_preco.replace('-',''), centavos)
    except:
        #print numero
        return numero


