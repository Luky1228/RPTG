import xml.etree.ElementTree as ET
from Classes.sqlconfig import *
from Classes.npc import *
from textwrap import dedent as td


# BODY CONSTRUCTOR

def get_parts(el):
    res = []
    for i in el:
        if (len(i) == 1):
            res.append(i[0].text)
        elif (len(i) == 3):
            res.append(i[0].text)
            res.append(i[2].text)
        else:
            res.append(i.text)
    return res


def read_body(root):
    parts = []
    for child in root:
        if child.tag == 'name':
            name = child.text
        if child.tag == 'parts':
            for p in child:
                parts.append(bpart(get_parts(p)))
    return parts


def read_body_from_xml(file):
    root = ET.fromstring(file)
    return read_body(root)


def store_body_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO bodies (name, map) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_body_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT map FROM bodies where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]


# EVENTS CONSTRUCTOR

def clfs(s):
    if s is not None:
        return s.split('|')
    else:
        return []


def read_events(root):
    events = []
    for child in root:
        if child.tag == 'e':
            events.append(
                event(child[1].text, int(child[0].text), child[2].text, clfs(child[3].text), clfs(child[4].text),
                      clfs(child[5].text), clfs(child[6].text)))
    return events


def read_attacks(root):
    attacks = []
    for child in root:
        if child.tag == 'at':
            attacks.append(attack(child[0].text, int(child[1].text)))
    return attacks


# NPC CONSTRUCTOR


def read_npc(root):
    e = []
    for i in root:
        if i.tag == 'name':
            n = i.text
        if i.tag == 'hpm':
            hpm = int(i.text)
        if i.tag == 'dm':
            dm = int(i.text)
        if i.tag == 'body_map':
            b = read_body(i)
        if i.tag == 'on_death':
            e = read_events(i)
        if i.tag == 'attacks':
            at = read_attacks(i)
        if i.tag == 'friendly':
            f = int(i.text)
    return npc(n, b, hpm, dm, e, [], at, f)


def read_npc_from_file(file):
    root = ET.fromstring(file)
    return read_npc(root)


def store_npc_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO npc (name, xml) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_npc_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM npc where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]


# OBJECT CONSTRUCTOR


def read_actions(root):
    actions = []
    for child in root:
        if (child.tag == 'a'):
            actions.append(action(child[0].text, child[1].text, read_events(child[2]), child[3].text))
    return actions


def read_object(root):
    desc = ""
    actions = []
    for i in root:
        if (i.tag == 'probability'):
            if rd(0, 100) >= int(i.text):
                return ["", []]
        if (i.tag == 'ob_desc' and i.text is not None):
            desc += i.text + ' '
        if (i.tag == 'actions'):
            actions = read_actions(i)
    return [desc, actions]


# ROOM CONSTRUCTOR

def read_room(root):
    r_desc = ''
    e_desc = ''
    actions = []
    for i in root:
        if i.tag == 'name':
            n = i.text
        if i.tag == 'text_map':
            tm = td(i.text.replace('\n', '').replace('\t', ''))
        if i.tag == 'r_obs':
            for j in i:
                obs = read_object(j)
                r_desc += obs[0]
                actions += obs[1]
        if i.tag == 'e_obs':
            for j in i:
                obs = read_object(j)
                e_desc += obs[0]
                actions += obs[1]
    text = tm.replace('|r_obs', r_desc + '\n').replace('|e_obs', e_desc + '\n')
    return [n, text, actions]


def read_room_from_file(file):
    root = ET.fromstring(file)
    return read_room(root)


def store_room_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO rooms (name, xml) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_room_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM rooms where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]


# QUEST CONSTRUCTOR

def read_steps(root):
    steps = []
    for s in root:
        steps.append(step([s[0].text, s[1].text, clfs(s[2].text), clfs(s[3].text), clfs(s[4].text)]))
    return steps


def read_quest(root):
    for i in root:
        if i.tag == 'name':
            n = i.text
        if i.tag == 'desc':
            d = i.text
        if i.tag == 'steps':
            s = read_steps(i)
        if i.tag == 'rewards':
            for j in i:
                if j.tag == 'events':
                    e = read_events(j)
    return quest([n, d, s, e])


def read_quest_from_file(file):
    root = ET.fromstring(file)
    return read_quest(root)


def store_quest_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO quests (name, xml) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_quest_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM quests where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]


# ITEM CONSTRUCTOR

def read_spells(root):
    res = dict()
    for child in root:
        s = read_events(child)
        for i in child:
            if i.tag == 'name':
                n = i.text
            if i.tag == 'desc':
                desc = i.text
        res[n] = spell([n, desc, s])
    return res


def store_spell_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO spells (name, xml) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_spell_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM spells where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]


def toint(s):
    if s is not None:
        return int(s)
    return None


def read_item(root):
    for i in root:
        if i.tag == 'name':
            n = i.text
        if i.tag == 'desc':
            desc = i.text
        if i.tag == 'price':
            p = toint(i.text)
        if i.tag == 'type':
            t = i.text
        if i.tag == 'slot':
            s = i.text
        if i.tag == 'damage_reduction':
            dr = toint(i.text)
        if i.tag == 'damage':
            d = toint(i.text)
        if i.tag == 'aglm':
            a = toint(i.text)
        if i.tag == 'ctb':
            c = toint(i.text)
        if i.tag == 'spells':
            sp = read_spells(i)
    return item([n, desc, p, t, s, dr, d, a, c, sp])


def read_item_from_file(file):
    root = ET.fromstring(file)
    return read_item(root)


def store_item_in_db(file):
    r = file
    root = ET.fromstring(r)
    name = root[0].text
    mycursor = mydb.cursor()
    sql = "INSERT INTO items (name, xml) VALUES (%s, %s)"
    val = (name, r)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def load_item_from_db(name):
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM items where name = %s"
    val = (name,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]

def load_random_item_from_db():
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM items"
    mycursor.execute(sql)
    c = mycursor.fetchone()[0]
    mycursor.close()
    n=rd(0, c)
    mycursor = mydb.cursor()
    sql = "SELECT xml FROM items LIMIT %s,1"
    val = (n-1,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    return myresult[0]