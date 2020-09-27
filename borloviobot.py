from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import dotenv
import logging
import sys

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting dotenv var
dotenv.load_dotenv()
mode = os.environ.get('MODE')
TOKEN = os.environ.get('TOKEN')
print(mode)
# Choosing mode
if mode == 'dev':
    def run(updater):
        updater.start_polling()

elif mode == 'prod':
    def run(updater):
        PORT = int(os.environ.get('PORT', 8443))
        HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
        updater.start_webhook(
            listen='0.0.0.0',
            port=PORT,
            url_path=TOKEN
            )
        updater.bot.set_webhook(f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')

else:
    logger.error('No MODE specified!')
    sys.exit(1)

# Commands

def start(update, context):
    user = update.message.from_user
    reply = f'''\
Hola {user['first_name']}\! Ingresa:
`/viste` _la peli/serie_ ?
para que pueda responderte
'''
    update.message.reply_markdown_v2(reply)

def viste(update, context):
    text = update.message['text'].title().split(' ')
    if len(text) == 1:
        reply = 'Pero tenes que decirme la peli/serie, lindis'
    else:
        film = ' '.join(text[1:]).replace('?', '')
        reply = f'No, Bor no vio _{film}_'
    update.message.reply_markdown_v2(reply)

def error(update, context):
    update.message.reply_text('Sorry pero asi no entiendo')

def main():
    logger.info('Starting bot')
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('viste', viste))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, error))
    run(updater)

if __name__ == '__main__':
    main()
