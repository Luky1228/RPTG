
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


from settings import BOT_TOKEN


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
        bot.send_message(chat_id=update.message.chat.id, text='What would you like to do?', reply_markup=reply_markup)

    def process(self, bot, update):
        pass

    def answer(self, bot, update):
        word = update.message.text
        chatid = update.message.chat.id
        if word == 'Create a hero':
            keyboard = [[KeyboardButton("Oknight")], [KeyboardButton("Helf")], [KeyboardButton("Gnome")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=chatid, text='Choose a hero!', reply_markup=reply_markup)
        elif word in ['Oknight', 'Helf', 'Gnome']:
            keyboard = [[KeyboardButton("Forest adventure")], [KeyboardButton("Weird adventure")], [KeyboardButton("#nickzatknis")], [KeyboardButton("Back to menu")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=update.message.chat.id, text='Great! Now choose an adventure:', reply_markup=reply_markup)
        elif word == 'Become immortal':
            bot.send_message(chat_id=chatid, text='R u sure about that?')
        elif word == '#nickzatknis':
            pass
        elif word == "Back to menu":
            keyboard = [[KeyboardButton("Create a hero")], [KeyboardButton("Become immortal")], [KeyboardButton("#nickzatknis")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=update.message.chat.id, text='What would you like to do?', reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=chatid, text='Me no comprendo')

    def work(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()


bot = Bot()
bot.work()