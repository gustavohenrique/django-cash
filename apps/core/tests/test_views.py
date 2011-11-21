# -*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from core.models import Account


__all__ = ['AccountViews']


class AccountViews(TestCase):

    fixtures = ['auth.xml', 'core.xml']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.client.login(username='admin', password='admin')
    
    def test_get_all_accounts_for_specific_user(self):
        expected = ('{"total": 3, "data": [' 
            '{"initial": "1", "agency": "7876-5", "number": "98871-X", "id": 2, "name": "Banco do Brasil"}, '
            '{"initial": "2", "agency": "7876-5", "number": "87936-1", "id": 3, "name": "Banco do Brasil"}, '
            '{"initial": "0", "agency": "3575", "number": "67546-5", "id": 1, "name": "Itau"}], '
            '"success": "true"}')
        response = self.client.get(reverse('accounts-list', kwargs={'user':'1'}))
        self.assertEquals(expected, response.content)

    def test_get_account_by_id(self):
        expected = '{"total": 5, "data": {"initial": "0", "agency": "3575", "number": "67546-5", "id": 1, "name": "Itau"}, "success": "true"}'
        response = self.client.get(reverse('accounts-read', kwargs={'id':1}))
        self.assertEquals(expected, response.content)
    
    def test_create_account_with_required_fields(self):
        request = {'data': [{'name':'Citibank', 'initial':'11'}]}
        expected = '{"total": 5, "data": {"initial": "11", "agency": "", "number": "", "id": 4, "name": "Citibank"}, "success": "true"}'
        response = self.client.post(reverse('accounts-create'), request, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(expected, response.content)

        account = Account.objects.get(id=4)
        self.assertEquals('Citibank', account.name)

    def test_update_account(self):
        request = {'data': [{'name':'Itau/Unibanco', 'initial':'500', 'agency': '2749', 'number':'39274-2'}]}
        expected = '{"total": 5, "data": {"initial": "500", "agency": "3575", "number": "39274-2]", "id": 1, "name": "Itau/Unibanco"}, "success": "true"}'
        response = self.client.put(reverse('accounts-update', kwargs={'id':'1'}), data=request, content_type='application/json')
        self.assertEquals(expected, response.content)

        account = Account.objects.get(id=1)
        self.assertEquals('Itau/Unibanco', account.name)


