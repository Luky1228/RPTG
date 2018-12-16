'''
from Classes.scenario import *


query=['Tark', 'male', '0', 3]
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
    res=None
    for i in basic_commands:
        ind=re.search(r''+i[0], msg)
        if ind is not None:
            res=eval(i[1])
            if isinstance(res, str):
                print(res)
            else:
                print(res[0])
            break
    if res is None:
        res=s.check_for_action(msg)
        if res is not None:
            print(res)
'''