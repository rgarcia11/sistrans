# -*- coding: iso-8859-15 -*-

import os
import sys
import tornado.web
import tornado.escape
from decorators import returnobj

def registrar_avion(cur, avion):
    stmt= '''
    INSERT INTO aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) 
    VALUES (:marca, :modelo, :numserie, :idavion, :anofabricacion, :idaerolinea)
    '''
    cur.execute(stmt, avion.__dict__)
    return avion


@returnobj #ret cursor y valor
def dar_aviones_admin(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    WITH todo AS(SELECT a.Marca, a.Modelo, a.NumSerie, a.AnoFabricacion, 
     aero.nombre AS NOMBRE_AEROLINEA, a.IdAerolinea, v.IdVuelo, 
     v.horaSalida - v.HoraLlegada AS TiempoDeVuelo
    FROM ISIS2304B121620.Aviones a, ISIS2304B121620.Vuelos v, ISIS2304B121620.Aerolineas aero
    WHERE a.idAvion = v.idAvion AND a.idAerolinea = aero.iataCod
      )--AND v.horaSalida > "2016:10:10" OR v.HoraSalida < "2016:10:11" OR v.horaLlegada > "2016:10:10" OR v.HoraLlegada < "2016:10:11")

    SELECT t.MARCA, t.MODELO, t.NUMSERIE, t.ANOFABRICACION, t.NOMBRE_AEROLINEA --, ABS(t.TIEMPODEVUELO)
    FROM todo t
    """
    
    # if 'fecha' in cuerpo:
    #     stmt+= " AND v.fecha=:fecha"
    # if 'tipovuelo' in cuerpo:
    #     stmt+= " AND v.tipovuelo=:tipovuelo"
    # if 'horasalida' in cuerpo:
    #     stmt+= " AND v.horasalida>=:horasalida"
    # if 'horallegada' in cuerpo:
    #     stmt+= " AND v.horallegada>=:horallegada"

    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values

@returnobj #ret cursor y valor
def dar_aviones(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    WITH todo AS(SELECT a.Marca, a.Modelo, a.NumSerie, a.AnoFabricacion, 
     aero.nombre AS NOMBRE_AEROLINEA, a.IdAerolinea, v.IdVuelo, 
     v.horaSalida - v.HoraLlegada AS TiempoDeVuelo
    FROM ISIS2304B121620.Aviones a, ISIS2304B121620.Vuelos v, ISIS2304B121620.Aerolineas aero
    WHERE a.idAvion = v.idAvion AND a.idAvion = :idavion AND aero.iatacod=:idaerolinea AND a.idAerolinea = aero.iataCod
      --(AND v.horaSalida > "2016:10:10" OR v.HoraSalida < "2016:10:11" OR v.horaLlegada > "2016:10:10" OR v.HoraLlegada < "2016:10:11")
    )
    SELECT t.MARCA, t.MODELO, t.NUMSERIE, t.ANOFABRICACION, t.NOMBRE_AEROLINEA --, ABS(t.TIEMPODEVUELO)
    FROM todo t
    """
    # if 'fecha' in cuerpo:
    #     stmt+= " AND v.fecha=:fecha"
    # if 'tipovuelo' in cuerpo:
    #     stmt+= " AND v.tipovuelo=:tipovuelo"
    # if 'horasalida' in cuerpo:
    #     stmt+= " AND v.horasalida>=:horasalida"
    # if 'horallegada' in cuerpo:
    #     stmt+= " AND v.horallegada>=:horallegada"
    print cuerpo
    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values