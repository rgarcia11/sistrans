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
        ret, perm, email, _type = yield self.authenticate(['administrador','viajero'])
        if perm:
            temp= self.json_args
            #{cod_aeropuerto:"XXX",fecha, aerolinea: "XX", tipovuelo, horasalida, horallegada, ordcol, ord }
            if "fecha" in temp:
                temp["fecha"] = datetime.datetime.strptime(temp['fecha'], '%Y-%m-%d')
            if "horasalida" in temp:
                temp["horasalida"] = datetime.datetime.strptime(temp['horasalida'], '%Y-%m-%d %H:%M:%S')
            if "horallegada" in temp:
                temp["horallegada"] = datetime.datetime.strptime(temp['horallegada'], '%Y-%m-%d %H:%M:%S')
            response= yield tm.dar_salidas_llegadas(temp)
            self.set_status(200)
            response = json.dumps(response)
        else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)

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

      @tornado.gen.coroutine
      def delete(self):
        if self.json_args is not None:
          ret, perm, email, _type = yield self.authenticate('administrador')
          if perm:
            #me entra idvuelo
            origendestino= yield tm.dar_origen_destino(self.json_args)
            print origendestino
            # raeliminar= yield tm.reservas_a_cancelar(self.json_args)
            # reservas= yield tm.reservas_num_vuelos(self.json_args)
            # cancelarvuelo= yield tm.cancelar_vuelo(self.json_args)
            # for actual in raeliminar:
            #     vuelo= yield tm.dar_vuelo(actual['idvuelo'])
            #     fecha= datetime.datetime.strptime(vuelo[0]['horasalida'], '%Y-%m-%d %H:%M:%S')
            #     # hoy= datetime.strptime('2017-02-14 00:00:00', '%Y-%m-%d %H:%M:%S')
            #     d = fecha - datetime.timedelta(days=1)
            #     hoy= datetime.datetime.now()
            #     if d>=hoy:
            #         # info= {'id_reserva':self.json_args['idreserva'], 'idvuelo':actual['idvuelo']}
            #         print '------------'
            #         print actual
            #         edgarin= reserva.Reserva.from_json(actual)
            #         print edgarin.json()
            #         response= yield tm.cancelar_reserva([actual['idreserva'],actual['idviajero']])
            #         cupitos= {'idvuelo': actual['idvuelo'], 'idreserva': self.json_args['idreserva']}
            #         holi= yield tm.liberar_cupos(cupitos)
            #         print holi
            #         self.set_status(201)
            #         response = actual
            #     else:
            #         response = tornado.escape.json_encode("No se puede cancelar la reserva el dia del vuelo")
            #         self.set_status(403)
            # for actual in reservas:
            #     # info= {'idviajero': , 'idvuelo': , 'idreserva':, 'numejec': , 'numecon':}
            #     edgarin= reserva.Reserva.from_json(info)
            #     print info
            #     response= yield tm.registrar_reserva(edgarin)
            #     self.set_status(201)
            #     print response
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
