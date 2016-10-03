# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.web
import tornado.escape
import logic.tm as tm
import models.model as model
import datetime
import base_handler

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
    def get(self):
        # ret, perm, email, _type = yield self.authenticate(['viajero','remitente'])
        # if perm:
            temp= self.json_args
            #{fechainicio, fechafin}
            if "fechainicio" in temp:
                temp["fechainicio"] = datetime.datetime.strptime(temp['fechainicio'], '%Y-%m-%d %H:%M:%S')
            if "fechafin" in temp:
                temp["fechafin"] = datetime.datetime.strptime(temp['fechafin'], '%Y-%m-%d %H:%M:%S')
            
            response= yield tm.producido_fechas_carga(temp)
            print response

            self.set_status(200)
            # response= response.json()
            # response= tornado.escape.json_encode(response)
            response = json.dumps(response)
        # else:
        #     response = tornado.escape.json_encode(ret)
        #     self.set_status(403)