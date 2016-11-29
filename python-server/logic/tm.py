# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import dtm
import datetime
import tornado.web
import tornado.escape
import db.dbconn as db
import dao.utils as utils
import dao.usuarios_dao as usuarios
import dao.flights_dao as flights
import dao.countries_dao as countries
import dao.aeropuertos_dao as aeropuertos
import dao.vuelos_dao as vuelos
import dao.administradores_dao as administradores
import dao.viajeros_dao as viajeros
import dao.remitentes_dao as remitentes
import dao.aerolineas_dao as aerolineas
import dao.aviones_dao as aviones
import dao.reservas_dao as reservas
import dao.envios_dao as envios
import dao.vuelos_realizados_dao as vuelos_realizados


@tornado.gen.coroutine
def list_countries(iso_code):
    conn = db.get_instance()
    if iso_code is None:
       results = yield conn.run_transaction(countries.get_countries)
    else:
       results = yield conn.run_transaction(countries.get_country, iso_code)
    raise tornado.gen.Return(results)

@tornado.gen.coroutine
def list_flights(data, col_name, start, length, order):
    conn = db.get_instance()
    total_size = 506190
    # total_size = total_size[0]['total']
    if data is None:
       results = yield conn.run_transaction(flights.get_flights, col_name, start, length, order)
       filtered = total_size
    else:
       results, filtered = yield conn.run_transaction(flights.get_flights_from_to_date, data, col_name, start, length, order)

    # total_records = yield conn.run_transaction(flights.get_total_num)
    raise tornado.gen.Return((results, total_size,filtered))

