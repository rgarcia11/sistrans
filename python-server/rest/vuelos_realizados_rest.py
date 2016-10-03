# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import models.vuelo_realizado as vuelo_realizado

class MainHandler(base_handler.BaseHandler):
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
          ret, perm, email, _type = yield self.authenticate('aeropuerto')
          if perm:
            tot= yield tm.dar_count_vuelos_realizados()
            self.json_args["idrealizado"]= int(tot[0]["total"])+1
            print self.json_args
            edgarin= vuelo_realizado.Vuelo_realizado.from_json(self.json_args)
            response= yield tm.registrar_vuelo_realizado(edgarin)
            self.set_status(201)
            response = response.json()
          else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
        else:
          self.set_status(400)
          response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)