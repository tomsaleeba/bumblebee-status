# -*- coding: UTF-8 -*-

import core.module
import core.widget
import util.cli
import re

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        # Default path to k10temp Tctl if not provided
        # get the new value if it changes with a new kernel with:
        #   grep -l "k10temp" /sys/class/hwmon/hwmon*/name
        self.__path = self.parameter("path", "/sys/class/hwmon/hwmon4/temp1_input")

    def full_text(self, widget):
        # 1. Get Temperature
        try:
            with open(self.__path, "r") as f:
                temp = float(f.read()) / 1000.0
        except:
            temp = 0.0

        # 2. Get Frequency
        mhz = 0
        try:
            with open("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq", "r") as f:
                mhz = int(float(f.read()) / 1000.0)
        except:
            try:
                cpuinfo = open("/proc/cpuinfo").read()
                m = re.search(r"cpu MHz\s+:\s+(\d+)", cpuinfo)
                if m: mhz = int(m.group(1))
            except:
                pass

        freq_str = "{:0.1f} GHz".format(mhz/1000.0) if mhz >= 1000 else "{} MHz".format(mhz)
        
        return "{:0.1f}°C @ {}".format(temp, freq_str)
