# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Aerolinea(model.Model):
    def __init__(self, entries):
        super(Aerolinea, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        return super(Aerolinea, cls).from_json(entries)