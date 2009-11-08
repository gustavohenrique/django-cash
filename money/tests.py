"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class MoneyTest(TestCase):
    fixtures = ['auth.json','money.json']

    def setUp(self):
        """
        Efetua o login
        """

        self.c = Client()
        self.c.login(username='gu', password='stavo')
        self.jsonRespOk = '{"status": "ok", "msg": "ok", "success": true}'


    def _addLancamento(self, data):
        """
        Adiciona um novo lancamento
        """

        d = {
            'credor': 1,
            'desc': 'Contas atrasadas',
            'vencimento': '05/10/2009',
            'valor': '100.00',
            'tipo': 'D',
            'forma_pagamento': 1,
            'caixa': 1,
            'pago': True,
            'tags': 'internet sites compras mercado'
        }
        
        d.update(data)
        response = self.c.post(reverse('money_add'), d)
        self.failUnlessEqual(response.content, self.jsonRespOk)
        #c.get('/customers/details/', {'name': 'fred', 'age': 7}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')


    def addLancamentoNumComVirgula(self):
        """
        Valor usando virgula como separador decimal
        """
        
        data = {'valor': '115,50'}
        self._addLancamento(data)


    def addLancamentoForeignKeysNotExist(self):
        """
        Chaves estrangeiras nao existem
        """

        data = {
            'credor': 9999,
            'forma_pagamento': '9999',
            'caixa': 9999
        }
        self._addLancamento(data)

    
    def editLancamento(self):
        """
        Dados de um lancamento a partir do id informado na URL
        """

        response = self.c.get('%s?id=1' % reverse('money_list'))
        self.failUnlessEqual(response.content, self.jsonRespOk)


    def listLancamento(self):
        """
        Lista de lancamentos, divididos por pagina de acordo com os valores
        informados na URL
        """

        response = self.c.get('%s?start=0&limit=10' % reverse('money_list'))
        self.assertContains(response, '"success": true', 1, 200)


    def deleteLancamento(self):
        """
        Deleta um lancamento
        """

        response = self.c.delete(reverse('money_del', args=[5]))
        self.failUnlessEqual(response.content, self.jsonRespOk)


    def updateLancamento(self):
        """
        Atualiza os dados do lancamento
        """

        d = {
            'credor': 2,
            'desc': 'Lancamento alterado',
            'vencimento': '08/01/1984',
            'valor': '1000.00',
            'tipo': 'C',
            'forma_pagamento': 1,
            'pago': False,
        }
        response = self.c.put(reverse('money_upd', args=[5]), d)
        self.failUnlessEqual(response.content, self.jsonRespOk)



__test__ = {"doctest": """
>>> from money.models import *
>>> caixa = Caixa.objects.create(caixa='Energia Eletrica')
>>> pagamento = FormaPagamento.objects.create(forma_pagamento='Dinheiro')
>>> l = Lancamento.objects.create(desc='Contas atrasadas',vencimento='2009-11-07',valor=100,tipo='D',forma_pagamento=pagamento,caixa=caixa,pago=True)
>>> l.tags = 'django javascript ajax'
>>> l.save()
>>> l2 = Lancamento.objects.get(pk=1)
>>> print l2.tags
[<Tag: ajax>, <Tag: django>, <Tag: javascript>]
>>> d = {'credor': 1, 'desc': 'Contas atrasadas', 'vencimento': '05/10/2009', 'valor': '100.00', 'tipo': 'D', 'forma_pagamento': 1, 'caixa': 1, 'pago': True, 'tags': 'internet sites compras mercado'}
>>> from money.forms import *
>>> form = LancamentoForm(d)
>>> form.is_valid()
>>> for item in form:
....    print item
....    5
"""}
