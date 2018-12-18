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
        self.character_options = []
        self.sens = []


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
        print(self.character_options, '\n')
        word = update.message.text
        chatid = update.message.chat.id
        if self.state == 'just started' or self.state == 'ded':
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
                convert = {"Slim shady": -1, "Normal one": 0, "Bulky hulk": 1}
                self.character_options.append(convert[word])
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
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
            bot.send_message(chat_id=chatid, text='Got it! Now, __{}__, choose an adventure!'.format(self.character_options[-1]), parse_mode='Markdown', reply_markup=reply_markup)
        elif self.state == 'choosing adventures' or word == 'Continue playing':
            self.state = 'adventuring'
            #start_adventure
            c = character(self.character_options[3], self.character_options[2], int(self.character_options[1]), self.character_options[0])
            q = read_quest_from_file(load_quest_from_db('The puzzle'))
            r = room(read_room_from_file(load_room_from_db('ruined_throne_room')))
            self.sens.append(scenario(q, c, r))
            bot.send_message(chat_id=chatid, text=self.sens[0].main_quest.desc)
            bot.send_message(chat_id=chatid, text=self.sens[0].get_action_list())
        elif self.state == 'adventuring':
            # self.sens[0]
            print(word)
            msg = word.lower()
            res = self.sens[0].check_for_basic_action(msg)
            print(res)
            if res is None and self.sens[0].check_for_battle():
                res = self.sens[0].check_for_baction(msg)
            print(res)
            if res is None:
                res = self.sens[0].check_for_action(msg)
            print(res)
            if res is not None:
                if isinstance(res, list):
                    if res[0] == 'b':
                        bot.send_message(chatid, res[1])
                    if res[0] == 'l':
                        bot.send_message(chatid, res[1])
                    if res[0] == 'msgs':
                        for i in res[1]:
                            bot.send_message(chatid, i)
                else:
                    bot.send_message(chatid, res)
            elif self.sens[0].check_for_battle():
                bot.send_message(chatid, self.sens[0].get_battle_actions())
            else:
                bot.send_message(chatid, '... and nothing happened')
            if self.sens[0].check_hero():
                self.state = "gameover"
            if self.sens[0].win:
                self.state = "win"
        elif self.state == 'gameover':
            keyboard = [[KeyboardButton("Create a hero")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=chatid, text='omg u ded!create a new hero!', reply_markup=reply_markup)
        elif self.state == 'gameover' or word == '👑':
            keyboard = [[KeyboardButton("👑")]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.send_message(chat_id=chatid, text='omg u win!', reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=chatid, text='Me no comprendo')

    def work(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()


bot = Bot()
bot.work()