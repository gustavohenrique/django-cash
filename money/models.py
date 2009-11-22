# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum

import datetime


class Conta(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    agencia = models.CharField(max_length=6, blank=True, null=True)
    conta =  models.CharField(max_length=10, blank=True, null=True)
    variacao =  models.CharField(max_length=2, blank=True, null=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['nome',]
        verbose_name = u'conta bancária'
        verbose_name_plural = u'contas bancárias'

    def __unicode__(self):
        return self.nome



class Credor(models.Model):
    credor = models.CharField(max_length=200)

    class Meta:
        ordering = ['credor',]
        verbose_name_plural = 'credores'

    def __unicode__(self):
        return self.credor


class Caixa(models.Model):
    caixa = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['caixa']
    
    def __unicode__(self):
        return self.caixa
        
        
class FormaPagamento(models.Model):
    forma_pagamento = models.CharField(max_length=200)

    class Meta:
        ordering = ['forma_pagamento',]

    def __unicode__(self):
        return self.forma_pagamento

#from tags import aplicar_tags
class Lancamento(models.Model):
    TIPO_CHOICES = (
        ('C',u'Crédito'),
        ('D',u'Débito'),
        ('T',u'Transferência')
    )
    caixa = models.ForeignKey(Caixa)
    credor = models.ForeignKey(Credor, blank=True, null=True)
    desc = models.CharField(max_length=255, verbose_name=u'Descrição')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    cadastro = models.DateField(auto_now_add=True)
    vencimento = models.DateField(verbose_name=u'Data')
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    forma_pagamento = models.ForeignKey(FormaPagamento, verbose_name=u'Pagamento')
    pago = models.BooleanField(default=True)

    class Meta:
        ordering = ['vencimento',]

    def __unicode__(self):
        return self.desc

    def save(self, **kwargs):
        if self.tipo == 'D':
            if self.valor > 0:
                self.valor = -self.valor
        else:
            if self.valor < 0:
                self.valor = -self.valor

        super(Lancamento, self).save()
        
import tagging
tagging.register(Lancamento)


    
    


