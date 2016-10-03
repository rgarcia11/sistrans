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