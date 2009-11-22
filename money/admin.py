# -8- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin

from money.models import *
from money.forms import *


site.register(Caixa)


class ContaAdmin(ModelAdmin):
    list_display = ('nome','saldo_inicial')
site.register(Conta, ContaAdmin)


class CredorAdmin(ModelAdmin):
    list_display = ['credor']
site.register(Credor, CredorAdmin)


class FormaPagamentoAdmin(ModelAdmin):
    list_display = ('id','forma_pagamento')
site.register(FormaPagamento, FormaPagamentoAdmin)


class LancamentoAdmin(ModelAdmin):
    list_display = ('vencimento','desc','valor','tipo','forma_pagamento','pago','caixa')
    form = LancamentoForm
site.register(Lancamento, LancamentoAdmin)




