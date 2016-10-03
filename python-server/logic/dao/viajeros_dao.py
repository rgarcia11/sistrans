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

def dar_count_viajeros(cur):
    stmt = 'SELECT COUNT(*) as total FROM viajeros'
    cur.execute(stmt)
    value = cur.fetchall()
    return cur, value
