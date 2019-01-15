# -*- coding: utf-8 -*-
import sys
import zmq
import json

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from server")
socket.connect("tcp://localhost:5556")

# Subscribe to system/EDConnector events
socket.setsockopt_string(zmq.SUBSCRIBE, u"sys")

# Subscribe to journal stuff
socket.setsockopt_string(zmq.SUBSCRIBE, u"journal")

# Subscribe to cmdr stuff
socket.setsockopt_string(zmq.SUBSCRIBE, u"cmdr")

# Subscribe to dashboard stuff
socket.setsockopt_string(zmq.SUBSCRIBE, u"dashboard")

running = True
# Process 5 updates
while running:
    string = socket.recv_string()
    print 'got:', string

