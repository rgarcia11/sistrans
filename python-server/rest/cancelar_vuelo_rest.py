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
    def delete(self):
      if self.json_args is not None:
        ret, perm, email, _type = yield self.authenticate('administrador')
        if perm:
          #me entra idvuelo
          origendestino= yield tm.dar_origen_destino(self.json_args)
          print origendestino
          raeliminar= yield tm.reservas_a_cancelar(self.json_args)
          print raeliminar
          reservas= yield tm.reservas_num_vuelos(self.json_args)
          print reservas
          r= []
          for actual in raeliminar:
              # reserva= yield tm.dar_reserva(raeliminar['idreserva'])
              vuelo= yield tm.dar_vuelo(actual['idvuelo'])
              fecha= datetime.datetime.strptime(vuelo[0]['horasalida'], '%Y-%m-%d %H:%M:%S')
              # hoy= datetime.strptime('2017-02-14 00:00:00', '%Y-%m-%d %H:%M:%S')
              d = fecha - datetime.timedelta(days=1)
              hoy= datetime.datetime.now()
              if d>=hoy:
                  # info= {'id_reserva':self.json_args['idreserva'], 'idvuelo':actual['idvuelo']}
                  print '------------'
                  print actual
                  # edgarin= reserva.Reserva.from_json(actual)
                  # print edgarin.json()
                  temp=yield tm.dar_reserva(actual['idreserva'])
                  print temp
                  r.append(temp[0])
                  response= yield tm.cancelar_reserva([actual['idreserva'],temp[0]['idviajero']])
                  cupitos= {'idvuelo': actual['idvuelo'], 'idreserva': actual['idreserva']}
                  holi= yield tm.liberar_cupos(cupitos)
                  print holi
                  self.set_status(201)
              else:
                  response = tornado.escape.json_encode("No se puede cancelar la reserva el dia del vuelo")
                  self.set_status(403)
          cancelarvuelo= yield tm.cancelar_vuelo(r[0]['idvuelo'])
          for actual in r:
              # info= {'idviajero': , 'idvuelo': , 'idreserva':, 'numejec': , 'numecon':}
              edgarin= reserva.Reserva.from_json(actual)
              print edgarin.json()
              response= yield tm.registrar_reserva(edgarin)
              self.set_status(201)
              print response
          response = actual
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
