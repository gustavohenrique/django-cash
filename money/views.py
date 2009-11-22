# -*- coding: utf-8 -*-

# Imports do Django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.forms import forms, fields
from django.forms.models import ModelChoiceField
from django.http import HttpResponse as R
from django.utils import simplejson
from django.views.generic.simple import direct_to_template

# Imports do Python
import datetime

# Imports do projeto
from utils.restview import RestView, JsonHttpResponse
from utils.utils import *
from money.models import *
from money.forms import *
from tagging.models import Tag


LIMITE_RESULTADO_GRID = 30

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
        
    
    @login_required
    def filter(self, request):
        """
        Exibe os lancamentos a partir de uma regra de filtragem
        """
        from money.filters import LancamentoFilter
        f = LancamentoFilter(request.GET, queryset=Lancamento.objects.all())
        return direct_to_template(request, 'index.html', extra_context={'f': f})

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
                if request.GET.get('modo') == 'filter':
                    GET = request.GET
                    
                    DADOS_GET = {}
                    # Adiciona em DADOS_GET apenas os campos que foram definidos no model Lancamento
                    for nome_campo in GET:
                        if nome_campo in [field.name for field in Lancamento._meta.fields] or nome_campo[:10] == 'vencimento':
                            if not GET.get(nome_campo) == '' and not GET.get(nome_campo)[:10] == 'Vencimento' and not GET.get(nome_campo)[:10] == 'Vencimento':
                                DADOS_GET.update({str(nome_campo): str(GET.get(nome_campo))})
                    
                    # o campo pago possui um valor booleano, entao substitui S por True e N por False
                    if DADOS_GET.has_key('pago'):
                        DADOS_GET['pago'] = [False, True] [DADOS_GET['pago'] == 'S']
                    
                    print DADOS_GET
                    form = LancamentoFormFilter(DADOS_GET)
                    if form.is_valid():
                        str_filter = ''
                        if DADOS_GET.has_key('vencimento_inicial'):
                            vencimento_inicial = DADOS_GET['vencimento_inicial'].split('/')
                            vencimento_inicial = '%s-%s-%s' % (vencimento_inicial[2], vencimento_inicial[1], vencimento_inicial[0])
                            str_filter = 'vencimento__gte="%s",' % vencimento_inicial
                        if DADOS_GET.has_key('vencimento_final'):
                            vencimento_final = DADOS_GET['vencimento_final'].split('/')
                            vencimento_final = '%s-%s-%s' % (vencimento_final[2], vencimento_final[1], vencimento_final[0])
                            str_filter = 'vencimento__lte="%s",' % vencimento_final
                            
                        if DADOS_GET.has_key('vencimento_inicial') and DADOS_GET.has_key('vencimento_final'):
                            str_filter = 'vencimento__gte="%s",vencimento__lte="%s",' % (vencimento_inicial, vencimento_final)
                        
                        try:
                            DADOS_GET.pop('vencimento_inicial')
                        except:
                            pass
                        try:
                            DADOS_GET.pop('vencimento_final')
                        except:
                            pass
                        
                        for item in DADOS_GET:
                            valor = '"%s"' % DADOS_GET[item]
                            
                            # o campo pago possui um valor booleano, entao retira as aspas
                            if item == 'pago':
                                valor = valor.replace('"','')
                            str_filter += '%s=%s,' % (item, valor)
                            
                        
                        str_filter = str_filter.rstrip(',')
                        
                        exec('l = Lancamento.objects.filter(%s)' % str_filter)
                        total = l.count()
                        
                        if request.GET.get('tags') != '':
                            print request.GET.get('tags')
                            lista_resultado_filtro = []
                            tags_via_get = request.GET.get('tags').split('+')
                            for lancamento in l:
                                lista_tags_do_objeto = []
                                tags_do_objeto = lancamento.tags.values()
                                for item in tags_do_objeto:
                                    lista_tags_do_objeto.append(item['slug'])
                                    # Remove o objeto do resultado cujo nao posui nenhuma das tags definidas no filtro
                                    for tag in tags_via_get:
                                        if tag in lista_tags_do_objeto:
                                            # Ok. O objeto possui pelo menos uma das tags do filtro
                                            # Evita duplicidade e adiciona o objeto a lista de resultado
                                            if not lancamento in lista_resultado_filtro:
                                                lista_resultado_filtro.append(lancamento)
                                        else:
                                            pass
                                            # O objeto é removido da lista de resultados
                            total = len(lista_resultado_filtro)
                            if total > 0:
                                l = lista_resultado_filtro
                            else:
                                json = {'rows': [{'id':0,'desc':'Nenhum objeto encontrado com as tags fornecidas'}], 'status': 'error', 'total': 0, 'success': True}
                                return JsonHttpResponse(json)
                        
                    else:
                        for field in form:
                            if field.errors:
                                msg = 'Validation error: %s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                                break
                        json = {'rows': [{'id':0,'desc':msg}], 'status': 'error', 'total': 0, 'success': True}
                        return JsonHttpResponse(json)
                else:
                    l = Lancamento.objects.all()
                    total = l.count()
                    
                start = int(request.GET.get('start',0)) +1
                limit = int(request.GET.get('limit', LIMITE_RESULTADO_GRID))

                

                paginator = Paginator(l, limit)
                try:
                    lancamentos = paginator.page(start)
                except (EmptyPage, InvalidPage):
                    # ultima pagina
                    lancamentos = paginator.page(paginator.num_pages)

                lista = []
                i = 0
                saldo = 0

                json = {'rows': [{'id':0,'desc':'Nenhum cadastro'}], 'status': 'error', 'total': total, 'success': True}

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
                        
                    if item.pago == True:
                        pago = '<div class="ok-icon">&nbsp;</div>'
                    else:
                        pago = '<div class="cancel-icon">&nbsp;</div>'

                    d = {
                      'id': item.pk,
                      'vencimento': item.vencimento.strftime('%d/%m/%Y'),
                      'desc': item.desc,
                      'tipo': item.get_tipo_display(),
                      'pago': pago,
                      'valor': v,
                      'saldo': s,
                    }
                    lista.append(d)
                    json = {'rows': lista, 'status': 'ok', 'total': total, 'success': True}
            except Exception, e:
                json = {'Success': True, 'status': 'error', 'msg': e.message}

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
    l = Lancamento.objects.filter(pago=False)
    form = LancamentoForm()
    tipos = []
    for item in Lancamento.TIPO_CHOICES:
        tipos.append({'id': item[0], 'tipo': item[1]})
        
    context={
        'caixas': x,
        'tags': t,
        'credores': c,
        'formaspagamento': f,
        'contas_nao_pagas': l,
        'tipos': tipos,
        'form': form
    }
    return direct_to_template(request, 'index.html', extra_context=context)


