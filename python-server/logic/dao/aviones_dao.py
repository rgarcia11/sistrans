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
