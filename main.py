import os
import sys
import time

app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds

#ref can be used to access internals when using interactive mode
tb = thirtybirds.Thirtybirds(settings, app_path)

tb.connection.subscribe_to_topic("test")

while True:
    tb.connection.send("test",{"a":1,"b":2})
    time.sleep(10)
