# -*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client


__all__ = ['AccountViews']


class AccountViews(TestCase):

    fixtures = ['auth.xml', 'core.xml']

    def setUp(self):
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
        #response = self.client.get('/api/read/1/')
        self.assertEquals(expected, response.content)


