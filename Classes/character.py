import re
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
        self.stamina = 100
        self.dead = False
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
        self.equipment = [['none', 0, 0]] * 3  # name, agility in %, damage reduction in %
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
        self.b_act = []
        self.effects = set()
        self.skills = dict()
        self.spells = dict()

    def add_item_to_inventory(self, it):
        self.inventory.append(it)

    def drop_manip_to(self, a):
        self.manipulation = a

    def take_damage(self, p):
        slot_dict = {'upper': 2, 'middle': 1, 'bottom': 0}
        l = len(self.body_map)
        r = rd(0, l - 1)
        sl = self.body_map[r].slot
        ag = 0
        dr = 0
        if sl in slot_dict:
            ag, dr = self.equipment[slot_dict[sl]][1:]
        if rd(0, 100) <= int((self.agility + ag) * self.aglm / 100 * self.manipulation / 100):
            return ['Вы уклоняетесь', None, False, 0]
        if rd(0, 100) <= int((self.weapon.ctb) * self.manipulation / 100) + self.block:
            return ['Вы блокируете удар', None, False, 0]
        d = int(p * (100 - dr) / 100)
        res = self.body_map[r].take_damage(d, self.hpm)  # ?
        if res[2]:
            self.body_map[r] = self.body_map[l - 1]
            if res[1] is not None:
                res[1] = eval('self.' + res[1])
        return res + [d]

    def deal_damage(self, d=0, spell=None):
        if spell:
            dmg = d
            desc = spell
        else:
            self.stamina = min(100, self.stamina + 10)
            dmg = int(self.weapon.damage * self.manipulation / 100)
            desc = 'Вы наносите удар основным оружием'
        return [desc, dmg, 'd']

    def restore_hp(self):
        self.body_map = read_body_from_xml(load_body_from_db('human_hero_body'))

    def kill(self):
        self.dead = True

    def give_absolute_block(self, s):
        self.block = 100
        return [s, 0, 'sup']

    def nulify(self):
        self.block = 0

    def get_spells(self):
        res = []
        for i in list(self.weapon.spells.values()):
            res.append([i.name + ': ' + i.desc + ' (' + str(i.cost) + ')',
                        i.events[0].character_handler[0].replace(' s)', ' ' + "'"+i.events[0].desc+"'" + ')'),
                        '(использовать ' + i.name + ')', 'sp'])
        return res

    def get_inventory_set(self):
        return set([i.name for i in self.inventory])

    def get_inventory_list(self):
        res = "Инвентарь:\n"
        for i in self.inventory:
            res += "-" + i.name + "\n"
        return res

    def get_actions(self, battle=False):
        res = [['Проверить инвентарь', 'get_inventory_list()', '((проверить инвентарь)|(что у меня есть)|(мои вещи))',
                'c'], ['Использовать предмет', 'use_item( iname)', '(использовать)', 'c']]
        return res

    def use_item(self, name):
        for i in self.inventory:
            if i.name == name:
                for j in list(i.spells.values()):
                    eval('self.'+j.events[0].character_handler[0])
                    return j.events[0].desc

    def get_battle_actions(self):
        res = []
        res += [['Нанести удар: нанести удар основным оружием', 'deal_damage()', '((нанести удар)|(ударить))', 'a']]
        res += self.get_spells()
        self.b_act = res
        return "Возможные действия:\n" + ('\n').join([i[0] for i in res])

    def check_for_actions(self, msg):
        for i in range(len(self.b_act)):
            print(msg)
            if re.search(r'' + self.b_act[i][2], msg) is not None:
                res = eval('self.' + self.b_act[i][1])
                return res

    def DropAgil(self):
        self.aglm = int(self.aglm * 0.8)

    def DropManip(self):
        self.manipulation = int(self.manipulation * 0.8)

    def get_hp(self):
        res = 0
        for i in self.body_map:
            res += i.hp
        return ceil(res / len(self.body_map))

    def inventory_add_random_item(self):
        res = load_random_item_from_db()
        ob = read_item_from_file(res)
        self.inventory.append(ob)
        return ob.name + " добавлено в инвентарь"

    def inventory_add(self, name):
        res = load_item_from_db(name)
        ob = read_item_from_file(res)
        self.inventory.append(ob)
        return ob.name + " добавлено в инвентарь"
