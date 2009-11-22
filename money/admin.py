# -8- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin, TabularInline

from money.models import *
from money.forms import *

#class TagAdmin(ModelAdmin):
#    pass
#site.register(Tag, TagAdmin)

class ContaAdmin(ModelAdmin):
    list_display = ('nome','saldo_inicial')
    form = ContaForm
site.register(Conta, ContaAdmin)


class CredorAdmin(ModelAdmin):
    list_display = ['credor']
site.register(Credor, CredorAdmin)


class FormaPagamentoAdmin(ModelAdmin):
    list_display = ('id','forma_pagamento')
site.register(FormaPagamento, FormaPagamentoAdmin)

site.register(Caixa)

class LancamentoAdmin(ModelAdmin):
    list_display = ('vencimento','desc','valor','tipo','forma_pagamento','pago','caixa')
    form = LancamentoForm
    
    #def save_model(self, request, obj, form, change):
        #super(LancamentoAdmin, self).save_model(request, obj, form, change)
        #obj.tags = form.cleaned_data['tags']

site.register(Lancamento, LancamentoAdmin)




