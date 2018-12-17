import os
from Classes.builders import *

def upload_items():
    path='items/'
    for file in os.listdir(path):
        f=open(path+file, encoding='utf-8').read()
        try:
            store_item_in_db(f)
        except:
            print('already in db')

def upload_npc():
    path='npc/'
    for file in os.listdir(path):
        f=open(path+file, encoding='utf-8').read()
        try:
            store_npc_in_db(f)
        except:
            print('already in db')

def upload_rooms():
    path='rooms/'
    for file in os.listdir(path):
        f=open(path+file, encoding='utf-8').read()
        try:
            store_room_in_db(f)
        except:
            print('already in db')


upload_items()