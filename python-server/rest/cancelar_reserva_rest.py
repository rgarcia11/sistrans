import os
import sys
import json
import datetime as datetime
import tornado.web
import tornado.escape
import logic.tm as tm
import base_handler
import json
import models.vuelo as vuelo
import models.reserva as reserva

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
    def delete(self):
        if self.json_args is not None:
          ret, perm, email, _type = yield self.authenticate('viajero')
          if perm:
            response= yield tm.dar_reserva(self.json_args['idreserva'])
            for actual in response:
                vuelo= yield tm.dar_vuelo(actual['idvuelo'])
                fecha= datetime.datetime.strptime(vuelo[0]['horasalida'], '%Y-%m-%d %H:%M:%S')
                # hoy= datetime.strptime('2017-02-14 00:00:00', '%Y-%m-%d %H:%M:%S')
                d = fecha - datetime.timedelta(days=1)
                hoy= datetime.datetime.now()
                if d>=hoy:
                    # info= {'id_reserva':self.json_args['idreserva'], 'idvuelo':actual['idvuelo']}
                    print '------------'
                    print actual
                    edgarin= reserva.Reserva.from_json(actual)
                    print edgarin.json()
                    response= yield tm.cancelar_reserva([actual['idreserva'],actual['idviajero']])
                    cupitos= {'idvuelo': actual['idvuelo'], 'idreserva': self.json_args['idreserva']}
                    holi= yield tm.liberar_cupos(cupitos)
                    print holi
                    self.set_status(201)
                    response = actual
                else:
                    response = tornado.escape.json_encode("No se puede cancelar la reserva el dia del vuelo")
                    self.set_status(403)
          else:
            response = tornado.escape.json_encode(ret)
            self.set_status(403)
        else:
          self.set_status(400)
          response = "Error: Content-Type must be application/json"
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(response)