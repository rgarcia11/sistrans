# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Vuelo_realizado(model.Model):
    def __init__(self, entries):
        super(Vuelo_realizado, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        entries["fechasalida"] = datetime.datetime.strptime(entries['fechasalida'], '%Y-%m-%d %H:%M:%S')
        entries["fechallegada"] = datetime.datetime.strptime(entries['fechallegada'], '%Y-%m-%d %H:%M:%S')
        return super(Vuelo_realizado, cls).from_json(entries)