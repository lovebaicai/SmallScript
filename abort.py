#!/usr/bin/env python
from datetime import datetime
db = {}
def newuser():
    prompt = 'login desired: '
    while True:
        name = input(prompt)
        if name in db:
            prompt = 'name taken, try another: '
            continue
        else:
            break
    pwd = input('passwd: ')
    db[name] = pwd

def olduser():
    name = input('login: ')
    pwd = input('passwd: ')
    passwd = db.get(name)
    if passwd == pwd:
        print ('welcome back', name, DATE)
        Date = print(datetime.now())
    else:
        print('login incorrect')

def showmenu():
    prompt = """
    (N)ew User Login
    (E)xisting User Login
    Enter choice: """
    done = False
    while not done:
        chosen = False
        while not chosen:
            try:
                choice = input(prompt).strip()[0].lower()
            except(EOFError, KeyboardInterrupt):
                choice = 'q'
            print('\nYour picked: [%s]') % choice
            if  choice not  in 'neq':
                print('invalid option, try again')
            else:
                chosen = True
                done = True
newuser()
olduser()
if __name__ == '__main__':
    showmenu()
