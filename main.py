import importlib
import os
import socket
import sys
import time
import settings


role_module = importlib.import_module('roles.{}.{}'.format(settings.Roles.hosts[socket.gethostname()],'main'))

"""
tb.subscribe_to_topic("test")

while True:
    #print(tb.connection.check_connections())
    #time.sleep(2)
    #tb.connection.subscribe_to_topic()
    time.sleep(2)
    
    #tb.connection.send("test")
    tb.publish("test",{"a":1,"b":2})
"""