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

@returnobj
#todos los vuelos de la aerolinea
def num_reservas_aerolinea(cur):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVAS, 
       SUM(r.NUMEJEC) AS NUM_EJEC, SUM(r.NUMECON) AS NUM_ECON
    FROM ISIS2304B121620.RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservas), 
       SUM(n.num_ejec), SUM(n.num_econ)
    FROM num_reservas_vuelo n, ISIS2304B121620.Vuelos vn
    WHERE n.idVuelo = vn.idVuelo
    GROUP BY vn.idAerolinea
    )
    '''

    cur.execute(stmt)
    values= cur.fetchall()
    return cur, values

@returnobj
def consultar_aerolinea_pasajeros_gerente(cur):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
    SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
    FROM RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
        SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
    FROM num_reservas_vuelo n, Vuelos vn
    WHERE n.idVuelo = vn.idVuelo
    GROUP BY vn.idAerolinea
    ), total_vuelos AS (
    SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
    FROM Aerolineas a, Vuelos v,
        AvionesPasajeros avc, Aviones av,
        total_aerolinea ta
        WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
        AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
        GROUP BY a.iatacod, a.nombre, a.pais
        )
        SELECT tvs.*, tas.NUM_RESERVAS, tas.NUM_EJEC, tas.NUM_ECON
        FROM total_aerolinea tas, total_vuelos tvs
        WHERE tas.idaerolinea = tvs.iatacod'''

    cur.execute(stmt)
    value = cur.fetchall()
    return cur, value

@returnobj
def consultar_aerolinea_pasajeros_aerolinea(cur, cod):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
       SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
    FROM RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
       SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
    FROM num_reservas_vuelo n, Vuelos vn
    WHERE n.idVuelo = vn.idVuelo AND vn.idaerolinea = :cod
    GROUP BY vn.idAerolinea
    ), total_vuelos AS (
    SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
    FROM Aerolineas a, Vuelos v,
        AvionesPasajeros avc, Aviones av,
        total_aerolinea ta
    WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
        AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
    GROUP BY a.iatacod, a.nombre, a.pais
    )
    SELECT tvs.*, tas.NUM_RESERVAS, tas.NUM_EJEC, tas.NUM_ECON
    FROM total_aerolinea tas, total_vuelos tvs
    WHERE tas.idaerolinea = tvs.iatacod
    '''

    cur.execute(stmt, (cod,))
    value = cur.fetchall()
    return cur, value

@returnobj
def consultar_aerolinea_pasajeros_aeropuerto(cur, cod):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
       SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
    FROM RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
       SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
    FROM num_reservas_vuelo n, Vuelos vn
    WHERE n.idVuelo = vn.idVuelo AND (vn.aeropuertoSalida = :cod OR vn.aeropuertoLlegada = :cod)
    GROUP BY vn.idAerolinea

    ), total_vuelos AS (
    SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
    FROM Aerolineas a, Vuelos v,
        AvionesPasajeros avc, Aviones av,
        total_aerolinea ta
    WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
      AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
    GROUP BY a.iatacod, a.nombre, a.pais
    )
    SELECT tvs.*, tas.NUM_RESERVAS, tas.NUM_EJEC, tas.NUM_ECON
    FROM total_aerolinea tas, total_vuelos tvs
    WHERE tas.idaerolinea = tvs.iatacod
    '''

    cur.execute(stmt, (cod,))
    value = cur.fetchall()
    return cur, value


@returnobj
def consultar_aerolinea_carga_gerente(cur):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
       SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
    FROM RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
       SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
    FROM num_reservas_vuelo n, Vuelos vn
    WHERE n.idVuelo = vn.idVuelo
    GROUP BY vn.idAerolinea

    ), total_vuelos AS (
    SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
    FROM Aerolineas a, Vuelos v,
     AvionesPasajeros avc, Aviones av,
     total_aerolinea ta
    WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
      AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
    GROUP BY a.iatacod, a.nombre, a.pais
    ), total_envios AS (
    SELECT e.idVuelo, SUM(e.Volumen) AS VOLUMEN_TOTAL,
           SUM(e.peso) as PESO_TOTAL
    FROM envios e
    GROUP BY idVuelo
    ), total_envios_aerolinea AS (
    SELECT v.idaerolinea, SUM(te.volumen_total) as volumen_total,
           SUM(te.peso_total) as peso_total
    FROM total_envios te, Vuelos v,
         Aviones a
    WHERE te.idVuelo = v.idVuelo AND a.idAvion = v.idAvion
    GROUP BY v.idaerolinea
    )

    SELECT tvs.*, tas.NUM_RESERVAS, tas.NUM_EJEC, tas.NUM_ECON, 
       tea.VOLUMEN_TOTAL, tea.PESO_TOTAL
    FROM total_aerolinea tas, total_vuelos tvs, total_envios_aerolinea tea
    WHERE tas.idaerolinea = tvs.iatacod AND tea.idAerolinea = tas.idAerolinea'''

    cur.execute(stmt)
    value = cur.fetchall()
    return cur, value


@returnobj
def consultar_aerolinea_carga_aerolinea(cur, cod):
    stmt= '''
    WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
           SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
    FROM RESERVAS r
    GROUP BY r.idVuelo
    ), total_aerolinea AS (
    SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
           SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
    FROM num_reservas_vuelo n, Vuelos vn
    WHERE n.idVuelo = vn.idVuelo
    GROUP BY vn.idAerolinea 

    ), total_vuelos AS (
    SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
    FROM Aerolineas a, Vuelos v,
         AvionesPasajeros avc, Aviones av,
         total_aerolinea ta
    WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
          AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
          AND a.iatacod = :cod
    GROUP BY a.iatacod, a.nombre, a.pais
    ), total_envios AS (
    SELECT e.idVuelo, SUM(e.Volumen) AS VOLUMEN_TOTAL,
           SUM(e.peso) as PESO_TOTAL
    FROM envios e
    GROUP BY idVuelo
    ), total_envios_aerolinea AS (
    SELECT v.idaerolinea, SUM(te.volumen_total) as volumen_total,
           SUM(te.peso_total) as peso_total
    FROM total_envios te, Vuelos v,
         Aviones a
    WHERE te.idVuelo = v.idVuelo AND a.idAvion = v.idAvion
    GROUP BY v.idaerolinea
    )   

    SELECT tvs.*, tas.NUM_RESERVAS, tas.NUM_EJEC, tas.NUM_ECON, 
           tea.VOLUMEN_TOTAL, tea.PESO_TOTAL
    FROM total_aerolinea tas, total_vuelos tvs, total_envios_aerolinea tea
    WHERE tas.idaerolinea = tvs.iatacod AND tea.idAerolinea = tas.idAerolinea'''

    cur.execute(stmt, (cod,))
    value = cur.fetchall()
    return cur, value


@returnobj
def consultar_aerolinea_carga_aeropuerto(cur, cod):
    stmt= '''
    WITH total_envios AS (
    SELECT e.idVuelo, SUM(e.Volumen) AS VOLUMEN_TOTAL,
       SUM(e.peso) as PESO_TOTAL
    FROM envios e
    GROUP BY idVuelo
    )
    SELECT v.idaerolinea, SUM(te.volumen_total) as volumen_total,
       SUM(te.peso_total) as peso_total
    FROM total_envios te, Vuelos v, Aviones a
    WHERE te.idVuelo = v.idVuelo
      AND (aeropuertoSalida = :cod OR aeropuertoLlegada = :cod)
      AND a.idAvion = v.idAvion
    GROUP BY v.idaerolinea'''

    cur.execute(stmt, (cod,))
    value = cur.fetchall()
    return cur, value
