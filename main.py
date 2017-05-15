import utils
import requests
import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, TelegramError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
TOKEN = ''


def log_message(update):  # logs messages
    logger.info('{} {}({}):{}'.format(update.message.chat.first_name, update.message.chat.last_name,
                                      update.message.chat.id, update.message.text))


def com_start(bot, update):
    log_message(update)
    keyboard = [
        ['Col1', 'Col2', 'Col3'],
        ['Row2'],
        ['Col1', 'Col2']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Some text', reply_markup=reply_markup)


def com_inline(bot, update):
    log_message(update)
    buttons = [InlineKeyboardButton('Yes', callback_data='Yes'), InlineKeyboardButton('No', callback_data='No')]
    inline_markup = InlineKeyboardMarkup(utils.build_menu(buttons, 2))
    bot.send_message(chat_id=update.message.chat_id, text='Some text', reply_markup=inline_markup)


def callback(bot, update):
    chat_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    text = update.callback_query.message.text
    cq_id = update.callback_query.id
    logger.info('{} {}({}):CallBackQuery-{}'.format(update.callback_query.message.chat.first_name,
                                                    update.callback_query.message.chat.last_name, chat_id, data))
    answer = 'WTF?'
    if data == 'Yes':
        answer = 'Positive answer'
    elif data == 'No':
        answer = 'Negative answer'
    bot.answer_callback_query(cq_id, answer)
    bot.send_message(chat_id=chat_id, text=answer)


def com_photo(bot, update):
    log_message(update)
    bot.send_photo(chat_id=update.message.chat_id, photo='http://www.ricoh-imaging.co.jp/english/r_dc/caplio/r7/img/sample_04.jpg')


def com_gif(bot, update):
    log_message(update)
    bot.send_document(chat_id=update.message.chat_id, document='https://vk.com/doc167410887_445555096?hash=113f8a6154e23e9ddb&dl=788c84d81a8ad75a2a&wnd=1&module=im&mp4=1')


def echo(bot, update):
    log_message(update)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text, reply_markup=ReplyKeyboardRemove())

def get_name_from_url(url):
    for i in range(len(url)-1, 0):
        if url[i] == '/':
            return url[i+1:len(url)]

def photo(bot, update):
    log_message(update)
    photo = update.message.photo[-1]
    try:
        download = bot.get_file(photo.file_id)
        url = download.file_path
        f = open('1.jpg', 'wb')
        f.write(requests.get(url).content)
        f.close()
    except TelegramError:
        logger.error('File too large')

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Message Handlers are set up here
    dp.add_handler(MessageHandler(filters=Filters.text, callback=echo))
    dp.add_handler(MessageHandler(filters=Filters.photo, callback=photo))

    # Command Handlers are set up here
    dp.add_handler(CommandHandler('start', com_start))
    dp.add_handler(CommandHandler('inline', com_inline))
    dp.add_handler(CommandHandler('photo', com_photo))
    dp.add_handler(CommandHandler('gif', com_gif))
    # Callback Query Handlers are set up here
    dp.add_handler(CallbackQueryHandler(callback))

    # starts getting updates
    updater.start_polling()
    # keeps bot working
    updater.idle()
