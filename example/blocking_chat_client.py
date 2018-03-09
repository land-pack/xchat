#coding: utf-8

import ujson
from subprocess import call
from websocket import create_connection

name = raw_input("Please input your name: ")

host_address = "ws://localhost:9001/ws?name={}".format(name)
ws = create_connection(host_address)

# Fetch online player
online_player = ws.recv()

print 'Online player', online_player


receiver_flag = []

while True:
   
    print("try again ...")
    if not receiver_flag:
        print("Who you like to chat? ")
        receivers_at = raw_input("")
        print("==>>>{}".format(receivers_at))
        receivers_at = receivers_at.partition(' ')[0]
        print(receivers_at)
        receivers_at = receivers_at.split("@")[1]
        receivers = [ receivers_at,]
        #receivers = [i.split("@")[1] for i in receivers_at if "@" in receivers_at]
        print("receivers >>{}".format(receivers))
        receiver_flag.append(receivers)
        continue
    else:
        input_content = raw_input(">>> \n")
        
    

    print("sending ... {}".format(input_content))
    data = {
        "receivers":receivers,
        "msg": input_content
    }

    data_str = ujson.dumps(data)
    if input_content:
        ws.send(data_str)

    recv_content = ws.recv()
    print("Recv << {}".format(recv_content))
    call(["say", recv_content])
    if recv_content == 'bye':
        ws.close()
        break
