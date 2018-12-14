class effect:
    def __init__(self, name, desc, res):
        self.name = name
        self.desc = desc
        self.result = res


class character:
    def __init__(self, name, gender, body_type, role, traits):
        self.name = name
        self.gender = gender
        self.body_type = int(body_type)
        self.manipulation = 100  # multiplier for all actions (dodging, attacking, blocking)
        self.agility = 10  # chance to dodge in %
        self.block = 0  # chance to block in %
        if self.body_type < 0:  # slim
            self.hpm = 80  # health multiplier in %
            self.aglm = 150  # aglitiy multiplier in %
        elif self.body_type == 0:  # balanced
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
        self.effects = []
        self.spells = dict()

    def drop_manip_to(self, a):
        self.manipulation = a


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
