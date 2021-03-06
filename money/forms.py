# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms import save_instance, Form
from django.forms.fields import CharField, DateField, ChoiceField, IntegerField, BooleanField
from django.forms.models import ModelForm
from django.forms.widgets import DateTimeInput, TextInput
from django.utils import simplejson
from django.utils.safestring import mark_safe

# Imports do projeto
from custom import *
from money.models import Lancamento, Conta
from utils.extjs import ExtJSONEncoder
from tagging.forms import TagField
from tagging.models import Tag


class AutoCompleteTagInput(TextInput):
    """
    Adiciona o recurso de autocompletar tags no admin.
    """
    
    class Media:
        css = {
            'all': ('%s/js/jquery/jquery.autocomplete.css' % settings.MEDIA_URL,)
        }
        js = (
            '%s/js/jquery.js' % settings.MEDIA_URL,
            '%s/js/jquery/lib/jquery.bgiframe.min.js' % settings.MEDIA_URL,
            '%s/js/jquery/lib/jquery.ajaxQueue.js' % settings.MEDIA_URL,
            '%s/js/jquery/jquery.autocomplete.js' % settings.MEDIA_URL
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        #page_tags = Tag.objects.usage_for_model(Lancamento)
        page_tags = Tag.objects.all()
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, tag_list))


class LancamentoForm(ModelForm):
    """
    Form para cadastro de lancamentos.
    """
    
    tags = TagField(max_length=50, label='Tags', required=False, widget=AutoCompleteTagInput())
    vencimento = DateField(('%d/%m/%Y',), label='Vencimento', widget=DateTimeInput(format='%d/%m/%Y'))
    tipo = ChoiceField(choices=Lancamento.TIPO_CHOICES)
    valor = PositiveDecimalField()
    
    class Meta:
        model = Lancamento
        fields = ['desc','vencimento','valor','tipo','forma_pagamento','credor','caixa','tags','pago']
    
    def __init__(self, *args, **kwargs):
        super(LancamentoForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.initial['tags'] = ' '.join([item.name for item in Tag.objects.get_for_object(self.instance)]) #()

    def as_ext(self):
        # Converte os campos para o formato ExtJS
        return mark_safe(simplejson.dumps(self,cls=ExtJSONEncoder))


class LancamentoFormEdit(LancamentoForm):
    """
    Os mesmos campos do LancamentoForm, apenas adicionando o campo id.
    """
    
    id = HiddenIdField() #(show_hidden_initial=True)
    
    class Meta:
        model = Lancamento
        fields = ['id','desc','vencimento','valor','tipo','forma_pagamento','credor','caixa','tags','pago']
    
    def as_ext(self):
        return mark_safe(simplejson.dumps(self,cls=ExtJSONEncoder))


class LancamentoFormFilter(Form):
    """
    Form apenas para validar os dados enviados para filtrar lancamentos.
    """
    
    cadastro = DateField(('%d/%m/%Y',), required=False, widget=DateTimeInput(format='%d/%m/%Y'))
    vencimento = DateField(('%d/%m/%Y',), required=False, widget=DateTimeInput(format='%d/%m/%Y'))
    credor = CharField(required=False)
    caixa = CharField(required=False)
    tipo = ChoiceField(choices=Lancamento.TIPO_CHOICES, required=False)
    pago = BooleanField(required=False)
    tags = TagField(max_length=50, required=False)
    
