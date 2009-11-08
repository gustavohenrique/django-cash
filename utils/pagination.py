# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson


def pagination(object_list, fields, page):
  """
  Paginacao ajax.

  Retorna um dicionario contendo os registros de determinada pagina.
  No lado client uma funcao em javascript cria um datagrid contendo os dados retornados.

  Parametros:

    object_list - Queryset de objetos a serem exibidos
    fields - Campos que serao exibidos de cada registro
    page - Pagina que sera exibida

  Exemple de uso:

    from sigep.ajaxtools.pagination import pagination
    page = 1
    fields = ['name','phone','email']
    cli = Client.objects.all()
    return pagination(cli, fields, page)
  """

  # numero de resultados por pagina
  show_per_page = 10
  # adiciona o campo id a lista de campos obtidos
  fields.insert(0,'id')

  paginator = Paginator(object_list,show_per_page)
  try:
    listing = paginator.page(page)
  except (EmptyPage, InvalidPage):
    listing = paginator.page(paginator.num_pages)

  li1 = []  # ['1','rio']
  li2 = []  # [['1','rio'], ['2','sao paulo'], {'previous_page_number:0','next_page_number':2}]

  for obj in listing.object_list:
    for f in fields:
      li1.append(str(eval('obj.'+f)))
    li2.append(li1)
    li1 = []

  data = [{
    'previous_page_number': listing.previous_page_number(),
    'next_page_number': listing.next_page_number(),
    'current_page': listing.number,
    'num_pages': paginator.num_pages,
    'total_result': object_list.count(),
    'listing': list(li2)
  }]

  """
  Retorna em formato JSON para ser utilizado com ajax
  Exemplo de retorno:

  [{
    'previous_page_number': 1,
    'next_page_number': 3,
    'current_page': 2,
    'num_pages': 1,
    'total_result': 2,
    'listing': [[1, 'Gustavo Henrique', '(22) 9123-8456'], [2, 'Maria', '(21) 3224-1234']]
  }]
  """
  json = simplejson.dumps(data)
  return HttpResponse(json,mimetype="application/json")

  # fields = ['name','mobile','birth']
  # retorna:
