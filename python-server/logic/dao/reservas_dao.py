# -*- coding: iso-8859-15 -*-

import os
import sys
import time
import datetime
from decorators import returnobj

def registrar_reserva(cur, reserva):

    stmt= '''
    
    INSERT INTO reservas(idviajero, idvuelo, idreserva, numejec, numecon) 
                VALUES (:idviajero, :idvuelo, :idreserva, :numejec, :numecon)
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    c= """Savepoint antesderegistrarreserva"""
    ser="""set transaction isolation level serializable"""
    cur.execute(c)
    cur.execute(ser)
    cur.execute(stmt, reserva.__dict__)
    return reserva

# @returnobj
def cancelar_reserva(cur, reserva):
    stmt= '''
    DELETE FROM reservas WHERE idreserva= :1 AND idvuelo= :2
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    # print reserva.__dict__
    c= """Savepoint antesdecancelarreserva"""
    ser="""set transaction isolation level serializable"""
    cur.execute(c)
    cur.execute(ser)
    cur.execute(stmt,reserva) #reserva.__dict__)
    # values= cur.fetchall()
    return reserva

@returnobj
def dar_reserva(cur, id_reserva):
    stmt= '''
    SELECT * FROM reservas r WHERE r.idreserva=:id_reserva
                '''

    cur.execute(stmt, (id_reserva,))
    values= cur.fetchall()
    print values
    return cur,values

@returnobj #ret cursor y valor
def reservas_a_cancelar(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    SELECT r.idReserva, v.IdVuelo
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.Vuelos v
    WHERE r.idVuelo = v.idVuelo
      AND v.idVuelo = :idvuelo
    """

    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values

@returnobj #ret cursor y valor
def reservas_num_vuelos(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    WITH reservas_borrar AS(SELECT r.idReserva
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.Vuelos v
    WHERE r.idVuelo = v.idVuelo
    AND v.idVuelo = :idvuelo)

    SELECT MIN(b.idReserva) AS idReserva, MIN(r.idViajero) AS idViajero, 
       COUNT(r.idVuelo) AS num_vuelos
    FROM reservas_Borrar b, ISIS2304B121620.Reservas r
    WHERE b.idReserva = r.idReserva
    GROUP BY r.idReserva
    ORDER BY num_vuelos DESC
    """

    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values