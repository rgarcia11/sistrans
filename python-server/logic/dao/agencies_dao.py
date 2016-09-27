import os
import sys
import tornado.web
import tornado.escape
from decorators import returnobj

@returnobj
def get_agencies(cur):
    stmt = 'SELECT * FROM AIRPORTS'
    cur.execute(stmt)
    values = cur.fetchall()
    return cur, values

@returnobj
def get_agency(cur, id_agency):
    stmt = 'SELECT * FROM AIRPORTS WHERE iata_code = :1'
    cur.execute(stmt, (iata_code,))
    value = cur.fetchall()
    return cur, value