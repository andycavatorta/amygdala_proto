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
            #if "internal_event" in message:
            #    pass

roboteq_data_receiver = Roboteq_Data_Receiver()
"""
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
"""
class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tb = thirtybirds.Thirtybirds(
            settings, 
            app_path,
            self.network_message_handler,
            self.network_status_change_handler,
            self.exception_handler
        )
        self.queue = queue.Queue()
        self.controllers = roboteq_command_wrapper.Controllers(
            roboteq_data_receiver.add_to_queue, 
            self.status_receiver, 
            self.network_status_change_handler, 
            {"bow":settings.Roboteq.BOARDS["bow"]},
            {
                "bow_height":settings.Roboteq.MOTORS["bow_height"],
                "bow_rotation":settings.Roboteq.MOTORS["bow_rotation"],
            }
        )
        #self.tb.subscribe_to_topic("pitch_slider_position")
        #self.tb.subscribe_to_topic("horsewheel_slider_position")
        #self.tb.subscribe_to_topic("pitch_slider_home")
        #self.tb.subscribe_to_topic("horsewheel_slider_home")
        self.tb.subscribe_to_topic("horsewheel_lifter_home")
        self.tb.subscribe_to_topic("horsewheel_speed")
        self.tb.subscribe_to_topic("horsewheel_lifter_position")
        self.tb.publish("transport_connected", True)
        self.start()

    def status_receiver(self, msg):
        print("status_receiver", msg)
    def network_message_handler(self,topic, message):
        print("network_message_handler",topic, message)
        self.add_to_queue(topic, message)
    def exception_handler(self, exception):
        print("exception_handler",exception)
    def network_status_change_handler(self,online_status):
        print("network_status_change_handler",online_status)
    def add_to_queue(self, topic, message):
        self.queue.put((topic, message))

    def run(self):
        while True:
            try:
                topic, message = self.queue.get(True)
                print(topic, message)
                if topic == "horsewheel_lifter_home":
                    self.tb.publish("horsewheel_lifter_home", True)
                if topic == b"horsewheel_speed":
                    self.controllers.macros["bow_rotation"].set_speed(int(message))
                if topic == b"horsewheel_lifter_position":
                    print("________", int(message))
                    
                    self.controllers.macros["bow_height"].go_to_absolute_position({"position":int(message), "speed":100})
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(e, repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))

main = Main()

"""
controllers.macros["bow_height"].set_speed(150)
time.sleep(5)
controllers.macros["bow_height"].coast()
time.sleep(1)
controllers.macros["bow_height"].set_speed(-150)
time.sleep(5)
controllers.macros["bow_height"].set_speed(150)
time.sleep(5)
controllers.macros["bow_height"].coast()
time.sleep(1)
controllers.macros["bow_height"].set_speed(-150)
time.sleep(5)
controllers.macros["bow_height"].coast()
time.sleep(1)
controllers.macros["bow_height"].set_speed(150)
time.sleep(5)
controllers.macros["bow_height"].coast()
time.sleep(1)
controllers.macros["bow_height"].set_speed(-150)
time.sleep(5)
controllers.macros["bow_height"].set_speed(150)
time.sleep(5)
controllers.macros["bow_height"].coast()
time.sleep(1)
controllers.macros["bow_height"].set_speed(-150)
time.sleep(5)
controllers.macros["bow_height"].coast()
controllers.macros["bow_height"].coast()
controllers.macros["bow_rotation"].coast()
controllers.macros["bow_rotation"].coast()

#controllers.macros["bow_rotation"].add_to_queue("coast")
#controllers.macros["bow_rotation"].add_to_queue("coast")
#controllers.macros["bow_rotation"].add_to_queue("coast")
#controllers.macros["bow_rotation"].add_to_queue("coast")
#controllers.macros["bow_rotation"].add_to_queue("coast")

controllers.motors["bow_rotation"].get_encoder_counter_absolute(True)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(7)
time.sleep(90)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_rotation"].get_encoder_counter_absolute(True)
#time.sleep(2)

controllers.motors["bow_height"].get_encoder_counter_absolute(True)
controllers.motors["bow_height"].go_to_speed_or_relative_position(-7)
time.sleep(5)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].get_encoder_counter_absolute(True)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)
#controllers.motors["bow_height"].go_to_speed_or_relative_position(0)

controllers.motors["bow_rotation"].set_operating_mode(0)
controllers.motors["bow_height"].set_operating_mode(0)
controllers.motors["bow_rotation"].go_to_speed_or_relative_position(0)
controllers.motors["bow_height"].go_to_speed_or_relative_position(0)

controllers.macros["pitch_slider"].add_to_queue("go_to_limit_switch")
controllers.macros["pitch_slider"].add_to_queue("go_to_absolute_position", {"position":3000000, "speed":100})
#controllers.macros["pitch_slider"].add_to_queue("oscillate", {"distance":500,"frequency":0.5,"duration":10})
"""


