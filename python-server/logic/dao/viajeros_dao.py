# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_viajero(cur, viajero):
    stmt= '''
    INSERT INTO viajeros(nombre, identificacion, idviajero) 
                VALUES (:nombre, :identificacion, :idviajero)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    cur.execute(stmt, viajero.__dict__)
    return viajero
