import importlib
import mido
import os
import queue
import sys
import threading
import time

app_path = os.path.dirname((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
print(app_path)
sys.path.append(os.path.split(app_path)[0])

import settings
from thirtybirds3 import thirtybirds

# Main handles network send/recv and can see all other classes directly
class Main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        class States:
            WAITING_FOR_CONNECTIONS = "waiting_for_connections"
            WAITING_FOR_HOMING = "waiting_for_homing"
            READY = "ready" 
        self.states =States()
        self.tb = thirtybirds.Thirtybirds(
            settings, 
            app_path,
            self.network_message_handler,
            self.network_status_change_handler,
            self.exception_handler
        )
        self.transport_connected = False
        self.horsewheel_connected = False

        self.pitch_slider_home = False
        self.horsewheel_slider_home = False
        self.horsewheel_lifter_home = False
        self.state = self.states.WAITING_FOR_CONNECTIONS

        self.queue = queue.Queue()
        self.tb.subscribe_to_topic("transport_connected")
        self.tb.subscribe_to_topic("horsewheel_connected")
        self.tb.subscribe_to_topic("pitch_slider_home")
        self.tb.subscribe_to_topic("horsewheel_slider_home")
        self.tb.subscribe_to_topic("horsewheel_lifter_home")

        self.tb.publish("pitch_slider_home", "start")
        self.tb.publish("horsewheel_slider_home", "start")
        self.tb.publish("horsewheel_lifter_home", "start")
        self.start()

    def network_message_handler(topic, message):
        print("network_message_handler",topic, message)
        self.add_to_queue(topic, message)
    def exception_handler(exception):
        print("exception_handler",exception)
    def network_status_change_handler(online_status):
        print("network_status_change_handler",online_status)
    def add_to_queue(self, topic, message):
        self.queue.put((topic, message))
    def run(self):
        self.state = self.states.READY # just for testing
        while True:
            try:
                #print("vvvvvvvvvvvvvv")
                #print("--------------",self.tb.check_connections())
                topic, message = self.queue.get(True)
                if self.state == self.states.WAITING_FOR_CONNECTIONS:
                    if topic == "transport_present":
                        self.transport_connected = True
                        if self.transport_connected and self.horsewheel_connected:
                            self.state = self.states.WAITING_FOR_HOMING
                            self.tb.publish("pitch_slider_home", False)
                            self.tb.publish("horsewheel_slider_home", False)
                            self.tb.publish("horsewheel_lifter_home", False)
                    if topic == "horsewheel_present":
                        self.horsewheel_connected = True
                        if self.transport_connected and self.horsewheel_connected:
                            self.state = self.states.WAITING_FOR_HOMING
                            self.tb.publish("pitch_slider_home", False)
                            self.tb.publish("horsewheel_slider_home", False)
                            self.tb.publish("horsewheel_lifter_home", False)

                if self.state == self.states.WAITING_FOR_HOMING:
                    if topic == "pitch_slider_home":
                        if message == True:
                            self.pitch_slider_home = True
                            if self.horsewheel_slider_home and self.pitch_slider_home and self.horsewheel_lifter_home:
                                self.state = self.states.READY
                    if topic == "horsewheel_slider_home":
                        if message == True:
                            self.horsewheel_slider_home = True
                            if self.horsewheel_slider_home and self.pitch_slider_home and self.horsewheel_lifter_home:
                                self.state = self.states.READY
                    if topic == "horsewheel_lifter_home":
                        if message == True:
                            self.horsewheel_lifter_home = True
                            if self.horsewheel_slider_home and self.pitch_slider_home and self.horsewheel_lifter_home:
                                self.state = self.states.READY
                if self.state == self.states.READY:
                    if topic in ["pitch_slider_position","horsewheel_slider_position","horsewheel_speed","horsewheel_lifter_position"]:
                        print(topic, message)
                        self.tb.publish(topic, message)

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(e, repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
main = Main()

class MIDI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.last_horsewheel_speed = 0
        self.start()
    def run(self):
        with mido.open_input("Q25:Q25 MIDI 1 20:0") as inport:
            for midi_o in inport:
                if midi_o.type == "note_on":
                    if midi_o.note < 59:
                        main.add_to_queue("pitch_slider_position", ((midi_o.note-48)*40000)+200000)
                    if midi_o.note > 59:
                        main.add_to_queue("horsewheel_slider_position", ((midi_o.note-48)*40000)+200000)
                if midi_o.type == "pitchwheel":
                    horsewheel_speed = int(midi_o.pitch/50)+70
                    if horsewheel_speed != self.last_horsewheel_speed:
                        self.last_horsewheel_speed = horsewheel_speed
                        main.add_to_queue("horsewheel_speed", horsewheel_speed)
                if midi_o.type == "control_change":
                    main.add_to_queue("horsewheel_lifter_position", midi_o.value * 5000)
midi = MIDI()
