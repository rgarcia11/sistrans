# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Aeropuerto(model.Model):
    def __init__(self, entries):
        super(Aeropuerto, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        # entries["birth_day"] = datetime.datetime.strptime(entries['birth_day'], '%d/%m/%Y').date()
        return super(Aeropuerto, cls).from_json(entries)
