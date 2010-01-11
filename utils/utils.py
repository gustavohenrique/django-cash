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

        if numero < 0:
            numero = numero * -1

        numero_em_string = numero.__str__()
        if '.' in numero_em_string:
            inteiro, centavos = numero_em_string.split('.')
        else:
            inteiro = numero_em_string
            centavos = '00'

        numero_separador_virgula = ''
        tamanho_algarismos_inteiro = len(inteiro)
        while tamanho_algarismos_inteiro > 0:
            numero_separador_virgula = numero_separador_virgula + inteiro[tamanho_algarismos_inteiro - 1]
            contador += 1
            if contador == 3 and tamanho_algarismos_inteiro > 1:
                numero_separador_virgula += '.'
                contador = 0
            tamanho_algarismos_inteiro -= 1

        tamanho_algarismos_inteiro = len(numero_separador_virgula)
        numero_formatado_como_moeda = ''
        while tamanho_algarismos_inteiro > 0:
            numero_formatado_como_moeda += numero_separador_virgula[tamanho_algarismos_inteiro - 1]
            tamanho_algarismos_inteiro -= 1

        return "R$ %s,%s" % (numero_formatado_como_moeda.replace('-',''), centavos)
    except:
        return numero



