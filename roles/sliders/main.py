import importlib
import os
import sys
import time
from adapters.actuators import roboteq_command_wrapper

app_path = os.path.dirname((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
print(app_path)
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds

def network_message_handler(topic, message):
    print("network_message_handler",topic, message)

def exception_handler(exception):
    print("exception_handler",exception)

def network_status_change_handler(online_status):
    print("network_status_change_handler",online_status)

tb = thirtybirds.Thirtybirds(
    settings, 
    app_path,
    network_message_handler,
    network_status_change_handler,
    exception_handler
)

