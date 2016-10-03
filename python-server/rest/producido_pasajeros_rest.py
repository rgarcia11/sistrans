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

    @tornado.gen.coroutine
    def get(self=None,sl=None, param=None):
      if param is not None:
        ret, perm, email, _type = yield self.authenticate('administrador')
        if perm:
          response= yield tm.producido_pasajeros(param)
          # response= yield tm.consultar_aerolinea_carga_aeropuerto(param)
          response = json.dumps(response)
          self.set_status(201)
          # self.write(tornado.escape.json_encode(response))
        else:
          response = tornado.escape.json_encode(ret)
          self.set_status(403)
      self.set_header('Content-Type', 'text/javascript;charset=utf-8')
      self.write(response)
