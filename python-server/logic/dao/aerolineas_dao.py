import os
import sys
import tornado.web
import tornado.escape
from decorators import returnobj

@returnobj
def get_airlines(cur):
    stmt = 'SELECT * FROM AIRLINES'
    cur.execute(stmt)
    values = cur.fetchall()
    return cur, values

@returnobj
def get_airline(cur, id_airline):
    stmt = 'SELECT * FROM AIRLINES WHERE id_airline = :1'
    cur.execute(stmt, (iata_code,))
    value = cur.fetchall()
    return cur, value

def registrar_aerolinea(cur, aerolinea):
    stmt= '''
    INSERT INTO aerolineas(iatacod, nombre, pais) 
                VALUES (:iatacod, :nombre, :pais)
                '''
    
    cur.execute(stmt, aerolinea.__dict__)
    return aerolinea
