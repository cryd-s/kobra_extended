 # 
 # This file is part of python-dgus (https://github.com/seho85/python-dgus).
 # Copyright (c) 2022 Sebastian Holzgreve
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #
 
from distutils.log import error
import os
import json
from threading import Thread, Lock
from time import sleep
from typing import Any, Callable
from websocket import WebSocketApp
from jsonmerge import merge
from queue import Queue

from dgus.display.serialization.json_serializable import JsonSerializable
from moonraker.request_id import WebsocktRequestId
from moonraker.moonraker_request import MoonrakerRequest

import logging

from moonraker.klippy_state import KlippyState
from moonraker.printer_state import PrinterState

class WebsocketInterface(JsonSerializable):
    ws_app : WebSocketApp
    thread : Thread
    cyclic_query_thread : Thread
    open : bool = False
    printer_ip = "1.2.3.4"
    port = 7125
    json_data_modell = {}
    server_info = {}
    cyclic_query_thread_running = False

    json_resouce_lock = Lock()

    _requests : Queue = Queue()
    _current_request : MoonrakerRequest = None

    _logger = logging.getLogger(__name__)

    _klippy_state : KlippyState = KlippyState.UNKOWN
    _klippy_state_text : str = ""
    _klippy_event_changed_callbacks = []

    _printer_state : PrinterState = PrinterState.UNKNOWN
    _printer_error_text : str = ""
    _printer_state_event_changed_callbacks = []

    query_req = {
        "jsonrpc": "2.0",
        "method": "printer.objects.query",
        "params": {
            "objects": {
                "extruder": None,
                "heater_bed": None
            }
        },
        "id": WebsocktRequestId.QUERY_PRINTER_OBJECTS
    }


    subscription_request = {
        "jsonrpc": "2.0",
        "method": "printer.objects.subscribe",
        "params": {
            "objects": {
                "heater_bed": None,
                "extruder": None
            }
        },
        "id": WebsocktRequestId.SUBSCRIBE_REQUEST
    }


    def __init__(self, printer_ip, port) -> None:
        self.printer_ip = printer_ip
        self.port = port

        self.create_websocket()
        

    def create_websocket(self):

        ws_url = f"ws://{self.printer_ip}:{str(self.port)}/websocket?token="

        self._logger.info("Using websocket URL: %s", ws_url)
       
        def on_close(ws_app, close_status, close_msg):
            self.ws_on_close(ws_app, close_status, close_msg)

        def on_error(ws_app, error):
            self.ws_on_error(ws_app, error)

        def on_message(ws_app, msg):
            self.ws_on_message(ws_app,msg)

        def on_open(ws_app):
            self.ws_on_open(ws_app)

        self.ws_app = WebSocketApp(
            url=ws_url,
            on_close=on_close,
            on_error=on_error,
            on_message=on_message,
            on_open=on_open
        )


    def start(self):
        self.thread = Thread(target=self.ws_app.run_forever)
        self.thread.start()
        self.cyclic_query_thread_running = True
        self.cyclic_query_thread = Thread(target=self.cyclic_query_thread_function)
        self.cyclic_query_thread.start()
        

    def cyclic_query_thread_function(self):
        while self.cyclic_query_thread_running:
            
            if self.open:
            
                query_server_info_json = {
                    "jsonrpc": "2.0",
                    "method": "server.info",
                    "id": WebsocktRequestId.QUERY_SERVER_INFO
                }

                #print("send cyclic query...")

            
                self.ws_app.send(json.dumps(query_server_info_json))


                query_server_info_json = {
                    "jsonrpc": "2.0",
                    "method": "printer.info",
                    "id": WebsocktRequestId.QUERY_PRINTER_INFO
                }

                self.ws_app.send(json.dumps(query_server_info_json))

                if not self._requests.empty():
                    if self._current_request is None:
                        self._current_request = self._requests.get()
                        self.ws_app.send(json.dumps(self._current_request.request))
                        self._current_request.request_was_send_callback()

            
            

            sleep(1)

    
    def stop(self):
        self.cyclic_query_thread_running = False
        self.cyclic_query_thread.join()
        self._logger.info("Stopped cyclic query thread...")
        
        self.ws_app.close()
        self.thread.join()
        self._logger.info("Stopped Websocket Communication....")
        

    def ws_on_open(self, ws_app):
        self.open = True
        self._logger.info("Connection to Moonraker websocket established...")
        self.send_query(ws_app)

    def ws_on_close(self,ws_app, close_status, close_msg):
        self.open = False

        self._logger.error("Websocket onClose %s, %s", close_status, close_msg)

        self.cyclic_query_thread_running = False
        self.cyclic_query_thread.join()

        self.start()

    def ws_on_error(self, ws_app, error):
        self._logger.critical("Websockt Error %s: %s", ws_app, error)

    def ws_on_message(self, ws_app, msg):
        response = json.loads(msg)
        #print(json.dumps(response, indent=3))
        #global json_data_modell

        if 'id' in response:
            # Response to our query data request 
            if response["id"] == WebsocktRequestId.QUERY_PRINTER_OBJECTS:
                #print(json.dumps(response, indent=2))
                with self.json_resouce_lock:
                    json_merged = merge(self.json_data_modell, response["result"]["status"])
                    self.json_data_modell = json_merged

                #print(json.dumps(self.json_data_modell, indent=3))
            
                self.add_subscription(ws_app)

            if response["id"] == WebsocktRequestId.QUERY_SERVER_INFO:
                #print(json.dumps(response, indent=3))

                #self.server_info = response["resut"]
                with self.json_resouce_lock:
                    json_merged = merge(self.json_data_modell["server_info"], response["result"] )
                    self.json_data_modell["server_info"] = json_merged

                    #print(json.dumps(response, indent=3))

            #if response["id"] == 8000:
            #    print(json.dumps(response, indent=3))

            if response["id"] == WebsocktRequestId.QUERY_PRINTER_INFO:
                #print(json.dumps(response, indent=3))

                if 'result' in response:
                    state_string = response["result"]["state"]
                    state_message = response["result"]["state_message"]
                    klippy_state = KlippyState.get_state_for_string(state_string)

                    if klippy_state != self._klippy_state or state_message != self._klippy_state_text:
                        self._set_klippy_state(klippy_state, state_message)


            if self._current_request is not None:
                if response["id"] == self._current_request.request["id"]:
                    self._current_request.response_received_callback(response)
                    self._current_request = None
            
        
        if 'method' in response:
            # Subscribed printer objects are send with method: "notifiy_status_update"
            # The subscribed objects are only published when the value has changed.
            # e.g. bed_temperature target set to 50°, extruder temperature has changed, bed_temperature has changed, a.s.o.
            if response['method'] == "notify_status_update":
                #print(json.dumps(response, indent=3))
                #TODO: Resource locking - possible data race!
                json_pub_data = response["params"][0]
                json_merged = merge(self.json_data_modell, json_pub_data)
                with self.json_resouce_lock:
                    printer_state_string = str(json_merged["print_stats"]["state"])
                    read_printer_state = PrinterState.get_state_for_string(printer_state_string)
                    if self._printer_state != read_printer_state:
                        self._set_printer_state(read_printer_state)
                    self.json_data_modell = json_merged


                    
                #print(json.dumps(self.json_data_modell["toolhead"]["homed_axes"], indent=3))
                #print(json.dumps(json_merged, indent=2))


            if response['method'] == "notify_klippy_ready":
                self.add_subscription(ws_app)
                self._logger.info("Received: notifiy_klippy_ready")
                self._set_klippy_state(KlippyState.READY)

            if response['method'] == "notify_klippy_shutdown":
                self._logger.info("Received: notifiy_klippy_shutdown")
                self._set_klippy_state(KlippyState.SHUTDOWN)
                

            if response['method'] == "notify_klippy_disconnected":
                self._logger.info("Received: notifiy_klippy_disconnected")
                self._set_klippy_state(KlippyState.DISCONNECTED)



    def send_query(self, ws):
       
        self.ws_app.send(json.dumps(self.query_req))

    def unsubscribe_all(self, ws):
        data = {
            "jsonrpc": "2.0",
            "method": "printer.objects.subscribe",
            "params": {
                "objects": { },
            },
            "id": WebsocktRequestId.UNSUBSCRIBE_PRINTER_OBJECTS
        }

        self.ws_app.send(json.dumps(data))


    def add_subscription(self, ws):
        self.ws_app.send(json.dumps(self.subscription_request))

    def write_json_config(self, websocket_json_config):

        with open(websocket_json_config, "w") as json_file:
            json_file.write(json.dumps(self.to_json(), indent=3))

    def read_json_config(self, websocket_json_config):

        try:
            with open(websocket_json_config) as json_file:
                json_data = json.load(json_file)
                return self.from_json(json_data)

        except FileNotFoundError:
            self._logger.critical("Unable to read configuration from %s",websocket_json_config)
            return False
            


    def get_klipper_data(self, klipper_data : list, array_index : int = -1):
        with self.json_resouce_lock:
            json_obj = self.json_data_modell
            for dp in klipper_data:
                json_obj = json_obj.get(dp)
                if json_obj is None:
                    print(f"Error Invalid Klipper Data {klipper_data}")
                    return None

            if array_index >= 0:
                json_obj = json_obj[array_index]
            return json_obj


    def queue_request(self, request : MoonrakerRequest):
        self._requests.put(request)
    #JsonSerializable implementation

    def from_json(self, json_data : dict):
        websocket_object = json_data.get("websocket")
        if websocket_object is None:
            print("Malformed Websocket.json: 'websocket' entry is missing!")
            return False
        
        ip_object = websocket_object.get("ip")
        if ip_object is None:
            print("Malformed Websocket.json: Missing 'ip' entry!")
            return False

        port_object = websocket_object.get("port")
        if port_object is None:
            print("Malformed JSON: Missing 'port' entry!")
            return False


        printer_objects_object = websocket_object.get("printer_objects")
        if printer_objects_object is None:
            print("Malformed JSON: Missing 'printer_objects' entry!")
            return False

        data_modell_object = websocket_object.get("data_model")
        if data_modell_object is None:
            print("Malformed JSON: Missing 'data_model' entry!")
            return False

        self.query_req["params"]["objects"] = printer_objects_object
        self.subscription_request["params"]["objects"] = printer_objects_object
        self.json_data_modell = data_modell_object

        self.printer_ip = ip_object
        self.port = port_object

        self.create_websocket()

        return True

    def to_json(self):
        websocket_json = {
            "websocket" : {
                "ip" : self.printer_ip,
                "port" : self.port,
                "printer_objects" : self.query_req["params"]["objects"],
                "data_model" : self.json_data_modell
            }
        }

        return websocket_json

    def _set_klippy_state(self, state : KlippyState, state_message = ""):
        self._klippy_state = state
        self._klippy_state_text = state_message
        self._logger.info("KlippyState Changed: %s", self._klippy_state)
        self._logger.info("State Message: %s", state_message.replace("\n", " "))

        for cb in self._klippy_event_changed_callbacks:
            cb(state, state_message)
      


    def register_klippy_state_event_receiver(self, callback : Callable[[KlippyState, str], Any]):
        self._klippy_event_changed_callbacks.append(callback)



    def _set_printer_state(self, state : PrinterState, error_msg = ""):
        
        self._printer_state = state
        self._printer_error_text = error_msg

        self._logger.info("PrinterState Changed: %s", self._printer_state)
        if self._printer_state == PrinterState.ERROR:
            self._logger.info("Error Message: %s", error_msg.replace("\n", " "))

        for callback in self._printer_state_event_changed_callbacks:
            callback(state, error_msg)


    def register_printer_state_event_receiver(self, callback : Callable[[PrinterState, str], Any]):
        self._printer_state_event_changed_callbacks.append(callback)