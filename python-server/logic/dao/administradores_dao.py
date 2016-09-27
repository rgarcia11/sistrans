# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_administrador(cur, administrador):
    stmt= '''
    INSERT INTO administradores(nombre, identificacion, idadministrador) 
                VALUES (:nombre, :identificacion, :idadministrador)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    cur.execute(stmt, administrador.__dict__)
    return administrador
