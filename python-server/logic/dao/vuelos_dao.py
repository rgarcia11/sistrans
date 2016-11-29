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
def dar_vuelo(cur, id_vuelo):
    stmt= '''
    SELECT * FROM VUELOS WHERE idvuelo=:id_vuelo'''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    cur.execute(stmt, (id_vuelo,))
    values= cur.fetchall()
    return cur, values

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

@returnobj #ret cursor y valor
def dar_avion_vuelo(cur, id_vuelo):
    stmt = '''
    WITH total_envios AS (
    SELECT r.idVuelo, SUM(r.numejec) AS num_ejec, SUM(r.numecon) AS num_econ
    FROM Reservas r
    GROUP BY r.idVuelo
    )
    SELECT MIN(av.idAvion) as min
    FROM total_envios te,
         Vuelos v,
         AvionesPasajeros av,
         Aviones avs
    WHERE te.idVuelo = :id_vuelo AND te.idVuelo = v.idVuelo AND
         avs.idAerolinea = v.idAerolinea AND
         avs.idAvion = av.idAvion AND
         v.idAvion != av.idAvion AND
         av.sillasEconomicas > te.NUM_EJEC AND
         av.sillasEjecutivas > te.NUM_ECON
    '''
    
    cur.execute(stmt, (id_vuelo,))
    values = cur.fetchall()
    print values

    return cur, values


# @returnobj #ret cursor y valor
def asignar_avion(cur, info):
    stmt= '''
    UPDATE vuelos SET idavion= :id_avion 
    WHERE idvuelo= :id_vuelo
    '''

    print info
    cur.execute(stmt, info)
    # values= cur.fetchall()
    return info

@returnobj #ret cursor y valor
def producido_pasajeros(cur, id_vuelo):
    stmt= '''
    SELECT v.idVuelo, v.COSTOEJECUTIVO * SUM(r.NUMEJEC)+
        v.COSTOECONOMICO * SUM(r.NUMECON) as PRODUCIDO
    FROM VuelosPasajeros v, Reservas r
    WHERE v.idVuelo = r.idVuelo AND v.idVuelo = :id_vuelo
    GROUP BY v.idVuelo, v.COSTOECONOMICO, v.COSTOEJECUTIVO
    '''

    cur.execute(stmt, (id_vuelo,))
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def producido_carga(cur, id_vuelo):
    stmt= '''
    SELECT SUM(v.costoDensidad* e.peso/ e.volumen) as producido
    FROM VuelosCarga v, Envios e
    WHERE v.idVuelo = e.idVuelo AND v.idVuelo = :id_vuelo
    '''

    cur.execute(stmt, (id_vuelo,))
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def producido_fechas_carga(cur, cuerpo):
    #{fechainicio: , fechafin }
    stmt = """ 
    WITH total_por_vuelo AS (
    SELECT  v.idAerolinea, v.idVuelo, 
            COUNT(e.idEnvio) as ELEMENTOS_ENVIADOS, 
            AVG(e.peso) AS PESO_PROMEDIO,
            SUM(vc.costoDensidad* e.peso/ e.volumen) AS TOTAL_FACTURADO
    FROM Vuelos v, VuelosCarga vc,
         Envios e
    WHERE v.idVuelo = vc.idVuelo AND v.fecha >= :fechainicio
    AND v.fecha <= :fechafin AND e.idVuelo = v.idVuelo
    GROUP BY v.idVuelo, v.idAerolinea
    )
    SELECT tpv.idaerolinea, COUNT(tpv.idVuelo) AS NUMERO_VIAJES, 
           SUM(tpv.ELEMENTOS_ENVIADOS) AS ELEMENTOS_ENVIADOS, 
           AVG(PESO_PROMEDIO) AS PESO_PROMEDIO, 
           SUM(TOTAL_FACTURADO) AS TOTAL_FACTURADO
    FROM total_por_vuelo tpv
    GROUP BY tpv.idAerolinea
    ORDER BY TOTAL_FACTURADO DESC
    """
    
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    return cur, values


