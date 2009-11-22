# -*- coding: utf-8 -*-

# Imports do Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.forms import forms, fields
from django.forms.models import ModelChoiceField
from django.http import HttpResponse as R
from django.http import QueryDict
from django.utils import simplejson
from django.views.generic.simple import direct_to_template

# Imports do Python
import datetime

# Imports do projeto
from utils.restview import RestView, JsonHttpResponse
from utils.utils import moeda
from money.models import *
from money.forms import *
from tagging.models import Tag


"""
Consultas Ajax geradas pelo ExtJS devem retornar um dict em formato JSON
contendo pelo menos 1 chave/valor com 'success': True. Significa que a
consulta foi realizada com sucesso.
Outras chaves são opcionais e nesse caso 'status' pode ser 'ok' - a
ação realizada foi com sucesso - ou 'error' - ocorreu um exception ou
uma consulta sem resultado.
'rows' é uma lista de valores à serem exibidos e 'total' o total de itens
contidos em 'rows'.
"""
DEFAULT_EXTJS_RESP = {"success": True, "status": "error", "msg": "", "rows": "", "total":0}

@login_required
def index(request):
    """
    Exibe a página inicial do projeto.
    
    Obtem os dados cadastrados para montar o formulário de filtro.
    Exibe os lançamentos que não foram pagos (contas à pagar).
    """
    
    x = Caixa.objects.all()                     # Caixas
    t = Tag.objects.all()                       # Tags
    c = Credor.objects.all()                    # Credores
    f = FormaPagamento.objects.all()            # Forma de pagamento
    l = Lancamento.objects.filter(pago=False)   # Lancamentos não pagos
    
    # Uma variável no models.py que define os tipos de pagamentos permitidos.
    tipos = []
    for item in Lancamento.TIPO_CHOICES:
        # Cria uma lista para ser usada da mesma forma que uma QuerySet no template
        tipos.append({'id': item[0], 'tipo': item[1]})
        
    context={
        'caixas': x,
        'tags': t,
        'credores': c,
        'formaspagamento': f,
        'contas_nao_pagas': l,
        'tipos': tipos,
    }
    # Carrega o template passando as variáveis
    return direct_to_template(request, 'index.html', extra_context=context)


@login_required
def new(request):
    """
    Cria o form para cadastro.
    Retorna os campos no formato json e convertidos para campos ExtJS.
    """

    try:
        f = LancamentoForm()
        json = f.as_ext()
    except:
        json = DEFAULT_EXTJS_RESP
        json = u'%s' % json.update({'msg': u'Formulário apresenta algum erro e não pode ser exibido'})

    return R(json,mimetype='application/json')


