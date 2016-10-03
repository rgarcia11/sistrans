# *- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import models.envio as envio

class MainHandler(base_handler.BaseHandler):
    def initialize(self, db=None):
        self.db = db
    
    def prepare(self):
        if "Content-Type" in self.request.headers: 
            if self.request.headers["Content-Type"].startswith("application/json"):
               print "Got JSON"
               self.json_args = json.loads(self.request.body)
            else:
               self.json_args = None

    @tornado.gen.coroutine
    def get(self, reject, iata_code):
        #self.set_status(403)
        airports = yield tm.get_airport(iata_code)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(tornado.escape.json_encode(airports))

    @tornado.gen.coroutine
    def post(self):
        if self.json_args is not None:
          ret, perm, email, _type = yield self.authenticate('remitente')
          if perm:
            edgarin= envio.Envio.from_json(self.json_args)
            response= yield tm.registrar_envio(edgarin)
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