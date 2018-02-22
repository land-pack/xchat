#coding: utf-8

from subprocess import call
from websocket import create_connection
ws = create_connection("ws://localhost:9001/ws")

while True:
    input_content = raw_input(">>> \n")
    ws.send(input_content)
    recv_content = ws.recv()
    call(["say", recv_content])
    if recv_content == 'bye':
        ws.close()
        break
