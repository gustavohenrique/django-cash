# -*- coding:utf-8 -*-
from django.contrib.admin import site, ModelAdmin
from core.models import *


site.register(Account)
site.register(Payee)
site.register(PaymentType)


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent')
site.register(Category, CategoryAdmin)


class TransactionAdmin(ModelAdmin):
    list_display = ('date', 'desc', 'amount', 'payment_type', 'payee', 'category', 'account')
    list_filter = ('account', 'category', 'payee')
    ordering = ['date', 'payment_type', 'payee']
site.register(Transaction, TransactionAdmin)
