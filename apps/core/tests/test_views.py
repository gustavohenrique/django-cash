# -*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client


__all__ = ['AccountViews']


class AccountViews(TestCase):

    fixtures = ['auth.xml', 'core.xml']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.client.login(username='admin', password='admin')
    
    def test_get_all_accounts(self):
        expected = ('{"total": 3, "data": [' 
            '{"initial": "1", "agency": "7876-5", "number": "98871-X", "id": 2, "name": "Banco do Brasil"}, '
            '{"initial": "2", "agency": "7876-5", "number": "87936-1", "id": 3, "name": "Banco do Brasil"}, '
            '{"initial": "0", "agency": "3575", "number": "67546-5", "id": 1, "name": "Itau"}], '
            '"success": "true"}')
        response = self.client.get(reverse('accounts-list', kwargs={'owner':'1'}))
        self.assertEquals(expected, response.content)

    def test_get_account_by_id(self):
        expected = '{"total": 5, "data": {"initial": "0", "agency": "3575", "number": "67546-5", "id": 1, "name": "Itau"}, "success": "true"}'
        response = self.client.get(reverse('accounts-read', kwargs={'owner':'1', 'id':1}))
        self.assertEquals(expected, response.content)
    
    def test_create_account_only_required_field(self):
        expected = '{"total": 5, "data": {"initial": "11", "agency": "", "number": "", "id": 4, "name": "Citibank"}, "success": "true"}'
        response = self.client.post(reverse('accounts-create'), {'data':[{'owner':'1', 'name':'Citibank', 'initial':'11'}]}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(expected, response.content)