@returnobj #ret cursor y valor
def producido_fechas_personas(cur, cuerpo):
    #{fechainicio: , fechafin }
    stmt = """ 
    WITH total_por_vuelo AS(
    SELECT v.idaerolinea, r.idVuelo,
           SUM(r.numejec) + SUM(r.numecon) AS TOTAL_PASAJEROS,
           MAX(vp.COSTOEJECUTIVO) * SUM(r.NUMEJEC)+
           MAX(vp.COSTOECONOMICO) * SUM(r.NUMECON) as PRODUCIDO
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.vuelosPasajeros vp,
         ISIS2304B121620.Vuelos v
    WHERE r.idVuelo = v.idVuelo AND v.idVuelo = vp.idVuelo AND v.fecha >= :fechainicio
          AND v.fecha <= :fechafin
    GROUP BY r.idVuelo, v.idaerolinea
    )
    SELECT tpv.idaerolinea, COUNT(tpv.idvuelo) AS TOTAL_VUELOS,
           SUM(tpv.TOTAL_PASAJEROS) AS TOTAL_PASAJEROS,
           SUM(tpv.producido) AS PRODUCIDO
    FROM total_por_vuelo tpv
    GROUP BY tpv.idAerolinea
    """
    
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def vuelo_directo(cur, datos):
    stmt = """ 
    SELECT v.idVuelo as idvuelo --, ars.Ciudad AS origen, arl.ciudad AS destino
    FROM ISIS2304B121620.Vuelos v, ISIS2304B121620.Aeropuertos ars, ISIS2304B121620.Aeropuertos arl,
     ISIS2304B121620.Aerolineas aero
     WHERE v.AeropuertoSalida = ars.iataCod AND v.aeropuertoLlegada = arl.iataCod AND
      v.idAerolinea = aero.iataCod 
      AND aero.iataCod = :idaerolinea
      AND ars.ciudad = :ciudadsalida
      AND arl.ciudad = :ciudaddestino
    """
    c= """commit"""
    ser="""set transaction read only"""
    # cur.execute(c)
    # cur.execute(ser)
    cur.execute(stmt, datos)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def una_escala(cur, datos):
    stmt = """ 
    WITH escalas AS (SELECT v.idVuelo, ars.Ciudad AS origen, arl.ciudad AS destino
    FROM ISIS2304B121620.Vuelos v, ISIS2304B121620.Aeropuertos ars, ISIS2304B121620.Aeropuertos arl,
     ISIS2304B121620.Aerolineas aero
    WHERE v.AeropuertoSalida = ars.iataCod AND v.aeropuertoLlegada = arl.iataCod AND
      v.idAerolinea = aero.iataCod AND aero.iataCod = :idaerolinea)

    SELECT escaO.idVuelo as idvuelo1, escaD.idvuelo as idvuelo2 
    FROM escalas escaO, escalas escaD
    WHERE escaO.Origen = :ciudadsalida AND escaD.Destino = :ciudaddestino
      AND escaO.destino = escaD.origen 
    """
    c= """commit"""
    ser="""set transaction read only"""
    # cur.execute(c)
    # cur.execute(ser)
    cur.execute(stmt, datos)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def mas_escalas(cur, datos):
    stmt = """ 
    WITH escalas AS (SELECT v.idVuelo, ars.Ciudad AS origen, arl.ciudad AS destino
    FROM ISIS2304B121620.Vuelos v, ISIS2304B121620.Aeropuertos ars, ISIS2304B121620.Aeropuertos arl,
     ISIS2304B121620.Aerolineas aero
    WHERE v.AeropuertoSalida = ars.iataCod AND v.aeropuertoLlegada = arl.iataCod AND
      v.idAerolinea = aero.iataCod AND aero.iataCod = :idaerolinea)

    SELECT escaO.idvuelo as idvuelo1, e1.idvuelo as idVuelo2, escaD.idvuelo as idVuelo3
    FROM escalas escaO, escalas escaD, escalas e1--, escalas e2
    WHERE escaO.Origen = :ciudadsalida AND escaD.Destino = :ciudaddestino
      AND escaO.destino = e1.origen 
      AND e1.Destino = escaD.Origen
    --AND e2.Destino = escaD.Origen
    """
    c= """commit"""
    ser="""set transaction read only"""
    # cur.execute(c)
    # cur.execute(ser)
    cur.execute(stmt, datos)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def liberar_cupos(cur, reserva):
    stmt = """ 
    WITH calculoReserva AS(SELECT r.numejec+r.numecon AS sillasReservadas, 
       avp.sillaseconomicas + avp.SillasEjecutivas AS CAPACIDAD_TOTAL
    FROM ISIS2304B121620.reservas r, ISIS2304B121620.Vuelos v, 
     ISIS2304B121620.Aviones av, ISIS2304B121620.AvionesPasajeros avp
    WHERE r.idvuelo = v.idVuelo AND idReserva = :idreserva AND v.idvuelo = :idvuelo
      AND av.idAvion = v.idavion AND av.idAvion = avp.idAvion),
      calculoTotal AS (SELECT SUM(r.NUMEJEC) + SUM(r.NUMECON) AS RESERVAS_ACTUALES 
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.Vuelos v
    WHERE v.idVuelo = 1573 AND r.idVuelo = v.idVuelo)
      
    SELECT cr.CAPACIDAD_TOTAL - ct.RESERVAS_ACTUALES as CUPOS_ACTUALES,
       cr.CAPACIDAD_TOTAL - ct.RESERVAS_ACTUALES + cr.SillasReservadas AS NUEVO_CUPO
    FROM calculoReserva cr, calculoTotal ct
    """

    c= """commit"""
    ser="""set transaction read only"""
    # cur.execute(c)
    # cur.execute(ser)
    cur.execute(stmt, reserva)
    values = cur.fetchall()
    print values
    return cur, values

