# -*- coding: utf-8 -*-

"""
models module
=========

Provides:
    1. Base object definition, i.e., Model module
    2. General object definition

How to use the documentation
----------------------------
Documentation is available in one form: docstrings provided
with the code

Copyright (c) 2016, Edgar A. Margffoy.
MIT, see LICENSE for more details.
"""

import os
import sys
import usuario
import vuelo
import model
import administrador
import aerolinea
import aeropuerto
import avion
import remitente
import viajero
import vuelo
import reserva

__version__ = '1.0.0'

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
