# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_envio(cur, envio):
    stmt= '''
    INSERT INTO envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) 
    VALUES (:idremitente, :idvuelo, :idenvio, :volumen, :peso, :contenido)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    c= """Savepoint antesderegistrarreserva"""
    ser="""set transaction isolation level serializable"""
    cur.execute(c)
    cur.execute(ser)
    cur.execute(stmt, envio.__dict__)
    return envio
