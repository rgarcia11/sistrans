# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Avion(model.Model):
    def __init__(self, entries):
        super(Avion, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        # entries["birth_day"] = datetime.datetime.strptime(entries['birth_day'], '%d/%m/%Y').date()
        entries["anofabricacion"] = datetime.datetime.strptime(entries['anofabricacion'], '%Y-%m-%d %H:%M:%S')
        return super(Avion, cls).from_json(entries)
