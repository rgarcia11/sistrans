# -*- coding: iso-8859-15 -*-

"""
routes
======

This module establishes and defines the Web Handlers and Websockets
that are associated with a specific URL routing name. New routing
associations must be defined here.

Notes
-----
For more information regarding routing URL and valid regular expressions
visit: http://www.tornadoweb.org/en/stable/guide/structure.html
"""

import os
import sys
import web
import rest

#Define new rest associations
REST = [
(r"/api/countries(/?([A-Z]{2})?)", rest.countries_rest.MainHandler),
(r'/api/vuelos', rest.vuelos_rest.MainHandler),
(r'/api/usuarios', rest.usuarios_rest.MainHandler),
(r'/api/aeropuertos/salidas_llegadas', rest.aeropuertos_salidas_llegadas_rest.MainHandler),
(r'/api/aerolineas', rest.aerolineas_rest.MainHandler),
(r'/api/aviones', rest.aviones_rest.MainHandler),
(r'/api/reservas', rest.reservas_rest.MainHandler),
(r'/api/envios', rest.envios_rest.MainHandler),
(r'/api/vuelos/realizados', rest.vuelos_realizados_rest.MainHandler),
(r'/api/aerolineas/gconsultar(/?([A-Z]{3})?)', rest.consultar_aerolinea_gerente_rest.MainHandler),
(r'/api/aerolineas/lconsultar(/?([A-Z]{2})?)', rest.consultar_aerolinea_aerolinea_rest.MainHandler),
(r'/api/aerolineas/cpconsultar(/?([A-Z]{3})?)', rest.consultar_aerolinea_carga_aeropuerto_rest.MainHandler),
(r'/api/aerolineas/ppconsultar(/?([A-Z]{3})?)', rest.consultar_aerolinea_persona_aeropuerto_rest.MainHandler),
(r'/api/pproducido(/?([0-9]*)?)', rest.producido_pasajeros_rest.MainHandler),
(r'/api/cproducido(/?([0-9]*)?)', rest.producido_carga_rest.MainHandler),
(r'/api/fcproducido', rest.producido_carga_fechas_rest.MainHandler),
(r'/api/fpproducido', rest.producido_pasajeros_fechas_rest.MainHandler),
(r'/api/aeropuertos', rest.aeropuertos_rest.MainHandler)
# (r'/api/airports(/?([A-Z]{3})?)', rest.airports_rest.MainHandler)
]

# Define new web rendering route associations
WEB = [
(r'/flights', web.flights_handler.MainHandler)
]

ROUTES = REST + WEB