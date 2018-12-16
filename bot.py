from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


from settings import LOCAL_BOT_TOKEN

from Classes.scenario import *

class Bot:
    def __init__(self):
        REQUEST_KWARGS = {
            'proxy_url': 'socks5://phobos.public.opennetwork.cc:1090',
            # Optional, if you need authentication:
            'urllib3_proxy_kwargs': {
                'username': '139218367',
                'password': 'UmKm1u6l',
            }
        }
        self.updater = Updater(LOCAL_BOT_TOKEN, request_kwargs=REQUEST_KWARGS)
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()
        self.state = ''
        self.character_created = False
        self.ingame = False
        self.character_options = []


    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.answer))
        self.dispatcher.add_handler(CommandHandler("stop", self.stop))
        self.dispatcher.add_handler(CallbackQueryHandler(self.process))

    def start(self, bot, update):
        if self.character_created:
            keyboard = [[KeyboardButton("Continue playing")], [KeyboardButton("Create a hero")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=update.message.chat.id, text='Welcome, hero! Choose your options:', reply_markup=reply_markup)
        else:
            keyboard = [[KeyboardButton("Create a hero")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=update.message.chat.id, text='Welcome, hero! It\'s time to begin your journey:', reply_markup=reply_markup)
        self.state = 'just started'

    def process(self, bot, update):
        pass

    def answer(self, bot, update):
        print(update.message.chat.username, self.state)
        word = update.message.text
        chatid = update.message.chat.id
        if self.state == 'just started':
            if word == 'Create a hero':
                keyboard = [[KeyboardButton("Knight")], [KeyboardButton("Mage")], [KeyboardButton("Raider")]]
                reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
                bot.send_message(chat_id=chatid, text='Choose your role!', reply_markup=reply_markup)
            elif word in ['Knight', 'Mage', 'Raider']:
                self.character_options.append(word)
                keyboard = [[KeyboardButton("Slim shady")], [KeyboardButton("Normal one")], [KeyboardButton("Bulky hulk")]]
                reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
                bot.send_message(chat_id=chatid, text='Choose your body type:', reply_markup=reply_markup)
            elif word in ["Slim shady","Normal one","Bulky hulk"]:
                self.character_options.append(word)
                keyboard = [[KeyboardButton("Male")], [KeyboardButton("Female")], [KeyboardButton("Email")]]
                reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
                bot.send_message(chat_id=chatid, text='Choose your gender:', reply_markup=reply_markup)
            elif word in ["Male","Female","Email"]:
                self.character_options.append(word)
                bot.send_message(chat_id=chatid, text='Great! So, what\'s your name?')
                self.state = 'choosing name'
            else:
                bot.send_message(chat_id=chatid, text='weird flex but ok')
        elif self.state == 'choosing name':
            self.character_options.append(word)
            self.character_created = True
            self.state = 'choosing adventures'
            keyboard = [[KeyboardButton("The puzzle")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=chatid, text='Got it! Now, __{}__, choose an adventure!'.format(self.character_options[-1]), parse_mode='Markdown', reply_markup=reply_markup)
        elif self.state == 'choosing adventures':
            self.state = 'adventuring'
            self.ingame = True
            #start_adventure

        else:
            bot.send_message(chat_id=chatid, text='Me no comprendo')

    def work(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()


bot = Bot()
bot.work()