import apiclient
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from settings import BOT_TOKEN

import sqlite3 as sql


class Bot:
    def __init__(self):
        self.updater = Updater(BOT_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.answer))
        self.dispatcher.add_handler(CommandHandler("stop", self.stop))
        self.dispatcher.add_handler(CallbackQueryHandler(self.process))

    def start(self, bot, update):
        keyboard = [[KeyboardButton("Create a hero")], [KeyboardButton("Become immortal")], [KeyboardButton("#nickzatknis")]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        bot.send_message(chat_id=update.message.chat.id, text='Что бы вы хотели сделать?',
                             reply_markup=reply_markup)

    def process(self, bot, update):
        word = update.callback_query.data
        chatid = update.callback_query.message.chat_id
        if word == 'Create a hero':
            create_a_hero()
        else:
            dont()
        whatever()
        pass

    def answer(self, bot, update):
        '''
        handles any text input
        :param bot:
        :param update:
        :return:
        '''

    def work(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

bot = Bot()
bot.work()
