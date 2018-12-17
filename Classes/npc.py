from random import randint as rd
from random import choice as rc
from Classes.actions import *
from math import ceil

class bpart:
    def __init__(self, body_parsed):
        self.name = body_parsed[0]
        self.hp = int(body_parsed[1])
        self.damage_desc = body_parsed[2]
        self.destroy_desc = body_parsed[3]
        self.reaction = body_parsed[4]
        if len(body_parsed) > 5:
            self.slot = body_parsed[5]
        else:
            self.slot = 'none'

    def take_damage(self, d, hpm=100):
        if self.hp == ' ':
            return ['Вы уклоняетесь', None, False, 0]
        self.hp = max(0, int(hpm / 100) * self.hp - d)
        if self.hp == 0:
            return [self.destroy_desc, self.reaction, True, d]  # description, event, flag of destruction, damage
        else:
            return [self.damage_desc, None, False, d]


class attack:
    def __init__(self, desc, dmg):
        self.desc = desc
        self.dmg = dmg


class npc:
    def __init__(self, name, body, hpm, dm, de, actions, attacks, f):
        self.name = name
        self.body_map = body
        self.health_multiplier = hpm
        self.damage_multiplier = dm
        self.death_event = de
        self.actions = actions
        self.attacks = attacks
        self.friendly = f
        self.dead=False

    def isfriendly(self):
        return self.friendly

    def drop_damage_to(self, p):
        self.damage_multiplier = p

    def take_damage(self, p):
        self.friendly = 0
        if len(self.body_map) < 1:
            return ['Противник уже мертв', None]
        r = rd(0, len(self.body_map)-1)
        res = self.body_map[r].take_damage(p, self.health_multiplier)
        if res[2]:
            self.body_map[r] = self.body_map[-1]
            self.body_map.pop()
            if res[1] is not None:
                res[1] = eval('self.' + res[1])
        return res

    def deal_damage(self):
        a = rc(self.attacks)
        return a.desc, int(a.dmg * self.damage_multiplier / 100)

    def get_hp(self):
        res=0
        for i in self.body_map:
             res+=i.hp
        return ceil(res/len(self.body_map))

    def kill(self):
        p = rd(0, 100)
        for i in self.death_event:
            if i.probability >= p:
                self.dead=True
                return i

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
                self.steps[i] = self.steps[-1]
                self.steps.pop()
        return len(self.steps)

    def describe_steps(self):
        desc = ""
        for i in self.steps:
            comp = ""
            if i.completed:
                comp = " (выполнено)"
            desc += '--' + i.name + comp + '\n' + i.desc + '\n'
        return desc


class item:
    def __init__(self, it):
        self.name = it[0]
        self.desc = it[1]
        self.price = it[2]
        self.type = it[3]
        self.slot = it[4]
        self.dr = it[5]
        self.damage = it[6]
        self.aglm = it[7]
        self.ctb = it[8]
        self.spells = it[9]


class spell:
    def __init__(self, it):
        self.name = it[0]
        self.desc = it[1]
        self.events = it[2]
        self.cost = it[3]
