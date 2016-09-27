# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Vuelo(model.Model):
    def __init__(self, entries):
        super(Vuelo, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        entries["horasalida"] = datetime.datetime.strptime(entries['horasalida'], '%Y-%m-%d %H:%M:%S')
        entries["horallegada"] = datetime.datetime.strptime(entries['horallegada'], '%Y-%m-%d %H:%M:%S')
        entries["fecha"] = datetime.datetime.strptime(entries['fecha'], '%Y-%m-%d %H:%M:%S')
        return super(Vuelo, cls).from_json(entries)