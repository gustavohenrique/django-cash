# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from money.models import *
from money.calculos import *

class MoneyTest(TestCase):

    fixtures = ['auth.json','money.json']

    def setUp(self):
        self.c = Client()
        self.c.login(username='gu', password='stavo')
        self.jsonRespOk = '{"status": "ok", "rows": "", "success": true, "msg": "ok", "total": 0}'


    def _adicionarLancamento(self, novos_dados):
        dados_lancamento = {
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

        dados_lancamento.update(novos_dados)
        response = self.c.post(reverse('money_add'), dados_lancamento)
        self.failUnlessEqual(response.content, self.jsonRespOk)
        #c.get('/customers/details/', {'name': 'fred', 'age': 7}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')


    def testAdicionarLancamentoNumComVirgula(self):
        self._adicionarLancamento({'valor': '115,50'})


    def testAdicionarLancamentoForeignKeysNaoExistem(self):
        dados_lancamento = {
            'credor': 9999,
            'desc': 'Contas atrasadas',
            'vencimento': '05/10/2009',
            'valor': '100.00',
            'tipo': 'D',
            'forma_pagamento': 9999,
            'caixa': 9999,
            'pago': True,
            'tags': 'internet sites compras mercado'
        }

        response = self.c.post(reverse('money_add'), dados_lancamento)
        self.assertNotEqual(response.content, self.jsonRespOk)


    def testEditarLancamentoComIdUm(self):
        self._adicionarLancamento({'valor': '1,99'})
        response = self.c.get('%s?id=1' % reverse('money_list'))
        jsonRespEditError = '{"Success": false, "status": "error", "msg": "Lancamento nao encontrado"}'
        self.assertNotEquals(response.content, jsonRespEditError)


    def testListarLancamentosCadastradosDeZeroAdez(self):
        response = self.c.get('%s?start=0&limit=10' % reverse('money_list'))
        self.assertContains(response, '"success": true', 1, 200)


    def testDeletarLancamentoComIdUm(self):
        self._adicionarLancamento({'valor': '1,99'})
        response = self.c.delete(reverse('money_del', args=[1]))
        self.failUnlessEqual(response.content, self.jsonRespOk)


    def testAtualizarLancamentoComIdUm(self):
        self._adicionarLancamento({'valor': '1,99'})
        response = self.c.get('%s?id=1' % reverse('money_list'))
        jsonRespEditError = '{"Success": false, "status": "error", "msg": "Lancamento nao encontrado"}'

        self.assertNotEquals(response.content, jsonRespEditError)

        dados_lancamento = {
            'credor': 1,
            'desc': 'Lancamento alterado',
            'vencimento': '08/01/2010',
            'valor': '350.00',
            'tipo': 'C',
            'caixa': 1,
            'forma_pagamento': 2,
            'pago': False,
        }
        response2 = self.c.put(reverse('money_upd', args=[1]), dados_lancamento)
        self.assertEqual(response2.content, self.jsonRespOk)

    def testCalcularInserirSaldoEmLancamentosPagina0(self):
        resultado_esperado = [{
            'id': 1,
            'vencimento': '01/03/2009',
            'desc': u'Salario',
            'tipo': u'Crédito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:green">R$ 1.000,00</span>',
            'saldo': u'<span style="color:green">R$ 1.000,00</span>'
        }, {
            'id': 2,
            'vencimento': '25/03/2009',
            'desc': u'Livro Code Complete',
            'tipo': u'Débito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 150,00</span>',
            'saldo': u'<span style="color:green">R$ 850,00</span>'
        }, {
            'id': 3,
            'vencimento': '25/03/2009',
            'desc': u'Livro Frameworks para Desenvolvimento PHP',
            'tipo': u'Débito',
            'pago': '<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 50,00</span>',
            'saldo': u'<span style="color:green">R$ 800,00</span>',
        }]
        resultados_por_pagina = 3
        pagina = 0
        lancamentos = Lancamento.objects.all().order_by('id')[:resultados_por_pagina]

        lista_lancamentos = CalculoLancamento().saldos_a_partir_de(lancamentos, pagina, resultados_por_pagina)
        self.assertEquals(lista_lancamentos, resultado_esperado)

    def testCalcularInserirSaldoEmLancamentosPagina1(self):
        resultado_esperado = [{
            'id': 4,
            'vencimento': '25/03/2009',
            'desc': u'Livro PHP Profissional - Aprenda a desenvolver sistemas',
            'tipo': u'Débito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 70,00</span>',
            'saldo': u'<span style="color:green">R$ 730,00</span>'
        }, {
            'id': 5,
            'vencimento': '31/03/2009',
            'desc': u'Salario',
            'tipo': u'Crédito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:green">R$ 1.170,00</span>',
            'saldo': u'<span style="color:green">R$ 1.900,00</span>'
        }, {
            'id': 6,
            'vencimento': '01/04/2009',
            'desc': u'Outras entradas',
            'tipo': u'Crédito',
            'pago': '<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:green">R$ 100,00</span>',
            'saldo': u'<span style="color:green">R$ 2.000,00</span>',
        }]

        resultados_por_pagina = 3
        pagina = 1
        lancamentos = Lancamento.objects.all().order_by('id')

        lista_lancamentos = CalculoLancamento().saldos_a_partir_de(lancamentos, pagina, resultados_por_pagina)
        self.assertEquals(lista_lancamentos, resultado_esperado)

    def testCalcularInserirSaldoEmLancamentosPagina1ResultadoPorPaginaIgual0(self):
        resultado_esperado = [{
            'id': 1,
            'vencimento': '01/03/2009',
            'desc': u'Salario',
            'tipo': u'Crédito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:green">R$ 1.000,00</span>',
            'saldo': u'<span style="color:green">R$ 1.000,00</span>'
        }, {
            'id': 2,
            'vencimento': '25/03/2009',
            'desc': u'Livro Code Complete',
            'tipo': u'Débito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 150,00</span>',
            'saldo': u'<span style="color:green">R$ 850,00</span>'
        }]

        resultados_por_pagina = 2
        pagina = 0
        lancamentos = Lancamento.objects.all().order_by('id')

        lista_lancamentos = CalculoLancamento().saldos_a_partir_de(lancamentos, pagina, resultados_por_pagina)
        self.assertEquals(lista_lancamentos, resultado_esperado)

    def testCalcularInserirSaldoEmLancamentosPagina1ResultadoPorPaginaIgual3(self):
        resultado_esperado = [{
            'id': 7,
            'vencimento': '10/04/2009',
            'desc': u'Mesa para telefone Artely',
            'tipo': u'Débito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 80,00</span>',
            'saldo': u'<span style="color:green">R$ 1.920,00</span>'
        }, {
            'id': 8,
            'vencimento': '28/04/2009',
            'desc': u'Teclado Multimidia USB',
            'tipo': u'Débito',
            'pago': u'<div class="ok-icon">&nbsp;</div>',
            'valor': u'<span style="color:red">R$ 35,00</span>',
            'saldo': u'<span style="color:green">R$ 1.885,00</span>'
        }]

        resultados_por_pagina = 2
        pagina = 3
        lancamentos = Lancamento.objects.all().order_by('id')

        lista_lancamentos = CalculoLancamento().saldos_a_partir_de(lancamentos, pagina, resultados_por_pagina)
        self.assertEquals(lista_lancamentos, resultado_esperado)





__test__ = {"doctest": """
"""}
