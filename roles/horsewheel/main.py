import importlib
import os
import queue
import sys
import threading
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

class Roboteq_Data_Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.start()

    def add_to_queue(self, message):
        self.queue.put(message)

    def run(self):
        while True:
            message = self.queue.get(True)
            print("data",message)
            if "internal_event" in message:
                do_tests()

roboteq_data_receiver = Roboteq_Data_Receiver()

controllers = roboteq_command_wrapper.Controllers(
    roboteq_data_receiver.add_to_queue, 
    tb.status_receiver, 
    tb.exception_receiver, 
    {"bow":settings.Roboteq.BOARDS["bow"]},
    {
        "bow_height":settings.Roboteq.MOTORS["bow_height"],
        "bow_rotation":settings.Roboteq.MOTORS["bow_rotation"],
    }
)


controllers.motors["bow_rotation"].get_encoder_counter_absolute(True)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(7)
time.sleep(60)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].get_encoder_counter_absolute(True)
#time.sleep(2)

"""
controllers.motors["bow_height"].get_encoder_counter_absolute(True)
controllers.motors["bow_height"].go_to_speed_or_relative_position(10)
time.sleep(2)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].get_encoder_counter_absolute(True)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].set_operating_mode(0)
controllers.motors["bow_height"].set_operating_mode(0)
"""



"""
controllers.macros["pitch_slider"].add_to_queue("go_to_limit_switch")
controllers.macros["pitch_slider"].add_to_queue("go_to_absolute_position", {"position":3000000, "speed":100})
#controllers.macros["pitch_slider"].add_to_queue("oscillate", {"distance":500,"frequency":0.5,"duration":10})
"""


