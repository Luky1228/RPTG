'''
from Classes.scenario import *


query=['Tark', 'male', 0, 'Mage']
c=character(query[0], query[1], int(query[2]), query[3])
q=read_quest_from_file(load_quest_from_db('The puzzle'))
r=room(read_room_from_file(load_room_from_db('ruined_throne_room')))

s=scenario(q, c, r)
print(s.main_quest.desc)

basic_commands = [["(какой основной квест)", "s.main_quest.name"],["(цели|задачи) (основного квеста|"+s.main_quest.name+")", "s.main_quest.describe_steps()"],
                  ["действия", "s.get_action_list()"]]


print(s.get_action_list())
while True:
    msg=input().lower()
    res=s.check_for_basic_action(msg)
    if res is None and s.check_for_battle():
        res=s.check_for_baction(msg)
    if res is None:
        res=s.check_for_action(msg)
    if res is not None:
        if isinstance(res, list):
            if(res[0]=='b'):
                print(res[1])
            if(res[0]=='l'):
                print(res[1])
            if(res[0]=='msgs'):
                for i in res[1]:
                    print(i)
                    print()
        else:
            print(res)
        s.check_main_quest()
    elif s.check_for_battle():
        print(s.get_battle_actions())
    if(s.check_hero()):
        print("Игра окончена")
        break
    if(s.win):
        print(s.win_text())
        break

        '''