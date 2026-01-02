# -*- coding: UTF-8 -*-

import time
import core.module
import core.widget
import os
import re

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        
        # Auto-discovery
        self.__base_path = self.parameter("path", self.__find_hwmon())
        # Default icon: FontAwesome 'microchip' (\uf2db). 
        # You can change this in your i3 config
        self.__icon = self.parameter("icon", "") 
        
        self.__prev_energy = 0.0
        self.__prev_time = time.time()
        self.__current_watts = 0.0

    def __find_hwmon(self):
        for d in os.listdir("/sys/class/hwmon"):
            try:
                with open(f"/sys/class/hwmon/{d}/name", "r") as f:
                    if "i915" in f.read():
                        return f"/sys/class/hwmon/{d}"
            except:
                continue
        return "/sys/class/hwmon/hwmon2"

    def full_text(self, widget):
        # 1. Get Temperature
        try:
            with open(f"{self.__base_path}/temp1_input", "r") as f:
                temp = float(f.read()) / 1000.0
        except:
            temp = 0.0

        # 2. Get Fan RPM
        try:
            with open(f"{self.__base_path}/fan1_input", "r") as f:
                fan = int(f.read())
        except:
            fan = 0

        # 3. Calculate Watts
        try:
            with open(f"{self.__base_path}/energy1_input", "r") as f:
                curr_energy = float(f.read())
                curr_time = time.time()
                if self.__prev_energy > 0:
                    diff_energy = curr_energy - self.__prev_energy
                    diff_time = curr_time - self.__prev_time
                    self.__current_watts = (diff_energy / 1000000.0) / diff_time
                self.__prev_energy = curr_energy
                self.__prev_time = curr_time
        except:
            self.__current_watts = 0.0

        return "{} {:0.0f}°C, {} RPM, {:0.1f}W".format(self.__icon, temp, fan, self.__current_watts)
