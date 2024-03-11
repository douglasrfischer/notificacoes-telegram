from multiprocessing import Process
from datetime import datetime
from time import sleep

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from controllers.inscricoes_controller import InscricoesController

from config import TOKEN
import rotinas.cargas as cargas
import rotinas.fechamentos as fechamentos


def executar_rotinas():
    while True:
        agora = datetime.now()
        if agora.hour == 7 and agora.minute == 30:
            cargas.executar()
            fechamentos.executar()
        sleep(60)  # Sem essa trava o consumo de CPU dispara de 0% para 13% :D


def executar_bot():
    foo = InscricoesController()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', foo.start))
    application.add_handler(
        CommandHandler('inscricoes', foo.alternar_inscricoes))
    application.add_handler(CallbackQueryHandler(foo.button))
    application.run_polling()


if __name__ == '__main__':
    # Criando processos distintos para o bot e as notificações (rotinas),
    # como as rotinas são executadas em um loop while True isso se faz 
    # necessário para que o bot não fique "congelado".
    p1 = Process(target=executar_bot, args=(), name='BotTelegram')
    p2 = Process(target=executar_rotinas, args=(), name='RotinasNotificacoes')

    p1.start()
    p2.start()

    with open('log_pids_bot.txt', 'w') as f:
        f.write(f'PID bot: {p1.pid}\nPID rotinas: {p2.pid}')

    print(f'PID bot: {p1.pid}')
    print(f'PID rotinas: {p2.pid}')