@returnobj #ret cursor y valor
def dar_viajes(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    SELECT aSalida.Ciudad AS Origen, Allegada.Ciudad AS Destino, vr.idVuelo, 
       viaj.Nombre AS nombreViajero, r.idViajero, a.Nombre AS NombreAerolinea,
       a.iataCod AS codigoAerolinea, vr.fechaSalida, 
       aSalida.iataCod AS codigoAeropuertoSalida, 
       aSalida.nombre AS nombreAeropuertoSalida, 
       vr.fechaLlegada, aLlegada.iataCod AS codigoAeropuertoLlegada, 
       aLlegada.nombre AS nombreAeropuertoLlegada, r.numejec, r.numecon,
       vr.fechaSalida - vr.fechaLlegada AS TiempoDeVuelo
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.Vuelos v,
     ISIS2304B121620.ViajesRealizados vr,
     ISIS2304B121620.Aeropuertos aSalida, ISIS2304B121620.Aeropuertos aLlegada,
     ISIS2304B121620.Aerolineas a, ISIS2304B121620.Viajeros viaj
    WHERE r.idViajero = :idviajero AND r.idVuelo = v.idVuelo AND v.aeropuertoSalida = aSalida.iataCod
      AND v.aeropuertoLlegada = aLlegada.iataCod AND a.IATACOD = v.idAerolinea
      AND viaj.idViajero = r.idViajero AND vr.idVuelo = v.idVuelo
    """
    if 'fecha' in cuerpo:
        stmt+= " AND v.fecha=:fecha"
    if 'tipovuelo' in cuerpo:
        stmt+= " AND v.tipovuelo=:tipovuelo"
    if 'horasalida' in cuerpo:
        stmt+= " AND v.horasalida>=:horasalida"
    if 'horallegada' in cuerpo:
        stmt+= " AND v.horallegada>=:horallegada"
    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    # cur.execute(c)
    print values
    return cur, values


@returnobj #ret cursor y valor
def dar_viajes_admin(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    SELECT aSalida.Ciudad AS Origen, Allegada.Ciudad AS Destino, vr.idVuelo, 
       viaj.Nombre AS nombreViajero, r.idViajero, a.Nombre AS NombreAerolinea,
       a.iataCod AS codigoAerolinea, vr.fechaSalida, 
       aSalida.iataCod AS codigoAeropuertoSalida, 
       aSalida.nombre AS nombreAeropuertoSalida, 
       vr.fechaLlegada, aLlegada.iataCod AS codigoAeropuertoLlegada, 
       aLlegada.nombre AS nombreAeropuertoLlegada, r.numejec, r.numecon,
       vr.fechaSalida - vr.fechaLlegada AS TiempoDeVuelo
    FROM ISIS2304B121620.Reservas r, ISIS2304B121620.Vuelos v,
     ISIS2304B121620.ViajesRealizados vr,
     ISIS2304B121620.Aeropuertos aSalida, ISIS2304B121620.Aeropuertos aLlegada,
     ISIS2304B121620.Aerolineas a, ISIS2304B121620.Viajeros viaj
    WHERE r.idVuelo = v.idVuelo AND v.aeropuertoSalida = aSalida.iataCod
      AND v.aeropuertoLlegada = aLlegada.iataCod AND a.IATACOD = v.idAerolinea
      AND viaj.idViajero = r.idViajero AND vr.idVuelo = v.idVuelo
    """
    if 'fecha' in cuerpo:
        stmt+= " AND v.fecha=:fecha"
    if 'tipovuelo' in cuerpo:
        stmt+= " AND v.tipovuelo=:tipovuelo"
    if 'horasalida' in cuerpo:
        stmt+= " AND v.horasalida>=:horasalida"
    if 'horallegada' in cuerpo:
        stmt+= " AND v.horallegada>=:horallegada"

    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values

@returnobj #ret cursor y valor
def dar_origen_destino(cur, cuerpo):
    c= """commit"""
    read= """SET TRANSACTION READ ONLY"""
    stmt = """ 
    SELECT ars.Ciudad as Oirgen, arl.Ciudad as Destino
    FROM ISIS2304B121620.Vuelos v, ISIS2304B121620.Aeropuertos ars, 
     ISIS2304B121620.Aeropuertos arl
    WHERE v.idVuelo = :idvuelo AND ars.iataCod = v.AeropuertoSalida
      AND arl.iataCod = v.aeropuertoLlegada
    """

    # cur.execute(c)
    cur.execute(read)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values

def cancelar_vuelo(cur, reserva):
    stmt= '''
    DELETE FROM vuelos WHERE idvuelo= :2
                '''
    # keys= ['idvuelo', 'idaerolinea', 'idnumvuelo', 'aeropuertosalida', 'aeropuertollegada', 
          # 'horasalida', 'horallegada', 'fecha', 'frecuencia', 'distancia', 'duracion', 'tipovuelo',
          # 'idavion' ]
    # print reserva.__dict__
    c= """Savepoint antesitosodematarlvuelo"""
    ser="""set transaction isolation level serializable"""
    # cur.execute(c)
    print '****'
    print reserva
    cur.execute(c)
    cur.execute(ser)
    cur.execute(stmt,(reserva,)) #reserva.__dict__)
    # values= cur.fetchall()
    return reserva

@returnobj #ret cursor y valor
def dar_trafico_aereo_vuelos_carga(cur, cuerpo):
    stmt = """ 
    Select v.*, sum(env.peso) AS Peso_total
    FROM ISIS2304B121620.vuelos v, ISIS2304B121620.aeropuertos aL, 
    ISIS2304B121620.aeropuertos aerS, ISIS2304B121620.envios env
    WHERE (aL.Ciudad = :ciudad1 OR aerS.Ciudad = :ciudad1)
      AND (aL.Ciudad = :ciudad2 OR aerS.Ciudad = :ciudad2)
      AND v.aeropuertoSalida = aerS.IATACOD AND v.aeropuertoLlegada = aL.iatacod
      AND (env.idVuelo = v.idVuelo)
    GROUP BY v.idVuelo, v.idAerolinea, v.idNumVuelo, v.aeropuertoSalida, 
         v.aeropuertoLlegada, v.HoraSalida, v.HoraLlegada, v.Fecha, v.frecuencia,
         v.distancia, v.duracion, v.tipoVuelo, v.idavion
    """

    print(stmt)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def dar_trafico_aereo_vuelos_pasajeros(cur, cuerpo):
    stmt = """ 
    Select v.*, sum(rv.numejec)+sum(rv.numecon) AS TOTAL_PASAJEROS
    FROM ISIS2304B121620.vuelos v, ISIS2304B121620.aeropuertos aL, 
     ISIS2304B121620.aeropuertos aerS, ISIS2304B121620.reservas rv
    WHERE (aL.Ciudad = :ciudad1 OR aerS.Ciudad = :ciudad1)
      AND (aL.Ciudad = :ciudad2 OR aerS.Ciudad = :ciudad2)
      AND v.aeropuertoSalida = aerS.IATACOD AND v.aeropuertoLlegada = aL.iatacod
      AND (rv.idVuelo = v.idVuelo)
    GROUP BY v.idVuelo, v.idAerolinea, v.idNumVuelo, v.aeropuertoSalida, 
         v.aeropuertoLlegada, v.HoraSalida, v.HoraLlegada, v.Fecha, v.frecuencia,
         v.distancia, v.duracion, v.tipoVuelo, v.idavion
    """

    print(stmt)
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    return cur, values

@returnobj #ret cursor y valor
def dar_no_vuelos(cur,cuerpo):
    stmt = """ 
    WITH negado AS(
    SELECT v.*
    FROM ISIS2304B121620.VUELOS v 
    WHERE (v.aeropuertosalida=:cod_aeropuerto
    OR v.aeropuertollegada=:cod_aeropuerto)
    AND v.idaerolinea =:aerolinea
    ), nonegado AS(
    SELECT *
    FROM ISIS2304B121620.Vuelos v
    WHERE (v.aeropuertoSalida=:cod_aeropuerto OR v.aeropuertoLlegada =:cod_aeropuerto)
    )
    SELECT
    nonegado.*
    FROM
    nonegado
    LEFT OUTER JOIN
    negado
    ON
    nonegado.idVuelo = negado.idVuelo
    WHERE
    negado.idVuelo IS NULL
    """
    cur.execute(stmt, cuerpo)
    values = cur.fetchall()
    print values
    return cur, values
