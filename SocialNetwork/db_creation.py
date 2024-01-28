import sqlite3
import time
import os
import hashlib
from getpass import getpass
from user_table_data import data
#from mentionsTID import mentions_tid
#from rtOUT import rt_out

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return
#
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password

def updateData():
    global connection, cursor
    c = connection.cursor()

    # Updates password with hashed password
    for i in range(1, 79):
        password = data[i]['pwd']
        c.execute("UPDATE users SET pwd=:pwd, usr=:id WHERE rowid=:id", {"pwd":(password), "id":i})
    
    # Genereates tweet ids and replyto values
    for i in range(1, 57):
        #tid = 132-i         # Just dummy values
        if i % 6 == 0:
            rep = i/2
        else:
            rep = None
        c.execute("UPDATE tweets SET tid=:tid, replyto=:rep WHERE rowid=:id", {"tid":i, "rep":rep, "id":i})
    
    connection.commit()
    #update_tid()
    #update_rt()
    return

def update_tid():
    global connection, cursor
    c = connection.cursor()
    for i in range(1,43):
        c.execute('UPDATE mentions SET tid=:tid WHERE rowid=:rid;', {"tid":mentions_tid[i-1]["tid"], "rid":i})
    connection.commit()
    return

def update_rt():
    global connection, cursor
    c = connection.cursor()
    for i in range(1, 26):
        print(i)
        c.execute('UPDATE retweets SET tid=:tid WHERE rowid=:rid;', {"tid":rt_out[i-1]["tid"], "rid":i})
    connection.commit()
    return

def main():
    global connection, cursor    
    path = "./X.db"
    connect(path)
    updateData()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()