''' Rotina de conferência da importação das vendas das unidades. Caso haja 
divergência nos valores emite notificação contendo as unidades em que foram 
registradas as divergências. '''

import csv

from .mandar_notificacao import Notificar
from config import PATH_FECHAMENTOS


def formatar_valor(val: str) -> str:
    '''Formata o valor inserido para moeda (##.###,00)'''
    reais = val.split('.')[0]
    cents = val.split('.')[1][:2]
    tam = len(reais)
    aux = []
    # Divide os valores de três em três, de trás para frente, e os add na lista
    for i in range(tam, 0, -3):
        aux.append(reais[i:i+3])
    # Lidando com números que "sobram"
    aux.append(reais[:tam%3])
    # Finalizando
    aux.remove('')
    aux.reverse()
    formatado = '.'.join(aux)
    return formatado+','+cents


def executar():
    diff = {}
    meta_s_venda = []
    with open(file=PATH_FECHAMENTOS, newline='') as file:
        registros = csv.reader(file)
        next(registros)

        for row in registros:
            # Se existe diferença

            # Tudo isso pra normalizar a diferença que, sabe-se lá porque
            # caralhinhos voadores, vem como notação E ao invés de 0,000...
            aux = format(abs(float(row[5].replace(',', '.'))), 'f')
            if not aux or float(aux) != 0:
                diff[row[0]] = f'R$ {formatar_valor(aux)}'

            # Se possui meta e não tem venda
            if row[1] == 'S' and row[2] == 'N':
                meta_s_venda.append(row[0])

    # ------------------------------------------------------------------
    
    if diff:
        aux = []
        for k, v in diff.items():
            aux.append(f'\n{k}: {v}')
        mensagem = f'🚢 Detectada diferença na importação da venda da(s) seguinte(s) unidade(s): {",".join(aux)}'
    else:
        mensagem = '✔️ Nenhum problema no fechamento das unidades.'

    notificar = Notificar('importa\u00e7\u00e3o das vendas')
    notificar.mandar_msg(mensagem)

    if meta_s_venda:
        meta_s_venda.sort()
        notificar.mandar_msg(
            f'🚢 A importação da(s) seguinte(s) unidade(s) apresentou falha (possui meta, mas não possui venda): {", ".join(meta_s_venda)}')
