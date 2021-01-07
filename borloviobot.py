from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import os
import dotenv
import logging
import sys
from commands import VISTE

# Enable log
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting env vars
dotenv.load_dotenv()
mode = os.environ.get('MODE')
TOKEN = os.environ.get('TOKEN')

# Defining mode
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
        updater.bot.set_webhook('https://{0}.herokuapp.com/{1}'.format(
            HEROKU_APP_NAME,
            TOKEN
        ))

else:
    logger.error('No MODE specified!')
    sys.exit(1)

# Commands

def start(update, context):
    user = update.message.from_user
    reply = "Hola, {0}! Qué querías preguntarme?".format(user['first_name'])
    update.message.reply_text(reply)

def viste(update, context):
    text = update.message['text'].title().split(' ')
    if len(text) == 1:
        reply = 'Pero tenes que decirme la peli/serie, lindis'
    else:
        film = ' '.join(text[1:]).replace('?', '')
        reply = 'No, no vi _{0}_'.format(film)
    update.message.reply_markdown_v2(reply)

def error(update, context):
    update.message.reply_text('Sorry pero asi no entiendo')

def controller(update, context):
    command = update.message['text'].split(' ')[0]
    if VISTE.match(command):
        viste(update, context)
    else:
        error(update, context)

# Init
def main():
    logger.info('Starting bot')
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, controller))
    run(updater)

if __name__ == '__main__':
    main()
