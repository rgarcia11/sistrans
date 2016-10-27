# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import models.reserva as reserva
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
        ret, perm, email, _type = yield self.authenticate('viajero')
        if perm:
          daticos= {'idaerolinea':self.json_args['idaerolinea'], 'ciudadsalida': self.json_args['ciudadsalida'], 'ciudaddestino': self.json_args['ciudaddestino']}
          # idvuelos= {}
          r={}
          response= yield tm.vuelo_directo(daticos)
          print response
          if len(response)!=0:
            r=response
          else:
            response= yield tm.una_escala(daticos)
            if len(response)!=0:
              r=response
            else:
              response= yield tm.mas_escalas(daticos)
              if len(response)!=0:
                r=response
          id_vuelos= r[0]
          print id_vuelos
          argumentitos= {'idviajero':self.json_args['idviajero'], 'idreserva':self.json_args['idreserva'],'numejec':self.json_args['numejec'], 'numecon': self.json_args['numecon']} 
          llaves= id_vuelos.keys()
          # print llaves
          yamaletas= 0
          for llave in llaves:
            argumentitos.update({'idvuelo':id_vuelos[llave]})
            edgarin= reserva.Reserva.from_json(argumentitos)
            print argumentitos
            response= yield tm.registrar_reserva(edgarin)
            self.set_status(201)
            # print response
            response = response.json()
            if 'idremitente' and 'idenvio' and 'volumen' and 'peso' and 'contenido' in self.json_args and yamaletas==0:
              print '----'
              print response
              print self.json_args
              holo= {'idenvio': self.json_args['idenvio'],'volumen': self.json_args['volumen'],'idremitente': self.json_args['idremitente'], 'peso': self.json_args['peso'], 'contenido': self.json_args['contenido']}
              holo.update({'idvuelo':id_vuelos[llave]})
              print '*****************'
              print holo
              edgarin= envio.Envio.from_json(holo)
              response= yield tm.registrar_envio(edgarin)
              yamaletas=1
              response= response.json()
        else:
          response = tornado.escape.json_encode(ret)
          self.set_status(403)
      else:
        self.set_status(400)
        response = "Error: Content-Type must be application/json"
      self.set_header('Content-Type', 'text/javascript;charset=utf-8')
      self.write(response)
