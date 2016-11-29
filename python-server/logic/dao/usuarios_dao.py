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
    usuario.tipo = dar_num_tipo(cur, usuario.tipo)
    print usuario.__dict__
    cur.execute(stmt, usuario.__dict__)
    return usuario

@returnobj
def dar_usuario(cur, email):
    stmt= '''
    SELECT t.ntipo as tipo FROM usuarios u, tipousuario t
    WHERE u.e_mail= :1 AND u.tipo = t.tipo
    '''
    cur.execute(stmt, (email,))
    values = cur.fetchall()
    print values
    return cur, values

def dar_num_tipo(cur, nombre):
    stmt= '''
    SELECT t.tipo FROM tipousuario t
    WHERE t.ntipo = :1
    '''
    cur.execute(stmt, (nombre,))
    values = cur.fetchall()
    print values
    return values[0][0]

@returnobj
def dar_usuarios(cur):
    stmt= '''
    SELECT * FROM usuarios 
    '''
    cur.execute(stmt)
    values = cur.fetchall()
    print values
    return cur, values