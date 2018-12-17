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
        self.win=False
        self.bact_list = [['Выбрать цель', 'room.get_enemy_list()', '(выбрать цель)', 's'],
                          ['Убежать', 'move_to_next_room(True)', '(убежать)', 's']]
        self.answ = []
        self.turn = None
        self.target = None
        self.tid = None
        self.basic_commands = [["(какой основной квест)", "self.main_quest.name"],
                               ["(цели|задачи) (основного квеста|" + self.main_quest.name + ")",
                                "self.main_quest.describe_steps()"],
                               ["действия", "self.get_action_list()"],
                               ['призвать скелет', "self.room.spawn_npc('skeleton')"]]

    def check_hero(self):
        return self.hero.dead

    def win_text(self):
        return self.main_quest.rewards[0].desc

    def move_to_next_room(self, ranaway=False):
        mycursor = mydb.cursor()
        sql = "SELECT xml FROM rooms"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mycursor.close()
        ad = ''
        if ranaway:
            ad = "ВЫ УБЕЖАЛИ \n \n"
        self.room = room(read_room_from_file(rc(myresult)[0]))
        self.act_list = []
        self.get_action_list()
        return ad + self.room.desc

    def get_action_list(self):
        options = ""
        res = [['Перейти в следующую комнату', 'move_to_next_room()', '(перейти)', 's']]
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

    def check_for_basic_action(self, msg):
        r = None
        for i in self.basic_commands:
            ind = re.search(r'' + i[0], msg)
            if ind is not None:
                res = eval(i[1])
                r = ''
                if isinstance(res, str):
                    r += res
                else:
                    r += res[0]
                ad = self.room.check_for_battle()
                if ad is None:
                    ad = ''
                r += ad
                return r

    def check_for_action(self, msg):
        for i in range(len(self.act_list)):
            if re.search(r'' + self.act_list[i][2], msg) is not None:
                print('!!!')
                desc = self.play_action(i, msg)
                b = self.room.check_for_battle()
                if b is not None:
                    desc += b
                    self.turn = 0
                return desc

    def check_for_battle(self):
        return self.room.state == 'battle'

    def get_battle_actions(self):
        return [i[0] for i in self.bact_list]

    def damage(self, p):
        return self.target.take_damage(p)[0]

    def check_for_baction(self, msg):
        if self.room.istargeting() and '.' in msg:
            self.tid = int(msg.split('.')[0])
            self.target = self.room.get_target(self.tid)
            desc = self.hero.get_battle_actions()
            return ['l', desc]
        elif self.target is not None:
            res = self.hero.check_for_actions(msg)
            if (res is not None):
                if res[2] == 'd':
                    desc = []
                    rms = res[0] + '\nУрон: ' + str(res[1]) + ' (осталось hp: ' + str(self.target.get_hp()) + ')' + '\n'
                    rms += self.damage(res[1])
                    desc.append(rms)
                    if self.target.dead:
                        self.room.drop_enemy(self.tid)
                        self.target=None
                        self.tid=None
                    for i in self.room.enemy_npc:
                        rms = ''
                        td = i.deal_damage()
                        rms += td[0] + '\n'
                        hd = self.hero.take_damage(td[1])
                        rms += 'Урон: ' + str(hd[3]) + ' (осталось hp: ' + str(self.hero.get_hp()) + ')' + '\n'
                        rms += hd[0].replace('_monster_', i.name) + '\n'
                        desc.append(rms)

                    return ['msgs', desc]
                if res[2] == 'sup':
                    return ['msgs', res[0]]
        for i in range(len(self.bact_list)):
            if re.search(r'' + '(' + self.bact_list[i][0].lower() + ')', msg) is not None:
                print('!!!')
                desc = eval('self.' + self.bact_list[i][1])
                if isinstance(desc, list):
                    return ['b', desc]
                return ['l', desc]

    def check_main_quest(self):
        c=0
        for i in self.main_quest.steps:
            if set(i.step_items).issubset(self.hero.get_inventory_set()):
                i.completed=True
            if i.completed:
                c+=1
        if(c==len(self.main_quest.steps)):
            self.win = True



    def play_action(self, i, msg=None):
        a = self.act_list[i]
        if a[3] == 'r':
            desc, e = self.room.play_action(int(a[1]))
            self.act_list[i] = self.act_list[-1]
            self.act_list.pop()
            for i in e.character_handler:
                t = eval('self.hero.' + i)
                if t is not None:
                    desc += '\n' + t
            for i in e.scenario_handler:
                eval('self.hero.' + i)
        elif a[3] == 'c':
            desc = eval('self.hero.' + a[1].replace(' iname)', "'"+ msg.split()[-1] + "'" + ")"))
        else:
            desc = eval('self.' + a[1])
        return desc

    def get_answ(self):
        return self.answ
