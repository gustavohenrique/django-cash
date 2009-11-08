# -*- coding: utf-8 -*-
from django.forms.fields import CharField, DecimalField, IntegerField
from django.forms.forms import ValidationError
from django.forms.widgets import Textarea, HiddenInput
from django.forms import Widget
from django.utils.safestring import mark_safe

from decimal import Decimal

class TextField(CharField):
    """
    Create a textarea with max_length=100000
    """

    def __init__(self, max_length=100000, min_length=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        self.widget = Textarea
        super(CharField, self).__init__(*args, **kwargs)


class PositiveDecimalWidget(Widget):
    """
    Retira o sinal de negativo (-) do valor
    """

    def render(self, name, value, attrs):
        if value:
            v = str(value).replace('-','')
        else:
            v = ''
        return mark_safe(u'<input type="text" id="id_%s" name="%s" value="%s">' % (name, name, v))


class PositiveDecimalField(DecimalField):
    """
    Troca a virgula (,) pelo ponto (.) como separador decimal
    """
    
    def __init__(self, max_value=None, min_value=0, max_digits=12, decimal_places=2, *args, **kwargs):
        self.widget = PositiveDecimalWidget()
        super(DecimalField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            value = 0
        else:
            try:
                value = Decimal(str(value).replace(',','.').replace('-',''))
            except:
                raise ValidationError('Informe um numero decimal %s' % value)
        return value


class HiddenIdField(IntegerField):
    """
    Campo oculto contendo o id do objeto. Útil em forms para alteração de dados
    """
    
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        self.widget = HiddenInput()
        super(IntegerField, self).__init__(*args, **kwargs)
    
