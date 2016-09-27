# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.web
import tornado.escape
import logic.tm as tm
import models.model as model

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db
    
    def prepare(self):
        if "Content-Type" in self.request.headers: 
            if self.request.headers["Content-Type"].startswith("application/json"):
               print "Got JSON"
               self.json_args = json.loads(self.request.body)
            else:
               self.json_args = None

    @tornado.gen.coroutine
    def get(self, reject, iata_code):
        #self.set_status(403)
        airports = yield tm.get_airport(iata_code)
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
        self.write(tornado.escape.json_encode(airports))

    @tornado.gen.coroutine
    def post(self):
        self.set_header('Content-Type', 'text/javascript;charset=utf-8')
