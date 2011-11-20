# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource
from core.models import Account


class AccountResource(ModelResource):
    model = Account
    fields = ('id', 'name', 'agency', 'number', 'initial')
    ordering = ('name',)
    allowed_methods = ('GET', 'POST')

    def filter_response(self, obj):
        """ 
        Override method that given the response content, filter it into a serializable object.
        """
        data = self.serialize(obj)
        return {'total':len(data), 'data':data, 'success':'true'}

