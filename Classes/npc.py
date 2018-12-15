from random import randint as rd
from random import choice as rc
from Classes.actions import *


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

    def take_damage(self, d):
        self.hp = max(0, self.hp - d)
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

    def isfriendly(self):
        return self.friendly

    def drop_damage_to(self, p):
        self.damage_multiplier = p

    def take_damage(self, p):
        l = len(self.body_map)
        self.friendly = 0
        if l < 1:
            return ['Противник уже мертв', None]
        r = rd(0, l - 1)
        res = self.body_map[r].take_damage(p)
        if res[2]:
            self.body_map[r] = self.body_map[l - 1]
            self.body_map.pop()
            if res[1] is not None:
                res[1] = eval('self.' + res[1])
        return res

    def deal_damage(self):
        a = rc(self.attacks)
        return a.desc, int(a.dmg*self.damage_multiplier/100)

    def kill(self):
        p = rd(0, 100)
        for i in self.death_event:
            if i.probability >= p:
                return i
