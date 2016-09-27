# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import models.usuario as usuario
import models.administrador as administrador
import models.viajero as viajero
import models.remitente as remitente

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
          temp= self.json_args
          act= usuario.Usuario.from_json(self.json_args)
          response= yield tm.registrar_usuario(act)
          if temp['tipo']==1:
            entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idadministrador':temp['identificacion']}
            act= administrador.Administrador.from_json(entries)
            response= yield tm.registrar_administrador(act)
          elif temp['tipo']==2:
            entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idviajero':temp['identificacion']}
            act= viajero.Viajero.from_json(entries)
            response= yield tm.registrar_viajero(act)
          elif temp['tipo']==3:
            entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idremitente':temp['identificacion']}
            act= remitente.Remitente.from_json(entries)
            response= yield tm.registrar_remitente(act)
          self.set_status(201)
        else:
          self.set_status(400)
          response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response.json())
