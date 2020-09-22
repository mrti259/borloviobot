from telegram.ext import Updater, CommandHandler
import os
import dotenv

dotenv.load_dotenv()

def start(update, context):
    user = update.message.from_user
    reply = \
f"""
Hola {user['first_name']}!
Ingresa: /viste la peli/serie
para que pueda responderte
"""
    update.message.reply_text(reply)

def viste(update, context):
    text = update.message['text'].split(' ')
    if len(text) == 1:
        reply = 'Pero tenes que decirme la peli/serie, lindis'
    else:
        film = ' '.join(text[1:]).replace('?', '')
        reply = f'No, no vio {film}'
    update.message.reply_text(reply)

def main():
    updater = Updater(os.environ.get('TOKEN'), use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('viste', viste))
    updater.start_polling(clean=True)
    print('Polling!')
    updater.idle()

if __name__ == '__main__':
    main()
