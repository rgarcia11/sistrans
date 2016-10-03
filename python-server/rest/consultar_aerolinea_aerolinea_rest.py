# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import   json
import models.vuelo as vuelo

class MainHandler(base_handler.BaseHandler):
    def initialize(self, db=None):
        self.db = db

    # def permpare(self):
    #     if self.request.headers["Content-Type"].startswith("application/json"):
    #        print "Got JSON"
    #        self.json_args = json.loads(self.request.body)
    #     else:
    #        self.json_args = None

    @tornado.gen.coroutine
    def get(self=None, sl=None, param=None):
        if param is not None:
          ret, perm, email, _type = yield self.authenticate('aerolinea')
          if perm:
            print "holooooooo"
            # response= yield tm.consultar_aerolinea_pasajeros_aerolinea(param)
            response= yield tm.consultar_aerolinea_carga_aerolinea(param)
            response = json.dumps(response)
            self.set_status(201)
          else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)
