from telegram import Update
from telegram.ext import ContextTypes

from models.usuarios_model import Usuarios


class ComandosController(Usuarios):
    '''Controler genérico e - por hora - não utilizado. A ideia é utilizá-lo
    futuramente, conforme o bot agregar mais funcionalidades'''


    async def consultar_bloqueio(self, user_id, context) -> bool:
        '''Se bloqueado, True. Override da classe pai.'''
        if super().consultar_bloqueio(user_id):
            await context.bot.send_message(
                user_id,
                '🚫 Usuário bloqueado. Entre em contato com o setor de BI para reavaliar o acesso.')
            return True
        return False


    async def consultar_pendente(self, user_id, context) -> bool:
        '''Se pendente, True.'''
        pendentes = super().carregar_pendentes()
        if str(user_id) in pendentes:
            await context.bot.send_message(
                user_id,
                '⌛ Sua aprovação está pendente. Aguarde a aprovação para poder acessar os recursos.')
            return True
        return False


    async def ajuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(
            update.effective_chat.id,
            ''
        )