# -*- coding: utf-8 -*-

"""Displays system idle time using xprintidle

Shows both previous and current idle times so you can see the last
sleep duration even if you just woke the screen.

contributed by `Tom`
"""

import core.module
import core.widget
import core.decorators

import util.cli


def format_idle(ms):
    """Format milliseconds into compact string like 1h24m, 3m05s, 45s, 120ms"""
    if ms < 1000:
        return "{}ms".format(ms)
    s = ms // 1000
    if s < 60:
        return "{}s".format(s)
    m = s // 60
    s = s % 60
    if m < 60:
        return "{}m{:02d}s".format(m, s)
    h = m // 60
    m = m % 60
    if h < 24:
        return "{}h{:02d}m".format(h, m)
    d = h // 24
    h = h % 24
    return "{}d{:02d}h".format(d, h)


class Module(core.module.Module):
    @core.decorators.every(seconds=20)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.idle_time))
        self.__prev = "---"
        self.__curr = "---"

    def idle_time(self, widget):
        try:
            ms = int(util.cli.execute("xprintidle").strip())
            formatted = format_idle(ms)
        except Exception:
            formatted = "n/a"
        self.__prev = self.__curr
        self.__curr = formatted
        return "idle: {:>5}, {:>5}".format(self.__prev, self.__curr)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
