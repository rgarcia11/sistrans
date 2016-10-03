# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_reserva(cur, reserva):
    stmt= '''
    INSERT INTO reservas(idviajero, idvuelo, idreserva, numejec, numecon) 
                VALUES (:idviajero, :idvuelo, :idreserva, :numejec, :numecon)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    cur.execute(stmt, reserva.__dict__)
    return reserva
