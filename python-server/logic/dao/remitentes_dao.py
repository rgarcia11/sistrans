# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_remitente(cur, remitente):
    stmt= '''
    INSERT INTO remitentes(nombre, identificacion, idremitente) 
                VALUES (:nombre, :identificacion, :idremitente)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    cur.execute(stmt, remitente.__dict__)
    return remitente
