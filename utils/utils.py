# -*- coding: utf-8 -*-
import time
import datetime

def str2datetime(s):
    if s:
        time_string = s.replace('T',' ')
        time_format = '%Y-%m-%d %H:%M:%S'
        mytime = time.strptime(time_string, time_format)
        return datetime.datetime(*mytime[:6])
    else:
        return s

def str2ymd(s):
    if s:
        time_format = '%Y-%m-%d'
        mytime = time.strptime(s, time_format)
        return datetime.datetime(*mytime[:6])
    else:
        return s

def dmy2date(s):
    try:
        d = s.split('/')
        return datetime.date(int(d[2]), int(d[1]), int(d[0]))
    except:
        return datetime.date.today()


def ymd2str(d):
    try:
        s = str(d).split('-')
        return '%s/%s/%s' % (s[2], s[1], s[0])
    except:
        return str(d)


def moeda(numero):
    """
    Retorna uma string no formato de moeda brasileira
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


def bool2str(b):
    if b == True:
        return u'Sim'
    else:
        return u'Não'
