# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import time
import datetime
import base_handler
import tornado.web
import tornado.escape
import logic.tm as tm
import models.usuario as usuario
import models.administrador as administrador
import models.viajero as viajero
import models.remitente as remitente

class MainHandler(base_handler.BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        self.set_status(403)

    @tornado.gen.coroutine
    def post(self):
        if self.json_args is not None:
          ret, perm, email, _type = yield self.authenticate('administrador')
          if perm:
            temp= self.json_args
            value = yield tm.buscar_nombre_tipo(temp['tipo'])
            act = usuario.Usuario.from_json(self.json_args)
            # temp['tipo'] = str(temp['tipo'])
            response = yield tm.registrar_usuario(act)
            if temp['tipo']=='administrador':
              temp['tipo'] = value
              entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idadministrador':temp['identificacion']}
              act= administrador.Administrador.from_json(entries)
              response= yield tm.registrar_administrador(act)
            elif temp['tipo']=='viajero':
              temp['tipo'] = value
              entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idviajero':temp['identificacion']}
              act= viajero.Viajero.from_json(entries)
              response= yield tm.registrar_viajero(act)
            elif temp['tipo']=='remitente':
              temp['tipo'] = value
              entries= {'nombre':temp['nombre'], 'identificacion':temp['identificacion'],'idremitente':temp['identificacion']}
              act= remitente.Remitente.from_json(entries)
              response= yield tm.registrar_remitente(act)
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
