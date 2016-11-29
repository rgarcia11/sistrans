# -*- coding: utf-8 -*-

"""
rest module
=========

Provides:
    1. Asynchronous execution of JSON services
    2. Asynchronous execution of Web Rendering

How to use the documentation
----------------------------
Documentation is available in one form: docstrings provided
with the code

Copyright (c) 2016, Edgar A. Margffoy.
MIT, see LICENSE for more details.
"""

import os
import sys
#New submodules defined inside this module must be imported here
import countries_rest
import flights_rest
import usuarios_rest
import aeropuertos_rest
import vuelos_rest
import aeropuertos_salidas_llegadas_rest
import aerolineas_rest
import aviones_rest
import reservas_rest
import envios_rest
import vuelos_realizados_rest
import consultar_aerolinea_gerente_rest
import consultar_aerolinea_aerolinea_rest
import consultar_aerolinea_carga_aeropuerto_rest
import consultar_aerolinea_persona_aeropuerto_rest
import producido_pasajeros_rest
import producido_carga_rest
import producido_carga_fechas_rest
import producido_pasajeros_fechas_rest
import cancelar_reserva_rest
import consultar_viajes_rest
import consultar_aviones_admin_rest
import consultar_viajes_admin_rest
import cancelar_vuelo_rest
import consultar_trafico_aereo_vuelos_pasajeros_rest
import consultar_trafico_aereo_vuelos_carga_rest
import consultar_no_vuelos_rest
import registrar_usuarios_rest

__version__ = '1.0.0'

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
