# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import models.aerolinea as aerolinea

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
           print "Got JSON"
           self.json_args = json.loads(self.request.body)
        else:
           self.json_args = None

    @tornado.gen.coroutine
    def get(self):
        self.set_status(403)

    @tornado.gen.coroutine
    def post(self):
        if self.json_args is not None:
           edgarin= aerolinea.Aerolinea.from_json(self.json_args)
           response= yield tm.registrar_aerolinea(edgarin)
           self.set_status(201)
        else:
           self.set_status(400)
           response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response.json())