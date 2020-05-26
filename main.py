import os
import sys
import time

app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds

def network_message_handler(topic, message):
    print("network_message_handler",topic, message)

def exception_handler(exception):
    print("exception_handler",exception)

def network_status_change_handler(online_status):
    print("network_status_change_handler",online_status)

#ref can be used to access internals when using interactive mode
tb = thirtybirds.Thirtybirds(
    settings, 
    app_path,
    network_message_handler,
    network_status_change_handler,
    exception_handler
)
tb.init()

tb.subscribe_to_topic("test")

while True:
    #print(tb.connection.check_connections())
    #time.sleep(2)
    #tb.connection.subscribe_to_topic()
    time.sleep(2)
    
    #tb.connection.send("test")
    tb.publish("test",{"a":1,"b":2})
