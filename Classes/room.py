from npc import *
from actions import *
from character import *
from builders import *


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
        print(n)
        npc = read_npc_from_file(load_npc_from_db(n))
        if npc.friendly:
            self.neut_npc.append(npc)
        else:
            self.enemy_npc.append(npc)

    def spawn_effect(self, effect):
        self.effect_list.append(effect)

    def play_action(self, i):
        e = self.actions[i].play_action()
        for i in e.room_handler:
            eval('self.' + i)
        return e.desc, e


class step:
    def __init__(self, s):
        self.name = s[0]
        self.desc = s[1]
        self.step_items = s[2]
        self.step_npc = s[3]
        self.step_loc = s[4]
        self.completed = 0


class quest:
    def __init__(self, q):
        self.name = q[0]
        self.desc = q[1]
        self.steps = q[2]
        self.rewards = q[3]

    def complete_step(self, n):
        for i in range(len(self.steps)):
            if self.steps[i].name == n:
                self.steps[i]=self.steps[len(self.steps)-1]
                self.steps.pop()
        return len(self.steps)

