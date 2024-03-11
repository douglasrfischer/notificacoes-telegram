''' Rotina da conferência das cargas. Caso a carga de um dos projetos na lista
tenha falhado/não tenha sido encontrado emite notificação. '''

from datetime import date
from json import load
from os import stat

from .mandar_notificacao import Notificar


def check_alteracao(path: str) -> bool : 
    ''' Verifica se a data da última alteração do arquivo é a data de hoje.
    Todas as barras invertidas (\ ) do caminho devem estar escapadas. '''
    mod_time = date.fromtimestamp(
        stat(path).st_mtime)
    hoje = date.today()
    return mod_time == hoje


def recuperar_caminhos() -> dict:
    '''Retorna arquivos a serem verificados no formato de dicionario.'''
    with open('data/caminhos.json', 'r', encoding='utf8') as f:
        caminhos = dict(load(f))
    return caminhos


def executar():
    caminhos = recuperar_caminhos()
    falhas_carga = []
    falhas_404 = []  # FileNotFoundError

    for nome, path in caminhos.items():
        try:
            if not check_alteracao(path):
                falhas_carga.append(nome)
        except FileNotFoundError:
            falhas_404.append(nome)

    # --------------------------------------------------------------------

    if falhas_carga:
        mensagem = f'🚨 Detectada falha na carga do(s) projeto(s): {", ".join(falhas_carga)}'
    else:
        mensagem = '✔️ Nenhum problema detectado nas cargas.'

    notificar = Notificar('cargas')
    notificar.mandar_msg(mensagem)    

    if falhas_404:
        notificar.mandar_msg(
            f'🚨 Os seguintes projetos não foram encontrados: {", ".join(falhas_404)}')
