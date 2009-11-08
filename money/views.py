# -*- coding: utf-8 -*-
from django.http import HttpResponse as R
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.forms import forms, fields
from django.forms.models import ModelChoiceField
from django.core.paginator import Paginator, EmptyPage, InvalidPage

#from decimal import Decimal
#from utils.extjs import ExtJSONEncoder
#from django.utils.safestring import mark_safe

from utils.restview import RestView, JsonHttpResponse
from utils.utils import *

from money.models import *
from money.forms import *
from tagging.models import Tag


class LancamentoView(object):
    @login_required
    def new(self, request):
        """
        novo form
        """

        try:
            f = LancamentoForm()
            json = f.as_ext()
        except Exception, e:
            json = '{"success": true, "status": "error", "msg": "%s"}' % e.message

        return R(json,mimetype='application/json')


class LancamentoRest(RestView):
    def GET(self, request):
        if request.GET.get('id'):
            # edit
            try:
                l = Lancamento.objects.get(id=request.GET.get('id'))
                form = LancamentoFormEdit(instance=l)
                json = form.as_ext()
            except Exception, e:
                json = {'Success': False, 'status': 'error', 'msg': e.message}

        else:
            try:
                start = int(request.GET.get('start')) +1
                limit = int(request.GET.get('limit'))
                
                

                l = Lancamento.objects.all() #[:3].reverse()
                total = l.count()

                paginator = Paginator(l, limit)
                try:
                    lancamentos = paginator.page(start)
                except (EmptyPage, InvalidPage):
                    # ultima pagina
                    lancamentos = paginator.page(paginator.num_pages)

                lista = []
                i = 0
                saldo = 0
                json = {'Success': False, 'status': 'error', 'msg': 'Nenhum lancamento cadastrado'}
                for item in lancamentos.object_list:
                    # O saldo inicial eh o valor do primeiro item
                    if i == 0 or item.tipo == 'T':
                        saldo = item.valor
                    else:
                        saldo = saldo + item.valor
                    i = i + 1

                    if item.valor < 0:
                        v = '<span style="color:red">%s</span>' % moeda(item.valor)
                    else:
                        v = '<span style="color:green">%s</span>' % moeda(item.valor)

                    if int(saldo) > 0:
                        s = '<span style="color:green">%s</span>' % moeda(saldo)
                    else:
                        s = '<span style="color:red">%s</span>' % moeda(saldo)

                    d = {
                      'id': item.pk,
                      'vencimento': ymd2str(item.vencimento),
                      'desc': item.desc,
                      'tipo': item.get_tipo_display(),
                      'pago': bool2str(item.pago),
                      'valor': v,
                      'saldo': s,
                    }
                    lista.append(d)
                    json = {'rows': lista, 'status': 'ok', 'total': total, 'success': True}
            except Exception, e:
                json = {'Success': False, 'status': 'error', 'msg': e.message}

        return JsonHttpResponse(json)

    def POST(self, request):
        msg = ''
        form = LancamentoForm(request.POST)
        if form.is_valid():
            f = form.save()
            f.tags = form.cleaned_data['tags']
            #P = request.POST
            #if P.get('tags'):
            #    tags = P.get('tags').split(',')
            #    for item in tags:
            #        tag = item.strip().lower()[:27]

            json = {'success': True, 'status': 'ok', 'msg': 'ok'}
        else:
            for field in form:
                if field.errors:
                    msg = 'Validation error: %s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                    break
            json = {'success': False, 'status': 'error', 'msg': msg}
        return JsonHttpResponse(json)

    def DELETE(self, request, id):
        try:
            l = Lancamento.objects.get(pk=id).delete()
            return JsonHttpResponse({'success': True, 'msg': 'ok'})
        except Exception, e:
            return JsonHttpResponse({'success': False, 'msg': e.message})

    def PUT(self, request, id):
        from django.http import QueryDict

        try:
            PUT = QueryDict(request.raw_post_data)
            l = Lancamento.objects.get(pk=id)
            form = LancamentoForm(PUT, instance=l)
            if form.is_valid():
                f = form.save()
                f.tags = form.cleaned_data['tags']
                return JsonHttpResponse({'success': True, 'status': 'ok', 'msg': 'ok'})
            else:
                msg = 'Invalid form'
                for field in form:
                    if field.errors:
                        msg = 'Validation error: %s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                return JsonHttpResponse({'success': True, 'status': 'error', 'msg': msg})
        except Exception, e:
            return JsonHttpResponse({'success': True, 'status': 'error', 'msg': e.message})



@login_required
def index(request):
    x = Caixa.objects.all()
    t = Tag.objects.all()
    c = Credor.objects.all()
    f = FormaPagamento.objects.all()
    form = LancamentoForm()
    context={'caixas': x, 'tags': t, 'credores': c, 'formaspagamento': f, 'form': form}
    return direct_to_template(request, 'index.html', extra_context=context)


