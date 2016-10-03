# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import models.vuelo as vuelo

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
          ret, perm, email, _type = yield self.authenticate('administrador')
          if perm:
            edgarin= vuelo.Vuelo.from_json(self.json_args)
            response= yield tm.registrar_vuelo(edgarin)
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


    @tornado.gen.coroutine
    def put(self):
      if self.json_args is not None:
          ret, perm, email, _type = yield self.authenticate('aerolinea')
          if perm:
            response= yield tm.dar_avion_vuelo(self.json_args['idvuelo'])
            if response[0]['min'] == str(None):
              response= tornado.escape.json_encode("No hay aviones disponibles")
              self.set_status(201)
            else:
              print 'iiiiiiiiiiiii'
              info= {'id_vuelo':self.json_args['idvuelo'], 'id_avion': response[0]['min']}
              response= yield tm.asignar_avion(info)
              print response
              self.set_status(201)
              response = json.dumps(response)
              # response = response.json()
          else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
      else:
          self.set_status(400)
          response = "Error: Content-Type must be application/json"
      self.set_header('Content-Type', 'text/javascript;charset=utf-8')
      self.write(response)
