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
import dao.airports_dao as airports
import dao.vuelos_dao as vuelos
import dao.administradores_dao as administradores
import dao.viajeros_dao as viajeros
import dao.remitentes_dao as remitentes
import dao.aerolineas_dao as aerolineas

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
def get_airport(iata_code):
    conn = db.get_instance()
    if iata_code is None:
       result = yield conn.run_transaction(airports.get_airports)
    else:
       result = yield conn.run_transaction(airports.get_airport, iata_code)
    raise tornado.gen.Return(result)


