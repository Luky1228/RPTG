from random import randint as rd
from Classes.builders import *


class effect:
    def __init__(self, name, desc, res):
        self.name = name
        self.desc = desc
        self.result = res


class character:
    def __init__(self, name, gender, body_type, role, traits=[]):
        self.name = name
        self.gender = gender
        self.body_map = read_body_from_xml(load_body_from_db('human_hero_body'))
        self.manipulation = 100  # multiplier for all actions (dodging, attacking, blocking)
        self.agility = 10  # chance to dodge in %
        self.block = 0  # chance to block in %
        if body_type < 0:  # slim
            self.hpm = 80  # health multiplier in %
            self.aglm = 150  # aglitiy multiplier in %
        elif body_type == 0:  # balanced
            self.hpm = 100
            self.aglm = 100
        else:  # hulking
            self.hpm = 150
            self.aglm = 50
        self.inventory = []
        self.equipment = ['none', 0, 0] * 3  # name, agility in %, damage reduction in %
        self.weapon = read_item_from_file(load_item_from_db('stick'))
        if role == 'Mage':
            armor = ['robe']
            self.weapon = read_item_from_file(load_item_from_db('staff'))
            for i in armor:
                p = read_item_from_file(load_item_from_db(i))
                if p.slot == 'middle':
                    self.equipment[1] = [p.name, p.dr, p.aglm]
                if p.slot == 'upper':
                    self.equipment[2] = [p.name, p.dr, p.aglm]
                if p.slot == 'bottom':
                    self.equipment[0] = [p.name, p.dr, p.aglm]

        self.role = role
        self.traits = traits
        self.effects = set()
        self.skills = dict()
        self.spells = dict()

    def add_item_to_inventory(self, it):
        self.inventory.append(it)

    def drop_manip_to(self, a):
        self.manipulation = a

    def take_damage(self, p):
        slot_dict = {'upper': 0, 'middle': 1, 'bottom': 2}
        l = len(self.body_map)
        r = rd(0, l - 1)
        sl = self.body_map[r].slot
        ag = 0
        dr = 0
        if sl in slot_dict:
            ag, dr = self.equipment[slot_dict[sl]][1:]
        if rd(0, 100) <= (self.agility + ag) * aglm:  # npc.item
            return ['Вы уклоняетесь', None, False]
        d = int(p * (100 - dr) / 100)
        res = self.body_map[r].take_damage(d, hpm)  # ?
        if res[2]:
            self.body_map[r] = self.body_map[l - 1]
            self.body_map.pop()
            if res[1] is not None:
                res[1] = eval('self.' + res[1])
        return res

    def get_spells(self):
        res = self.skills.copy()
        res.update(self.weapon.spells)
        return res

    def get_inventory_list(self):
        res="Инвентарь:\n"
        for i in self.inventory:
            res+="-"+i.name + "\n"
        return res

    def get_actions(self):
        res=[['Проверить инвентарь', 'get_inventory_list()', '((проверить инвентарь)|(что у меня есть))', 'c']]
        return res

    def inventory_add_random_item(self):
        res=load_random_item_from_db()
        ob=read_item_from_file(res)
        self.inventory.append(ob)
