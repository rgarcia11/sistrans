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
        ret, perm, email, _type = yield self.authenticate(['viajero'])
        if perm:
            temp= self.json_args
            #{cod_aeropuerto:"XXX",fecha, aerolinea: "XX", tipovuelo, horasalida, horallegada, ordcol, ord }
            if "fecha" in temp:
                temp["fecha"] = datetime.datetime.strptime(temp['fecha'], '%Y-%m-%d')
            if "horasalida" in temp:
                temp["horasalida"] = datetime.datetime.strptime(temp['horasalida'], '%Y-%m-%d %H:%M:%S')
            if "horallegada" in temp:
                temp["horallegada"] = datetime.datetime.strptime(temp['horallegada'], '%Y-%m-%d %H:%M:%S')
            response= yield tm.dar_viajes(temp)
            self.set_status(200)
            response = json.dumps(response)
        else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)
