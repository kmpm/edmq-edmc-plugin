# -*- coding: utf-8 -*-
import sys
import zmq
import json


this = sys.modules[__name__]	# For holding module globals

class Server: 
    def __init__(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:" + str(port))
        self.context = context
        self.socket = socket
    
    def send_sys(self, data):
        if isinstance(data, basestring):
            data = {"data": data}
        self.socket.send_string(u"sys %s" % (json.dumps(data)))
    
    def send_journal(self, text):
        self.socket.send_string(u'journal {}'.format(text))

    def send_cmdr(self, text):
        self.socket.send_string(u'cmdr {}'.format(text))

    def send_dashboard(self, text):
        self.socket.send_string(u'dashboard {}'.format(text))