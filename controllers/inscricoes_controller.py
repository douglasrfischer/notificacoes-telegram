from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from models.usuarios_model import Usuarios


class InscricoesController(Usuarios):
    '''Controller responsável pelas inscrições em listas de notificações (lida 
    com os COMANDOS recebidos pelo bot dos usuários).'''


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
    

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        if await self.consultar_bloqueio(chat_id, context):
            return
        
        nome = update.effective_user.full_name
        super().adiciona_pendente(chat_id, nome)
        await context.bot.send_message(
            chat_id,
            'Bem-vindo(a) ao sistema de notificações do setor de BI. Caso seja seu primeiro contato aguarde a aprovação do seu acesso para prosseguir. Utilize o comando /ajuda para obter a lista de comandos e suas descrições.'
        )


    async def alternar_inscricoes(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        if await self.consultar_bloqueio(chat_id, context):
            return
        
        if await self.consultar_pendente(chat_id, context):
            return

        keyboard = [
            [
                InlineKeyboardButton('Cargas de projetos', callback_data='cargas'),
                InlineKeyboardButton('Importação das vendas', callback_data='importação das vendas')
            ],
        ]
        await context.bot.send_message(
            chat_id,
            f'Atualmente você está recebendo as notificações de: {", ".join(super().consultar_inscricoes(chat_id))}.\n'
                'Escolha qual inscrição deseja alterar no menu abaixo:',
            reply_markup = InlineKeyboardMarkup(keyboard))


    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        if super().alterar_inscricao(update.effective_chat.id, query.data) == 0:
            texto = f'Você não receberá mais notificações de {query.data}'
        else:
            texto = f'Você passará a receber notificações de {query.data}'

        await context.bot.send_message(
            update.effective_chat.id,
            texto
        )
