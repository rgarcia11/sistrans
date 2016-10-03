# -*- coding: iso-8859-15 -*-

import os
import sys
import json
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
    result = yield conn.run_transaction(viajeros.dar_count_viajeros

        )
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
def get_airport(iata_code):
    conn = db.get_instance()
    if iata_code is None:
       result = yield conn.run_transaction(airports.get_airports)
    else:
       result = yield conn.run_transaction(airports.get_airport, iata_code)
    raise tornado.gen.Return(result)


