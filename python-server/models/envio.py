# -*- coding: utf-8 -*-

import os
import sys
import model
import datetime

class Envio(model.Model):
    def __init__(self, entries):
        super(Envio, self).__init__(entries)

    @classmethod
    def from_json(cls, entries):
        return super(Envio, cls).from_json(entries)