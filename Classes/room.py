from Classes.builders import *


class room:
    def __init__(self, rdesc):
        self.name = rdesc[0]
        self.desc = rdesc[1]
        self.actions = rdesc[2]
        self.dead_npc = []
        self.enemy_npc = []
        self.neut_npc = []
        self.effect_list = []
        self.state = 'roaming'
        self.targeting = False

    def __str__(self):
        return self.name

    def spawn_npc(self, n):
        npc = read_npc_from_file(load_npc_from_db(n))
        if npc.friendly:
            self.neut_npc.append(npc)
        else:
            self.enemy_npc.append(npc)
        return npc.name + " призван \n"

    def check_for_battle(self):
        if len(self.enemy_npc) > 0 and self.state != 'battle':
            self.state = 'battle'
            return "\n БОЙ \n"

    def spawn_effect(self, effect):
        self.effect_list.append(effect)

    def drop_enemy(self, i):
        self.enemy_npc[i]=self.enemy_npc[-1]
        self.enemy_npc.pop()

    def play_action(self, i):
        e = self.actions[i].play_action()
        self.actions[i] = self.actions[-1]
        self.actions.pop()
        for i in e.room_handler:
            eval('self.' + i)
        return e.desc, e

    def get_target(self, i):
        return self.enemy_npc[i]

    def istargeting(self):
        return self.targeting

    def get_enemy_list(self):
        res = []
        self.targeting = True
        for i in range(len(self.enemy_npc)):
            res.append(str(i) + '. ' + self.enemy_npc[i].name + ', hp: ' + str(self.enemy_npc[i].get_hp()))
        return res
