# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from money.views import LancamentoRest, LancamentoView

urlpatterns = patterns('money.views',
    url(r'^$', 'index', name='money_index'),

    url(r'^lancamento/$', LancamentoRest(), name='money_list'),
    url(r'^lancamento/add/$', LancamentoRest(), name='money_add'),
    url(r'^lancamento/del/(?P<id>\d+)/$', LancamentoRest(), name='money_del'),
    url(r'^lancamento/update/(?P<id>\d+)/$', LancamentoRest(), name='money_upd'),
)

urlpatterns += patterns('',
    url(r'^lancamento/new/$', LancamentoView().new, name='money_new'),
    url(r'^lancamento/filter/$', LancamentoView().filter, name='money_filter'),
)
