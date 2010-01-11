# -*- coding: utf-8 -*-
from utils.utils import moeda

class CalculoLancamento(object):
    def saldos_a_partir_de(self, lancamentos, pagina, lancamentos_por_pagina):

        #pagina -= 1
        indice_inicial = pagina * lancamentos_por_pagina
        indice_final = indice_inicial + lancamentos_por_pagina

        lista_resultado = []
        contador = 0
        saldo = 0


        # Para cada objeto retornado na consulta...
        for lancamento in lancamentos:
            """
            O saldo inicial é igual ao valor do primeiro item.
            Se o tipo de pagamento for Transferência (tipo='T'), o valor do lançamento
            não vai ser somado ou subtraído ao saldo.
            """
            if contador == 0 or lancamento.tipo == 'T':
                saldo = lancamento.valor
            else:
                # Saldo igual a soma dos valores
                saldo = saldo + lancamento.valor

            contador = contador + 1

            texto_valor_positivo = u'<span style="color:green">%s</span>'
            texto_valor_negativo = u'<span style="color:red">%s</span>'

            if lancamento.valor > 0:
                valor_formatado = texto_valor_positivo % moeda(lancamento.valor)
            else:
                valor_formatado = texto_valor_negativo % moeda(lancamento.valor)

            if int(saldo) > 0:
                saldo_formatado = texto_valor_positivo % moeda(saldo)
            else:
                saldo_formatado = texto_valor_negativo % moeda(saldo)

            if lancamento.pago == True:
                pago_formatado = u'<div class="ok-icon">&nbsp;</div>'
            else:
                pago_formatado = u'<div class="cancel-icon">&nbsp;</div>'

            # Dados do lançamento
            dados_lancamento = {
                'id': lancamento.pk,
                'vencimento': lancamento.vencimento.strftime('%d/%m/%Y'),
                'desc': lancamento.desc,
                'tipo': lancamento.get_tipo_display(),
                'pago': pago_formatado,
                'valor': valor_formatado,
                'saldo': saldo_formatado,
            }

            lista_resultado.append(dados_lancamento)

        return lista_resultado[indice_inicial:indice_final]
