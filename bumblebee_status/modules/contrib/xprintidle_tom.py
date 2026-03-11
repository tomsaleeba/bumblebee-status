# -*- coding: utf-8 -*-

"""Displays system idle time using xprintidle

contributed by `Tom`
"""

import core.module
import core.widget
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(seconds=20)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.idle_time))
        self.__info = ""

    def idle_time(self, widget):
        try:
            self.__info = util.cli.execute("xprintidle -H").strip()
        except Exception:
            self.__info = "n/a"
        return "idle: {}".format(self.__info)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
