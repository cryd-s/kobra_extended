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

import logging
from json import dumps
from dgus.display.communication.request import Request
from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.display import Display
from controls.moonraker_data_variable import MoonrakerDataVariable
from moonraker.websocket_interface import WebsocketInterface
from dgus.display.communication.protocol import build_write_vp
from keycodes import KeyCodes
from moonraker.moonraker_request import MoonrakerRequest
from data_addresses import DataAddress
from moonraker.request_id import WebsocktRequestId



class AxesDisplayMask(Mask):
    
    web_socket : WebsocketInterface = None
    display : Display = None
    distance : int = 10

    logger = logging.getLogger(__name__)


    def __init__(self, com_interface: SerialCommunication, web_sock : WebsocketInterface, display : Display) -> None:
        super().__init__(1, com_interface)
        self.web_socket = web_sock
        self.display = display

        self.xpos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_X_POS, 2, DataAddress.UNDEFINED, self.web_socket)
        #self.xpos.set_klipper_data(["toolhead", "position"], 0)
        self.xpos.set_klipper_data(["motion_report", "live_position"], 0)
        self.controls.append(self.xpos)

        self.ypos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_Y_POS, 2, DataAddress.UNDEFINED, self.web_socket)
        #self.ypos.set_klipper_data(["toolhead", "position"], 1)
        self.ypos.set_klipper_data(["motion_report", "live_position"], 1)
        self.controls.append(self.ypos)

        self.zpos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_Z_POS, 2, DataAddress.UNDEFINED, self.web_socket)
        #self.zpos.set_klipper_data(["toolhead", "position"], 2)
        self.zpos.set_klipper_data(["motion_report", "live_position"], 2)
        self.controls.append(self.zpos)

        com_interface.register_spontaneous_callback(DataAddress.SPONT_MOVE_DISTANCE, self.move_distance_changed)
        com_interface.register_spontaneous_callback(DataAddress.SPONT_MOVE_BUTTON, self.key_pressed)

    def move_distance_changed(self, data):
        response_payload = data[7:]

        self.distance = int.from_bytes(response_payload, byteorder='big')

        biticon_val = 0
        
        if self.distance == 1:
            biticon_val = 1

        if self.distance == 10:
            biticon_val = 2

        if self.distance == 100:
            biticon_val = 4

        if self.distance == 1000:
            biticon_val = 8

        def send_biticon_state():
            req_bytes = build_write_vp(DataAddress.MOVE_DISTANCE_BITICON, biticon_val.to_bytes(byteorder='big', length=2))
            return req_bytes
            

        req = Request(send_biticon_state, None, "SendBit IconState")
        self._com_interface.queue_request(req)

        self.logger.info('Move Distance changed to %s', self.distance)

    def key_pressed(self, data):
        response_payload = data[7:]
        keycode = int.from_bytes(response_payload, byteorder='big')

        #print(f'keycode: {keycode}')

        if self.is_keycode_a_move_key(keycode):
            self.perform_move(keycode)

        if self.is_keycode_a_home_key(keycode):
            self.perform_homing()

        if keycode == KeyCodes.Z_TILT:
            self.logger.debug("Z-Tilt pressed...")
            self.perform_z_tilt()


        if keycode == KeyCodes.USER_POS1:
            self.logger.debug("User POS1 pressed...")
            self.perform_user_pos(1)

        if keycode == KeyCodes.USER_POS2:
            self.logger.debug("User POS2 pressed...")
            self.perform_user_pos(2)


    def is_keycode_a_move_key(self, key_code):
        is_a_movex_key = key_code == KeyCodes.MoveXMinus or key_code == KeyCodes.MoveXPlus
        is_a_movey_key = key_code == KeyCodes.MoveYMinus or key_code == KeyCodes.MoveYPlus
        is_a_movez_key = key_code == KeyCodes.MoveZMinus or key_code == KeyCodes.MoveZPlus

        is_a_move_key = is_a_movex_key or is_a_movey_key or is_a_movez_key
        return is_a_move_key

    def perform_move(self, keycode):
        axe = "Y"
        move_sign = "-"
        move_distance = str(self.distance / 10)
        accell = 1000

        if keycode == KeyCodes.MoveXPlus:
            axe = "X"
            move_sign = "+"
            accell = 6000

        if keycode == KeyCodes.MoveXMinus:
            axe = "X"
            move_sign = "-"
            accell = 6000

        if keycode == KeyCodes.MoveYPlus:
            axe = "Y"
            move_sign = "+"
            accell = 6000

        if keycode == KeyCodes.MoveYMinus:
            axe = "Y"
            move_sign = "-"
            accell = 6000

        if keycode == KeyCodes.MoveZPlus:
            axe = "Z"
            move_sign = "+"
            accell = 1500

        if keycode == KeyCodes.MoveZMinus:
            axe = "Z"
            move_sign = "-"
            accell = 1500

        #print(f'G1 {axe}{move_sign}{move_distance} F{accell}')
        
        move_cmd = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": f'G91\n G1 {axe}{move_sign}{move_distance} F{accell}\n G90',
                                
            },
            "id": WebsocktRequestId.PERFORM_MOVE_CMD
        }
        self.web_socket.ws_app.send(dumps(move_cmd))

    def is_keycode_a_home_key(self, keycode):
        is_a_home_key = keycode == KeyCodes.HomeAll or keycode == KeyCodes.HomeXY or keycode == KeyCodes.HomeZ

        return is_a_home_key

    def perform_homing(self):
        home_cmd = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": 'M18 X Y Z\n G28',
                                
            },
            "id": WebsocktRequestId.TURN_MOTORS_OFF_CMD
        }

        req = MoonrakerRequest(
            request_was_send_callback=self.homing_request_send,
            response_received_callback=self.home_request_finished,
            request=home_cmd
        )

        self.web_socket.queue_request(req)

    def homing_request_send(self):
        self.logger.info("Homing request was send....")
        self.display.switch_to_mask(51, False)


    def home_request_finished(self, json_data):
        self.logger.info("Homing request finished....")
        self.display.switch_to_mask(self.mask_no, False)

    def perform_z_tilt(self):
        ztilt_cmd = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": 'DGUS_ZTILT',
                                
            },
            "id": WebsocktRequestId.PERFORM_Z_TILT
        }
        self.logger.debug("'Perform Z-Tilt' Websocket Request: %s", dumps(ztilt_cmd, indent=3))
        self.web_socket.ws_app.send(dumps(ztilt_cmd))


    def perform_user_pos(self, pos : int):
        user_pos_cmd = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": f'DGUS_USER_POS{pos}',
                                
            },
            "id": WebsocktRequestId.SET_USER_POS
        }
        self.logger.debug("User Pos Websocket Request: %s", dumps(user_pos_cmd, indent=3))
        self.web_socket.ws_app.send(dumps(user_pos_cmd))