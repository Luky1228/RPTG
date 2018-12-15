from random import randint as rd


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
        self.weapon = ['stick', 5, 80, 100, 5,
                       'smash']  # name, damage, hitchance in %, agility multiplier, chance to block, spell
        self.role = role
        self.traits = traits
        self.effects = set()
        self.spells = dict()

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
        if rd(0, 100) <= (self.agility + ag) * aglm:
            return ['Вы уклоняетесь', None, False]
        d = int(p * (100 - dr) / 100)
        res = self.body_map[r].take_damage(d)
        if res[2]:
            self.body_map[r] = self.body_map[l - 1]
            self.body_map.pop()
            if res[1] is not None:
                res[1] = eval('self.' + res[1])
        return res


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
