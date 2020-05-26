import importlib
import os
import sys
import time

app_path = os.path.dirname((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds
from thirtybirds3.adapters.actuators import roboteq_command_wrapper

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


print(settings.Roboteq.BOARDS)
print(settings.Roboteq.MOTORS)


"""
controllers = roboteq_command_wrapper.init(
    data_receiver.add_to_queue, 
    status_receiver.add_to_queue, 
    exception_receiver.add_to_queue, 
    config
)
"""

