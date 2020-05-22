import os
import sys
import time

app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds

#ref can be used to access internals when using interactive mode
tb = thirtybirds.Thirtybirds(settings, app_path)
#tb.init()

tb.connection.subscribe_to_topic("test")

while True:
    #print(tb.connection.check_connections())
    #time.sleep(2)
    #tb.connection.subscribe_to_topic()
    time.sleep(2)
    
    #tb.connection.send("test")
    #tb.connection.send("test",{"a":1,"b":2})
