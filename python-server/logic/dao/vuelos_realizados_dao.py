# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import utils
import tornado.web
import tornado.escape
from decorators import returnobj

@returnobj
def dar_count_vuelos_realizados(cur):
    stmt = 'SELECT COUNT(*) as total FROM viajesrealizados'
    cur.execute(stmt)
    value = cur.fetchall()
    return cur, value

def registrar_vuelo_realizado(cur, vuelo_realizado):
    stmt= '''
    INSERT INTO viajesrealizados(idavion, idvuelo, idrealizado, idaerolinea, fechasalida, fechallegada) 
    VALUES (:idavion, :idvuelo, :idrealizado, :idaerolinea, :fechasalida, :fechallegada)
    '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    print vuelo_realizado
    cur.execute(stmt, vuelo_realizado.__dict__)
    return vuelo_realizado


# @returnobj #ret cursor y valor
# def dar_salidas_llegadas(cur, cuerpo):
#     #{cod_aeropuerto:"XXX",fecha, aerolinea: "XX", tipovuelo, horasalida, horallegada, ordcol, ord }
#     stmt = """ 
#     SELECT * FROM VUELOS WHERE (aeropuertosalida=:cod_aeropuerto
#     OR aeropuertollegada=:cod_aeropuerto)  
#     """
#     if 'fecha' in cuerpo:
#         stmt+= " AND fecha=:fecha"
#     if 'aerolinea' in cuerpo:
#         stmt+= " AND idaerolinea=:aerolinea"
#     if 'tipovuelo' in cuerpo:
#         stmt+= " AND tipovuelo=:tipovuelo"
#     if 'horasalida' in cuerpo:
#         stmt+= " AND horasalida>=:horasalida"
#     if 'horallegada' in cuerpo:
#         stmt+= " AND horallegada>=:horallegada"
#     if 'ordcol' in cuerpo:
#         stmt+= " ORDER BY %s %s" % (cuerpo["ordcol"], cuerpo["ord"])
    
#     print(stmt)
#     cur.execute(stmt, cuerpo)
#     values = cur.fetchall()
#     return cur, values

