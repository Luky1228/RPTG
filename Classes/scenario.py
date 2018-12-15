import re
from Classes.builders import *
from Classes.room import *
from Classes.character import *


class scenario:
    def __init__(self, quest, character, start):
        self.hero = character
        self.main_quest = quest
        self.room = start
        self.quests = []
        self.act_list = []
        self.answ = []

    def move_to_next_room(self):
        mycursor = mydb.cursor()
        sql = "SELECT xml FROM rooms"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mycursor.close()
        self.room = room(read_room_from_file(rc(myresult)[0]))
        self.act_list = []
        self.get_action_list()
        return self.room.desc

    def get_action_list(self):
        options = ""
        res = [['Перейти в следующую комнату', self.move_to_next_room, '(перейти)', 's']]
        options += '-- ' + res[0][0] + '\n'
        l = len(res)
        for i in range(len(self.room.actions)):
            res.append([self.room.actions[i].hints, i, '(' + self.room.actions[i].keywords + ')', 'r'])
            options += '-- ' + res[i + l][0] + '\n'
        ca = self.hero.get_actions()
        res += ca
        for i in ca:
            options += '-- ' + i[0] + '\n'
        self.act_list = res
        return options

    def check_for_action(self, msg):
        for i in range(len(self.act_list)):
            if re.search(r'' + self.act_list[i][2], msg) is not None:
                print('!!!')
                return self.play_action(i)

    def battle(self):
        while len(self.room.enemy_npc) > 0:
            if 'stun' not in self.hero.effects:
                print("Выберите цель")
                print("Ваши действия")

    def play_action(self, i):
        a = self.act_list[i]
        if a[3] == 'r':
            desc, e = self.room.play_action(int(a[1]))
            self.act_list[i] = self.act_list[-1]
            self.act_list.pop()
            for i in e.character_handler:
                eval('self.hero.' + i)
            for i in e.scenario_handler:
                eval('self.hero.' + i)
        elif a[3] == 'c':
            desc=eval('self.hero.'+a[1])
        else:
            desc = a[1]()
        return desc

    def get_answ(self):
        return self.answ
