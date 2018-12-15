from random import choice as rc

class event:
    def __init__(self, name, p, desc, rh, ch, sh, bh):
        self.name = name
        self.probability = p
        self.desc = desc
        self.room_handler = rh
        self.character_handler = ch
        self.scenario_handler = sh
        self.battle_handler = bh


class action:
    def __init__(self, n, k, e, h):
        self.name = n
        self.keywords = k
        self.events = e
        self.hints = h

    def __str__(self):
        return self.name

    def play_action(self):
        return rc(self.events)