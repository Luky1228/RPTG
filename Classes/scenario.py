from Classes.builders import *


class scenario:
    def __init__(self, quest, character, start):
        self.hero = character
        self.main_quest = quest
        self.room = start
        self.quests = []
        self.act_list = []

    def move_to_next_room(self):
        mycursor = mydb.cursor()
        sql = "SELECT xml FROM rooms"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mycursor.close()
        self.room = read_room_from_file(rc(myresult)[0])
        return self.room.desc

    def get_action_list(self):
        res = [['Перейти в следующую комнату', self.move_to_next_room, '', 's']]
        for i in range(len(self.room.actions)):
            res.append([self.room.actions[i].hints, i, self.room.actions[i].keywords, 'r'])
        self.act_list = res
        return res

    def battle(self):
        while len(self.room.enemy_npc) > 0:
            if 'stun' not in self.hero.effects:
                print("Выберите цель")
                print("Ваши действия")

    def play_action(self, i):
        a = self.act_list[i]
        if a[3] == 'r':
            desc, e = self.room.play_action(a[2])[1]
            for i in e.character_handler:
                eval('self.hero.' + i)
            for i in e.scenario_handler:
                eval('self.hero.' + i)
        else:
            a[2]()
