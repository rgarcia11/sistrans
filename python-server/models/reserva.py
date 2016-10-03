# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Reserva(model.Model):
    def __init__(self, entries):
        super(Reserva, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        return super(Reserva, cls).from_json(entries)