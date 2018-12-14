from actions import *
from npc import *


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

    def spawn_npc(self, npc, dead):
        if dead:
            self.dead_npc.append(npc)
        elif npc.friendly:
            self.neut_npc.append(npc)
        else:
            self.enemy_npc.append(npc)

    def spawn_effect(self, effect):
        self.effect_list.append(effect)

    def spawn_object(self, obj):
        self.object_list.append(obj)


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


class scenario:
    def __init__(self, quest, character, biome_list, start):
        self.hero = character
        self.main_quest = quest
        self.biomes = biome_list
        self.start = start
        self.quests = []


