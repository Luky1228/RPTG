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

    def __str__(self):
        return self.name

    def spawn_npc(self, n):
        npc = read_npc_from_file(load_npc_from_db(n))
        if npc.friendly:
            self.neut_npc.append(npc)
        else:
            self.enemy_npc.append(npc)

    def spawn_effect(self, effect):
        self.effect_list.append(effect)

    def play_action(self, i):
        e = self.actions[i].play_action()
        self.actions[i]=self.actions[-1]
        self.actions.pop()
        for i in e.room_handler:
            eval('self.' + i)
        return e.desc, e



