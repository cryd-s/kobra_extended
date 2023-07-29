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

from typing import List
from dgus.display.controls.data_variable import DataVariable
from dgus.display.communication.communication_interface import SerialCommunication

from moonraker.websocket_interface import WebsocketInterface
from controls.klipper_value_format import KlipperValueType

class MoonrakerDataVariable(DataVariable):

    websock : WebsocketInterface = None
    klipper_data : List = []

    klipper_value_type : KlipperValueType = None
    array_index = -1

    fixed_point_decimal_places : int = 1
    
    def __init__(self, comInterface: SerialCommunication, dataAddress: int, dataLength: int, configAddress: int, websock : WebsocketInterface, klipper_value_type = KlipperValueType.FLOAT) -> None:
        super().__init__(comInterface, dataAddress, dataLength, configAddress)
        self.websock = websock
        self.klipper_value_type = klipper_value_type


    def set_klipper_data(self, klipper_data, array_index=-1):
        
        self.klipper_data = klipper_data
        self.array_index = array_index
        self.get_control_data_cb = self.read_moonraker_data_callback

    def value_to_fixed_point(self, data, decimal_places):

        if self.klipper_value_type == KlipperValueType.PERCENTAGE:
            #print(f"value ori: {data} value_scaled{float(data)*100}")
            data = float(data) * 100

        temp_float = float(data) * pow(10, decimal_places)

        #print(f'data var: {temp_float}')

        return int(temp_float)


    def read_moonraker_data_callback(self):
        json_obj = self.websock.get_klipper_data(self.klipper_data, self.array_index)
        val = self.value_to_fixed_point(json_obj, self.fixed_point_decimal_places)
        return val.to_bytes(length=2, byteorder='big', signed=True)

