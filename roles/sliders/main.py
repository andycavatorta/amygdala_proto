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

roboteq_data_receiver = Roboteq_Data_Receiver()

controllers = roboteq_command_wrapper.Controllers(
    roboteq_data_receiver.add_to_queue, 
    tb.status_receiver, 
    tb.exception_receiver, 
    settings.Roboteq.BOARDS,
    settings.Roboteq.MOTORS
)

#time.sleep(10)
print(controllers.boards)
for board_name in controllers.boards:
    print(controllers.boards[board_name].read_mixed_mode())


time.sleep(10)
print("controllers.motors", controllers.motors)
print('controllers.motors["pitch_slider"]', controllers.motors["pitch_slider"])
controllers.motors["pitch_slider"].go_to_speed_or_relative_position(200)
"""
controllers.motors["bow_position_slider"].go_to_speed_or_relative_position(200)
controllers.motors["bow_height"].go_to_speed_or_relative_position(200)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(200)
time.sleep(5)
controllers.motors["pitch_slider"].go_to_speed_or_relative_position(00)
controllers.motors["bow_position_slider"].go_to_speed_or_relative_position(00)
controllers.motors["bow_height"].go_to_speed_or_relative_position(00)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(00)
time.sleep(5)
controllers.motors["pitch_slider"].go_to_speed_or_relative_position(-200)
controllers.motors["bow_position_slider"].go_to_speed_or_relative_position(-200)
controllers.motors["bow_height"].go_to_speed_or_relative_position(-200)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(-200)
time.sleep(5)
controllers.motors["pitch_slider"].go_to_speed_or_relative_position(00)
controllers.motors["bow_position_slider"].go_to_speed_or_relative_position(00)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
time.sleep(5)
"""