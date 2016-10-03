# -*- coding: iso-8859-15 -*-

import os
import sys
import tornado.web
import tornado.escape
from decorators import returnobj

@returnobj
def get_airports(cur):
    stmt = 'SELECT * FROM AIRPORTS'
    cur.execute(stmt)
    values = cur.fetchall()
    return cur, values

@returnobj
def get_airport(cur, iata_code):
    stmt = 'SELECT * FROM AIRPORTS WHERE iata_code = :1'
    cur.execute(stmt, (iata_code,))
    value = cur.fetchall()
    return cur, value

def registrar_aeropuerto(cur, aeropuerto):
    stmt= '''
    INSERT INTO aeropuertos(ciudad, capacidadaviones, iatacod, nombre) 
    VALUES (:ciudad, :capacidadaviones, :iatacod, :nombre)
    '''
    cur.execute(stmt, aeropuerto.__dict__)
    return aeropuerto

