# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_usuario(cur, usuario):
    stmt= '''
    INSERT INTO usuarios(nombre, identificacion, e_mail, tipo) 
                VALUES (:nombre, :identificacion, :e_mail, :tipo)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    print usuario
    cur.execute(stmt, usuario.__dict__)
    return usuario
