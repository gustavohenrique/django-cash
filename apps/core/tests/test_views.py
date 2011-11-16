# -*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client


__all__ = ['AccountViews']


class AccountViews(TestCase):

    fixtures = ['auth.xml', 'core.xml']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_get_all_accounts_by_user(self):
        expected = '{"total":2,"data":["id":1,"name":""]}'
        response = self.client.get(reverse('account_get'))
        self.assertEquals(expected, response.content)
