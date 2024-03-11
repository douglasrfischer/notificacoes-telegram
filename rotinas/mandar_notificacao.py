from requests import post

from config import TOKEN
from models.usuarios_model import Usuarios


class Notificar:

    _URL = 'https://api.telegram.org/bot' + TOKEN

    def __init__(self, lista: str):
        self.lista = lista
        self.notificados = Usuarios().carregar_notificados()[self.lista]


    def mandar_msg(self, msg: str) -> None:
        for notificado in self.notificados:
            post(self._URL+'/sendMessage', json={'chat_id': notificado, 'text': msg})
