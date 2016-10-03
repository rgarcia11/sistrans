# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import logic.tm as tm

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    def prepare(self):
        if 'Content-Type' in self.request.headers:
            if self.request.headers["Content-Type"].startswith("application/json"):
                print "Got JSON"
                self.json_args = json.loads(self.request.body)
            else:
                self.json_args = None

    @tornado.gen.coroutine
    def authenticate(self, usr_type):
        if 'User-Email' not in self.request.headers:
            raise tornado.gen.Return(("User-Email must be defined as header", False, None, None)) 
        email = self.request.headers['User-Email']
        _type = yield tm.buscar_tipo(email)
        print _type
        if len(_type) == 0:
            raise tornado.gen.Return(("Email %s & Co. does not exist" % (email), False, None, None))
        exists = False
        _type = _type[0]
        if isinstance(usr_type, list):
            exists = _type['tipo'] in usr_type
        else:
            exists = _type['tipo'] == usr_type
        raise tornado.gen.Return(("User %s does not have permissions to do this task" % (email), exists, email, _type['tipo']))
        

