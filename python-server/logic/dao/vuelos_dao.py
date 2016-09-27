# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import utils
import tornado.web
import tornado.escape
from decorators import returnobj

@returnobj
def get_flight_count(cur):
    stmt = 'SELECT COUNT(*) as total FROM VUELOS'
    cur.execute(stmt)
    value = cur.fetchall()
    return cur, value

def registrar_vuelo(cur, vuelo):
    stmt= '''
    INSERT INTO VUELOS(idvuelo, idaerolinea, idnumvuelo, aeropuertosalida, aeropuertollegada,
                horasalida, horallegada, fecha, frecuencia, distancia, duracion, tipovuelo, idavion) 
                VALUES (:idvuelo, :idaerolinea, :idnumvuelo, :aeropuertosalida, :aeropuertollegada,
                :horasalida, :horallegada, :fecha, :frecuencia, :distancia, :duracion, :tipovuelo, :idavion)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    print vuelo
    cur.execute(stmt, vuelo.__dict__)
    return vuelo


@returnobj #ret cursor y valor
def dar_salidas_llegadas(cur, cuerpo):
    #{cod_aeropuerto:"XXX",fecha, aerolinea: "XX", tipovuelo, horasalida, horallegada, ordcol, ord }
    stmt = """ 
    SELECT * FROM VUELOS WHERE (aeropuertosalida=:cod_aeropuerto
    OR aeropuertollegada=:cod_aeropuerto)  
    """
    if 'fecha' in cuerpo:
        stmt+= " AND fecha=:fecha"
    if 'aerolinea' in cuerpo:
        stmt+= " AND idaerolinea=:aerolinea"
    if 'tipovuelo' in cuerpo:
        stmt+= " AND tipovuelo=:tipovuelo"
    if 'horasalida' in cuerpo:
        stmt+= " AND horasalida>=:horasalida"
    if 'horallegada' in cuerpo:
        stmt+= " AND horallegada>=:horallegada"
    if 'ordcol' in cuerpo:
        stmt+= " ORDER BY %s %s" % (cuerpo["ordcol"], cuerpo["ord"])
    
    print(stmt)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    return cur, values