@tornado.gen.coroutine
def registrar_usuario(usuario):
    conn = db.get_instance()
    result = yield conn.run_transaction(usuarios.registrar_usuario, usuario)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_administrador(administrador):
    conn = db.get_instance()
    result = yield conn.run_transaction(administradores.registrar_administrador, administrador)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_viajero(viajero):
    conn = db.get_instance()
    result = yield conn.run_transaction(viajeros.registrar_viajero, viajero)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_remitente(remitente):
    conn = db.get_instance()
    result = yield conn.run_transaction(remitentes.registrar_remitente, remitente)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_aerolinea(aerolinea):
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.registrar_aerolinea, aerolinea)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_aeropuerto(aeropuerto):
    conn = db.get_instance()
    result = yield conn.run_transaction(aeropuertos.registrar_aeropuerto, aeropuerto)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_avion(avion):
    conn = db.get_instance()
    result = yield conn.run_transaction(aviones.registrar_avion, avion)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def buscar_tipo(email):
    conn = db.get_instance()
    result = yield conn.run_transaction(usuarios.dar_usuario, email)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def buscar_nombre_tipo(nombre):
    conn = db.get_instance()
    result = yield conn.run_transaction(usuarios.dar_num_tipo, nombre)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_vuelo(vuelo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.registrar_vuelo, vuelo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_salidas_llegadas(cuerpo):
    conn = db.get_instance()
    result= yield conn.run_transaction(vuelos.dar_salidas_llegadas, cuerpo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_reserva(reserva):
    conn = db.get_instance()
    result = yield conn.run_transaction(reservas.registrar_reserva, reserva)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_envio(envio):
    conn = db.get_instance()
    result = yield conn.run_transaction(envios.registrar_envio, envio)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def registrar_vuelo_realizado(vuelo_realizado):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos_realizados.registrar_vuelo_realizado, vuelo_realizado)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_count_vuelos_realizados():
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos_realizados.dar_count_vuelos_realizados)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_count_viajeros():
    conn = db.get_instance()
    result = yield conn.run_transaction(viajeros.dar_count_viajeros)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_pasajeros_gerente():
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_pasajeros_gerente)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_pasajeros_aerolinea(cod):
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_pasajeros_aerolinea, cod)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_pasajeros_aeropuerto(cod):
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_pasajeros_aeropuerto, cod)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_carga_gerente():
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_carga_gerente)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_avion_vuelo(id_vuelo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_avion_vuelo,id_vuelo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def asignar_avion(info):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.asignar_avion,info)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def producido_pasajeros(id_vuelo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.producido_pasajeros,id_vuelo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def producido_carga(id_vuelo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.producido_carga,id_vuelo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def producido_fechas_carga(cuerpo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.producido_fechas_carga,cuerpo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def producido_fechas_personas(cuerpo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.producido_fechas_personas,cuerpo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_carga_aerolinea(cod):
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_carga_aerolinea, cod)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def consultar_aerolinea_carga_aeropuerto(cod):
    conn = db.get_instance()
    result = yield conn.run_transaction(aerolineas.consultar_aerolinea_carga_aeropuerto, cod)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def cancelar_reserva(cod):
    conn = db.get_instance()
    result = yield conn.run_transaction(reservas.cancelar_reserva, cod)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_reserva(id_reserva):
    conn = db.get_instance()
    result = yield conn.run_transaction(reservas.dar_reserva, id_reserva)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_vuelo(id_vuelo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_vuelo, id_vuelo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def liberar_cupos(reserva):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.liberar_cupos, reserva)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def vuelo_directo(datos):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.vuelo_directo, datos)
    raise tornado.gen.Return(result)


@tornado.gen.coroutine
def una_escala(datos):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.una_escala, datos)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def mas_escalas(datos):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.mas_escalas, datos)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_viajes(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_viajes, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_viajes_admin(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_viajes_admin, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_aviones_admin(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(aviones.dar_aviones_admin, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_aviones(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(aviones.dar_aviones, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_origen_destino(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_origen_destino, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def reservas_a_cancelar(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(reservas.reservas_a_cancelar, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def reservas_num_vuelos(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(reservas.reservas_num_vuelos, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def cancelar_vuelo(temp):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.cancelar_vuelo, temp)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def get_airport(iata_code):
    conn = db.get_instance()
    if iata_code is None:
       result = yield conn.run_transaction(airports.get_airports)
    else:
       result = yield conn.run_transaction(airports.get_airport, iata_code)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_trafico_aereo_vuelos_carga(cuerpo):
    conn = db.get_instance()
    result= yield conn.run_transaction(vuelos.dar_trafico_aereo_vuelos_carga, cuerpo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_trafico_aereo_vuelos_pasajeros(cuerpo):
    conn = db.get_instance()
    result= yield conn.run_transaction(vuelos.dar_trafico_aereo_vuelos_pasajeros, cuerpo)
    raise tornado.gen.Return(result)

@tornado.gen.coroutine
def dar_no_vuelos(cuerpo):
    conn = db.get_instance()
    result = yield conn.run_transaction(vuelos.dar_no_vuelos, cuerpo)
    raise tornado.gen.Return(result)

def test_func(cur1, conn_2, conn_3):
    stmt = """
        WITH Maximus AS(
        SELECT r.idViajero, COUNT(r.idReserva) AS NUMVIAJES
        FROM ISIS2304B121620.Viajeros v, ISIS2304B121620.Reservas r
        WHERE v.idViajero = r.idViajero
        GROUP BY v.idViajero
        )
        SELECT MAX(m.idviajero), MAX(m.numViajes)
        FROM Maximus m
    """
    stmt1 = """
        SELECT *  FROM CLIENTES_VIAJEROS WHERE MILLAS >= 10000   
    """
    stmt2 = """
        SELECT CLIENTE_VIAJERO.* FROM 
        CLIENTE_VIAJERO 
        JOIN 
        (
        SELECT VIAJES_REALIZADOS_PASAJERO.ID_CLIENTE_PAS AS ID_CLIENT, COUNT (VIAJES_REALIZADOS_PASAJERO.ID_CLIENTE_PAS) AS NUM_VIAJES FROM 
        VIAJES_REALIZADOS_PASAJERO GROUP BY VIAJES_REALIZADOS_PASAJERO.ID_CLIENTE_PAS
        ) J
        ON CLIENTE_VIAJERO.ID_VIAJERO = J.ID_CLIENT 
        WHERE J.NUM_VIAJES >= 1 and cliente_viajero.identificacion=5120
    """

    cur2 = conn_2.cursor()
    cur3 = conn_3.cursor()
    cur1.execute(stmt)
    print 'ejecute1'
    cur2.execute(stmt1)
    print 'ejecute2'
    cur3.execute(stmt2)
    print 'ejecute3'
    count1 = cur1.fetchall()
    print count1
    # dao.utils.obj_conv()
    count2= cur2.fetchall()
    print count2
    count3= cur3.fetchall()
    print count3
    c1 = utils.obj_conv(cur1, count1)
    c2 = utils.obj_conv(cur2, count2)
    c3 = utils.obj_conv(cur3, count3)
    print "Wooooo"
    return {'c1':c1, 'c2':c2, 'c3':c3}

@tornado.gen.coroutine
def two_phase_commit_example(conn_2, conn_3):    
    conn_1 = db.get_instance()
    print 'entrecito'
    result = yield conn_1.run_transaction(test_func, conn_2, conn_3)
    # result = yield result
    raise tornado.gen.Return(result)    

@tornado.gen.coroutine
def dar_usuarios_remote(mq):    
    usuarios_local= yield dar_usuarios()
    usuarios_remote= yield dtm.dar_usuarios_remote(mq)
    print usuarios_remote
    usuarios_local.append(usuarios_remote)
    # usuarios_local['usuarios'] += usuarios_remote
    raise tornado.gen.Return(usuarios_local) 

@tornado.gen.coroutine
def dar_usuarios():
    # result= {"usuarios":[{'id':1, 'name':'Empire Strikes Back', 'duration':120}, {'id':2, 'name':'Dr Strangelove', 'duration':120}]}
    conn = db.get_instance()
    result = yield conn.run_transaction(usuarios.dar_usuarios)
    print result
    raise tornado.gen.Return(result)   

def test_func2(cur1, conn_2, conn_3):
    stmt = """
        WITH num_reservas_vuelo AS (SELECT r.idVuelo, COUNT(r.idReserva) AS NUM_RESERVASN, 
        SUM(r.NUMEJEC) AS NUM_EJECN, SUM(r.NUMECON) AS NUM_ECONN
        FROM ISIS2304B121620.RESERVAS r
        GROUP BY r.idVuelo
        ), total_aerolinea AS (
        SELECT vn.idaerolinea, SUM(n.num_reservasn) as NUM_RESERVAS, 
        SUM(n.num_ejecn) as NUM_EJEC, SUM(n.num_econn) as NUM_ECON
        FROM num_reservas_vuelo n, ISIS2304B121620.Vuelos vn
        WHERE n.idVuelo = vn.idVuelo
        GROUP BY vn.idAerolinea
        ), total_vuelos AS (
        SELECT a.*, COUNT(v.idVuelo) as NUM_VUELOS
        FROM ISIS2304B121620.Aerolineas a, ISIS2304B121620.Vuelos v,
        ISIS2304B121620.AvionesPasajeros avc, ISIS2304B121620.Aviones av,
        total_aerolinea ta
        WHERE a.iatacod = v.idAerolinea AND avc.idAvion = v.idAvion
        AND av.IDAVION = avc.idavion AND ta.idaerolinea = a.iatacod
        GROUP BY a.iatacod, a.nombre, a.pais
        )
        SELECT tvs.iatacod, tas.NUM_EJEC + tas.NUM_ECON AS PRODUCIDO
        FROM total_aerolinea tas, total_vuelos tvs
        WHERE tas.idaerolinea = tvs.iatacod
    """
    stmt1 = """
        WITH ganancias AS(
        SELECT a.aerolinea, vpr.id_vuelo, vpr.pasajeros_econ*vp.costo_econ AS gananciaEcon, vpr.pasajeros_ejec*vp.costo_ejec AS GananciaEjec
        FROM VIAJES_PASAJEROS_REALIZADOS vpr, Vuelos_pasajeros vp, Vuelos v, aeronaves a
        WHERE vpr.id_vuelo = vp.id_vuelo AND vp.id_vuelo = v.id AND v.aeronave = a.NO_SERIE
        )
        SELECT g.aerolinea, COUNT(g.id_vuelo) AS numVuelos, SUM(g.GananciaEcon)+SUM(g.GananciaEjec) AS Ingresos
        FROM ganancias g
        GROUP BY g.aerolinea
    """
    stmt2 = """
        WITH numecon AS (
        SELECT COUNT(rv.id)*costo_economica AS numEcon, vp.id_vuelo, vp.costo_economica, vp.id_aerolinea
        FROM Reserva_viaje rv, Vuelo_pasajeros vp
        WHERE rv.id_vuelo = vp.id_vuelo
        GROUP BY vp.id_Vuelo, vp.costo_economica, vp.id_aerolinea
        )
        SELECT SUM(n.numecon) AS ingreso, n.id_aerolinea
        FROM numecon n
        GROUP BY n.id_aerolinea
    """

    cur2 = conn_2.cursor()
    cur3 = conn_3.cursor()
    cur1.execute(stmt)
    print 'ejecute1'
    cur2.execute(stmt1)
    print 'ejecute2'
    cur3.execute(stmt2)
    print 'ejecute3'
    count1 = cur1.fetchall()
    print count1
    # dao.utils.obj_conv()
    count2= cur2.fetchall()
    print count2
    count3= cur3.fetchall()
    print count3
    c1 = utils.obj_conv(cur1, count1)
    c2 = utils.obj_conv(cur2, count2)
    c3 = utils.obj_conv(cur3, count3)
    return {'c1':c1, 'c2':c2, 'c3':c3}

@tornado.gen.coroutine
def two_phase_commit_example2(conn_2, conn_3):    
    conn_1 = db.get_instance()
    result = yield conn_1.run_transaction(test_func2, conn_2, conn_3)
    # result = yield result
    raise tornado.gen.Return(result)   