class LancamentoRest(RestView):
    """
    Utiliza Restful para CRUD.
    
    GET: editar um objeto ou obter uma lista de objetos.
    POST: cadastrar um objeto.
    DELETE: excluir um objeto.
    PUT: atualizar um objeto.
    """
    
    @login_required
    def GET(self, request):
        """
        Consulta de objetos.
        
        Se for passado um ID para a URL, então obtém os dados do objeto
        que possui esse ID, cria o formulário preenchido com esses dados
        e retorna utilzando o formato JSON.
        
        Se nenhum ID foi passado, então verifica se é para exibir todos
        os objetos ou objetos de acordo com determinados parametros
        passados para a URL (um filtro).
        """
        
        if request.GET.get('id'):
            # Editar um objeto
            try:
                l = Lancamento.objects.get(id=request.GET.get('id'))
                form = LancamentoFormEdit(instance=l)
                json = form.as_ext()
            except DoesNotExists:
                json = {'Success': False, 'status': 'error', 'msg': e.message}

        else:
            try:
                # Consulta baseada em filtro
                if request.GET.get('modo') == 'filter':
                    # Copia os dados do request.GET
                    GET = request.GET
                    
                    # Dicionario que vai armazenar apenas os valores do GET que serão utilizados
                    DADOS_GET = {}
                    
                    for nome_campo in GET:
                        """
                        Adiciona em DADOS_GET apenas os campos/valores que fazem parte do model Lancamento
                        ou se o campo enviado pelo formulário começa com o nome 'vencimento'. Isso porque
                        existe o campo vencimento no models mas no form de filtro existe 'vencimento_inicial'
                        e 'vencimento_final'.
                        Caso o campo a ser adicionado esteja vazio ('') ou comece com 'Vencimento', não será
                        adicionado. O ExtJS envia a string definida como emptyText caso o campo não seja
                        preenchido, sendo assim, os campos 'vencimento_inicial' e 'vencimento_final' não
                        enviarão valores válidos se o usuário deixar o campo em branco.
                        """
                        if nome_campo in [field.name for field in Lancamento._meta.fields] or nome_campo[:10] == 'vencimento':
                            if not GET.get(nome_campo) == '' and not GET.get(nome_campo)[:10] == 'Vencimento' and not GET.get(nome_campo)[:10] == 'Vencimento':
                                DADOS_GET.update({str(nome_campo): str(GET.get(nome_campo))})
                    
                    # O campo pago possui um valor booleano, então substitui 'S' por True e qualquer outro valor por False
                    if DADOS_GET.has_key('pago'):
                        DADOS_GET['pago'] = [False, True] [DADOS_GET['pago'] == 'S']
                    
                    """
                    LancamentoFormFilter foi criado apenas para validar os dados
                    enviados para filtrar uma consulta.
                    """
                    form = LancamentoFormFilter(DADOS_GET)
                    if form.is_valid():
                        # str_filter vai conter os campos e valores a serem passados ao método filter()
                        str_filter = ''
                        
                        # Converte data do formato 'dd/mm/yyyy' para 'yyyy-mm-dd'
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
                        
                        """
                        Tente remover os campos 'vencimento_inicial' e 'vencimento_final'
                        porque não existem na classe Lancamento. A função desses campos
                        é apenas fornecer o intervalo de datas de vencimento.
                        Esses campos só existem em DADOS_GET se foram preenchidos no form.
                        """
                        try:
                            DADOS_GET.pop('vencimento_inicial')
                        except:
                            pass
                        try:
                            DADOS_GET.pop('vencimento_final')
                        except:
                            pass
                        
                        """
                        Adiciona em str_filter os campos e valores contidos em DADOS_GET
                        e coloca uma virgula (,) após cada valor.
                        """
                        for item in DADOS_GET:
                            valor = '"%s"' % DADOS_GET[item]
                            
                            """
                            O campo pago possui um valor booleano, entao retira as aspas
                            de "True" e fica como True.
                            """
                            if item == 'pago':
                                valor = valor.replace('"','')
                            str_filter += '%s=%s,' % (item, valor)
                            
                        # Remove a última vírgula da string
                        str_filter = str_filter.rstrip(',')
                        
                        # Instância o objeto passando a string como parâmetro para o filter()
                        exec('l = Lancamento.objects.filter(%s)' % str_filter)
                        
                        # Total de objetos "filtrados"
                        total = l.count()
                        
                        """
                        Se foram informadas tags no filtro, verifica se cada objeto
                        dentro da QuerySet l possui pelo menos uma das tags definidas pelo
                        usuário. Caso não tenham nenhuma delas então o objeto é removido
                        da lista de resultados.
                        """
                        if request.GET.get('tags') != '':
                            
                            # Lista similar à uma QuerySet que vai conter os objetos a serem exibidos
                            lista_resultado_filtro = []
                            
                            # Tags são enviadas como string separadas pelo sinal de (+).
                            tags_via_get = request.GET.get('tags').split('+')
                            
                            # Para cada objeto retornado pelo filtro...
                            for lancamento in l:
                                # Lista que vai conter todas as tags do objeto
                                lista_tags_do_objeto = []
                                
                                # Dict com o id, slug e nome de cada tag do objeto
                                tags_do_objeto = lancamento.tags.values()
                                
                                # Para cada tag do objeto, adiciona o seu slug à lista de tags
                                for item in tags_do_objeto:
                                    lista_tags_do_objeto.append(item['slug'])
                                    
                                    # Remove o objeto do resultado que não posui nenhuma das tags definidas no filtro
                                    for tag in tags_via_get:
                                        if tag in lista_tags_do_objeto:
                                            # Ok. O objeto possui pelo menos uma das tags do filtro
                                            # Evita duplicidade e adiciona o objeto a lista de resultado
                                            if not lancamento in lista_resultado_filtro:
                                                lista_resultado_filtro.append(lancamento)
                                        else:
                                            # O objeto não foi adicionado à lista de resultados
                                            pass

                            # Total de objetos que possuem pelo menos uma das tags definida no filtro
                            total = len(lista_resultado_filtro)
                            if total > 0:
                                # A variável l passa a conter a lista de resultados
                                l = lista_resultado_filtro
                            else:
                                # O filtro não retornou nenhum resultado
                                json = {'rows': [{'id':0,'desc':'Nenhum resultado encontrado com as tags fornecidas'}], 'status': 'error', 'total': 0, 'success': True}
                                return JsonHttpResponse(json)
                        
                    else:
                        # O formulário de filtro não foi preenchido corretamente. Obtém a mensagem de erro e exibe no grid
                        for field in form:
                            if field.errors:
                                msg = u'Erro de Validação: %s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                                break
                        json = DEFAULT_EXTJS_RESP
                        json.update({'rows': [{'id': 0, 'desc': msg}]})
                        return JsonHttpResponse(json)
                        
                else:
                    # Nenhum filtro foi definido, então obtém todos os objetos de Lancamento
                    l = Lancamento.objects.all()
                    total = l.count()

                # Faz a paginação do resultado a ser exibido no grid
                start = int(request.GET.get('start',0)) +1
                limit = int(request.GET.get('limit', settings.LINHAS_POR_GRID))
                paginator = Paginator(l, limit)
                try:
                    lancamentos = paginator.page(start)
                except (EmptyPage, InvalidPage):
                    # ultima pagina
                    lancamentos = paginator.page(paginator.num_pages)

                # Resposta se a consulta não retornou nenhum resultado
                json = DEFAULT_EXTJS_RESP
                json.update({'rows': [{'id':0,'desc':'Nenhum cadastro'}], 'total': total})
                
                # Lista que vai ter os valores já formatados que vão ser exibidos no grid
                lista_resultado = []
                
                # Contador do loop
                cont = 0
                
                # Saldo é a soma total dos lançamentos que vão ser exibidos
                saldo = 0
                
                # Para cada objeto retornado na consulta...
                for item in lancamentos.object_list:
                    """
                    O saldo inicial é igual ao valor do primeiro item.
                    Se o tipo de pagamento for Transferência (tipo='T'), o valor do lançamento
                    não vai ser somado ou subtraído ao saldo.
                    """
                    if cont == 0 or item.tipo == 'T':
                        # Saldo inicial é igual ao valor do primeiro lançamento
                        saldo = item.valor
                    else:
                        # Saldo igual a soma dos valores
                        saldo = saldo + item.valor
                        
                    # Incrementa o contador
                    cont = cont + 1
                    
                    # A funcao moeda é similar ao metodo locale.currency (nao existe no python-2.4)
                    # Se o valor do lançamento for negativo, retira o sinal de menos e define a cor vermelha
                    if item.valor < 0:
                        v = '<span style="color:red">%s</span>' % moeda(item.valor)
                    else:
                        v = '<span style="color:green">%s</span>' % moeda(item.valor)

                    # Se o valor do lançamento for positivo, define a cor verde
                    if int(saldo) > 0:
                        s = '<span style="color:green">%s</span>' % moeda(saldo)
                    else:
                        s = '<span style="color:red">%s</span>' % moeda(saldo)
                    
                    # Troca o valor booleano por uma imagem
                    if item.pago == True:
                        pago = '<div class="ok-icon">&nbsp;</div>'
                    else:
                        pago = '<div class="cancel-icon">&nbsp;</div>'
                        
                    # Dados do lançamento
                    d = {
                        'id': item.pk,
                        'vencimento': item.vencimento.strftime('%d/%m/%Y'),
                        'desc': item.desc,
                        'tipo': item.get_tipo_display(),
                        'pago': pago,
                        'valor': v,
                        'saldo': s,
                    }
                    
                    # Adiciona o lançamento à lista de resultados
                    lista_resultado.append(d)
                
                json = DEFAULT_EXTJS_RESP
                json.update({'rows': lista_resultado, 'status': 'ok', 'total': total})
                
            except:
                # Erro ao tentar realizar uma consulta ou executar o filtro
                json = DEFAULT_EXTJS_RESP
                json.update({'msg': 'Erro inesperado ao tentar executar a consulta'})

        return JsonHttpResponse(json)

    
    @login_required
    def POST(self, request):
        """
        Cadastra um objeto.
        Verifica se os dados enviados pelo formulário são válidos e então cadastra.
        """
        
        json = DEFAULT_EXTJS_RESP
        
        # Instancia o form passando os dados submetidos via POST
        form = LancamentoForm(request.POST)
        if form.is_valid():
            # Se o formulário for válido, cadastra no banco de dados
            f = form.save()
            
            # LancamentoForm ao ser instanciado verifica se há tags fornecidas no form e então as adiciona ao objeto.
            # Consulte arquivo forms.py
            f.tags = form.cleaned_data['tags']
            json.update({'status': 'ok'})
        else:
            # form inválido
            for field in form:
                if field.errors:
                    msg = '%s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                    break
            #json.update({'rows': [{'id': 0, 'desc': msg}]})
            json.update({'msg': msg})
            
        return JsonHttpResponse(json)

    
    @login_required
    def DELETE(self, request, id):
        """
        Exclui um objeto a partir do id fornecido.
        """
        
        json = DEFAULT_EXTJS_RESP
        try:
            l = Lancamento.objects.get(pk=id).delete()
            json.update({'msg': 'ok'})
        except:
            json.update({'msg': 'Erro ao tentar excluir'})
            
        return JsonHttpResponse(json)


    @login_required
    def PUT(self, request, id):
        """
        Atualiza o objeto a partir do id fornecido.
        """
        
        json = DEFAULT_EXTJS_RESP
        try:
            # Obtem os dados enviados pelo formulário
            PUT = QueryDict(request.raw_post_data)
            
            # Instancia o objeto de acordo com o id
            l = Lancamento.objects.get(pk=id)
            
            # Instancia o form passando os dados do formulário e o objeto
            form = LancamentoForm(PUT, instance=l)
            
            # Se o form for válido, atualiza os dados e as tags
            if form.is_valid():
                f = form.save()
                f.tags = form.cleaned_data['tags']
                json.update({'status': 'ok', 'msg': 'ok'})
            else:
                for field in form:
                    if field.errors:
                        msg = '%s, %s' % (field.label, field.errors[0].replace('<ul class="errorlist"><li>',''))
                        break
                json.update({'msg': msg})
                
        except Exception, e:
            json.update({'msg': 'Erro desconhecido ao tentar atualizar os dados'})
        
        return JsonHttpResponse(json)






